#!/usr/bin/env python3
"""고용노동부 행정해석 수집 스크립트.

법제처 Open API (open.law.go.kr)를 사용하여 고용노동부 행정해석을 수집하고
Supabase에 적재한다.

API: http://www.law.go.kr/DRF/lawSearch.do?target=moelCgmExpc
- 목록 조회 및 전문 조회 지원
- 키워드 검색, 기간 필터링 가능
- JSON/XML 응답 포맷 지원

Usage:
  cd /home/ubuntu/work-orchestrator/repos/labor-law-guide
  export $(cat supabase/.env | xargs)
  cd /home/ubuntu/work-orchestrator/repos/labor-decisions-search

  # 키워드로 수집 (2024~2026년)
  python3 scripts/molab_interpretations_collector.py \
    --keywords "해고,임금,퇴직금,근로계약,취업규칙,산재,괴롭힘,노동조합,최저임금,근로시간" \
    --start-year 2024

  # 특정 기간만 수집
  python3 scripts/molab_interpretations_collector.py \
    --keywords "임금" \
    --start-date 20240101 --end-date 20241231

  # 건수 제한으로 테스트
  python3 scripts/molab_interpretations_collector.py \
    --keywords "해고" \
    --limit 50 \
    --dry-run

  # 수집 결과를 JSON/JSONL로만 저장 (Supabase 적재 X)
  python3 scripts/molab_interpretations_collector.py \
    --keywords "임금" \
    --output-dir ./molab_interpretations \
    --skip-db

Parameters:
  --keywords: 쉼표로 구분된 검색 키워드 (필수)
  --start-year: 시작 연도 (기본: 2024)
  --start-date: 시작 일자 (형식: YYYYMMDD, 옵션)
  --end-date: 종료 일자 (형식: YYYYMMDD, 옵션)
  --output-dir: JSON/JSONL 저장 경로 (기본: ./molab_interpretations)
  --limit: 수집 건수 제한 (옵션)
  --skip-db: Supabase 적재 스킵 (옵션, --dry-run 포함)
  --dry-run: 실제 저장 없이 시뮬레이션 (옵션)
  --api-key OC: 법제처 API 인증값 (환경변수 MOLAB_API_KEY로 대체 가능)
"""

import requests
import json
import os
import sys
import re
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# --- Config ---
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
MOLAB_API_KEY = os.environ.get('MOLAB_API_KEY', 'iceamericano9')
MOLAB_API_LIST_BASE = 'http://www.law.go.kr/DRF/lawSearch.do'    # 목록 조회
MOLAB_API_DETAIL_BASE = 'http://www.law.go.kr/DRF/lawService.do'  # 본문 조회

# 기본값
DEFAULT_OUTPUT_DIR = './molab_interpretations'
DEFAULT_START_YEAR = 2024
BATCH_SIZE = 50
REQUEST_DELAY = 0.5  # 레이트 리미트 회피용

# --- Parse Arguments ---
keywords = []
start_date = None
end_date = None
start_year = DEFAULT_START_YEAR
output_dir = DEFAULT_OUTPUT_DIR
skip_db = False
dry_run = False
limit = None
api_key = MOLAB_API_KEY
collect_all_mode = False

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '--keywords' and i + 1 < len(sys.argv):
        keywords = [k.strip() for k in sys.argv[i + 1].split(',')]
        i += 2
    elif arg == '--start-year' and i + 1 < len(sys.argv):
        start_year = int(sys.argv[i + 1])
        i += 2
    elif arg == '--start-date' and i + 1 < len(sys.argv):
        start_date = sys.argv[i + 1]
        i += 2
    elif arg == '--end-date' and i + 1 < len(sys.argv):
        end_date = sys.argv[i + 1]
        i += 2
    elif arg == '--output-dir' and i + 1 < len(sys.argv):
        output_dir = sys.argv[i + 1]
        i += 2
    elif arg == '--limit' and i + 1 < len(sys.argv):
        limit = int(sys.argv[i + 1])
        i += 2
    elif arg == '--api-key' and i + 1 < len(sys.argv):
        api_key = sys.argv[i + 1]
        i += 2
    elif arg == '--skip-db':
        skip_db = True
        i += 1
    elif arg == '--dry-run':
        dry_run = True
        i += 1
    elif arg == '--all':
        collect_all_mode = True
        i += 1
    else:
        i += 1

