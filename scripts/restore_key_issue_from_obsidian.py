#!/usr/bin/env python3
"""
restore_key_issue_from_obsidian.py
==================================
nlrc_decisions.key_issue가 ~150자에서 truncate된 문제 복원.

옵시디언 볼트의 id_NNNNNN.md 파일에서 ## 판정요지 섹션을 추출 →
nlrc_decisions.key_issue 컬럼을 풀버전으로 업데이트.

매칭: nlrc_decisions.id (id_NNNNNN) ↔ obsidian 파일명 (id_NNNNNN.md)

사용법:
    python scripts/restore_key_issue_from_obsidian.py            # DRY RUN (5건 미리보기)
    python scripts/restore_key_issue_from_obsidian.py --check    # 매칭 통계만
    python scripts/restore_key_issue_from_obsidian.py --apply    # 실제 UPDATE
"""

from __future__ import annotations
import argparse
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterator

import requests

VAULT_DIR = Path("/home/ubuntu/onedrive/5.산업안전/문서/Obsidian Vault/노동위판정례")
SUPABASE_URL = "https://mewqgevgdgghhatqtuos.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY"
)

if not SUPABASE_KEY:
    env_path = "/home/ubuntu/work-orchestrator/repos/labor-law-guide/supabase/.env"
    if Path(env_path).exists():
        for line in Path(env_path).read_text().splitlines():
            if line.startswith("SUPABASE_SERVICE_KEY="):
                SUPABASE_KEY = line.split("=", 1)[1].strip()
                break

if not SUPABASE_KEY:
    sys.exit("SUPABASE_SERVICE_KEY 환경변수 또는 .env 파일 필요")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}

# 판정요지 섹션 추출: "## 판정요지" 다음 줄부터 다음 ## 또는 --- 까지
PANJEONG_RE = re.compile(
    r"##\s*판정요지\s*\n+(.+?)(?=\n##|\n---|\Z)", re.DOTALL
)


def parse_obsidian(path: Path) -> str | None:
    """옵시디언 md 파일에서 판정요지 본문 추출."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = PANJEONG_RE.search(text)
    if not m:
        return None
    body = m.group(1).strip()
    # frontmatter 잔여 제거
    body = re.sub(r"^---\n.*?\n---\n", "", body, flags=re.DOTALL)
    return body if len(body) >= 50 else None


def iter_id_files() -> Iterator[tuple[str, Path]]:
    """id_NNNNNN.md 형식 파일만 yield."""
    for p in VAULT_DIR.iterdir():
        if not p.is_file() or p.suffix != ".md":
            continue
        if not p.stem.startswith("id_"):
            continue
        yield p.stem, p


def fetch_db_best(case_id: str) -> tuple[str | None, str | None, int | None]:
    """DB에서 key_issue/holding_summary/holding_points 중 가장 긴 텍스트를 반환.
    returns: (current_key_issue, longest_db_text, longest_db_len)"""
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/nlrc_decisions",
        params={
            "select": "key_issue,holding_summary,holding_points",
            "id": f"eq.{case_id}",
        },
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
        timeout=15,
    )
    if r.status_code != 200:
        return None, None, None
    arr = r.json()
    if not arr:
        return None, None, None
    ki = (arr[0].get("key_issue") or "").strip()
    hs = (arr[0].get("holding_summary") or "").strip()
    hp = (arr[0].get("holding_points") or "").strip()
    longest = max(ki, hs, hp, key=len)
    return ki, longest, len(longest)


def update_key_issue(case_id: str, new_text: str) -> bool:
    r = requests.patch(
        f"{SUPABASE_URL}/rest/v1/nlrc_decisions",
        params={"id": f"eq.{case_id}"},
        headers=HEADERS,
        json={"key_issue": new_text},
        timeout=20,
    )
    return r.status_code in (200, 204)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제 UPDATE 수행")
    ap.add_argument("--check", action="store_true", help="매칭 통계만 출력")
    ap.add_argument(
        "--limit", type=int, default=0, help="처리할 최대 건수 (0=전체)"
    )
    ap.add_argument(
        "--min-improvement",
        type=int,
        default=200,
        help="옵시디언 텍스트가 DB보다 최소 N자 길어야 업데이트 (기본 200)",
    )
    args = ap.parse_args()

    print(f"[scan] {VAULT_DIR}")
    files = list(iter_id_files())
    print(f"[scan] id_*.md 파일 {len(files):,}건 발견")

    if args.check:
        # 처음 100개로 샘플 통계
        parsed_ok = 0
        for stem, path in files[:200]:
            if parse_obsidian(path):
                parsed_ok += 1
        print(
            f"[check] 200개 샘플 중 판정요지 파싱 성공: {parsed_ok}/200 "
            f"({parsed_ok/200*100:.0f}%)"
        )
        return 0

    updated = 0
    skipped_short = 0
    skipped_nodb = 0
    skipped_parse = 0
    preview_done = 0
    started = time.time()

    target = files if args.limit == 0 else files[: args.limit]
    print(f"[run] 처리 대상: {len(target):,}건  apply={args.apply}")

    for idx, (stem, path) in enumerate(target):
        new_text = parse_obsidian(path)
        if not new_text:
            skipped_parse += 1
            continue

        cur_ki, longest_db, longest_len = fetch_db_best(stem)
        if longest_len is None:
            skipped_nodb += 1
            continue

        # 옵시디언 vs DB 컬럼 중 가장 긴 것 비교 (key_issue 기준 개선분만 측정)
        cur_ki_len = len(cur_ki or "")
        # final_text: 옵시디언과 DB 최장값 중 더 긴 것
        final_text = new_text if len(new_text) >= longest_len else longest_db
        improvement = len(final_text) - cur_ki_len
        if improvement < args.min_improvement:
            skipped_short += 1
            continue

        if not args.apply:
            if preview_done < 5:
                src = "옵시디언" if final_text == new_text else "DB(holding_summary/points)"
                print(f"\n=== [{stem}] DRY (소스: {src}) ===")
                print(f"  현재 key_issue({cur_ki_len}자): ...{(cur_ki or '')[-60:]}")
                print(f"  새 텍스트({len(final_text)}자): ...{final_text[-80:]}")
                preview_done += 1
            updated += 1
        else:
            if update_key_issue(stem, final_text):
                updated += 1
                if updated % 200 == 0:
                    elapsed = time.time() - started
                    rate = updated / elapsed if elapsed else 0
                    print(
                        f"  진행: {updated:,}건 업데이트 ({rate:.1f} req/s, "
                        f"{idx+1}/{len(target)})"
                    )
            else:
                skipped_nodb += 1

    elapsed = time.time() - started
    print(
        f"\n=== 완료 ({elapsed:.0f}s) ===\n"
        f"  업데이트{'' if args.apply else ' (DRY)'}: {updated:,}\n"
        f"  스킵 (DB 미존재): {skipped_nodb:,}\n"
        f"  스킵 (개선 < {args.min_improvement}자): {skipped_short:,}\n"
        f"  스킵 (판정요지 파싱 실패): {skipped_parse:,}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
