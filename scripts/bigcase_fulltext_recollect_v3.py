"""
BigCase 로그인 세션 기반 전문 재수집 v3 — __NEXT_DATA__ 파싱 방식

v2 대비 변경점:
- __NEXT_DATA__ JSON에서 caseDetail.fulltext 직접 추출 (핵심 개선)
- body.get_text() 방식은 fallback으로만 사용
- PAYWALL_MARKERS에서 UI 요소 제거 (잘못된 본문 절단 방지)
- member_only 판정 개선 (__NEXT_DATA__ 기반)
- completeness_flag 로직 수정

# 병렬 실행 예시 (PowerShell)
# 0..7 | ForEach-Object -Parallel {
#   $env:BIGCASE_REFRESH_TOKEN = "<refresh-token>"
#   $env:BIGCASE_USER_ID = "<user-id>"
#   python scripts/bigcase_fulltext_recollect_v3.py --shard-index $_ --shard-count 8
# } -ThrottleLimit 8
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
from bs4 import BeautifulSoup


REPO_DIR = Path(__file__).parent.parent
LOG_DIR = REPO_DIR / "evaluation" / "bigcase_bulk" / "logs" / "recollect_v3"
DEFAULT_PARSE_VERSION = "recollect-v3"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SPACE_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n{3,}")
NEXT_DATA_RE = re.compile(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)

# 진짜 페이월 마커만 남김 (UI 요소 제거)
PAYWALL_MARKERS = [
    "회원에게만 공개되는 판례입니다.",
    "가입하고 판례 전문 보기",
    "이미 빅케이스 회원이신가요?로그인",
    "지금 가입하고",
]

RAW_SECTION_MARKER_RE = re.compile(r"^\s*(\[[^\]]+\]|판시사항|재판요지|주 문|이 유|주문|이유|판결이유|청구취지)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recollect BigCase full text v3 (__NEXT_DATA__)")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=8)
    parser.add_argument("--parse-version", default=DEFAULT_PARSE_VERSION)
    parser.add_argument("--mode", choices=["missing-only", "all", "upgrade-summary"], default="missing-only")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--dry-run", action="store_true", help="파싱만 하고 DB 적재 안 함")
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


def build_headers() -> dict[str, str]:
    service_key = require_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
        "User-Agent": USER_AGENT,
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


def fetch_paginated(endpoint: str, params: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    page_size = 1000
    headers = build_headers()
    supabase_url = require_env("SUPABASE_URL")

    while True:
        merged_params = dict(params)
        merged_params["limit"] = str(page_size)
        merged_params["offset"] = str(offset)
        for _retry in range(3):
            response = requests.get(
                f"{supabase_url}/rest/v1/{endpoint}",
                headers=headers,
                params=merged_params,
                timeout=60,
            )
            if response.status_code < 500:
                break
            time.sleep(5 * (_retry + 1))
        response.raise_for_status()
        chunk = response.json()
        if not chunk:
            break
        rows.extend(chunk)
        if len(chunk) < page_size:
            break
        offset += page_size

    return rows


def fetch_bigcase_decisions() -> list[dict[str, Any]]:
    fields = "id,title,case_number,department,url,source"
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    queries = [
        {"select": fields, "source": "eq.bigcase.ai"},
        {"select": fields, "url": "ilike.*bigcase.ai*"},
    ]
    for params in queries:
        for row in fetch_paginated("nlrc_decisions", params):
            decision_id = str(row.get("id") or "")
            if not decision_id or decision_id in seen:
                continue
            seen.add(decision_id)
            rows.append(row)
    rows.sort(key=lambda row: str(row.get("id")))
    return rows


def fetch_existing_source_ids(parse_version: str) -> set[str]:
    rows = fetch_paginated(
        "decision_source_documents",
        {"select": "internal_decision_id", "parse_version": f"eq.{parse_version}"},
    )
    return {str(row.get("internal_decision_id")) for row in rows if row.get("internal_decision_id")}


def fetch_summary_only_ids(parse_version: str) -> set[str]:
    """v2에서 summary_only로 분류된 건만 가져오기 (upgrade 모드용)"""
    rows = fetch_paginated(
        "decision_source_documents",
        {
            "select": "internal_decision_id",
            "parse_version": f"eq.{parse_version}",
            "completeness_flag": "eq.summary_only",
        },
    )
    return {str(row.get("internal_decision_id")) for row in rows if row.get("internal_decision_id")}


def shard_rows(rows: list[dict[str, Any]], shard_index: int, shard_count: int) -> list[dict[str, Any]]:
    return [row for idx, row in enumerate(rows) if idx % shard_count == shard_index]


def _login_and_get_tokens() -> dict[str, str]:
    """POST /api/v1/auth/signin → accessToken + refreshToken 발급."""
    email = os.environ.get("BIGCASE_EMAIL")
    password = os.environ.get("BIGCASE_PASSWORD")
    if not email or not password:
        return {}
    resp = requests.post(
        "https://bigcase.ai/api/v1/auth/signin",
        json={"email": email, "password": password},
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
        timeout=15,
    )
    if resp.status_code == 200:
        data = resp.json()
        return {
            "accessToken": data.get("accessToken", ""),
            "refreshToken": data.get("refreshToken", ""),
            "userId": data.get("user", {}).get("_id", ""),
        }
    print(f"  [auth] login failed: {resp.status_code} {resp.text[:200]}")
    return {}


def _renew_access_token(session: requests.Session) -> str | None:
    """POST /api/v1/auth/renew → 새 accessToken. 실패 시 재로그인."""
    refresh_token = session.cookies.get("refreshToken", domain="bigcase.ai")
    if refresh_token:
        resp = requests.post(
            "https://bigcase.ai/api/v1/auth/renew",
            json={"refreshToken": refresh_token},
            headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            new_at = data.get("accessToken", "")
            new_rt = data.get("refreshToken", "")
            if new_at:
                session.cookies.set("accessToken", new_at, domain="bigcase.ai", path="/")
            if new_rt:
                session.cookies.set("refreshToken", new_rt, domain="bigcase.ai", path="/")
            return new_at
    # renew 실패 → 재로그인
    tokens = _login_and_get_tokens()
    if tokens.get("accessToken"):
        session.cookies.set("accessToken", tokens["accessToken"], domain="bigcase.ai", path="/")
        session.cookies.set("refreshToken", tokens["refreshToken"], domain="bigcase.ai", path="/")
        return tokens["accessToken"]
    return None


# 전역 카운터: N건마다 토큰 갱신
_ACCESS_TOKEN_RENEW_INTERVAL = 50
_request_counter = 0


def build_cookie_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    # 1) 먼저 로그인으로 fresh 토큰 발급
    tokens = _login_and_get_tokens()
    if tokens.get("accessToken"):
        print(f"  [auth] login success — accessToken len={len(tokens['accessToken'])}")
        session.cookies.set("accessToken", tokens["accessToken"], domain="bigcase.ai", path="/")
        session.cookies.set("refreshToken", tokens["refreshToken"], domain="bigcase.ai", path="/")
        session.cookies.set("userId", tokens.get("userId", ""), domain="bigcase.ai", path="/")
    else:
        # fallback: 환경변수 토큰 사용
        print("  [auth] login failed, falling back to env tokens")
        refresh_token = require_env("BIGCASE_REFRESH_TOKEN")
        user_id = require_env("BIGCASE_USER_ID")
        session.cookies.set("refreshToken", refresh_token, domain="bigcase.ai", path="/")
        session.cookies.set("userId", user_id, domain="bigcase.ai", path="/")
        access_token = os.environ.get("BIGCASE_ACCESS_TOKEN")
        if access_token:
            session.cookies.set("accessToken", access_token, domain="bigcase.ai", path="/")
    session.cookies.set("hasMembership", os.environ.get("BIGCASE_HAS_MEMBERSHIP", "true"), domain="bigcase.ai", path="/")
    session.cookies.set("keepLogin", "true", domain="bigcase.ai", path="/")
    return session


def maybe_renew_token(session: requests.Session) -> None:
    """N건마다 토큰 갱신 (만료 방지)."""
    global _request_counter
    _request_counter += 1
    if _request_counter % _ACCESS_TOKEN_RENEW_INTERVAL == 0:
        new_at = _renew_access_token(session)
        if new_at:
            print(f"  [auth] token renewed at request #{_request_counter}")
        else:
            print(f"  [auth] token renewal failed at request #{_request_counter}")


# ============================================================
# __NEXT_DATA__ 파싱 (v3 핵심)
# ============================================================

def extract_next_data(html: str) -> dict[str, Any] | None:
    """HTML에서 __NEXT_DATA__ JSON 추출"""
    match = NEXT_DATA_RE.search(html)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        return None


def extract_from_next_data(next_data: dict[str, Any]) -> dict[str, Any] | None:
    """
    __NEXT_DATA__에서 전문 구조화 추출.

    Returns:
        {
            "full_text": str,       # 결합된 전문 텍스트
            "sections": list,       # 구조화된 섹션들
            "ai_summary": str,      # AI 요약
            "member_only": bool,    # 회원전용 여부
            "method": "next_data",  # 추출 방법 표시
        }
        또는 None (caseDetail이 없을 때)
    """
    page_props = next_data.get("props", {}).get("pageProps", {})
    case_data = page_props.get("caseDetail")

    if not case_data:
        return None

    fulltext = case_data.get("fulltext") or {}
    sections: list[dict[str, Any]] = []
    full_text_parts: list[str] = []
    order = 0

    # 판결정보 (법원명, 사건번호 등)
    if fulltext.get("body_court"):
        court_text = clean_text(fulltext["body_court"])
        if court_text:
            sections.append({"type": "body", "title": "판결정보", "text": court_text, "order": order})
            full_text_parts.append(court_text)
            order += 1

    # 부가 정보 (당사자, 대리인 등)
    if fulltext.get("body_infos"):
        info_lines = []
        for info in fulltext["body_infos"]:
            item = clean_text(info.get("item", ""))
            content = clean_text(info.get("content", ""))
            if item and content:
                info_lines.append(f"{item}: {content}")
        if info_lines:
            info_text = "\n".join(info_lines)
            sections.append({"type": "body", "title": "당사자정보", "text": info_text, "order": order})
            full_text_parts.append(info_text)
            order += 1

    # 판시사항
    if fulltext.get("holding"):
        holding_text = clean_text(fulltext["holding"])
        if holding_text:
            sections.append({"type": "holding", "title": "판시사항", "text": holding_text, "order": order})
            full_text_parts.append(f"\n[판시사항]\n{holding_text}")
            order += 1

    # 재판요지
    if fulltext.get("summary"):
        summary_text = clean_text(fulltext["summary"])
        if summary_text:
            sections.append({"type": "holding", "title": "재판요지", "text": summary_text, "order": order})
            full_text_parts.append(f"\n[재판요지]\n{summary_text}")
            order += 1

    # 주문
    if fulltext.get("disposition"):
        disposition_text = clean_text(fulltext["disposition"])
        if disposition_text:
            sections.append({"type": "order", "title": "주문", "text": disposition_text, "order": order})
            full_text_parts.append(f"\n[주문]\n{disposition_text}")
            order += 1

    # 이유 (가장 중요한 부분)
    if fulltext.get("reasoning"):
        reasoning_text = clean_text(fulltext["reasoning"])
        if reasoning_text:
            sections.append({"type": "reasoning", "title": "이유", "text": reasoning_text, "order": order})
            full_text_parts.append(f"\n[이유]\n{reasoning_text}")
            order += 1

    # 청구취지
    if fulltext.get("claim"):
        claim_text = clean_text(fulltext["claim"])
        if claim_text:
            sections.append({"type": "claim", "title": "청구취지", "text": claim_text, "order": order})
            full_text_parts.append(f"\n[청구취지]\n{claim_text}")
            order += 1

    # AI 요약
    ai_summary = clean_text(
        case_data.get("ai_full_summary_md")
        or case_data.get("ai_summary")
        or ""
    )

    # 회원전용 판단: fulltext 필드가 비어있고 AI 요약만 있는 경우
    has_fulltext_content = bool(fulltext.get("reasoning") or fulltext.get("disposition"))
    member_only = not has_fulltext_content and bool(ai_summary)

    combined_text = "\n\n".join(full_text_parts)

    return {
        "full_text": combined_text,
        "sections": sections,
        "ai_summary": ai_summary,
        "member_only": member_only,
        "method": "next_data",
    }


# ============================================================
# Fallback: body text 파싱 (v2 방식, 개선)
# ============================================================

def extract_body_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "header", "footer"]):
        tag.decompose()
    body = soup.body or soup
    return clean_text(body.get_text("\n"))


def build_stacked_court_regex(court: str) -> re.Pattern[str] | None:
    court = clean_text(court)
    if not court:
        return None
    chars = [re.escape(ch) for ch in court if not ch.isspace()]
    if not chars:
        return None
    pattern = r"\s*".join(chars) + r"\s*(?:제\s*\d+\s*\S+\s*)?판\s*결"
    return re.compile(pattern)


def extract_original_text_fallback(body_text: str, court_hint: str) -> str:
    """v2 방식 fallback (개선: UI 마커 제거)"""
    text = clean_text(body_text)
    if not text:
        return ""

    regex = build_stacked_court_regex(court_hint)
    if regex:
        matches = list(regex.finditer(text))
        if matches:
            text = text[matches[-1].start():].strip()

    markers = ["주 문", "이 유", "판결이유", "판시사항", "재판요지"]
    positions = [text.find(marker) for marker in markers if text.find(marker) != -1]
    if positions:
        start = max(min(positions) - 500, 0)
        text = text[start:].strip()

    cutoff = len(text)
    for marker in PAYWALL_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            cutoff = min(cutoff, idx)
    text = text[:cutoff].strip()
    return clean_text(text)


def extract_sections_from_raw_text(raw_text: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    cleaned = clean_text(raw_text)
    if not cleaned:
        return sections

    lines = cleaned.splitlines()
    metadata_lines: list[str] = []
    current_title = "원문"
    current_lines: list[str] = []
    order = 0
    seen_body_marker = False

    def flush(title: str) -> None:
        nonlocal current_lines, order
        text = clean_text("\n".join(current_lines))
        if text:
            sections.append({
                "type": infer_type(title),
                "title": title,
                "text": text,
                "order": order,
            })
            order += 1
        current_lines = []

    for line in lines:
        marker_match = RAW_SECTION_MARKER_RE.match(line)
        if not seen_body_marker and ":" in line and not marker_match:
            metadata_lines.append(line)
            continue
        if marker_match:
            if metadata_lines and not sections:
                sections.append({
                    "type": "body",
                    "title": "판결정보",
                    "text": clean_text("\n".join(metadata_lines)),
                    "order": order,
                })
                order += 1
                metadata_lines = []
            flush(current_title)
            current_title = line.strip().strip("[]")
            seen_body_marker = True
            continue
        current_lines.append(line)

    if metadata_lines and not sections:
        sections.append({
            "type": "body",
            "title": "판결정보",
            "text": clean_text("\n".join(metadata_lines)),
            "order": order,
        })
        order += 1

    flush(current_title)
    return sections


def infer_type(title: str) -> str:
    normalized = clean_text(title)
    if normalized in {"주문", "주 문"}:
        return "order"
    if normalized in {"이유", "이 유", "판결이유"}:
        return "reasoning"
    if normalized in {"판시사항", "재판요지"}:
        return "holding"
    if normalized in {"청구취지"}:
        return "claim"
    return "body"


# ============================================================
# 통합 추출 + 분류
# ============================================================

def extract_all(html: str, court_hint: str) -> dict[str, Any]:
    """
    __NEXT_DATA__와 fallback body text 둘 다 추출 후, 더 긴 쪽을 채택.
    Returns: {full_text, sections, ai_summary, member_only, method}
    """
    next_data_result = None
    fallback_result = None
    ai_summary = ""

    # 1차: __NEXT_DATA__ 파싱
    next_data = extract_next_data(html)
    if next_data:
        next_data_result = extract_from_next_data(next_data)
        # AI 요약은 항상 __NEXT_DATA__에서 추출
        page_props = next_data.get("props", {}).get("pageProps", {})
        case_data = page_props.get("caseDetail") or {}
        ai_summary = clean_text(
            case_data.get("ai_full_summary_md")
            or case_data.get("ai_summary")
            or ""
        )

    # 2차: fallback body text (항상 시도)
    body_text = extract_body_text(html)
    member_only = any(m in body_text for m in PAYWALL_MARKERS[:2])
    extracted = extract_original_text_fallback(body_text, court_hint)
    if extracted and len(extracted) > 100:
        sections = extract_sections_from_raw_text(extracted)
        fallback_result = {
            "full_text": extracted,
            "sections": sections,
            "ai_summary": ai_summary,
            "member_only": member_only,
            "method": "fallback_body",
        }

    # 둘 다 있으면 더 긴 쪽 채택
    nd_len = len(next_data_result["full_text"]) if next_data_result else 0
    fb_len = len(fallback_result["full_text"]) if fallback_result else 0

    if nd_len > 0 and nd_len >= fb_len:
        # __NEXT_DATA__가 더 길거나 같으면 구조화된 데이터 우선
        return next_data_result
    elif fb_len > 0:
        # fallback이 더 길면 fallback 채택
        return fallback_result
    elif next_data_result:
        return next_data_result

    # 둘 다 없으면 빈 fallback 반환
    return {
        "full_text": extracted or "",
        "sections": [],
        "ai_summary": ai_summary,
        "member_only": member_only,
        "method": "fallback_body",
    }


def compute_coverage_ratio(full_text_clean: str) -> float:
    return min(len(full_text_clean) / 10000.0, 1.0)


def compute_completeness_flag(full_text_clean: str, member_only: bool, has_reasoning: bool) -> str:
    """v3: reasoning 유무를 추가 판단 기준으로"""
    length = len(full_text_clean)

    if member_only and length < 500:
        return "summary_only"

    # reasoning이 있으면 full 가능성 높음
    if has_reasoning and length >= 1000:
        return "full"
    if length >= 3000:
        return "full"
    if length >= 500:
        return "partial"
    return "summary_only"


def fetch_html(session: requests.Session, url: str, retries: int = 3) -> str:
    maybe_renew_token(session)
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=(10, 30))  # (connect, read)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
            html = response.text
            # 페이월 감지 → 토큰 갱신 후 재시도
            if "회원에게만 공개되는 판례입니다" in html and attempt < retries - 1:
                print(f"    PAYWALL detected, renewing token...")
                new_at = _renew_access_token(session)
                if new_at:
                    response = session.get(url, timeout=(10, 30))
                    response.raise_for_status()
                    response.encoding = response.apparent_encoding or "utf-8"
                    html = response.text
            return html
        except (requests.Timeout, requests.ConnectionError) as e:
            if attempt < retries - 1:
                wait = (attempt + 1) * 15  # 15s, 30s, 45s
                print(f"    RETRY {attempt+1}/{retries} for {url[:60]}... ({e.__class__.__name__}), wait {wait}s")
                time.sleep(wait)
            else:
                raise


def build_source_row(
    decision: dict[str, Any],
    html: str,
    result: dict[str, Any],
    parse_version: str,
) -> dict[str, Any]:
    full_text = result["full_text"]
    sections = result["sections"]
    member_only = result["member_only"]

    # reasoning 섹션 존재 여부
    has_reasoning = any(s.get("type") == "reasoning" for s in sections)

    raw_payload = {
        "source_kind": "bigcase_html",
        "member_only": member_only,
        "extraction_method": result["method"],
        "ai_summary": result.get("ai_summary", ""),
    }
    content_hash = hashlib.md5(full_text.encode("utf-8", errors="replace")).hexdigest()

    return {
        "internal_decision_id": decision["id"],
        "source_provider": "bigcase",
        "source_case_id": decision.get("case_number") or None,
        "source_url": decision.get("url") or None,
        "full_text_raw": raw_payload,
        "full_text_clean": full_text or None,
        "body_sections": sections or None,
        "summary_raw": result.get("ai_summary") or None,
        "parse_version": parse_version,
        "content_hash": content_hash,
        "coverage_ratio": compute_coverage_ratio(full_text),
        "completeness_flag": compute_completeness_flag(full_text, member_only, has_reasoning),
        "last_verified_at": datetime.now(timezone.utc).isoformat(),
    }


def upsert_source_row(row: dict[str, Any]) -> None:
    headers = build_headers()
    supabase_url = require_env("SUPABASE_URL")
    response = requests.post(
        f"{supabase_url}/rest/v1/decision_source_documents?on_conflict=internal_decision_id,parse_version",
        headers=headers,
        json=row,
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{response.status_code} {response.text[:1000]}")


def log_line(log_path: Path, payload: dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main() -> None:
    load_env_file()
    args = parse_args()
    if args.shard_index < 0 or args.shard_index >= args.shard_count:
        raise SystemExit("--shard-index must be in range 0..shard-count-1")

    all_rows = fetch_bigcase_decisions()

    if args.mode == "upgrade-summary":
        # v2에서 summary_only였던 건만 v3로 재수집
        target_ids = fetch_summary_only_ids("recollect-v2")
        pending_rows = [row for row in all_rows if row["id"] in target_ids]
        print(f"UPGRADE_MODE: {len(target_ids)} summary_only targets from v2")
    elif args.mode == "missing-only":
        existing_ids = fetch_existing_source_ids(args.parse_version)
        pending_rows = [row for row in all_rows if row["id"] not in existing_ids]
    else:
        pending_rows = all_rows

    shard_rows_list = shard_rows(pending_rows, args.shard_index, args.shard_count)
    if args.limit:
        shard_rows_list = shard_rows_list[:args.limit]

    print(f"TOTAL_BIGCASE_ROWS {len(all_rows)}")
    print(f"PENDING {len(pending_rows)}")
    print(f"SHARD {args.shard_index}/{args.shard_count}")
    print(f"SHARD_TARGET {len(shard_rows_list)}")
    print(f"PARSE_VERSION {args.parse_version}")
    print(f"MODE {args.mode}")
    if args.dry_run:
        print("DRY_RUN enabled — no DB writes")

    session = build_cookie_session()

    stats = {"full": 0, "partial": 0, "summary_only": 0, "next_data": 0, "fallback": 0, "failures": 0}
    completed = 0
    fail_log = LOG_DIR / f"recollect_v3_shard_{args.shard_index}.failures.jsonl"

    for idx, decision in enumerate(shard_rows_list, start=1):
        try:
            url = str(decision.get("url") or "")
            if not url:
                stats["failures"] += 1
                continue

            html = fetch_html(session, url)
            court_hint = str(decision.get("department") or "")
            result = extract_all(html, court_hint)

            # 통계
            stats[result["method"] if result["method"] == "next_data" else "fallback"] += 1

            row = build_source_row(decision, html, result, args.parse_version)
            flag = row["completeness_flag"]
            stats[flag] = stats.get(flag, 0) + 1

            if not args.dry_run:
                upsert_source_row(row)

            completed += 1

            if idx <= 20 or idx % 50 == 0:
                print(f"  [{idx}] {decision.get('case_number','')} → {flag} "
                      f"(len={len(result['full_text'])}, method={result['method']}, "
                      f"sections={len(result['sections'])})")

        except Exception as exc:
            stats["failures"] += 1
            log_line(fail_log, {
                "internal_decision_id": decision.get("id"),
                "url": decision.get("url"),
                "case_number": decision.get("case_number"),
                "error": str(exc)[:1000],
            })
            if idx <= 50 or idx % 50 == 0:
                print(f"  FAIL [{idx}] {decision.get('case_number', decision.get('id'))} {exc.__class__.__name__}: {str(exc)[:200]}")

        if idx % 100 == 0 or idx == len(shard_rows_list):
            print(f"shard {args.shard_index}: {idx}/{len(shard_rows_list)} "
                  f"(full={stats['full']}, partial={stats['partial']}, "
                  f"summary={stats['summary_only']}, fail={stats['failures']})")

        time.sleep(args.delay)

    print("\n" + "=" * 60)
    print("DONE")
    print(f"COMPLETED {completed}")
    print(f"FAILED {stats['failures']}")
    print(f"STATS full={stats['full']} partial={stats['partial']} summary_only={stats['summary_only']}")
    print(f"METHOD next_data={stats['next_data']} fallback={stats['fallback']}")
    print(f"FAIL_LOG {fail_log}")


if __name__ == "__main__":
    main()