# --- Validation ---
if not keywords and not collect_all_mode:
    print('Error: --keywords 또는 --all 필수. 예: --keywords "해고,임금" 또는 --all')
    sys.exit(1)
if collect_all_mode:
    keywords = ['']  # 빈 쿼리 = 전체 조회

# 기간 필터는 명시적으로 지정된 경우에만 사용
# (법제처 moelCgmExpc API에서 explYd 파라미터가 비표준이라 전수 수집이 기본)

# --- Setup ---
Path(output_dir).mkdir(parents=True, exist_ok=True)

headers = {
    'User-Agent': 'Python/molab-collector',
    'Accept': 'application/json',
}

def generate_id(case_id: str, org_code: str) -> str:
    """고용노동부 행정해석 고유 ID 생성"""
    raw = f"molab_cgm_{case_id}_{org_code}"
    h = hashlib.md5(raw.encode()).hexdigest()[:8]
    return f"ml_{h}"


def fetch_interpretations_list(
    query: str,
    page: int = 1,
    display: int = 100
) -> Tuple[List[Dict], bool, int]:
    """
    행정해석 목록 조회 API 호출

    Args:
        query: 검색 키워드
        page: 페이지 번호 (1-indexed)
        display: 페이지당 결과 수 (1-100)

    Returns:
        (항목 리스트, 다음 페이지 존재 여부, 총 건수)
    """
    params = {
        'target': 'moelCgmExpc',
        'type': 'JSON',
        'OC': api_key,
        'display': min(display, 100),
        'page': page,
    }
    if query:  # 빈 쿼리 = 전체 조회
        params['query'] = query
    if start_date and end_date:
        params['explYd'] = f'{start_date}~{end_date}'

    try:
        r = requests.get(MOLAB_API_LIST_BASE, params=params, headers=headers, timeout=30)
        r.raise_for_status()

        # JSON 파싱 시도 — 법제처 API가 때때로 비표준 JSON 반환
        text = r.text.strip()
        if text.startswith('\ufeff'):
            text = text[1:]
        data = json.loads(text)

        # 에러 응답 확인
        if isinstance(data, dict) and data.get('result') and 'error' in str(data.get('result', '')).lower():
            print(f'  API 오류: {data.get("msg", data.get("result", "Unknown error"))}')
            return [], False, 0

        # 법제처 API 실제 응답: {"CgmExpc": {"cgmExpc": [...], "totalCnt": "226", ...}}
        items = []
        total = 0
        if isinstance(data, dict):
            # 래퍼 키 탐색: CgmExpc → cgmExpc (배열)
            inner = data
            for wrapper_key in ('CgmExpc', 'moelCgmExpc'):
                if wrapper_key in data and isinstance(data[wrapper_key], dict):
                    inner = data[wrapper_key]
                    break
            # 배열 키 탐색
            for key in ('cgmExpc', 'moelCgmExpc', 'items', 'list'):
                if key in inner and isinstance(inner[key], list):
                    items = inner[key]
                    break
            # 총 건수
            total = int(inner.get('totalCnt', 0) or inner.get('total', 0) or data.get('totalCnt', 0) or 0)
        elif isinstance(data, list):
            items = data
            total = len(items)

        has_next = (page * display) < total if total > 0 else False
        return items, has_next, total
    except requests.RequestException as e:
        print(f'  API 요청 오류: {e}')
        return [], False, 0
    except (json.JSONDecodeError, ValueError) as e:
        print(f'  JSON 파싱 오류: {e}')
        return [], False, 0


def fetch_interpretation_detail(case_id: int) -> Optional[Dict]:
    """
    행정해석 본문 조회 API 호출

    Args:
        case_id: 법령해석 일련번호

    Returns:
        해석 상세정보 또는 None
    """
    params = {
        'target': 'moelCgmExpc',
        'type': 'JSON',
        'OC': api_key,
        'ID': case_id,
    }

    try:
        r = requests.get(MOLAB_API_DETAIL_BASE, params=params, headers=headers, timeout=30)
        r.raise_for_status()

        text = r.text.strip()
        if text.startswith('\ufeff'):
            text = text[1:]
        data = json.loads(text)

        # 법제처 본문 조회 실제 응답: {"CgmExpcService": {"안건명": ..., "질의요지": ..., "회답": ...}}
        if isinstance(data, dict):
            # 래퍼 키 탐색
            for key in ('CgmExpcService', 'moelCgmExpc', 'cgmExpc'):
                val = data.get(key)
                if isinstance(val, dict):
                    return val
                if isinstance(val, list) and len(val) > 0:
                    return val[0]
            # 직접 최상위에 필드가 있는 경우
            if '질의요지' in data or '회답' in data:
                return data
        return None
    except requests.RequestException as e:
        print(f'  상세조회 API 오류 (ID={case_id}): {e}')
        return None
    except json.JSONDecodeError as e:
        print(f'  JSON 파싱 오류 (ID={case_id}): {e}')
        return None


