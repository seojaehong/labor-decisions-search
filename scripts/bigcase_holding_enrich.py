"""
BigCase holding_summary 보강 수집기 (회원 인증 버전)
— nlrc_decisions에서 holding_summary < 100자인 **전체** 건 대상
— BigCase 회원 로그인(email/password) → 쿠키 세션으로 수집
— 50건마다 토큰 자동 갱신, 페이월 감지 시 즉시 갱신
— BigCase URL 없는 건은 case_number로 BigCase 검색 시도
— rate limit 회피를 위해 60초 딜레이 (기본)
— nohup/pm2로 백그라운드 실행 권장
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

REPO_DIR = Path(__file__).parent.parent
LOG_DIR = REPO_DIR / "evaluation" / "bigcase_bulk" / "logs" / "holding_enrich"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SPACE_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n{3,}")
NEXT_DATA_RE = re.compile(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8699916672")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich short holding_summary from BigCase (auth)")
    parser.add_argument("--delay", type=float, default=60.0, help="초 단위 딜레이 (기본 60초)")
    parser.add_argument("--limit", type=int, help="최대 수집 건수")
    parser.add_argument("--offset", type=int, default=0, help="시작 오프셋")
    parser.add_argument("--dry-run", action="store_true", help="DB 업데이트 없이 테스트")
    parser.add_argument("--max-summary-len", type=int, default=100, help="이 길이 미만인 건만 대상")
    return parser.parse_args()


def load_env_file() -> None:
    """supabase/.env + .env.bigcase 로드"""
    candidates = [
        REPO_DIR / "supabase" / ".env",
        REPO_DIR / ".env.local",
        REPO_DIR / ".env",
        REPO_DIR / ".env.bigcase",
    ]
    for candidate in candidates:
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
# BigCase 회원 인증
# ============================================================

_ACCESS_TOKEN_RENEW_INTERVAL = 50
_request_counter = 0


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


def build_cookie_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    tokens = _login_and_get_tokens()
    if tokens.get("accessToken"):
        print(f"  [auth] login success — accessToken len={len(tokens['accessToken'])}")
        session.cookies.set("accessToken", tokens["accessToken"], domain="bigcase.ai", path="/")
        session.cookies.set("refreshToken", tokens["refreshToken"], domain="bigcase.ai", path="/")
        session.cookies.set("userId", tokens.get("userId", ""), domain="bigcase.ai", path="/")
    else:
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
# Supabase
# ============================================================

def build_headers() -> dict[str, str]:
    service_key = require_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }


def fetch_short_summary_decisions(max_len: int) -> list[dict[str, Any]]:
    """holding_summary가 짧은 전체 건 조회 (URL 종류 무관)"""
    service_key = require_env("SUPABASE_SERVICE_KEY")
    supabase_url = require_env("SUPABASE_URL")
    rows: list[dict[str, Any]] = []
    page_size = 1000
    start = 0

    while True:
        headers = {
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Range": f"{start}-{start + page_size - 1}",
            "Range-Unit": "items",
        }
        resp = requests.get(
            f"{supabase_url}/rest/v1/nlrc_decisions",
            headers=headers,
            params={
                "select": "id,case_number,url,holding_summary,holding_points",
                "holding_summary": "not.is.null",
                "order": "id",
            },
            timeout=60,
        )
        if resp.status_code == 416:
            break
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break
        for row in chunk:
            hs = row.get("holding_summary") or ""
            if 0 < len(hs) < max_len:
                rows.append(row)
        if len(chunk) < page_size:
            break
        start += page_size

    return rows


def update_decision(decision_id: str, updates: dict[str, Any]) -> bool:
    """nlrc_decisions 레코드 업데이트"""
    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    headers["Prefer"] = "return=minimal"
    resp = requests.patch(
        f"{supabase_url}/rest/v1/nlrc_decisions?id=eq.{decision_id}",
        headers=headers,
        json=updates,
        timeout=60,
    )
    return resp.status_code < 400


# ============================================================
# BigCase HTML 수집 + 파싱 (회원 인증)
# ============================================================

def resolve_bigcase_url(decision: dict[str, Any]) -> str | None:
    """기존 URL이 BigCase면 그대로, 아니면 case_number로 BigCase URL 생성 시도"""
    url = str(decision.get("url") or "")
    if "bigcase.ai" in url:
        return url

    # law.go.kr 등 → case_number로 BigCase 검색 URL 생성
    case_number = decision.get("case_number") or ""
    if not case_number:
        return None

    # BigCase URL 패턴: https://bigcase.ai/cases/{법원}/{사건번호}
    # 법원명은 모르므로 BigCase 검색 API 사용
    return f"https://bigcase.ai/search?query={quote(case_number)}"


def fetch_html_auth(session: requests.Session, url: str, retries: int = 3) -> str:
    """회원 인증 세션으로 HTML 수집"""
    maybe_renew_token(session)
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=(10, 30))
            if resp.status_code == 429 or "/reach-limit" in (resp.headers.get("location", "")):
                wait = 120 * (attempt + 1)
                print(f"    RATE_LIMIT, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"
            html = resp.text
            # 페이월 감지 → 토큰 갱신 후 재시도
            if "회원에게만 공개되는 판례입니다" in html and attempt < retries - 1:
                print(f"    PAYWALL detected, renewing token...")
                new_at = _renew_access_token(session)
                if new_at:
                    resp = session.get(url, timeout=(10, 30))
                    resp.raise_for_status()
                    resp.encoding = resp.apparent_encoding or "utf-8"
                    html = resp.text
            return html
        except (requests.Timeout, requests.ConnectionError) as e:
            if attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"    RETRY {attempt+1}/{retries} ({e.__class__.__name__}), wait {wait}s")
                time.sleep(wait)
            else:
                raise
    return ""


def try_search_and_fetch(session: requests.Session, case_number: str) -> str:
    """BigCase 검색 페이지에서 첫 결과 URL을 찾아 해당 페이지 HTML 반환"""
    search_url = f"https://bigcase.ai/search?query={quote(case_number)}"
    try:
        html = fetch_html_auth(session, search_url)
    except requests.HTTPError:
        return ""
    if not html:
        return ""

    # 검색 결과 페이지의 __NEXT_DATA__에서 첫 결과 URL 추출
    match = NEXT_DATA_RE.search(html)
    if not match:
        return ""
    try:
        next_data = json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        return ""

    page_props = next_data.get("props", {}).get("pageProps", {})
    results = page_props.get("searchResults") or page_props.get("cases") or []
    if not results:
        # dehydratedState에서 찾기
        dehydrated = page_props.get("dehydratedState", {})
        queries = dehydrated.get("queries", [])
        for q in queries:
            data = q.get("state", {}).get("data", {})
            hits = data.get("hits") or data.get("results") or data.get("cases") or []
            if hits:
                results = hits
                break

    if not results:
        return ""

    # 첫 결과에서 case URL 추출
    first = results[0] if isinstance(results, list) else results
    case_url = None
    if isinstance(first, dict):
        # URL 직접 있는 경우
        case_url = first.get("url") or first.get("case_url")
        if not case_url:
            # slug로 URL 구성
            slug = first.get("slug") or first.get("_id") or first.get("id")
            court = first.get("court") or first.get("courtName")
            cn = first.get("caseNumber") or first.get("case_number")
            if court and cn:
                case_url = f"https://bigcase.ai/cases/{quote(court)}/{quote(cn)}"
            elif slug:
                case_url = f"https://bigcase.ai/cases/{slug}"

    if not case_url:
        return ""

    if not case_url.startswith("http"):
        case_url = f"https://bigcase.ai{case_url}"

    # 실제 판례 페이지 수집
    time.sleep(5)  # 검색 → 상세 사이 짧은 딜레이
    return fetch_html_auth(session, case_url)


def extract_from_html(html: str) -> dict[str, str]:
    """__NEXT_DATA__에서 판시사항/재판요지/AI요약 추출"""
    match = NEXT_DATA_RE.search(html)
    if not match:
        return {"holding": "", "summary": "", "ai_summary": "", "method": "no_next_data"}

    try:
        next_data = json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        return {"holding": "", "summary": "", "ai_summary": "", "method": "json_error"}

    page_props = next_data.get("props", {}).get("pageProps", {})
    case_data = page_props.get("caseDetail")
    if not case_data:
        return {"holding": "", "summary": "", "ai_summary": "", "method": "no_case_detail"}

    fulltext = case_data.get("fulltext") or {}

    holding = clean_text(fulltext.get("holding"))
    summary = clean_text(fulltext.get("summary"))
    ai_summary = clean_text(
        case_data.get("ai_full_summary_md")
        or case_data.get("ai_summary")
        or ""
    )

    return {
        "holding": holding,
        "summary": summary,
        "ai_summary": ai_summary,
        "method": "next_data",
    }


def build_enriched_summary(existing: str, extracted: dict[str, str]) -> str | None:
    """추출된 데이터로 보강된 holding_summary 생성"""
    # 재판요지 우선, 없으면 판시사항, 없으면 AI 요약
    content = extracted["summary"] or extracted["holding"] or extracted["ai_summary"]
    if not content:
        return None

    # 기존 summary와 합쳐서 300~500자 목표
    target_add = max(300 - len(existing), 100)
    new_summary = f"{existing} {content[:target_add]}"
    return new_summary


def send_telegram(msg: str) -> None:
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
            timeout=10,
        )
    except Exception:
        pass


# ============================================================
# Main
# ============================================================

def main() -> None:
    load_env_file()
    args = parse_args()

    print(f"=== BigCase holding_summary 보강 수집기 (회원 인증) ===")
    print(f"DELAY: {args.delay}s | MAX_SUMMARY_LEN: {args.max_summary_len}")

    # 회원 인증 세션 구축
    print("Building authenticated session...")
    session = build_cookie_session()

    print(f"Fetching target decisions...")
    all_targets = fetch_short_summary_decisions(args.max_summary_len)

    # BigCase URL 있는 건 우선, 나머지는 뒤로
    bc_targets = [r for r in all_targets if "bigcase" in (r.get("url") or "")]
    other_targets = [r for r in all_targets if "bigcase" not in (r.get("url") or "")]
    all_targets = bc_targets + other_targets

    print(f"TOTAL TARGETS: {len(all_targets)} (bigcase_url={len(bc_targets)}, search={len(other_targets)})")

    # offset/limit 적용
    pending = all_targets[args.offset:]
    if args.limit:
        pending = pending[:args.limit]

    print(f"PENDING: {len(pending)} (offset={args.offset}, limit={args.limit})")
    if args.dry_run:
        print("DRY_RUN — no DB writes")

    stats = {"enriched": 0, "no_data": 0, "search_miss": 0, "fail": 0}
    log_path = LOG_DIR / f"enrich_auth_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    send_telegram(f"🔄 holding 보강 시작 (auth): {len(pending)}건 (delay={args.delay}s)")

    for idx, decision in enumerate(pending, start=1):
        try:
            url = str(decision.get("url") or "")
            case_number = decision.get("case_number") or ""
            is_bigcase_url = "bigcase" in url

            # BigCase URL이면 직접 수집, 아니면 검색으로 시도
            if is_bigcase_url:
                html = fetch_html_auth(session, url)
            elif case_number:
                html = try_search_and_fetch(session, case_number)
            else:
                stats["fail"] += 1
                continue

            if not html:
                stats["search_miss" if not is_bigcase_url else "fail"] += 1
                label = "search_miss" if not is_bigcase_url else "no_html"
            else:
                extracted = extract_from_html(html)
                existing_summary = decision.get("holding_summary") or ""
                new_summary = build_enriched_summary(existing_summary, extracted)

                if not new_summary or len(new_summary) <= len(existing_summary) + 10:
                    stats["no_data"] += 1
                    label = f"no_data (method={extracted['method']})"
                else:
                    updates: dict[str, Any] = {"holding_summary": new_summary}

                    # holding_points도 짧으면 보강
                    existing_points = decision.get("holding_points") or ""
                    if len(existing_points) < 200:
                        full_content = extracted["holding"] or extracted["summary"] or ""
                        if full_content and len(full_content) > len(existing_points):
                            updates["holding_points"] = full_content

                    if not args.dry_run:
                        update_decision(decision["id"], updates)
                    stats["enriched"] += 1
                    label = f"enriched ({len(existing_summary)} → {len(new_summary)} chars)"

            case_id = case_number or decision["id"]
            src = "BC" if is_bigcase_url else "SR"
            print(f"  [{idx}/{len(pending)}] [{src}] {case_id} → {label}")

            # 로그
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "idx": idx, "id": decision["id"], "case_number": case_id,
                    "source": "bigcase_url" if is_bigcase_url else "search",
                    "label": label, "timestamp": datetime.now(timezone.utc).isoformat(),
                }, ensure_ascii=False) + "\n")

            # 진행 상황
            if idx % 50 == 0:
                msg = f"  --- {idx}/{len(pending)} (enriched={stats['enriched']}, no_data={stats['no_data']}, search_miss={stats['search_miss']}, fail={stats['fail']})"
                print(msg)

            # 100건마다 텔레그램 알림
            if idx % 100 == 0:
                send_telegram(f"📊 보강 진행: {idx}/{len(pending)} (enriched={stats['enriched']}, search_miss={stats['search_miss']}, fail={stats['fail']})")

        except Exception as exc:
            stats["fail"] += 1
            case_id = decision.get("case_number") or decision["id"]
            print(f"  [{idx}] {case_id} → FAIL: {exc}")

        # 딜레이
        if idx < len(pending):
            time.sleep(args.delay)

    summary = f"enriched={stats['enriched']}, no_data={stats['no_data']}, search_miss={stats['search_miss']}, fail={stats['fail']}"
    print(f"\n=== DONE === {summary}")
    print(f"Log: {log_path}")
    send_telegram(f"✅ holding 보강 완료 (auth)!\n{summary}\nLog: {log_path}")


if __name__ == "__main__":
    main()
