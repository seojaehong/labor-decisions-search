#!/usr/bin/env python3
"""BigCase 29,622건을 nlrc_decisions 테이블에 INSERT하는 스크립트.

Usage:
  cd /home/ubuntu/work-orchestrator/repos/labor-law-guide
  export $(cat supabase/.env | xargs)
  cd /home/ubuntu/work-orchestrator/repos/labor-decisions-search
  python3 scripts/bigcase_to_db.py [--dry-run] [--limit N]
"""

import requests, json, os, sys, re, glob, time, hashlib
from datetime import datetime

# --- Config ---
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
JSONL_DIR = 'evaluation/bigcase_bulk'
DRY_RUN = '--dry-run' in sys.argv
LIMIT = None
for i, arg in enumerate(sys.argv):
    if arg == '--limit' and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])

if not SUPABASE_URL or not SUPABASE_KEY:
    print('Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set')
    sys.exit(1)

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal,resolution=ignore-duplicates'
}

# --- Mappings ---
RESULT_MAP = {
    '원고승': 'granted',
    '원고패': 'dismissed',
    '원고일부승': 'partial',
    '원고항소기각': 'dismissed',  # 원고의 항소 기각 = 원고 패소 유지
    '상고기각': 'upheld',
    '항소기각': 'upheld',
    '피고항소기각': 'granted',   # 피고(사용자)의 항소 기각 = 근로자 승 유지
    '각하': 'rejected',
    '1심취소, 원고패': 'dismissed',
    '1심취소, 원고승': 'granted',
    '파기환송': 'overturned',
}

CATEGORY_MAP = {
    'contract_expiry': ['contract_expiry'],
    'embezzlement': ['embezzlement'],
    'misconduct': ['misconduct'],
    'no_dismissal': ['no_dismissal'],
    'redundancy': ['redundancy'],
    'sexual_harassment': ['sexual_harassment'],
    'transfer': ['transfer'],
    'violence': ['violence'],
    'Q1_무단결근': ['absence'],
    'Q2_결근절차': ['absence'],
    'Q3_괴롭힘성립': ['workplace_bullying'],
    'Q4_괴롭힘보복': ['workplace_bullying'],
    'Q5_수습해고': ['probation'],
    'Q6_수습절차': ['probation'],
    'Q7_저성과': ['incompetence'],
    'Q8_징계양정': ['misconduct'],
}

def generate_id(case_number: str, court: str) -> str:
    """BigCase 케이스 고유 ID 생성"""
    raw = f"bigcase_{case_number}_{court}"
    h = hashlib.md5(raw.encode()).hexdigest()[:8]
    return f"bc_{h}"

def map_result(result: str) -> str:
    """BigCase result → nlrc_decisions decision_result"""
    if not result:
        return 'unknown'
    # 직접 매핑
    if result in RESULT_MAP:
        return RESULT_MAP[result]
    # 패턴 매칭
    if '원고승' in result:
        return 'granted'
    if '원고패' in result:
        return 'dismissed'
    if '기각' in result:
        return 'dismissed'
    if '취소' in result:
        return 'overturned'
    return 'unknown'

def extract_holding_points(full_text: dict, summary: str) -> str:
    """full_text에서 핵심 판단 내용 추출"""
    if not full_text:
        return summary or ''

    # body_infos에서 '이유' 파트 추출 시도
    body_infos = full_text.get('body_infos', [])
    for info in body_infos:
        if isinstance(info, dict) and info.get('item', '') in ('이유', '판결이유', '주문'):
            content = info.get('content', '')
            if content and len(content) > 100:
                return content[:3000]

    # full_text 전체에서 추출
    body = full_text.get('body_court', '')
    if body and len(body) > 200:
        return body[:3000]

    return summary or ''

