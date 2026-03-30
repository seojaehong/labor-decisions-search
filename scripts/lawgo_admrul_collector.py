#!/usr/bin/env python3
"""법제처 행정규칙(훈령/예규/고시) 수집 스크립트.

고용노동부 소관 행정규칙을 법제처 Open API로 전수 수집하여 Supabase에 적재.
API: http://www.law.go.kr/DRF/lawSearch.do?target=admrul (목록)
     http://www.law.go.kr/DRF/lawService.do?target=admrul (본문)

Usage:
  cd /home/ubuntu/work-orchestrator/repos/labor-decisions-search

  # 고용노동부 소관 전수 수집
  python3 scripts/lawgo_admrul_collector.py --all --skip-db

  # 키워드 + Supabase 적재
  python3 scripts/lawgo_admrul_collector.py --keywords "근로,고용,임금"

  # 드라이런
  python3 scripts/lawgo_admrul_collector.py --all --dry-run --limit 10
"""

import requests
import json
import os
import sys
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# --- Config ---
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
OC = os.environ.get('MOLAB_API_KEY', 'iceamericano9')
LIST_API = 'http://www.law.go.kr/DRF/lawSearch.do'
DETAIL_API = 'http://www.law.go.kr/DRF/lawService.do'

OUTPUT_DIR = './lawgo_admrul'
BATCH_SIZE = 50
DELAY = 0.5
MOLAB_FILTER = True  # 고용노동부 소관만 필터

# --- Args ---
keywords = []
collect_all = False
skip_db = False
dry_run = False
limit = None
no_filter = False

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '--keywords' and i + 1 < len(sys.argv):
        keywords = [k.strip() for k in sys.argv[i + 1].split(',')]
        i += 2
    elif arg == '--all':
        collect_all = True
        i += 1
    elif arg == '--skip-db':
        skip_db = True
        i += 1
    elif arg == '--dry-run':
        dry_run = True
        i += 1
    elif arg == '--limit' and i + 1 < len(sys.argv):
        limit = int(sys.argv[i + 1])
        i += 2
    elif arg == '--output-dir' and i + 1 < len(sys.argv):
        OUTPUT_DIR = sys.argv[i + 1]
        i += 2
    elif arg == '--no-filter':
        no_filter = True
        i += 1
    else:
        i += 1

if not keywords and not collect_all:
    print('Error: --keywords "근로,고용" 또는 --all 필수')
    sys.exit(1)

if collect_all:
    # 고용노동부 관련 키워드로 광범위 검색 후 소관부처 필터
    keywords = ['근로', '고용', '임금', '산업안전', '직업', '노동', '산재', '퇴직',
                '최저임금', '파견', '기간제', '취업', '장애인고용', '직업훈련',
                '건설근로', '선원', '외국인근로', '육아휴직', '출산', '모성보호']

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
headers = {'User-Agent': 'Python/lawgo-collector', 'Accept': 'application/json'}


def generate_id(rule_id: str) -> str:
    h = hashlib.md5(f'admrul_{rule_id}'.encode()).hexdigest()[:8]
    return f'ar_{h}'


