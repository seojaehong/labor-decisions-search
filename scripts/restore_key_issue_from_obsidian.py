#!/usr/bin/env python3
"""
restore_key_issue_from_obsidian.py
==================================
nlrc_decisions.key_issue가 ~150자에서 truncate된 문제 복원.

전략:
1. DB에서 short-key_issue 행 페이지네이션으로 fetch (빠름)
2. 각 행마다 옵시디언 id_NNNNNN.md 파일 직접 path 접근 (lookup)
3. 옵시디언 vs DB 컬럼(key_issue/holding_summary/holding_points) 중 가장 긴 텍스트로 UPDATE

사용법:
    python scripts/restore_key_issue_from_obsidian.py            # DRY 5건 미리보기
    python scripts/restore_key_issue_from_obsidian.py --limit N  # 처음 N건 처리
    python scripts/restore_key_issue_from_obsidian.py --apply    # 전체 실제 UPDATE
"""

from __future__ import annotations
import argparse
import os
import re
import sys
import time
from pathlib import Path

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

PATCH_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}
GET_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

PANJEONG_RE = re.compile(
    r"##\s*판정요지\s*\n+(.+?)(?=\n##|\n---|\Z)", re.DOTALL
)


def parse_obsidian_file(stem: str) -> str | None:
    """파일명(stem) → 판정요지 본문."""
    p = VAULT_DIR / f"{stem}.md"
    try:
        text = p.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return None
    m = PANJEONG_RE.search(text)
    if not m:
        return None
    body = m.group(1).strip()
    return body if len(body) >= 50 else None


def find_obsidian(case_id: str, case_number: str | None) -> str | None:
    """nlrc_decisions.id 또는 case_number로 옵시디언 파일 lookup. 둘 다 시도."""
    # 1차: id_NNNNNN.md 형식 (newer files)
    if case_id and case_id.startswith("id_"):
        body = parse_obsidian_file(case_id)
        if body:
            return body
    # 2차: case_number (예: 2015부해OOO.md, older files)
    if case_number:
        body = parse_obsidian_file(case_number)
        if body:
            return body
    return None


def fetch_short_rows(offset: int, batch: int) -> list[dict]:
    """key_issue가 짧은 (200자 이하) 행을 페이지네이션으로 가져옴."""
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/nlrc_decisions",
        params={
            "select": "id,case_number,key_issue,holding_summary,holding_points",
            "order": "id.asc",
            "limit": batch,
            "offset": offset,
        },
        headers=GET_HEADERS,
        timeout=30,
    )
    if r.status_code != 200:
        return []
    return r.json()


def update_key_issue(case_id: str, new_text: str) -> bool:
    r = requests.patch(
        f"{SUPABASE_URL}/rest/v1/nlrc_decisions",
        params={"id": f"eq.{case_id}"},
        headers=PATCH_HEADERS,
        json={"key_issue": new_text},
        timeout=20,
    )
    return r.status_code in (200, 204)


def pick_best(ki: str, hs: str, hp: str, obsidian: str | None) -> tuple[str, str]:
    """key_issue/holding_summary/holding_points/obsidian 중 가장 긴 것을 선택. (text, source) 반환"""
    candidates = [(ki or "", "key_issue"), (hs or "", "holding_summary"), (hp or "", "holding_points")]
    if obsidian:
        candidates.append((obsidian, "obsidian"))
    best = max(candidates, key=lambda c: len(c[0]))
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제 UPDATE 수행")
    ap.add_argument("--limit", type=int, default=0, help="처리할 행 수 (0=전체)")
    ap.add_argument("--batch", type=int, default=200, help="페이지 사이즈")
    ap.add_argument(
        "--min-improvement",
        type=int,
        default=200,
        help="key_issue 대비 +N자 이상 개선되어야 update (기본 200)",
    )
    ap.add_argument("--start-offset", type=int, default=0)
    ap.add_argument(
        "--no-obsidian",
        action="store_true",
        help="옵시디언 lookup 건너뛰기 (DB 컬럼만 사용, 빠름)",
    )
    ap.add_argument(
        "--vault-dir",
        type=str,
        default=str(VAULT_DIR),
        help="옵시디언 vault 경로 (로컬 캐시 사용 시 변경)",
    )
    args = ap.parse_args()
    if args.vault_dir != str(VAULT_DIR):
        globals()["VAULT_DIR"] = Path(args.vault_dir)

    print(f"[run] apply={args.apply}  limit={args.limit}  batch={args.batch}")
    started = time.time()

    seen = 0
    updated = 0
    by_source = {"obsidian": 0, "holding_summary": 0, "holding_points": 0, "key_issue": 0}
    skipped_no_change = 0
    preview_done = 0
    offset = args.start_offset

    while True:
        rows = fetch_short_rows(offset, args.batch)
        if not rows:
            break

        for row in rows:
            seen += 1
            cur_id = row["id"]
            case_no = (row.get("case_number") or "").strip()
            ki = (row.get("key_issue") or "").strip()
            hs = (row.get("holding_summary") or "").strip()
            hp = (row.get("holding_points") or "").strip()

            obsidian_text = None if args.no_obsidian else find_obsidian(cur_id, case_no)

            best_text, source = pick_best(ki, hs, hp, obsidian_text)
            improvement = len(best_text) - len(ki)
            if improvement < args.min_improvement or best_text == ki:
                skipped_no_change += 1
                continue

            by_source[source] = by_source.get(source, 0) + 1

            if not args.apply:
                if preview_done < 5:
                    print(f"\n=== [{cur_id}] DRY (소스: {source}) ===")
                    print(f"  현재 ki({len(ki)}자): {ki[:80]}...")
                    print(f"  새 텍스트({len(best_text)}자, +{improvement}): {best_text[:120]}")
                    preview_done += 1
                updated += 1
            else:
                if update_key_issue(cur_id, best_text):
                    updated += 1
                    if updated % 200 == 0:
                        elapsed = time.time() - started
                        rate = updated / max(elapsed, 1)
                        print(
                            f"  진행: {updated:,} update / {seen:,} seen ({rate:.1f}/s)"
                        )

            if args.limit > 0 and seen >= args.limit:
                break

        if args.limit > 0 and seen >= args.limit:
            break
        offset += args.batch

    elapsed = time.time() - started
    print(
        f"\n=== 완료 ({elapsed:.0f}s) ===\n"
        f"  스캔: {seen:,}\n"
        f"  업데이트{'' if args.apply else ' (DRY)'}: {updated:,}\n"
        f"  소스별: {by_source}\n"
        f"  변경 없음: {skipped_no_change:,}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