def parse_interpretation(item: Dict, detail: Optional[Dict] = None) -> Dict:
    """
    API 응답을 정규화된 형식으로 변환

    Args:
        item: 목록 조회 응답 항목
        detail: 상세 조회 응답 (선택)

    Returns:
        정규화된 행정해석 데이터
    """
    # 법제처 API 실제 필드명: 법령해석일련번호, 안건명, 안건번호, 해석일자,
    # 해석기관명, 질의기관명, 질의요지, 회답, 이유, 관련법령, 데이터기준일시
    case_id = str(item.get('법령해석일련번호') or item.get('id') or item.get('ID') or '')
    case_number = item.get('안건번호') or item.get('case_number') or case_id
    org_code = 'MOLAB'

    title = item.get('안건명') or item.get('title') or ''
    inquiry_org = item.get('질의기관명') or item.get('inquiry_org') or ''
    answer_org = item.get('해석기관명') or item.get('answer_org') or '고용노동부'

    # 날짜
    date_str = str(item.get('해석일자') or item.get('decision_date') or item.get('explYmd') or '')
    decision_date = None
    if date_str:
        clean = date_str.replace('-', '').replace('.', '').strip()
        if len(clean) >= 8 and clean[:8].isdigit():
            decision_date = f'{clean[0:4]}-{clean[4:6]}-{clean[6:8]}'

    # 질의요지/회답/이유 (목록 조회에서도 올 수 있고, 상세 조회에서 더 상세)
    inquiry_summary = item.get('질의요지') or item.get('inquiry_summary') or ''
    answer_summary = item.get('회답') or item.get('answer_summary') or ''
    reason = item.get('이유') or ''

    # 상세 조회 결과로 보강
    if detail:
        if not inquiry_summary:
            inquiry_summary = detail.get('질의요지') or detail.get('content') or ''
        if not answer_summary:
            answer_summary = detail.get('회답') or detail.get('answer') or ''
        if not reason:
            reason = detail.get('이유') or ''

    # 전문: 질의요지 + 회답 + 이유 결합
    full_parts = []
    if inquiry_summary:
        full_parts.append(f'[질의요지]\n{inquiry_summary}')
    if answer_summary:
        full_parts.append(f'[회답]\n{answer_summary}')
    if reason:
        full_parts.append(f'[이유]\n{reason}')
    full_text = '\n\n'.join(full_parts)

    # URL
    url = f'https://www.law.go.kr/행정해석/{case_number}'

    # 관련 법령
    related_laws = []
    laws_str = item.get('관련법령') or item.get('related_laws') or ''
    if laws_str:
        related_laws = [l.strip() for l in re.split(r'[,\n]', laws_str) if l.strip()]

    # 태그 추출
    tags = []
    text_for_tags = f'{title} {inquiry_summary} {answer_summary}'.lower()
    for kw in keywords:
        if kw.lower() in text_for_tags:
            tags.append(kw)

    rid = generate_id(case_id, org_code)

    return {
        'id': rid,
        'case_id': case_id,
        'case_number': case_number,
        'title': title[:500],
        'inquiry_org': inquiry_org[:200],
        'answer_org': answer_org[:200],
        'decision_date': decision_date,
        'inquiry_summary': inquiry_summary[:2000],
        'answer_summary': answer_summary[:5000],
        'full_text': full_text[:20000],
        'related_laws': related_laws,
        'tags': list(set(tags)),
        'url': url,
        'source': 'molab.api',
        'collected_at': datetime.utcnow().isoformat(),
    }