def parse_bigcase(record: dict) -> dict:
    """BigCase record → nlrc_decisions row"""
    case_number = record.get('case_number', '')
    court = record.get('court', '')
    rid = generate_id(case_number, court)

    full_text = record.get('full_text', {})
    if isinstance(full_text, str):
        try:
            full_text = json.loads(full_text)
        except:
            full_text = {}

    summary = record.get('summary', '')
    holding = extract_holding_points(full_text, summary)

    category = record.get('category', '')
    reason_cats = CATEGORY_MAP.get(category, ['other'])

    result = map_result(record.get('result', ''))

    # key_issue 추출 (summary 첫 줄)
    key_issue = ''
    if summary:
        first_line = summary.split('\n')[0].replace('#', '').strip()
        if len(first_line) > 10:
            key_issue = first_line[:200]

    return {
        'id': rid,
        'title': record.get('title', '')[:500],
        'case_number': case_number,
        'department': court,
        'decision_date': record.get('date') or None,
        'case_type': record.get('case_type', '행정'),
        'decision_result': result,
        'reason_category': reason_cats,
        'holding_points': holding[:5000] if holding else None,
        'holding_summary': summary[:2000] if summary else None,
        'key_issue': key_issue or None,
        'url': record.get('url', ''),
        'source': 'bigcase.ai',
        'tags': record.get('keywords', []),
    }

# --- Main ---
def main():
    all_files = sorted(glob.glob(f'{JSONL_DIR}/*_details.jsonl'))
    if not all_files:
        # Try all_details.jsonl
        all_files = [f'{JSONL_DIR}/all_details.jsonl']

    total_parsed = 0
    total_inserted = 0
    total_skipped = 0
    seen_ids = set()
    batch = []
    BATCH_SIZE = 100

    for filepath in all_files:
        fname = os.path.basename(filepath)
        print(f'\nProcessing {fname}...')

        with open(filepath) as f:
            for line_num, line in enumerate(f):
                if LIMIT and total_parsed >= LIMIT:
                    break

                try:
                    record = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                row = parse_bigcase(record)

                # 중복 방지
                if row['id'] in seen_ids:
                    total_skipped += 1
                    continue
                seen_ids.add(row['id'])

                batch.append(row)
                total_parsed += 1

                if len(batch) >= BATCH_SIZE:
                    if DRY_RUN:
                        total_inserted += len(batch)
                        print(f'  [DRY RUN] Would insert {len(batch)} rows (total: {total_inserted})')
                    else:
                        r = requests.post(
                            f'{SUPABASE_URL}/rest/v1/nlrc_decisions',
                            headers=headers,
                            json=batch,
                            timeout=30
                        )
                        if r.status_code in (200, 201):
                            total_inserted += len(batch)
                        else:
                            print(f'  Error: {r.status_code} {r.text[:200]}')
                            # 개별 insert fallback
                            for row in batch:
                                r2 = requests.post(
                                    f'{SUPABASE_URL}/rest/v1/nlrc_decisions',
                                    headers=headers,
                                    json=row,
                                    timeout=10
                                )
                                if r2.status_code in (200, 201):
                                    total_inserted += 1
                                # 중복은 무시 (resolution=ignore-duplicates)
                        time.sleep(0.3)
                    batch = []

        if LIMIT and total_parsed >= LIMIT:
            break

    # 남은 배치 처리
    if batch:
        if DRY_RUN:
            total_inserted += len(batch)
        else:
            r = requests.post(
                f'{SUPABASE_URL}/rest/v1/nlrc_decisions',
                headers=headers,
                json=batch,
                timeout=30
            )
            if r.status_code in (200, 201):
                total_inserted += len(batch)
            else:
                print(f'Final batch error: {r.status_code} {r.text[:200]}')

    print(f'\n=== Done ===')
    print(f'Parsed: {total_parsed}')
    print(f'Inserted: {total_inserted}')
    print(f'Skipped (dup): {total_skipped}')
    if DRY_RUN:
        print('[DRY RUN - no actual inserts]')

if __name__ == '__main__':
    main()
