"""BigCase 판례 수집 — 8개 영역별 20건씩 사실관계 추출

Usage:
    python scripts/bigcase_test_collect.py
    python scripts/bigcase_test_collect.py --category 무단결근 --limit 5
"""
import sys
import os
import json
import subprocess
import argparse
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

LEGAL_AUTO_DIR = r"C:\dev\neuro-coach\legal-automation"
OUTPUT_DIR = r"C:\dev\labor-decisions-search\evaluation\bigcase_test"

CATEGORIES = {
    "Q1_무단결근": "무단결근 해고 정당성",
    "Q2_결근절차": "무단결근 서면통지 위반 부당해고",
    "Q3_괴롭힘성립": "직장내괴롭힘 성립 징계",
    "Q4_괴롭힘보복": "직장내괴롭힘 신고 보복 불이익",
    "Q5_수습해고": "수습 본채용거부 정당성",
    "Q6_수습절차": "수습 해고 서면통지 절차위반",
    "Q7_저성과": "정규직 저성과 업무능력부족 해고",
    "Q8_징계양정": "징계양정 과다 부당해고",
}


def extract_court_from_title(title):
    """제목에서 법원 풀네임 추출: '서울고등법원 2023. 4. 14. 선고' → '서울고등법원'"""
    import re
    match = re.match(r'([가-힣]+(?:법원|대법원))', title)
    return match.group(1) if match else ''


def run_bc_search(query, limit=20):
    """BigCase 검색 실행 — 테이블 2줄 구조 파싱"""
    import re
    cmd = [sys.executable, "main.py", "bc-search", query]
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding='utf-8',
        cwd=LEGAL_AUTO_DIR, timeout=60
    )

    lines = result.stdout.split('\n')
    cases = []
    seen = set()

    # 테이블 행에서 사건번호가 있는 줄 찾기
    for i, line in enumerate(lines):
        if '│' not in line:
            continue
        parts = [p.strip() for p in line.split('│')]
        if len(parts) < 4:
            continue

        # 사건번호 패턴: 숫자+한글+숫자 (예: 2022누62309, 88다카19804)
        # parts: ['', '', 법원, 사건번호, 제목, 유형, '']
        case_num = parts[3].strip() if len(parts) > 3 else ''
        if not re.match(r'\d{2,4}[가-힣]', case_num):
            continue
        case_num = case_num.rstrip('…').strip()
        if case_num in seen or case_num == '사건번호':
            continue

        # 법원명: parts[2] 또는 제목(parts[4])에서
        court_raw = parts[2].strip().rstrip('…').strip()
        title = parts[4].strip() if len(parts) > 4 else ''

        # 제목에서 풀네임 추출
        court_match = re.match(r'([가-힣]+(?:법원|대법원))', title)
        court = court_match.group(1) if court_match else court_raw

        # 다음 줄에 제목 이어짐 확인
        if i + 1 < len(lines) and '│' in lines[i + 1]:
            next_parts = [p.strip() for p in lines[i + 1].split('│')]
            if len(next_parts) > 4 and next_parts[4].strip():
                title = title + ' ' + next_parts[4].strip()

        if not court:
            court = '대법원' if '대법원' in title else '법원'

        seen.add(case_num)
        cases.append({
            'court': court,
            'case_number': case_num,
            'title': title,
            'type': parts[5].strip() if len(parts) > 5 else '',
        })

    return cases[:limit]


def run_bc_detail(court, case_number):
    """BigCase 상세 조회"""
    cmd = [sys.executable, "main.py", "bc-detail", court, case_number]
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding='utf-8',
        cwd=LEGAL_AUTO_DIR, timeout=60
    )
    return result.stdout