def collect_all(keywords_list: List[str]) -> Tuple[List[Dict], int, int]:
    """
    모든 키워드에 대해 행정해석 수집

    Returns:
        (수집된 항목, 총 처리건수, 중복 제거된 건수)
    """
    all_records = []
    seen_ids = set()
    total_fetched = 0
    total_skipped = 0

    for keyword in keywords_list:
        print(f'\n[키워드] {keyword}')
        page = 1
        keyword_count = 0

        while True:
            if limit and total_fetched >= limit:
                print(f'  수집 제한({limit}) 도달')
                break

            print(f'  페이지 {page}...', end='', flush=True)
            items, has_next, total = fetch_interpretations_list(keyword, page=page)

            if not items:
                print(f' (API 오류 또는 결과 없음)')
                break

            print(f' {len(items)}건 조회 (전체: {total})')

            for item in items:
                if limit and total_fetched >= limit:
                    break

                case_id = str(item.get('법령해석일련번호') or item.get('id') or item.get('ID') or '')
                if case_id in seen_ids:
                    total_skipped += 1
                    continue

                # 본문 조회 (lawService.do) — 질의요지, 회답, 이유 가져오기
                serial = item.get('법령해석일련번호') or case_id
                detail = fetch_interpretation_detail(int(serial)) if str(serial).isdigit() else None
                if detail:
                    time.sleep(REQUEST_DELAY)  # 본문 조회 레이트 리미트

                record = parse_interpretation(item, detail)
                all_records.append(record)
                seen_ids.add(case_id)
                total_fetched += 1
                keyword_count += 1

            if not has_next:
                print(f'  [완료] 총 {keyword_count}건')
                break

            page += 1
            time.sleep(REQUEST_DELAY)

        time.sleep(REQUEST_DELAY)

    return all_records, total_fetched, total_skipped


def save_to_files(records: List[Dict], output_path: str):
    """
    수집 결과를 JSON 및 JSONL로 저장

    Args:
        records: 수집된 행정해석 목록
        output_path: 저장 디렉토리
    """
    Path(output_path).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = f'{output_path}/molab_interpretations_{timestamp}.json'
    jsonl_file = f'{output_path}/molab_interpretations_{timestamp}.jsonl'

    # JSON 저장
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f'\n✓ JSON 저장: {json_file} ({len(records)}건)')

    # JSONL 저장
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(f'✓ JSONL 저장: {jsonl_file} ({len(records)}건)')

    return json_file, jsonl_file