def fetch_list(query: str = '', page: int = 1, display: int = 100) -> Tuple[List[Dict], bool, int]:
    params = {
        'target': 'admrul', 'type': 'JSON', 'OC': OC,
        'display': min(display, 100), 'page': page,
    }
    if query:
        params['query'] = query
    try:
        r = requests.get(LIST_API, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        text = r.text.strip()
        if text.startswith('\ufeff'):
            text = text[1:]
        data = json.loads(text)

        inner = data
        for k in ('AdmRulSearch',):
            if k in data and isinstance(data[k], dict):
                inner = data[k]
                break

        items = []
        for k in ('admrul', 'items', 'list'):
            if k in inner and isinstance(inner[k], list):
                items = inner[k]
                break

        total = int(inner.get('totalCnt', 0) or 0)
        has_next = (page * display) < total
        return items, has_next, total
    except Exception as e:
        print(f'  목록 조회 오류: {e}')
        return [], False, 0


def fetch_detail(rule_id: str) -> Optional[Dict]:
    params = {'target': 'admrul', 'type': 'JSON', 'OC': OC, 'ID': rule_id}
    try:
        r = requests.get(DETAIL_API, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        text = r.text.strip()
        if text.startswith('\ufeff'):
            text = text[1:]
        data = json.loads(text)

        if isinstance(data, dict):
            for k in ('AdmRulService', 'admrul'):
                val = data.get(k)
                if isinstance(val, dict):
                    return val
                if isinstance(val, list) and len(val) > 0:
                    return val[0]
            if '행정규칙명' in data:
                return data
        return None
    except Exception as e:
        print(f'  본문 조회 오류 (ID={rule_id}): {e}')
        return None


def parse_item(item: Dict, detail: Optional[Dict] = None) -> Dict:
    rule_id = str(item.get('행정규칙일련번호') or item.get('행정규칙ID') or item.get('id') or '')
    name = item.get('행정규칙명', '')
    rule_type = item.get('행정규칙종류', '')
    org = item.get('소관부처명', '')
    issued = str(item.get('발령일자', ''))
    effective = str(item.get('시행일자', ''))

    issued_date = None
    if issued and len(issued) >= 8:
        issued_date = f'{issued[0:4]}-{issued[4:6]}-{issued[6:8]}'

    effective_date = None
    if effective and len(effective) >= 8:
        effective_date = f'{effective[0:4]}-{effective[4:6]}-{effective[6:8]}'

    # 본문
    full_text = ''
    if detail:
        # 행정규칙 본문은 조문 형태로 올 수 있음
        content_parts = []
        for field in ('조문내용', '본문', 'content', '행정규칙본문'):
            val = detail.get(field, '')
            if val:
                content_parts.append(str(val))
        if not content_parts:
            # 모든 텍스트 필드 수집
            for k, v in detail.items():
                if isinstance(v, str) and len(v) > 50:
                    content_parts.append(f'[{k}]\n{v}')
        full_text = '\n\n'.join(content_parts)

    rid = generate_id(rule_id)

    return {
        'id': rid,
        'rule_id': rule_id,
        'name': name[:500],
        'rule_type': rule_type,
        'org': org[:200],
        'issued_date': issued_date,
        'effective_date': effective_date,
        'full_text': full_text[:30000],
        'status': item.get('현행연혁구분', ''),
        'revision_type': item.get('제개정구분명', ''),
        'issue_number': item.get('발령번호', ''),
        'url': f'https://www.law.go.kr/행정규칙/{name}' if name else '',
        'source': 'lawgo.admrul',
        'collected_at': datetime.utcnow().isoformat(),
    }


def collect(keywords_list: List[str]) -> List[Dict]:
    all_records = []
    seen_ids = set()
    total_fetched = 0

    for kw in keywords_list:
        print(f'\n[키워드] {kw}')
        page = 1

        while True:
            if limit and total_fetched >= limit:
                print(f'  수집 제한({limit}) 도달')
                break

            print(f'  페이지 {page}...', end='', flush=True)
            items, has_next, total = fetch_list(kw, page=page)

            if not items:
                print(' (결과 없음)')
                break

            print(f' {len(items)}건 (전체: {total})')

            for item in items:
                if limit and total_fetched >= limit:
                    break

                rid = str(item.get('행정규칙일련번호') or item.get('행정규칙ID') or '')
                if rid in seen_ids:
                    continue

                # 고용노동부 소관 필터
                org = item.get('소관부처명', '')
                if MOLAB_FILTER and not no_filter and '고용노동' not in org:
                    continue

                # 본문 조회
                detail = fetch_detail(rid) if rid else None
                if detail:
                    time.sleep(DELAY)

                record = parse_item(item, detail)
                all_records.append(record)
                seen_ids.add(rid)
                total_fetched += 1

            if not has_next:
                break

            page += 1
            time.sleep(DELAY)

        if limit and total_fetched >= limit:
            break
        time.sleep(DELAY)

    return all_records


def save_files(records: List[Dict]):
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_path = f'{OUTPUT_DIR}/admrul_{ts}.json'
    jsonl_path = f'{OUTPUT_DIR}/admrul_{ts}.jsonl'

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f'\nJSON 저장: {json_path} ({len(records)}건)')

    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'JSONL 저장: {jsonl_path} ({len(records)}건)')


def push_supabase(records: List[Dict]) -> Tuple[int, int]:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print('Supabase 키 없음 — 스킵')
        return 0, len(records)

    h = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal,resolution=ignore-duplicates',
    }
    inserted = 0
    failed = 0
    batch = []

    for i, rec in enumerate(records):
        batch.append(rec)
        if len(batch) >= BATCH_SIZE or i == len(records) - 1:
            if dry_run:
                inserted += len(batch)
                print(f'  [DRY RUN] {len(batch)}건 (누적: {inserted})')
            else:
                try:
                    r = requests.post(f'{SUPABASE_URL}/rest/v1/lawgo_admrul',
                                      headers=h, json=batch, timeout=30)
                    if r.status_code in (200, 201):
                        inserted += len(batch)
                    else:
                        print(f'  적재 오류 ({r.status_code}): {r.text[:200]}')
                        failed += len(batch)
                except Exception as e:
                    print(f'  적재 오류: {e}')
                    failed += len(batch)
            batch = []
            time.sleep(DELAY)

    return inserted, failed


def main():
    print('=' * 60)
    print('법제처 행정규칙 수집 (고용노동부 소관)')
    print('=' * 60)
    print(f'키워드: {len(keywords)}개')
    print(f'필터: {"고용노동부 소관만" if MOLAB_FILTER and not no_filter else "전체"}')
    if limit:
        print(f'제한: {limit}건')
    if dry_run:
        print('[DRY RUN]')
    print()

    records = collect(keywords)
    print(f'\n총 수집: {len(records)}건')

    if not records:
        print('수집된 항목 없음')
        return

    save_files(records)

    if not skip_db and not dry_run:
        print('\nSupabase 적재 중...')
        ok, fail = push_supabase(records)
        print(f'적재: {ok}건 성공, {fail}건 실패')
    elif skip_db:
        print('\n[스킵] DB 적재 안 함')

    print('\n' + '=' * 60)
    print('완료!')
    print('=' * 60)


if __name__ == '__main__':
    main()
