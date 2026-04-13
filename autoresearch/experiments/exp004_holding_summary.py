#!/usr/bin/env python3
"""실험 004: holding_summary NULL 685건 보강
key_issue가 있는 경우 → key_issue를 holding_summary로 복사
key_issue도 NULL인 경우 → title에서 추출
"""

import json
from urllib.request import Request, urlopen
from urllib.parse import quote
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


def get_records(url, key, filter_params, select='id,title,key_issue', page_size=1000):
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

    print('=== 실험 004: holding_summary NULL 보강 ===')

    records = get_records(url, key, 'holding_summary=is.null')
    print(f'대상: {len(records)}건')

    done = 0
    for i, rec in enumerate(records):
        rid = rec['id']
        key_issue = rec.get('key_issue') or ''
        title = rec.get('title') or ''

        if key_issue:
            summary = key_issue
        elif title:
            # title에서 판결 유형 추출: "대법원 2021. 5. 14. 선고 ... 판결 해고무효확인등"
            # → "해고무효확인등에 관한 사건"
            parts = title.split(' ')
            if len(parts) > 5:
                case_type = ' '.join(parts[-1:])  # 마지막 부분이 보통 사건 유형
                summary = f"{case_type}에 관한 사건"
            else:
                summary = title
        else:
            continue

        try:
            patch_one(url, key, rid, {'holding_summary': summary})
            done += 1
        except Exception as e:
            print(f'  WARN {rid}: {e}')

        if (i + 1) % 100 == 0:
            print(f'  {done}/{len(records)}...')

    print(f'\n완료: {done}/{len(records)}')


if __name__ == '__main__':
    run()
