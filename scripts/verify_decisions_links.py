#!/usr/bin/env python3
"""
/decisions/[id] 라우트 전수 검증.

전략:
- nlrc_decisions에서 ID 목록 fetch (offset/limit 페이지네이션)
- 각 ID에 대해 prod URL (?source= 자동 결정) HEAD/GET
- 200 + 본문에 "찾을 수 없습니다" 미포함이면 OK
- broken: 404, 5xx, 또는 not_found 콘텐츠

사용:
    python scripts/verify_decisions_links.py --sample 100         # 빠른 검증
    python scripts/verify_decisions_links.py --sample 500         # 중간 sample
    python scripts/verify_decisions_links.py --all                # 전수
    python scripts/verify_decisions_links.py --resume             # checkpoint 이어서
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILES = [ROOT / "supabase" / ".env", ROOT / ".env.local"]
RESULT_DIR = ROOT / "evaluation" / "link-verify"
RESULT_DIR.mkdir(parents=True, exist_ok=True)

PROD = "https://labor-decisions-search.vercel.app"
SUPABASE_URL = "https://mewqgevgdgghhatqtuos.supabase.co"
NOT_FOUND_PHRASES = [
    "판결을 찾을 수 없습니다",
    "판정례를 찾을 수 없습니다",
    "판례를 찾을 수 없습니다",
]


def load_env() -> None:
    for f in ENV_FILES:
        if not f.exists():
            continue
        for line in f.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def supabase_get(path: str, key: str) -> list[dict]:
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{path}",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def fetch_ids(key: str, sample: int | None) -> list[str]:
    """sample이면 prefix별로 비율대로 가져와 다양성 확보."""
    if not sample:
        # 전체
        ids: list[str] = []
        page_size = 1000
        offset = 0
        while True:
            path = f"nlrc_decisions?select=id&order=id.asc&limit={page_size}&offset={offset}"
            rows = supabase_get(path, key)
            if not rows:
                break
            ids.extend(r["id"] for r in rows)
            if len(rows) < page_size:
                break
            offset += page_size
        return ids

    # sample: prefix별 비율
    # bc_: 27%, id_: 71%, masked: 0.2%, others: 0.0% — 비례 sampling
    bc_target = max(int(sample * 0.27), 10)
    id_target = max(int(sample * 0.70), 10)
    masked_target = max(int(sample * 0.02), 5)
    out: list[str] = []
    for prefix_filter, n in [
        (f"id=like.bc_*&limit={bc_target}&order=id.asc", bc_target),
        (f"id=like.id_*&limit={id_target}&order=id.asc", id_target),
        (f"id=like.*OOO*&limit={masked_target}&order=id.asc", masked_target),
    ]:
        path = f"nlrc_decisions?select=id&{prefix_filter}"
        try:
            rows = supabase_get(path, key)
            out.extend(r["id"] for r in rows)
        except Exception as e:
            print(f"  fetch fail {prefix_filter}: {e}")
    return out[:sample]


def determine_source(case_id: str) -> str | None:
    if case_id.startswith("bc_"):
        return "bigcase"
    if case_id.startswith("prec_"):
        return "lawgo"
    return None  # default = nlrc


def check_link(case_id: str) -> dict:
    source = determine_source(case_id)
    qs = f"?source={source}" if source else ""
    url = f"{PROD}/decisions/{urllib.parse.quote(case_id)}{qs}"
    started = time.time()
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
        not_found = any(p in body for p in NOT_FOUND_PHRASES)
        ok = status == 200 and not not_found
        return {
            "id": case_id,
            "source": source or "nlrc",
            "status": status,
            "ok": ok,
            "not_found_text": not_found,
            "elapsed_ms": int((time.time() - started) * 1000),
        }
    except Exception as e:
        return {
            "id": case_id,
            "source": source or "nlrc",
            "status": 0,
            "ok": False,
            "error": str(e)[:200],
            "elapsed_ms": int((time.time() - started) * 1000),
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="샘플 건수 (0 = 전체)")
    ap.add_argument("--all", action="store_true", help="전수 (--sample 무시)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--resume", action="store_true", help="checkpoint 이어서")
    args = ap.parse_args()

    load_env()
    key = (
        os.environ.get("SUPABASE_SERVICE_KEY")
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    )
    if not key:
        sys.exit("Supabase 키 필요")

    sample = None if args.all else (args.sample or 100)
    print(f"[verify] sample={'ALL' if args.all else sample} workers={args.workers}")

    ids = fetch_ids(key, sample)
    print(f"  fetched {len(ids)}건")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_path = RESULT_DIR / f"verify_{timestamp}.jsonl"
    summary_path = RESULT_DIR / f"verify_{timestamp}_summary.json"

    done_ids: set[str] = set()
    if args.resume:
        latest = sorted(RESULT_DIR.glob("verify_*.jsonl"))
        if latest:
            for line in latest[-1].read_text().splitlines():
                try:
                    done_ids.add(json.loads(line)["id"])
                except Exception:
                    pass
            out_path = latest[-1]
            print(f"  resume from {out_path.name} ({len(done_ids)}건 skip)")

    targets = [i for i in ids if i not in done_ids]
    started = time.time()
    ok_count = 0
    broken_count = 0
    error_count = 0

    with out_path.open("a", encoding="utf-8") as out:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(check_link, cid): cid for cid in targets}
            for i, f in enumerate(as_completed(futures), 1):
                result = f.result()
                out.write(json.dumps(result, ensure_ascii=False) + "\n")
                out.flush()
                if result["ok"]:
                    ok_count += 1
                elif result.get("error"):
                    error_count += 1
                else:
                    broken_count += 1
                if i % 50 == 0 or i == len(targets):
                    elapsed = time.time() - started
                    rate = i / max(elapsed, 1)
                    eta = (len(targets) - i) / max(rate, 0.1)
                    print(
                        f"  [{i}/{len(targets)}] ok={ok_count} broken={broken_count} "
                        f"err={error_count} | {rate:.1f}/s eta={eta:.0f}s"
                    )

    summary = {
        "total": len(targets),
        "ok": ok_count,
        "broken": broken_count,
        "error": error_count,
        "ok_pct": round(ok_count / max(len(targets), 1) * 100, 2),
        "elapsed_s": round(time.time() - started, 1),
        "out": str(out_path),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n=== summary ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # broken 사건 sample 10건 추출
    if broken_count > 0:
        print("\n=== broken sample (최대 10건) ===")
        broken_samples = []
        for line in out_path.read_text().splitlines():
            try:
                r = json.loads(line)
                if not r["ok"] and not r.get("error"):
                    broken_samples.append(r)
                    if len(broken_samples) >= 10:
                        break
            except Exception:
                pass
        for r in broken_samples:
            print(f"  - {r['id']} ({r.get('source')}) status={r['status']} not_found={r.get('not_found_text')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
