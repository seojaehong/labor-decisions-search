#!/usr/bin/env python3
"""BigCase 레코드 중 비노동 판례를 식별하고 exclusion_flags에 마킹하는 스크립트.

Usage:
  export $(cat /home/ubuntu/work-orchestrator/repos/labor-law-guide/supabase/.env | xargs)
  python3 scripts/bigcase_filter_nonlabor.py [--dry-run] [--limit N]
"""

import requests, os, sys, re, time

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
DRY_RUN = '--dry-run' in sys.argv
LIMIT = None
for i, arg in enumerate(sys.argv):
    if arg == '--limit' and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])

headers_read = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
headers_write = {
    'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json', 'Prefer': 'return=minimal'
}

# 비노동 판례 키워드 패턴
NON_LABOR_PATTERNS = [
    # 형사 사건
    re.compile(r'사기죄|절도죄|상해죄|폭행죄|살인죄|마약|음주운전.*죄|도로교통법.*위반'),
    # 순수 민사/상사
    re.compile(r'이사\s*해임|주주총회|상법.*위반|회사에\s*관한\s*소송|합병|분할'),
    # 가사
    re.compile(r'이혼|양육권|재산분할|친권'),
    # 부동산/건설 분쟁 (노동 아닌 것)
    re.compile(r'소유권\s*이전|등기\s*말소|건물\s*명도|토지\s*인도|임대차'),
    # 세금/행정 (노동 아닌 것)
    re.compile(r'부가가치세|소득세|법인세|관세|세무'),
    # 지적재산
    re.compile(r'특허|상표|저작권\s*침해|영업비밀.*침해'),
]

# 노동 관련 확인 키워드 (이게 있으면 노동 판례)
LABOR_CONFIRM_PATTERNS = [
    re.compile(r'해고|부당해고|부당징계|부당전보|부당노동행위'),
    re.compile(r'근로자|사용자|근로계약|임금|퇴직금|수당'),
    re.compile(r'노동위원회|노동조합|단체협약|단체교섭'),
    re.compile(r'산재|산업재해|업무상\s*재해'),
    re.compile(r'직장.*내.*괴롭힘|성희롱|차별'),
    re.compile(r'근로기준법|노동조합법|기간제법|파견법'),
    re.compile(r'정리해고|경영상\s*해고|구조조정'),
    re.compile(r'징계|면직|파면|정직|감봉|견책'),
]


def is_non_labor(rec):
    """비노동 판례 여부 판단. True면 비노동."""
    text = ' '.join(filter(None, [
        rec.get('title') or '',
        (rec.get('holding_points') or '')[:500],
        (rec.get('holding_summary') or '')[:300],
        rec.get('key_issue') or '',
    ]))

    if not text:
        return False

    # 노동 키워드가 있으면 노동 판례
    labor_hits = sum(1 for p in LABOR_CONFIRM_PATTERNS if p.search(text))
    if labor_hits >= 2:
        return False  # 확실한 노동 판례

    # 비노동 키워드가 있으면 비노동
    non_labor_hits = sum(1 for p in NON_LABOR_PATTERNS if p.search(text))
    if non_labor_hits >= 1 and labor_hits == 0:
        return True  # 비노동 확실

    # 애매한 경우: case_type이 '형사'이고 노동 키워드 없으면 비노동
    case_type = rec.get('case_type', '')
    if case_type == '형사' and labor_hits == 0:
        return True

    return False


def main():
    total = 0
    filtered = 0
    offset = 0

    while True:
        if LIMIT and total >= LIMIT:
            break

        r = requests.get(
            f'{SUPABASE_URL}/rest/v1/nlrc_decisions?id=like.bc_*&select=id,title,holding_points,holding_summary,key_issue,case_type,exclusion_flags&order=id&limit=500&offset={offset}',
            headers=headers_read, timeout=30
        )
        if r.status_code != 200:
            print(f'Read error: {r.status_code}')
            time.sleep(5)
            continue

        data = r.json()
        if not isinstance(data, list) or not data:
            break

        for rec in data:
            if LIMIT and total >= LIMIT:
                break
            total += 1

            if is_non_labor(rec):
                filtered += 1
                existing_flags = rec.get('exclusion_flags') or []
                if 'unrelated_to_dismissal' not in existing_flags:
                    new_flags = list(set(existing_flags + ['unrelated_to_dismissal']))

                    if DRY_RUN:
                        if filtered <= 10:
                            print(f"  FILTER: {rec['id']} - {rec.get('title','')[:60]}")
                            print(f"    key_issue: {rec.get('key_issue','')[:80]}")
                    else:
                        try:
                            requests.patch(
                                f'{SUPABASE_URL}/rest/v1/nlrc_decisions?id=eq.{rec["id"]}',
                                headers=headers_write,
                                json={'exclusion_flags': new_flags},
                                timeout=10
                            )
                        except:
                            pass

        offset += 500
        if total % 2000 < 500:
            print(f'Scanned {total}, filtered {filtered}...', flush=True)
        time.sleep(0.2)

    print(f'\nDone! Scanned: {total}, Non-labor filtered: {filtered} ({filtered/total*100:.1f}%)')
    if DRY_RUN:
        print('[DRY RUN]')


if __name__ == '__main__':
    main()