def push_to_supabase(records: List[Dict]) -> Tuple[int, int]:
    """
    Supabase에 행정해석 적재

    Args:
        records: 수집된 항목 리스트

    Returns:
        (성공 건수, 실패 건수)
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        print('Error: SUPABASE_URL과 SUPABASE_SERVICE_KEY 필요')
        return 0, len(records)

    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal,resolution=ignore-duplicates',
    }

    inserted = 0
    failed = 0
    batch = []

    for i, record in enumerate(records):
        batch.append(record)

        if len(batch) >= BATCH_SIZE or i == len(records) - 1:
            if dry_run:
                inserted += len(batch)
                print(f'  [DRY RUN] {len(batch)}건 insert 예정 (누적: {inserted})')
            else:
                try:
                    r = requests.post(
                        f'{SUPABASE_URL}/rest/v1/molab_interpretations',
                        headers=headers,
                        json=batch,
                        timeout=30,
                    )
                    if r.status_code in (200, 201):
                        inserted += len(batch)
                        print(f'  ✓ {len(batch)}건 insert 성공 (누적: {inserted})')
                    else:
                        # 대량 insert 실패 시 개별 처리
                        print(f'  ⚠ 대량 insert 실패 ({r.status_code}), 개별 처리 중...')
                        for item in batch:
                            r2 = requests.post(
                                f'{SUPABASE_URL}/rest/v1/molab_interpretations',
                                headers=headers,
                                json=item,
                                timeout=10,
                            )
                            if r2.status_code in (200, 201):
                                inserted += 1
                            else:
                                failed += 1
                        print(f'    개별 처리: {inserted}건 성공, {failed}건 실패')
                except requests.RequestException as e:
                    print(f'  ✗ 요청 오류: {e}')
                    failed += len(batch)

            batch = []
            time.sleep(REQUEST_DELAY)

    return inserted, failed


def generate_sample_data() -> List[Dict]:
    """테스트용 샘플 데이터 생성"""
    samples = [
        {
            'id': '1001',
            'case_number': '해석-2024-00001',
            'title': '근로기준법상 시간급 근로자의 퇴직금 산정 기준',
            'inquiry_org': '중소벤처기업부',
            'answer_org': '고용노동부',
            'decision_date': '2024-01-15',
            'inquiry_summary': 'Q. 시간급 근로자가 5년 이상 근속했을 때 퇴직금을 지급받을 수 있는가?',
            'answer_summary': 'A. 근로기준법 제34조에 따라 1년 이상 근속한 모든 근로자는 퇴직금 대상이며, 평균임금과 근속기간으로 계산합니다.',
        },
        {
            'id': '1002',
            'case_number': '해석-2024-00002',
            'title': '정당한 사유 없는 해고에 해당하는 구체적 판단',
            'inquiry_org': '노동청',
            'answer_org': '고용노동부',
            'decision_date': '2024-02-20',
            'inquiry_summary': 'Q. 경영상 어려움만으로 근로자를 해고할 수 있는가?',
            'answer_summary': 'A. 경영상 이유로 근로자를 해고하려면 긴박한 경영상 필요성, 대체인원 감축의 합리성, 인원선정의 공정성, 해고회피노력 등을 종합고려합니다.',
        },
        {
            'id': '1003',
            'case_number': '해석-2024-00003',
            'title': '직장 내 괴롭힘의 법적 정의 및 사용자 책임',
            'inquiry_org': '여성가족부',
            'answer_org': '고용노동부',
            'decision_date': '2024-03-10',
            'inquiry_summary': 'Q. 업무상 지시와 직장 내 괴롭힘을 구분하는 기준은?',
            'answer_summary': 'A. 직장 내 괴롭힘은 상대방에게 신체적·정신적 고통을 주는 행위로, 합리적 이유 없는 경우 해당됩니다. 사용자는 적절한 조사와 예방조치를 해야 합니다.',
        },
    ]
    return samples


def main():
    print('='*70)
    print('고용노동부 행정해석 수집 스크립트')
    print('='*70)
    print(f'API: {MOLAB_API_LIST_BASE}')
    print(f'키워드: {", ".join(keywords)}')
    print(f'기간: {start_date} ~ {end_date}')
    print(f'출력 디렉토리: {output_dir}')
    if limit:
        print(f'수집 제한: {limit}건')
    if dry_run:
        print('[DRY RUN 모드]')
    if api_key == 'test':
        print('\n⚠️  경고: 테스트 API 키를 사용 중입니다.')
        print('   IP 미등록 시 실제 데이터를 받을 수 없습니다.')
        print('   공식 API 키는 02-2109-6446 (법제처)으로 문의하세요.')
    print()

    # 1. 수집
    print('Step 1: 행정해석 수집 중...')
    records, total_fetched, total_skipped = collect_all(keywords)

    # API 오류 시 샘플 데이터 사용 (테스트 목적)
    if not records and dry_run:
        print('  ⚠️  실제 API 응답 없음 (IP 미등록). 샘플 데이터로 테스트합니다.')
        sample_records = generate_sample_data()
        records = [parse_interpretation(s) for s in sample_records[:min(len(sample_records), limit or 10)]]
        total_fetched = len(records)
        total_skipped = 0

    print(f'\n총 수집: {total_fetched}건')
    print(f'중복 제거: {total_skipped}건')
    print(f'최종 저장: {len(records)}건')

    if not records:
        print('\n경고: 수집된 항목이 없습니다.')
        print('해결 방법:')
        print('1. API 키 확인: export MOLAB_API_KEY="your-key"')
        print('2. IP 주소 등록: 02-2109-6446 (법제처 콜센터)')
        print('3. 테스트용: --dry-run 옵션 사용')
        return

    # 2. 파일 저장
    print('\nStep 2: 파일 저장 중...')
    json_file, jsonl_file = save_to_files(records, output_dir)

    # 3. Supabase 적재 (옵션)
    if not skip_db and not dry_run:
        print('\nStep 3: Supabase 적재 중...')
        inserted, failed = push_to_supabase(records)
        print(f'적재 완료: {inserted}건 성공, {failed}건 실패')
    elif skip_db:
        print('\n[스킵] Supabase 적재 스킵됨 (--skip-db)')
    elif dry_run:
        print('\n[DRY RUN] Supabase 적재 스킵됨')

    print('\n' + '='*70)
    print('수집 완료!')
    print('='*70)


if __name__ == '__main__':
    main()