def parse_detail(detail_text):
    """상세 내용에서 사실관계/판결 추출"""
    info = {
        'raw': detail_text,
        'case_number': '',
        'court': '',
        'date': '',
        'result': '',
        'facts': '',
        'holding': '',
        'ai_summary': '',
    }

    lines = detail_text.split('\n')
    section = ''

    for line in lines:
        line_stripped = line.strip()

        if '사건번호:' in line:
            info['case_number'] = line.split('사건번호:')[1].strip()
        elif '법원:' in line:
            info['court'] = line.split('법원:')[1].strip()
        elif '선고일:' in line:
            info['date'] = line.split('선고일:')[1].strip()
        elif '주문:' in line:
            info['result'] = line.split('주문:')[1].strip()
        elif 'AI 요약:' in line:
            section = 'ai_summary'
        elif '사실관계' in line_stripped and len(line_stripped) < 20:
            section = 'facts'
        elif '핵심 쟁점' in line_stripped or '법원의 판단' in line_stripped:
            section = 'holding'
        elif '관련 판례' in line_stripped:
            section = ''
        elif section == 'facts':
            info['facts'] += line + '\n'
        elif section == 'holding':
            info['holding'] += line + '\n'
        elif section == 'ai_summary':
            info['ai_summary'] += line + '\n'

    return info


def collect_category(category_key, query, limit=20):
    """한 영역 수집"""
    print(f"\n{'='*60}")
    print(f"영역: {category_key} — 검색: {query}")
    print(f"{'='*60}")

    # 검색
    cases = run_bc_search(query, limit=limit)
    print(f"검색 결과: {len(cases)}건")

    collected = []
    for i, case in enumerate(cases):
        print(f"  [{i+1}/{len(cases)}] {case['court']} {case['case_number']}...", end=' ')

        try:
            # 상세 조회
            detail = run_bc_detail(case['court'], case['case_number'])
            info = parse_detail(detail)

            collected.append({
                'category': category_key,
                'query': query,
                'index': i + 1,
                'court': info.get('court') or case['court'],
                'case_number': info.get('case_number') or case['case_number'],
                'date': info.get('date', ''),
                'result': info.get('result', ''),
                'facts': info.get('facts', '').strip(),
                'holding': info.get('holding', '').strip(),
                'ai_summary': info.get('ai_summary', '').strip(),
                'title': case.get('title', ''),
            })

            print(f"✅ {info.get('result', '?')}")

            # rate limit
            time.sleep(2)

        except Exception as e:
            print(f"❌ {e}")
            collected.append({
                'category': category_key,
                'query': query,
                'index': i + 1,
                'court': case['court'],
                'case_number': case['case_number'],
                'error': str(e),
            })

    return collected


def main():
    parser = argparse.ArgumentParser(description='BigCase 판례 수집')
    parser.add_argument('--category', help='특정 영역만 (예: Q1_무단결근)')
    parser.add_argument('--limit', type=int, default=20, help='영역당 건수')
    parser.add_argument('--output-dir', default=OUTPUT_DIR)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    categories = CATEGORIES
    if args.category:
        if args.category in CATEGORIES:
            categories = {args.category: CATEGORIES[args.category]}
        else:
            print(f"알 수 없는 카테고리: {args.category}")
            print(f"가능한 값: {list(CATEGORIES.keys())}")
            return

    all_results = []

    for cat_key, query in categories.items():
        results = collect_category(cat_key, query, limit=args.limit)
        all_results.extend(results)

        # 영역별 저장
        cat_path = os.path.join(args.output_dir, f"{cat_key}.jsonl")
        with open(cat_path, 'w', encoding='utf-8') as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        print(f"  저장: {cat_path} ({len(results)}건)")

    # 전체 저장
    all_path = os.path.join(args.output_dir, "all_bigcase_test.jsonl")
    with open(all_path, 'w', encoding='utf-8') as f:
        for r in all_results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # 요약
    print(f"\n{'='*60}")
    print(f"수집 완료")
    print(f"{'='*60}")
    print(f"전체: {len(all_results)}건")
    for cat_key in categories:
        cat_count = sum(1 for r in all_results if r.get('category') == cat_key)
        err_count = sum(1 for r in all_results if r.get('category') == cat_key and 'error' in r)
        print(f"  {cat_key}: {cat_count}건 (에러 {err_count})")
    print(f"저장: {all_path}")


if __name__ == '__main__':
    main()
