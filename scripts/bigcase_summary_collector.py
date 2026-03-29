"""
BigCase 비회원 요지 수집기
— 인증 없이 __NEXT_DATA__에서 판시사항/재판요지/AI요약만 수집
— rate limit 회피를 위해 60초 딜레이
— 회원 정보 절대 사용 안 함
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

REPO_DIR = Path(__file__).parent.parent
LOG_DIR = REPO_DIR / "evaluation" / "bigcase_bulk" / "logs" / "summary_collector"
DEFAULT_PARSE_VERSION = "summary-noauth-v1"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SPACE_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n{3,}")
NEXT_DATA_RE = re.compile(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BigCase summary collector (no auth)")
    parser.add_argument("--parse-version", default=DEFAULT_PARSE_VERSION)
    parser.add_argument("--mode", choices=["missing-only", "all", "upgrade-summary"], default="missing-only")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--delay", type=float, default=60.0, help="초 단위 딜레이 (기본 60초)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--offset", type=int, default=0, help="시작 오프셋 (이어서 수집)")
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip()
            if name not in os.environ:
                os.environ[name] = value.strip()


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Error: {name} must be set")
    return value


def build_supabase_headers() -> dict[str, str]:
    service_key = require_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }


def clean_text(value: str | list | None) -> str:
    if not value:
        return ""
    if isinstance(value, list):
        value = "\n".join(str(v) for v in value)
    value = str(value)
    text = value.replace("\\n", "\n").replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    text = "\n".join(SPACE_RE.sub(" ", line).strip() for line in text.splitlines())
    text = BLANK_RE.sub("\n\n", text)
    return text.strip()


# ============================================================
# Supabase 통신
# ============================================================

def fetch_paginated(endpoint: str, params: dict[str, str], id_field: str = "id") -> list[dict[str, Any]]:
    """Range-header pagination to handle large tables (offset > 10000)."""
    rows: list[dict[str, Any]] = []
    page_size = 1000
    service_key = require_env("SUPABASE_SERVICE_KEY")
    supabase_url = require_env("SUPABASE_URL")
    start = 0

    while True:
        merged = dict(params)
        headers = {
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Range": f"{start}-{start + page_size - 1}",
            "Range-Unit": "items",
        }
        for _retry in range(3):
            resp = requests.get(
                f"{supabase_url}/rest/v1/{endpoint}",
                headers=headers,
                params=merged,
                timeout=60,
            )
            if resp.status_code < 500:
                break
            time.sleep(5 * (_retry + 1))
        if resp.status_code == 416:  # Range not satisfiable = no more rows
            break
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break
        rows.extend(chunk)
        if len(chunk) < page_size:
            break
        start += page_size
    return rows


def fetch_target_decisions() -> list[dict[str, Any]]:
    """nlrc_decisions에서 bigcase URL이 있는 건 가져오기"""
    fields = "id,title,case_number,department,url,source"
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    # source=bigcase.ai 로 필터 (ilike는 대용량 테이블에서 timeout 발생)
    queries = [
        {"select": fields, "source": "eq.bigcase.ai"},
    ]
    for params in queries:
        for row in fetch_paginated("nlrc_decisions", params):
            decision_id = str(row.get("id") or "")
            if not decision_id or decision_id in seen:
                continue
            seen.add(decision_id)
            rows.append(row)

    # cases 테이블에서도 bigcase URL이 있는 건 가져오기
    cases_params = {"select": "id,title,case_number,url", "url": "like.*bigcase*"}
    for row in fetch_paginated("cases", cases_params):
        decision_id = str(row.get("id") or "")
        if not decision_id or decision_id in seen:
            continue
        seen.add(decision_id)
        row["department"] = row.get("court", "")
        row["source"] = "bigcase.ai"
        rows.append(row)

    rows.sort(key=lambda row: str(row.get("id")))
    return rows


def fetch_existing_ids(parse_version: str) -> set[str]:
    rows = fetch_paginated(
        "decision_source_documents",
        {"select": "internal_decision_id", "parse_version": f"eq.{parse_version}"},
        id_field="internal_decision_id",
    )
    return {str(row.get("internal_decision_id")) for row in rows if row.get("internal_decision_id")}


def fetch_already_collected_ids() -> set[str]:
    """모든 parse_version에서 partial/full인 건 (재수집 불필요)"""
    rows = fetch_paginated(
        "decision_source_documents",
        {
            "select": "internal_decision_id",
            "completeness_flag": "in.(partial,full)",
        },
        id_field="internal_decision_id",
    )
    return {str(row.get("internal_decision_id")) for row in rows if row.get("internal_decision_id")}


def fetch_summary_only_ids() -> set[str]:
    """기존 v3에서 summary_only인 건 (업그레이드 대상)"""
    rows = fetch_paginated(
        "decision_source_documents",
        {
            "select": "internal_decision_id",
            "completeness_flag": "eq.summary_only",
        },
        id_field="internal_decision_id",
    )
    return {str(row.get("internal_decision_id")) for row in rows if row.get("internal_decision_id")}


# ============================================================
# 비회원 HTML 수집 (인증 없음)
# ============================================================

def fetch_html_noauth(url: str, retries: int = 3) -> str:
    """인증 없이 순수 GET 요청"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9",
    }
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=(10, 30))
            if resp.status_code == 429 or "/reach-limit" in (resp.headers.get("location", "")):
                wait = 120 * (attempt + 1)
                print(f"    RATE_LIMIT, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"
            return resp.text
        except (requests.Timeout, requests.ConnectionError) as e:
            if attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"    RETRY {attempt+1}/{retries} ({e.__class__.__name__}), wait {wait}s")
                time.sleep(wait)
            else:
                raise
    return ""


