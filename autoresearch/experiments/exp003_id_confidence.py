#!/usr/bin/env python3
"""실험 003: id_ confidence_level NULL 1,568건 세팅
id_ 레코드는 대부분 0.9였으나 일부 누락. 동일 기준 적용."""

import json
from urllib.request import Request, urlopen
from pathlib import Path
import time

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
        except Exception:
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
        if (i // batch_size) % 10 == 0:
            print(f'  {total}/{len(ids)}...')
    return total


def run():
    env = load_env()
    url = env['SUPABASE_URL'].rstrip('/')
    key = env['SUPABASE_SERVICE_KEY']

    print('=== 실험 003: id_ confidence_level 세팅 ===')

    # 0.9: all fields
    ids_09 = get_ids(url, key, 'id=like.id_*&confidence_level=is.null&title=not.is.null&holding_summary=not.is.null&key_issue=not.is.null')
    print(f'[0.9] {len(ids_09)}건')
    n1 = patch_by_ids(url, key, ids_09, {'confidence_level': '0.9'}) if ids_09 else 0

    ids_07 = get_ids(url, key, 'id=like.id_*&confidence_level=is.null&title=not.is.null&holding_summary=not.is.null&key_issue=is.null')
    print(f'[0.7] {len(ids_07)}건')
    n2 = patch_by_ids(url, key, ids_07, {'confidence_level': '0.7'}) if ids_07 else 0

    ids_05 = get_ids(url, key, 'id=like.id_*&confidence_level=is.null&title=not.is.null&holding_summary=is.null')
    print(f'[0.5] {len(ids_05)}건')
    n3 = patch_by_ids(url, key, ids_05, {'confidence_level': '0.5'}) if ids_05 else 0

    ids_03 = get_ids(url, key, 'id=like.id_*&confidence_level=is.null')
    print(f'[0.3] {len(ids_03)}건')
    n4 = patch_by_ids(url, key, ids_03, {'confidence_level': '0.3'}) if ids_03 else 0

    # Also handle any non-bc/non-id records
    ids_other = get_ids(url, key, 'confidence_level=is.null')
    if ids_other:
        print(f'[기타] {len(ids_other)}건')
        patch_by_ids(url, key, ids_other, {'confidence_level': '0.6'})

    print(f'\n총: 0.9={n1}, 0.7={n2}, 0.5={n3}, 0.3={n4}')


if __name__ == '__main__':
    run()
