#!/usr/bin/env python3
"""
nlrc_decisions 임베딩 재계산 (마이그레이션 후 stale 1536d 갱신)

전략:
- 입력 텍스트: f"{title}\n{key_issue}\n{holding_points[:500]}" (마이그레이션 후 풀버전 기준)
- 모델: text-embedding-3-small (1536d, $0.02/1M tokens)
- 배치: 100건씩 OpenAI batch endpoint
- DB: REST PATCH (parallel workers 4개)
- checkpoint: 처리한 ID는 별도 jsonl에 기록 → 중단 시 resume

사용법:
    python scripts/embed_recompute.py --sample 100             # 100건 시간/비용 측정 (DRY 1차)
    python scripts/embed_recompute.py --sample 100 --apply     # 100건 실제 측정 + UPDATE
    python scripts/embed_recompute.py --apply                  # 전체 실행
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterator

import requests

ROOT = Path(__file__).resolve().parent.parent
ENV_FILES = [ROOT / "supabase" / ".env", ROOT / ".env.local"]
CHECKPOINT = ROOT / "evaluation" / "embed_recompute_checkpoint.jsonl"


def load_env() -> None:
    for f in ENV_FILES:
        if not f.exists():
            continue
        for line in f.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def fetch_decisions_to_embed(
    sb_url: str, key: str, batch: int, offset: int
) -> list[dict]:
    """nlrc_decisions에서 페이지네이션. 5xx 일시 에러는 exponential backoff."""
    last_err = None
    for attempt in range(5):
        try:
            r = requests.get(
                f"{sb_url}/rest/v1/nlrc_decisions",
                params={
                    "select": "id,title,key_issue,holding_points",
                    "order": "id.asc",
                    "limit": batch,
                    "offset": offset,
                },
                headers={"apikey": key, "Authorization": f"Bearer {key}"},
                timeout=60,
            )
            if r.status_code == 200:
                return r.json()
            if r.status_code >= 500 or r.status_code == 429:
                wait = 5 * (2**attempt)
                print(f"  fetch {r.status_code} offset={offset}, {wait}s 대기 후 재시도 ({attempt+1}/5)")
                time.sleep(wait)
                last_err = f"{r.status_code}: {r.text[:200]}"
                continue
            r.raise_for_status()
        except requests.RequestException as e:
            wait = 5 * (2**attempt)
            print(f"  fetch RequestException, {wait}s 후 재시도: {e}")
            time.sleep(wait)
            last_err = str(e)
    print(f"  fetch 5회 실패, offset={offset} skip: {last_err}")
    return []


def build_input_text(row: dict) -> str:
    title = (row.get("title") or "").strip()
    ki = (row.get("key_issue") or "").strip()
    hp = (row.get("holding_points") or "").strip()
    parts = [p for p in [title, ki, hp[:500]] if p]
    return "\n".join(parts) or "(no content)"


def embed_batch(texts: list[str], openai_key: str) -> list[list[float]]:
    """OpenAI text-embedding-3-small batch."""
    r = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
        json={"model": "text-embedding-3-small", "input": texts},
        timeout=60,
    )
    r.raise_for_status()
    return [d["embedding"] for d in r.json()["data"]]


def patch_embedding(sb_url: str, key: str, dec_id: str, vec: list[float]) -> bool:
    r = requests.patch(
        f"{sb_url}/rest/v1/nlrc_decisions",
        params={"id": f"eq.{dec_id}"},
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        json={"embedding": vec},
        timeout=30,
    )
    return r.status_code in (200, 204)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="샘플 건수 (0=전체)")
    ap.add_argument("--batch", type=int, default=50, help="OpenAI batch size")
    ap.add_argument("--workers", type=int, default=4, help="DB PATCH 병렬")
    ap.add_argument("--start-offset", type=int, default=0)
    ap.add_argument("--apply", action="store_true", help="실제 UPDATE")
    args = ap.parse_args()

    load_env()
    sb_url = os.environ.get("SUPABASE_URL", "https://mewqgevgdgghhatqtuos.supabase.co")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not sb_key:
        sys.exit("SUPABASE_SERVICE_KEY 필요")
    if not openai_key:
        sys.exit("OPENAI_API_KEY 필요")

    target = args.sample or float("inf")
    print(f"[embed] sample={args.sample or 'ALL'} batch={args.batch} workers={args.workers} apply={args.apply}")
    started = time.time()
    seen = 0
    embedded = 0
    failed = 0
    cost_tokens = 0
    offset = args.start_offset

    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    cp = CHECKPOINT.open("a", encoding="utf-8") if args.apply else None

    while seen < target:
        rows = fetch_decisions_to_embed(sb_url, sb_key, args.batch, offset)
        if not rows:
            break

        texts = [build_input_text(r) for r in rows]
        try:
            t0 = time.time()
            vectors = embed_batch(texts, openai_key)
            embed_dt = time.time() - t0
            cost_tokens += sum(len(t) for t in texts) // 4  # 대략 tok ≈ chars/4
        except Exception as e:
            print(f"  embed batch fail offset={offset}: {e}")
            offset += args.batch
            failed += len(rows)
            continue

        if args.apply:
            t1 = time.time()
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futures = {
                    ex.submit(patch_embedding, sb_url, sb_key, rows[i]["id"], vectors[i]): i
                    for i in range(len(rows))
                }
                ok_count = 0
                for f in as_completed(futures):
                    i = futures[f]
                    try:
                        if f.result():
                            ok_count += 1
                            if cp:
                                cp.write(json.dumps({"id": rows[i]["id"], "ts": time.time()}) + "\n")
                        else:
                            failed += 1
                    except Exception:
                        failed += 1
            patch_dt = time.time() - t1
            embedded += ok_count
        else:
            patch_dt = 0
            embedded += len(rows)

        seen += len(rows)
        offset += args.batch

        elapsed = time.time() - started
        rate = seen / max(elapsed, 1)
        eta_total = 57833 / max(rate, 0.001)
        print(
            f"  offset={offset} embedded={embedded} failed={failed} | "
            f"embed_dt={embed_dt:.1f}s patch_dt={patch_dt:.1f}s | "
            f"rate={rate:.1f}/s eta={eta_total/60:.1f}min ({eta_total/3600:.1f}h)"
        )

        if seen >= target:
            break

    if cp:
        cp.close()

    elapsed = time.time() - started
    cost_usd = cost_tokens * 0.02 / 1_000_000  # $0.02 / 1M tokens
    print(f"\n=== 완료 ({elapsed:.0f}s) ===")
    print(f"  처리: {seen}, 임베딩: {embedded}, 실패: {failed}")
    print(f"  추정 토큰: {cost_tokens:,} (~${cost_usd:.4f})")
    print(f"  실측 rate: {seen/max(elapsed,1):.1f}/s → 전체 ETA: {57833 / max(seen/max(elapsed,1), 0.001) / 60:.0f}분")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
