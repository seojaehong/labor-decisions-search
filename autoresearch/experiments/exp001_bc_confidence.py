#!/usr/bin/env python3
"""실험 001: bc_ confidence_level 일괄 세팅
전략: 먼저 ID 목록 가져온 뒤 소규모 배치로 PATCH"""

import json
from urllib.request import Request, urlopen
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[2].parent / 'labor-law-guide' / 'supabase' / '.env'


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
    """GET으로 ID 목록 가져오기 (Supabase 1000건 제한 페이지네이션)"""
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
        print(f'  fetched {len(ids)} ids so far...')
        if len(rows) < page_size:
            break
        offset += page_size
    return ids


def patch_by_ids(url, key, ids, body, batch_size=50):
    """ID 목록으로 소규모 배치 PATCH"""
    from urllib.parse import quote
    import time
    total = 0
    for i in range(0, len(ids), batch_size):
        batch = ids[i:i+batch_size]
        id_csv = ','.join(batch)
        filter_str = f'id=in.({id_csv})'
        full = f"{url}/rest/v1/nlrc_decisions?{filter_str}"
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
            print(f'  WARN batch {i}: {e}, retrying with smaller batch...')
            for sid in batch:
                try:
                    one_url = f"{url}/rest/v1/nlrc_decisions?id=eq.{sid}"
                    req2 = Request(one_url, method='PATCH')
                    req2.add_header('apikey', key)
                    req2.add_header('Authorization', f'Bearer {key}')
                    req2.add_header('Content-Type', 'application/json')
                    req2.add_header('Prefer', 'return=minimal')
                    with urlopen(req2, data=data, timeout=30) as r:
                        r.read()
                    total += 1
                except Exception:
                    pass
            time.sleep(0.5)
        if (i // batch_size) % 20 == 0:
            print(f'  {total}/{len(ids)}...')
    return total


def run():
    env = load_env()
    url = env['SUPABASE_URL'].rstrip('/')
    key = env['SUPABASE_SERVICE_KEY']

    print('=== 실험 001: bc_ confidence_level 세팅 ===')

    # 0.9: all fields present
    print('\n[0.9] title + holding_summary + key_issue 모두 있는 bc_')
    ids_09 = get_ids(url, key,
        'id=like.bc_*&confidence_level=is.null&title=not.is.null&holding_summary=not.is.null&key_issue=not.is.null')
    print(f'  대상: {len(ids_09)}건')
    n1 = patch_by_ids(url, key, ids_09, {'confidence_level': '0.9'}) if ids_09 else 0

    # 0.7: title + holding, no key_issue
    print('\n[0.7] title + holding_summary 있고 key_issue NULL')
    ids_07 = get_ids(url, key,
        'id=like.bc_*&confidence_level=is.null&title=not.is.null&holding_summary=not.is.null&key_issue=is.null')
    print(f'  대상: {len(ids_07)}건')
    n2 = patch_by_ids(url, key, ids_07, {'confidence_level': '0.7'}) if ids_07 else 0

    # 0.5: title only
    print('\n[0.5] title만 있고 holding_summary NULL')
    ids_05 = get_ids(url, key,
        'id=like.bc_*&confidence_level=is.null&title=not.is.null&holding_summary=is.null')
    print(f'  대상: {len(ids_05)}건')
    n3 = patch_by_ids(url, key, ids_05, {'confidence_level': '0.5'}) if ids_05 else 0

    # 0.3: remaining
    print('\n[0.3] 나머지')
    ids_03 = get_ids(url, key, 'id=like.bc_*&confidence_level=is.null')
    print(f'  대상: {len(ids_03)}건')
    n4 = patch_by_ids(url, key, ids_03, {'confidence_level': '0.3'}) if ids_03 else 0

    print(f'\n총: 0.9={n1}, 0.7={n2}, 0.5={n3}, 0.3={n4} (합계 {n1+n2+n3+n4})')


if __name__ == '__main__':
    run()
