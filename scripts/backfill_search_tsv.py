#!/usr/bin/env python3
"""
search_tsv 차등 가중치 backfill.
트리거 함수는 이미 setweight 버전으로 업데이트됨 (apply_migration).
이 스크립트는 기존 57k 행을 작은 batch로 update해 setweight 적용.

사용:
  python scripts/backfill_search_tsv.py             # 전수 진행
  python scripts/backfill_search_tsv.py --batch 200 # 배치 크기 변경
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILES = [
    Path("/home/ubuntu/work-orchestrator/repos/labor-law-guide/supabase/.env"),
    ROOT / "supabase" / ".env",
    ROOT / ".env.local",
]
SUPABASE_URL = "https://mewqgevgdgghhatqtuos.supabase.co"


def load_env() -> None:
    for f in ENV_FILES:
        if not f.exists():
            continue
        for line in f.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def get(path: str, key: str) -> list[dict]:
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{path}",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def patch(path: str, key: str, body: list[dict]) -> int:
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{path}",
        method="PATCH",
        data=json.dumps(body).encode(),
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    resp = urllib.request.urlopen(req, timeout=60)
    return resp.status


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=200, help="batch size")
    ap.add_argument("--start-from", type=str, default="", help="resume cursor (id)")
    ap.add_argument("--max-rounds", type=int, default=400, help="safety cap")
    ap.add_argument("--sleep", type=float, default=0.5, help="seconds between batches")
    args = ap.parse_args()

    load_env()
    key = (
        os.environ.get("SUPABASE_SERVICE_KEY")
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    )
    if not key:
        sys.exit("Supabase service key 필요 (SUPABASE_SERVICE_KEY)")

    cursor = args.start_from
    total_updated = 0
    started = time.time()
    log_path = ROOT / "evaluation" / "search_tsv_backfill.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    for r in range(args.max_rounds):
        # 다음 batch의 id 목록 가져오기 (cursor 이후)
        cursor_filter = f"&id=gt.{urllib.parse.quote(cursor)}" if cursor else ""
        rows = get(
            f"nlrc_decisions?select=id,title,case_number,key_issue,holding_summary,holding_points,case_type&order=id.asc&limit={args.batch}{cursor_filter}",
            key,
        )
        if not rows:
            print(f"[done] no more rows after cursor={cursor!r}")
            break

        # PATCH: 같은 컬럼 값을 그대로 다시 쓰면 트리거가 search_tsv 재계산 — 트랜잭션 가벼움
        # title, case_number 등 컬럼 자체는 변경 없이 동일 값 PATCH
        for row in rows:
            url = (
                f"nlrc_decisions?id=eq.{urllib.parse.quote(row['id'])}"
            )
            try:
                patch(
                    url,
                    key,
                    {"title": row.get("title")},  # 트리거 발동을 위해 단일 컬럼 재쓰기
                )
                total_updated += 1
            except Exception as e:
                print(f"  fail id={row['id']}: {e}")

        cursor = rows[-1]["id"]
        elapsed = time.time() - started
        rate = total_updated / max(elapsed, 1)
        eta = (57841 - total_updated) / max(rate, 0.1)
        msg = f"[round {r+1}] cursor={cursor[:30]} total={total_updated} elapsed={elapsed:.0f}s rate={rate:.1f}/s eta={eta:.0f}s"
        print(msg)
        with log_path.open("a") as f:
            f.write(msg + "\n")

        time.sleep(args.sleep)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
