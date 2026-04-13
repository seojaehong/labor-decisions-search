#!/usr/bin/env python3
"""BigCase 데이터 품질 벤치마크 — autoresearch 패턴의 '평가 함수'"""

import json
import sys
from urllib.request import Request, urlopen
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1].parent / 'labor-law-guide' / 'supabase' / '.env'
RESULTS_PATH = Path(__file__).resolve().parent / 'results.tsv'


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith('#') or '=' not in s:
            continue
        k, v = s.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def count(url, key, query_params):
    full = f"{url}/rest/v1/nlrc_decisions?select=id&{query_params}&limit=1"
    req = Request(full)
    req.add_header('apikey', key)
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('Prefer', 'count=exact')
    with urlopen(req, timeout=30) as r:
        cr = r.getheader('content-range', '0-0/0')
    return int(cr.split('/')[-1])


def run_benchmark():
    env = load_env()
    url = env['SUPABASE_URL'].rstrip('/')
    key = env['SUPABASE_SERVICE_KEY']

    total = count(url, key, 'id=neq.IMPOSSIBLE')
    bc_total = count(url, key, 'id=like.bc_*')
    id_total = count(url, key, 'id=like.id_*')

    # confidence_level
    conf_null = count(url, key, 'confidence_level=is.null')
    bc_conf_null = count(url, key, 'id=like.bc_*&confidence_level=is.null')
    id_conf_null = count(url, key, 'id=like.id_*&confidence_level=is.null')

    # tier
    tier_null = count(url, key, 'tier=is.null')
    bc_tier_null = count(url, key, 'id=like.bc_*&tier=is.null')

    # search_tsv (the broken column)
    tsv_null = count(url, key, 'search_tsv=is.null')

    # search_vector is GENERATED ALWAYS — can't query is.null directly via REST
    # Instead we check if the source fields are all null (which would make search_vector empty)
    vec_null = count(url, key, 'title=is.null&holding_points=is.null&holding_summary=is.null&key_issue=is.null')

    # key fields completeness
    title_null = count(url, key, 'title=is.null')
    holding_null = count(url, key, 'holding_summary=is.null')
    key_issue_null = count(url, key, 'key_issue=is.null')
    reason_cat_null = count(url, key, 'reason_category=is.null')

    metrics = {
        'total': total,
        'bc_total': bc_total,
        'id_total': id_total,
        'conf_null': conf_null,
        'conf_null_pct': round(conf_null / total * 100, 1),
        'bc_conf_null': bc_conf_null,
        'bc_conf_null_pct': round(bc_conf_null / bc_total * 100, 1) if bc_total else 0,
        'id_conf_null': id_conf_null,
        'tier_null': tier_null,
        'tier_null_pct': round(tier_null / total * 100, 1),
        'bc_tier_null': bc_tier_null,
        'search_tsv_null': tsv_null,
        'search_tsv_null_pct': round(tsv_null / total * 100, 1),
        'search_vector_null': vec_null,
        'search_vector_null_pct': round(vec_null / total * 100, 1),
        'title_null': title_null,
        'holding_null': holding_null,
        'key_issue_null': key_issue_null,
        'reason_cat_null': reason_cat_null,
        # composite score: lower is better (like val_bpb)
        'quality_score': round(
            (conf_null / total * 30) +
            (tier_null / total * 20) +
            (holding_null / total * 25) +
            (key_issue_null / total * 15) +
            (reason_cat_null / total * 10),
            4
        ),
    }

    return metrics


def print_report(m):
    print("=" * 60)
    print("BigCase 데이터 품질 벤치마크")
    print("=" * 60)
    print(f"총 레코드: {m['total']:,} (bc_: {m['bc_total']:,} / id_: {m['id_total']:,})")
    print()
    print(f"confidence_level NULL: {m['conf_null']:,} ({m['conf_null_pct']}%)")
    print(f"  bc_ NULL: {m['bc_conf_null']:,} ({m['bc_conf_null_pct']}%)")
    print(f"  id_ NULL: {m['id_conf_null']:,}")
    print(f"tier NULL: {m['tier_null']:,} ({m['tier_null_pct']}%)")
    print(f"  bc_ tier NULL: {m['bc_tier_null']:,}")
    print(f"search_tsv NULL: {m['search_tsv_null']:,} ({m['search_tsv_null_pct']}%)")
    print(f"search_vector NULL: {m['search_vector_null']:,} ({m['search_vector_null_pct']}%)")
    print(f"title NULL: {m['title_null']:,}")
    print(f"holding_summary NULL: {m['holding_null']:,}")
    print(f"key_issue NULL: {m['key_issue_null']:,}")
    print(f"reason_category NULL: {m['reason_cat_null']:,}")
    print()
    print(f"--- quality_score: {m['quality_score']:.4f} (lower is better) ---")
    print()


if __name__ == '__main__':
    m = run_benchmark()
    print_report(m)
    # output JSON for programmatic use
    if '--json' in sys.argv:
        print(json.dumps(m, ensure_ascii=False, indent=2))