# ============================================================
# __NEXT_DATA__ 파싱 (요지만 추출)
# ============================================================

def extract_summary_from_html(html: str) -> dict[str, Any]:
    """비회원 __NEXT_DATA__에서 요지/판시사항/AI요약만 추출"""
    match = NEXT_DATA_RE.search(html)
    if not match:
        return {"full_text": "", "sections": [], "ai_summary": "", "method": "no_next_data"}

    try:
        next_data = json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        return {"full_text": "", "sections": [], "ai_summary": "", "method": "json_error"}

    page_props = next_data.get("props", {}).get("pageProps", {})
    case_data = page_props.get("caseDetail")
    if not case_data:
        return {"full_text": "", "sections": [], "ai_summary": "", "method": "no_case_detail"}

    fulltext = case_data.get("fulltext") or {}
    sections: list[dict[str, Any]] = []
    text_parts: list[str] = []
    order = 0

    # 판시사항
    holding = clean_text(fulltext.get("holding"))
    if holding:
        sections.append({"type": "holding", "title": "판시사항", "text": holding, "order": order})
        text_parts.append(f"[판시사항]\n{holding}")
        order += 1

    # 재판요지
    summary = clean_text(fulltext.get("summary"))
    if summary:
        sections.append({"type": "holding", "title": "재판요지", "text": summary, "order": order})
        text_parts.append(f"[재판요지]\n{summary}")
        order += 1

    # 주문 (비회원도 보통 보임)
    disposition = clean_text(fulltext.get("disposition"))
    if disposition:
        sections.append({"type": "order", "title": "주문", "text": disposition, "order": order})
        text_parts.append(f"[주문]\n{disposition}")
        order += 1

    # AI 요약
    ai_summary = clean_text(
        case_data.get("ai_full_summary_md")
        or case_data.get("ai_summary")
        or ""
    )

    combined = "\n\n".join(text_parts)

    return {
        "full_text": combined,
        "sections": sections,
        "ai_summary": ai_summary,
        "method": "next_data_noauth",
    }


def build_source_row(
    decision: dict[str, Any],
    result: dict[str, Any],
    parse_version: str,
) -> dict[str, Any]:
    full_text = result["full_text"]
    sections = result["sections"]
    content_hash = hashlib.md5(full_text.encode("utf-8", errors="replace")).hexdigest()

    length = len(full_text)
    if length >= 500:
        flag = "partial"
    else:
        flag = "summary_only"

    return {
        "internal_decision_id": decision["id"],
        "source_provider": "bigcase",
        "source_case_id": decision.get("case_number") or None,
        "source_url": decision.get("url") or None,
        "full_text_raw": {
            "source_kind": "bigcase_html_noauth",
            "extraction_method": result["method"],
            "ai_summary": result.get("ai_summary", ""),
        },
        "full_text_clean": full_text or None,
        "body_sections": sections or None,
        "summary_raw": result.get("ai_summary") or None,
        "parse_version": parse_version,
        "content_hash": content_hash,
        "coverage_ratio": min(length / 10000.0, 1.0),
        "completeness_flag": flag,
        "last_verified_at": datetime.now(timezone.utc).isoformat(),
    }


