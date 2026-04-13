#!/usr/bin/env python3
"""실험 002: tier 일괄 세팅
reason_category는 배열 타입 → cs (contains) 필터 사용
"""

import json
from urllib.request import Request, urlopen
from pathlib import Path
import time

ENV_PATH = Path(__file__).resolve().parents[2].parent / 'labor-law-guide' / 'supabase' / '.env'

HIGH_PRIORITY_CATS = [
    'workplace_bullying', 'unfair_dismissal', 'wage_theft', 'wage',
    'industrial_accident', 'sexual_harassment', 'probation_dismissal',
    'probation', 'redundancy', 'transfer'
]


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith('#') or '=' not in s:
            continue
        k, v = s.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def get_ids(url, key, filter_params, page_size=1000):
    ids = []
    offset = 0
    while True:
        full = f"{url}/rest/v1/nlrc_decisions?select=id&{filter_params}&limit={page_size}&offset={offset}&order=id"
        req = Request(full)
        req.add_header('apikey', key)
        req.add_header('Authorization', f'Bearer {key}')
        with urlopen(req, timeout=60) as r:
            rows = json.loads(r.read().decode('utf-8'))
        if not rows:
            break
        ids.extend(row['id'] for row in rows)
        if len(rows) < page_size:
            break
        offset += page_size
    return ids


def patch_by_ids(url, key, ids, body, batch_size=50):
    total = 0
    for i in range(0, len(ids), batch_size):
        batch = ids[i:i+batch_size]
        id_csv = ','.join(batch)
        full = f"{url}/rest/v1/nlrc_decisions?id=in.({id_csv})"
        req = Request(full, method='PATCH')
        req.add_header('apikey', key)
        req.add_header('Authorization', f'Bearer {key}')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Prefer', 'return=minimal')
        data = json.dumps(body).encode('utf-8')
        try:
            with urlopen(req, data=data, timeout=60) as r:
                r.read()
            total += len(batch)
        except Exception as e:
            for sid in batch:
                try:
                    req2 = Request(f"{url}/rest/v1/nlrc_decisions?id=eq.{sid}", method='PATCH')
                    req2.add_header('apikey', key)
                    req2.add_header('Authorization', f'Bearer {key}')
                    req2.add_header('Content-Type', 'application/json')
                    req2.add_header('Prefer', 'return=minimal')
                    with urlopen(req2, data=data, timeout=30) as r:
                        r.read()
                    total += 1
                except Exception:
                    pass
            time.sleep(0.3)
        if (i // batch_size) % 20 == 0:
            print(f'  {total}/{len(ids)}...')
    return total


def run():
    env = load_env()
    url = env['SUPABASE_URL'].rstrip('/')
    key = env['SUPABASE_SERVICE_KEY']

    print('=== 실험 002: tier 세팅 ===')

    # Step 1: high_priority — 각 카테고리별 contains 쿼리
    all_high_ids = set()
    for cat in HIGH_PRIORITY_CATS:
        # cs = contains: reason_category array contains this value
        ids = get_ids(url, key, f'tier=is.null&reason_category=cs.{{{cat}}}')
        all_high_ids.update(ids)
        if ids:
            print(f'  {cat}: {len(ids)}건')

    print(f'\n[high_priority] 총 {len(all_high_ids)}건')
    n1 = patch_by_ids(url, key, list(all_high_ids), {'tier': 'high_priority'}) if all_high_ids else 0

    # Step 2: standard — reason_category NOT NULL이고 아직 tier NULL
    print(f'\n[standard] reason_category 있고 tier 아직 NULL')
    ids_std = get_ids(url, key, 'tier=is.null&reason_category=not.is.null')
    print(f'  대상: {len(ids_std)}건')
    n2 = patch_by_ids(url, key, ids_std, {'tier': 'standard'}) if ids_std else 0

    # Step 3: low_priority — 나머지
    print(f'\n[low_priority] 나머지 tier NULL')
    ids_low = get_ids(url, key, 'tier=is.null')
    print(f'  대상: {len(ids_low)}건')
    n3 = patch_by_ids(url, key, ids_low, {'tier': 'low_priority'}) if ids_low else 0

    print(f'\n총: high={n1}, standard={n2}, low={n3} (합계 {n1+n2+n3})')


if __name__ == '__main__':
    run()
