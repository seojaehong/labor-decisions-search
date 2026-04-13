#!/usr/bin/env python3
"""실험 005: key_issue NULL 545건 보강
holding_summary가 있는 경우 → holding_summary를 key_issue로 복사
둘 다 NULL인 경우 → title에서 추출
"""

import json
from urllib.request import Request, urlopen
from urllib.parse import quote
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


def get_records(url, key, filter_params, select='id,title,holding_summary', page_size=1000):
    records = []
    offset = 0
    while True:
        full = f"{url}/rest/v1/nlrc_decisions?select={select}&{filter_params}&limit={page_size}&offset={offset}&order=id"
        req = Request(full)
        req.add_header('apikey', key)
        req.add_header('Authorization', f'Bearer {key}')
        with urlopen(req, timeout=60) as r:
            rows = json.loads(r.read().decode('utf-8'))
        if not rows:
            break
        records.extend(rows)
        if len(rows) < page_size:
            break
        offset += page_size
    return records


def patch_one(url, key, record_id, body):
    encoded = quote(record_id, safe='')
    full = f"{url}/rest/v1/nlrc_decisions?id=eq.{encoded}"
    req = Request(full, method='PATCH')
    req.add_header('apikey', key)
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Prefer', 'return=minimal')
    with urlopen(req, data=json.dumps(body).encode('utf-8'), timeout=30) as r:
        r.read()


def run():
    env = load_env()
    url = env['SUPABASE_URL'].rstrip('/')
    key = env['SUPABASE_SERVICE_KEY']

    print('=== 실험 005: key_issue NULL 보강 ===')

    records = get_records(url, key, 'key_issue=is.null')
    print(f'대상: {len(records)}건')

    done = 0
    for i, rec in enumerate(records):
        rid = rec['id']
        holding = rec.get('holding_summary') or ''
        title = rec.get('title') or ''

        if holding:
            issue = holding
        elif title:
            # title에서 사건 유형 추출
            parts = title.split(' ')
            if len(parts) > 5:
                case_type = parts[-1]
                issue = f"{case_type}에 관한 쟁점"
            else:
                issue = title
        else:
            continue

        try:
            patch_one(url, key, rid, {'key_issue': issue})
            done += 1
        except Exception as e:
            print(f'  WARN {rid}: {e}')

        if (i + 1) % 100 == 0:
            print(f'  {done}/{len(records)}...')

    print(f'\n완료: {done}/{len(records)}')


if __name__ == '__main__':
    run()