def upsert_row(row: dict[str, Any]) -> None:
    headers = build_supabase_headers()
    supabase_url = require_env("SUPABASE_URL")
    resp = requests.post(
        f"{supabase_url}/rest/v1/decision_source_documents?on_conflict=internal_decision_id,parse_version",
        headers=headers,
        json=row,
        timeout=60,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"{resp.status_code} {resp.text[:1000]}")


def log_line(log_path: Path, payload: dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


# ============================================================
# Main
# ============================================================

def main() -> None:
    load_env_file()
    args = parse_args()

    all_rows = fetch_target_decisions()

    if args.mode == "upgrade-summary":
        target_ids = fetch_summary_only_ids()
        pending = [r for r in all_rows if r["id"] in target_ids]
        print(f"UPGRADE_MODE: {len(target_ids)} summary_only targets")
    elif args.mode == "missing-only":
        existing = fetch_existing_ids(args.parse_version)
        already_good = fetch_already_collected_ids()
        skip_ids = existing | already_good
        pending = [r for r in all_rows if r["id"] not in skip_ids]
        print(f"ALREADY_GOOD (partial/full from any version): {len(already_good)}")
    else:
        pending = all_rows

    # offset 적용
    if args.offset > 0:
        pending = pending[args.offset:]

    if args.limit:
        pending = pending[:args.limit]

    print(f"TOTAL_ROWS {len(all_rows)}")
    print(f"PENDING {len(pending)}")
    print(f"PARSE_VERSION {args.parse_version}")
    print(f"MODE {args.mode}")
    print(f"DELAY {args.delay}s")
    print(f"NO_AUTH (비회원 모드)")
    if args.dry_run:
        print("DRY_RUN — no DB writes")

    stats = {"partial": 0, "summary_only": 0, "empty": 0, "fail": 0}
    log_path = LOG_DIR / f"summary_collector_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    for idx, decision in enumerate(pending, start=1):
        try:
            url = str(decision.get("url") or "")
            if not url:
                stats["fail"] += 1
                continue

            html = fetch_html_noauth(url)
            if not html:
                stats["fail"] += 1
                continue

            result = extract_summary_from_html(html)
            length = len(result["full_text"])

            if length == 0 and not result["ai_summary"]:
                stats["empty"] += 1
                label = "empty"
            else:
                row = build_source_row(decision, result, args.parse_version)
                if not args.dry_run:
                    upsert_row(row)
                flag = row["completeness_flag"]
                stats[flag] = stats.get(flag, 0) + 1
                label = f"{flag} (len={length}, method={result['method']}, sections={len(result['sections'])})"

            case_num = decision.get("case_number") or decision["id"]
            print(f"  [{idx}] {case_num} → {label}")

            log_line(log_path, {
                "idx": idx,
                "id": decision["id"],
                "case_number": case_num,
                "label": label,
                "length": length,
                "method": result["method"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

            # 진행 상황 출력
            if idx % 50 == 0:
                total_done = idx
                print(f"  --- {total_done}/{len(pending)} (partial={stats['partial']}, summary={stats['summary_only']}, empty={stats['empty']}, fail={stats['fail']})")

        except Exception as exc:
            stats["fail"] += 1
            case_num = decision.get("case_number") or decision["id"]
            print(f"  [{idx}] {case_num} → FAIL: {exc}")
            log_line(log_path, {"idx": idx, "id": decision["id"], "error": str(exc)})

        # 딜레이
        if idx < len(pending):
            time.sleep(args.delay)

    print(f"\n=== DONE ===")
    print(f"partial={stats['partial']}, summary_only={stats['summary_only']}, empty={stats['empty']}, fail={stats['fail']}")
    print(f"Log: {log_path}")


if __name__ == "__main__":
    main()
