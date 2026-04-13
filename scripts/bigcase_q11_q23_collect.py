"""BigCase Q11/Q23 전용 수집 — 루브릭 점수 개선용 우선순위 수집

Q11: 개선기회 부여 후 해고 / 저성과자 해고 (incompetence + improvement opportunity)
Q23: 괴롭힘 불인정 + 갈등 확대 (workplace_bullying denied + conflict)

인증된 세션으로 전문 텍스트까지 수집 → Supabase 직접 저장

Usage:
    source supabase/.env && source .env.bigcase
    python3 scripts/bigcase_q11_q23_collect.py
    python3 scripts/bigcase_q11_q23_collect.py --query-type q11
    python3 scripts/bigcase_q11_q23_collect.py --query-type q23
    python3 scripts/bigcase_q11_q23_collect.py --search-only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

REPO_DIR = Path(__file__).parent.parent
OUTPUT_DIR = REPO_DIR / "evaluation" / "bigcase_bulk" / "q11_q23"
LOG_DIR = OUTPUT_DIR / "logs"

BIGCASE_BASE = "https://bigcase.ai"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
NEXT_DATA_RE = re.compile(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)

# ── Q11 키워드: 개선기회 + 해고 ─────────────────────────────────
Q11_KEYWORDS = [
    "개선기회 부여 해고",
    "개선기회 부여하지 않고 해고",
    "저성과자 해고",
    "저성과자 프로그램 해고",
    "교육훈련 후 해고",
    "업무능력 부족 해고",
    "업무능력 부족 면직",
    "직무수행능력 부족 해고",
    "근무성적 불량 해고",
    "시정기회 부여 해고",
    "경고 후 해고",
    "근무실적 부진 해고",
    "업무태만 해고",
    "통상해고 업무능력",
    "저성과 통상해고",
    "개선 기간 해고",
    "PIP 해고",
    "업무수행 미흡 해고",
    "근무성적 하위 해고",
]

# ── Q23 키워드: 괴롭힘 불인정 + 갈등 ────────────────────────────
Q23_KEYWORDS = [
    "괴롭힘 인정되지 않",
    "괴롭힘 해당하지 않",
    "괴롭힘 존재하지 않",
    "괴롭힘 불인정",
    "괴롭힘 아닌",
    "괴롭힘 미해당",
    "직장내 괴롭힘 부정",
    "괴롭힘 신고 갈등",
    "괴롭힘 신고 후 불이익",
    "괴롭힘 신고 보복",
    "괴롭힘 주장 배척",
    "괴롭힘 주장 기각",
    "업무상 지시 괴롭힘 아닌",
    "정당한 인사권 괴롭힘",
    "갈등 괴롭힘 구별",
    "개인 갈등 괴롭힘",
    "신고 후 직위해제",
    "괴롭힘 허위신고",
]

QUERY_CONFIGS = {
    "q11": {
        "name": "Q11 (개선기회+해고)",
        "keywords": Q11_KEYWORDS,
        "reason_category": "incompetence",
    },
    "q23": {
        "name": "Q23 (괴롭힘 불인정+갈등)",
        "keywords": Q23_KEYWORDS,
        "reason_category": "workplace_bullying",
    },
}


# ── Auth (쿠키 기반, v3 방식) ────────────────────────────────────
def _login_and_get_tokens() -> dict[str, str]:
    """POST /api/v1/auth/signin → accessToken + refreshToken"""
    email = os.environ.get("BIGCASE_EMAIL", "")
    password = os.environ.get("BIGCASE_PASSWORD", "")
    if not email or not password:
        return {}
    resp = requests.post(
        f"{BIGCASE_BASE}/api/v1/auth/signin",
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
    """POST /api/v1/auth/renew → 새 accessToken"""
    refresh_token = session.cookies.get("refreshToken", domain="bigcase.ai")
    if refresh_token:
        resp = requests.post(
            f"{BIGCASE_BASE}/api/v1/auth/renew",
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


class BigCaseSession:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        self.request_count = 0

    def login(self):
        tokens = _login_and_get_tokens()
        if tokens.get("accessToken"):
            print(f"  [auth] 로그인 성공 — accessToken len={len(tokens['accessToken'])}")
            self.session.cookies.set("accessToken", tokens["accessToken"], domain="bigcase.ai", path="/")
            self.session.cookies.set("refreshToken", tokens["refreshToken"], domain="bigcase.ai", path="/")
            self.session.cookies.set("userId", tokens.get("userId", ""), domain="bigcase.ai", path="/")
        else:
            # fallback: 환경변수 토큰
            print("  [auth] 로그인 실패, 환경변수 토큰 사용")
            rt = os.environ.get("BIGCASE_REFRESH_TOKEN", "")
            uid = os.environ.get("BIGCASE_USER_ID", "")
            if rt:
                self.session.cookies.set("refreshToken", rt, domain="bigcase.ai", path="/")
            if uid:
                self.session.cookies.set("userId", uid, domain="bigcase.ai", path="/")
        self.session.cookies.set("hasMembership", os.environ.get("BIGCASE_HAS_MEMBERSHIP", "true"), domain="bigcase.ai", path="/")

    def renew_token(self):
        new_at = _renew_access_token(self.session)
        if new_at:
            print(f"  [auth] token renewed at request #{self.request_count}")
        else:
            print(f"  [auth] token renewal failed, re-login...")
            self.login()

    def get(self, url, **kwargs):
        self.request_count += 1
        if self.request_count % 50 == 0:
            self.renew_token()
        return self.session.get(url, timeout=20, **kwargs)


# ── Build ID ─────────────────────────────────────────────────────
def get_build_id(session: BigCaseSession) -> str:
    resp = session.get(BIGCASE_BASE + "/")
    match = re.search(r'"buildId"\s*:\s*"([^"]+)"', resp.text)
    if match:
        return match.group(1)
    raise RuntimeError("buildId를 찾을 수 없습니다")


# ── Search ───────────────────────────────────────────────────────
def search_cases(session: BigCaseSession, build_id: str, query: str, max_items=500):
    """빅케이스 검색 API"""
    q_enc = urllib.parse.quote(query)
    items = {}
    page = 1

    while len(items) < max_items:
        url = f"{BIGCASE_BASE}/_next/data/{build_id}/search/case.json?q={q_enc}&page={page}"
        try:
            resp = session.get(url)
            if resp.status_code != 200:
                break
            data = resp.json()
            props = data.get("pageProps", {})
            lst = props.get("list", [])
            total = props.get("totalItems", 0)

            if not lst:
                break

            for item in lst:
                court = item.get("court", "")
                case_number = item.get("case_number", "")
                key = f"{court}_{case_number}"
                if key not in items:
                    items[key] = {
                        "court": court,
                        "case_number": case_number,
                        "title": item.get("case_expression", ""),
                        "case_type": item.get("case_type", ""),
                        "keywords": [query],
                    }
                else:
                    if query not in items[key]["keywords"]:
                        items[key]["keywords"].append(query)

            if len(lst) < 10 or len(items) >= total:
                break

            page += 1
            time.sleep(0.3)

        except Exception as e:
            print(f"    검색 에러 (p={page}): {e}")
            break

    return items


# ── Detail fetch (인증 + __NEXT_DATA__) ──────────────────────────
def _flatten_fulltext(fulltext_obj) -> str:
    """fulltext가 구조체(dict)일 경우 텍스트로 합침"""
    if isinstance(fulltext_obj, str):
        return fulltext_obj
    if not isinstance(fulltext_obj, dict):
        return str(fulltext_obj) if fulltext_obj else ""

    parts = []
    # body_court
    if fulltext_obj.get("body_court"):
        parts.append(fulltext_obj["body_court"])
    # body_infos
    for info in fulltext_obj.get("body_infos", []):
        item = info.get("item", "")
        content = info.get("content", "")
        parts.append(f"[{item}] {content}")
    # disposition (주문)
    if fulltext_obj.get("disposition"):
        parts.append(f"[주 문]\n{fulltext_obj['disposition']}")
    # claim (청구취지)
    for c in fulltext_obj.get("claim", []):
        item = c.get("item", "청구취지")
        content = c.get("content", "")
        parts.append(f"[{item}]\n{content}")
    # reasoning (이유)
    if fulltext_obj.get("reasoning"):
        parts.append(f"[이 유]\n{fulltext_obj['reasoning']}")

    text = "\n\n".join(parts)
    # 태그 정리
    text = re.sub(r"<[^>]+>", "", text)
    return text


def fetch_detail_authenticated(session: BigCaseSession, build_id: str, court: str, case_number: str) -> dict | None:
    """인증된 세션으로 판례 상세 + 전문 텍스트 가져오기"""
    court_enc = urllib.parse.quote(court)
    case_enc = urllib.parse.quote(case_number)

    detail = None

    # 1차: __NEXT_DATA__ JSON API
    json_url = f"{BIGCASE_BASE}/_next/data/{build_id}/cases/{court_enc}/{case_enc}.json"
    try:
        resp = session.get(json_url)
        if resp.status_code == 200:
            data = resp.json()
            detail = data.get("pageProps", {}).get("caseDetail")
    except Exception:
        pass

    # 2차: HTML 페이지에서 __NEXT_DATA__ 파싱
    if not detail:
        html_url = f"{BIGCASE_BASE}/cases/{court_enc}/{case_enc}"
        try:
            resp = session.get(html_url)
            if resp.status_code != 200:
                return None
            m = NEXT_DATA_RE.search(resp.text)
            if m:
                nd = json.loads(m.group(1))
                detail = nd.get("props", {}).get("pageProps", {}).get("caseDetail")
        except Exception:
            pass

    if not detail:
        return None

    # fulltext 구조체 → 텍스트로 변환
    raw_ft = detail.get("fulltext", "")
    flat_text = _flatten_fulltext(raw_ft)
    detail["fulltext"] = flat_text
    detail["_method"] = "next_data_structured" if isinstance(raw_ft, dict) else "next_data"

    return detail


# ── Supabase 저장 ───────────────────────────────────────────────
def make_internal_id(case_number: str, court: str) -> str:
    raw = f"{case_number}{court}"
    return f"bc_{hashlib.md5(raw.encode()).hexdigest()[:8]}"


def upsert_to_supabase(detail: dict, reason_category: str, keywords: list[str]) -> str:
    """nlrc_decisions + decision_source_documents에 저장"""
    supa_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "") or os.environ.get("SUPABASE_URL", "")
    supa_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not supa_url or not supa_key:
        return "skip_no_env"

    headers = {
        "apikey": supa_key,
        "Authorization": f"Bearer {supa_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }

    court = detail.get("court", "")
    case_number = detail.get("case_number", "")
    internal_id = make_internal_id(case_number, court)
    fulltext = detail.get("fulltext", "")

    # 1. nlrc_decisions upsert
    decision_row = {
        "id": internal_id,
        "case_number": case_number,
        "department": court,
        "title": detail.get("case_expression", ""),
        "decision_date": detail.get("judgment_date") or None,
        "case_type": detail.get("case_type", ""),
        "decision_result": _map_outcome(detail.get("outcome", "")),
        "reason_category": [reason_category],
        # key_issue 추출: bigcase_to_db.py와 동일한 방식
        # - ai_full_summary_md 전체를 500자 잘라 쓰던 방식은 마크다운 헤딩(#)과
        #   불필요한 본문까지 포함되어 의미 있는 핵심 쟁점을 담지 못함.
        # - 첫 줄만 추출하고 # 헤딩 기호를 제거한 뒤 최대 200자로 제한.
        # - 첫 줄이 10자 미만이면 제목 역할을 못 하므로 빈 문자열로 처리.
        "key_issue": (lambda s: (
            s.split('\n')[0].replace('#', '').strip()[:200]
            if len(s.split('\n')[0].replace('#', '').strip()) > 10
            else ''
        ))(detail.get("ai_full_summary_md", "")),
        "source": "bigcase",
        "url": f"{BIGCASE_BASE}/cases/{urllib.parse.quote(court)}/{urllib.parse.quote(case_number)}",
    }
    # null 제거
    decision_row = {k: v for k, v in decision_row.items() if v is not None}

    resp = requests.post(
        f"{supa_url}/rest/v1/nlrc_decisions",
        headers=headers,
        json=decision_row,
        timeout=15,
    )
    if resp.status_code not in (200, 201):
        # conflict는 이미 존재 — 업데이트 시도
        if resp.status_code == 409:
            # reason_category 병합
            _merge_reason_category(supa_url, headers, internal_id, reason_category)
        else:
            return f"fail_decision_{resp.status_code}"

    # 2. decision_source_documents upsert (전문 텍스트)
    if fulltext and len(fulltext) > 100:
        method = detail.get("_method", "next_data")
        sections = _count_sections(fulltext)
        doc_row = {
            "internal_decision_id": internal_id,
            "source_provider": "bigcase",
            "source_case_id": case_number,
            "source_url": f"{BIGCASE_BASE}/cases/{urllib.parse.quote(court)}/{urllib.parse.quote(case_number)}",
            "full_text_raw": fulltext,
            "full_text_clean": fulltext,
            "parse_version": "q11q23-collect-v1",
            "completeness_flag": "full" if len(fulltext) > 1000 else "partial",
        }
        doc_headers = {**headers}
        doc_headers["Prefer"] = "return=minimal"
        resp2 = requests.post(
            f"{supa_url}/rest/v1/decision_source_documents",
            headers=doc_headers,
            json=doc_row,
            timeout=15,
        )
        if resp2.status_code in (200, 201):
            return f"full (len={len(fulltext)}, sections={sections})"
        elif resp2.status_code == 409:
            return f"exists (len={len(fulltext)})"
        else:
            return f"fail_doc_{resp2.status_code}"

    return f"meta_only (no fulltext)"


def _merge_reason_category(supa_url, headers, internal_id, new_cat):
    """기존 reason_category에 새 카테고리 병합"""
    get_resp = requests.get(
        f"{supa_url}/rest/v1/nlrc_decisions?id=eq.{internal_id}&select=reason_category",
        headers=headers,
        timeout=10,
    )
    if get_resp.status_code == 200:
        rows = get_resp.json()
        if rows:
            existing = rows[0].get("reason_category") or []
            if new_cat not in existing:
                existing.append(new_cat)
                patch_headers = {**headers, "Prefer": "return=minimal"}
                requests.patch(
                    f"{supa_url}/rest/v1/nlrc_decisions?id=eq.{internal_id}",
                    headers=patch_headers,
                    json={"reason_category": existing},
                    timeout=10,
                )


def _map_outcome(outcome: str) -> str:
    if not outcome:
        return ""
    o = outcome.lower()
    if "인용" in o or "취소" in o:
        return "granted"
    if "기각" in o:
        return "dismissed"
    if "일부" in o:
        return "partial"
    if "각하" in o:
        return "rejected"
    return outcome


def _count_sections(text: str) -> int:
    markers = re.findall(r"^\s*(\[.+?\]|판시사항|재판요지|주\s*문|이\s*유|판결이유|청구취지)", text, re.MULTILINE)
    return len(markers)


# ── Existing keys (Supabase) ─────────────────────────────────────
def load_existing_from_supabase() -> set[str]:
    """Supabase에서 이미 수집된 case_number 세트"""
    supa_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "") or os.environ.get("SUPABASE_URL", "")
    supa_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not supa_url or not supa_key:
        return set()

    headers = {"apikey": supa_key, "Authorization": f"Bearer {supa_key}"}
    keys = set()
    offset = 0
    while True:
        resp = requests.get(
            f"{supa_url}/rest/v1/nlrc_decisions?select=case_number,department&limit=1000&offset={offset}",
            headers=headers,
            timeout=30,
        )
        if resp.status_code != 200:
            break
        rows = resp.json()
        if not rows:
            break
        for r in rows:
            keys.add(f"{r.get('department', '')}_{r['case_number']}")
        offset += len(rows)
        if len(rows) < 1000:
            break

    return keys


# ── Main ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="BigCase Q11/Q23 전용 수집")
    parser.add_argument("--query-type", choices=["q11", "q23", "both"], default="both")
    parser.add_argument("--search-only", action="store_true", help="검색만 수행")
    parser.add_argument("--target", type=int, default=300, help="카테고리당 목표 건수")
    parser.add_argument("--delay", type=float, default=1.0, help="요청 간 딜레이(초)")
    parser.add_argument("--skip-existing-check", action="store_true")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # 세션 초기화 + 로그인
    bc = BigCaseSession()
    print("=" * 60)
    print(f"Q11/Q23 전용 수집 시작 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("=" * 60)

    bc.login()

    build_id = get_build_id(bc)
    print(f"Build ID: {build_id}")

    # 기존 수집 키 로드
    existing_keys = set()
    if not args.skip_existing_check:
        print("기존 수집 현황 확인...", end=" ", flush=True)
        existing_keys = load_existing_from_supabase()
        print(f"{len(existing_keys)}건")

    # 수집할 타입 결정
    types = ["q11", "q23"] if args.query_type == "both" else [args.query_type]

    grand_total = {"searched": 0, "new": 0, "fetched": 0, "saved": 0, "errors": 0}

    for qtype in types:
        config = QUERY_CONFIGS[qtype]
        print(f"\n{'='*60}")
        print(f"  {config['name']}")
        print(f"{'='*60}")

        # Phase 1: 검색
        all_items = {}
        search_cache = OUTPUT_DIR / f"{qtype}_search.json"

        # 기존 검색 결과 로드
        if search_cache.exists():
            cached = json.loads(search_cache.read_text(encoding="utf-8"))
            for item in cached.get("items", []):
                key = f"{item['court']}_{item['case_number']}"
                all_items[key] = item
            print(f"  캐시된 검색 결과: {len(all_items)}건")

        print(f"  키워드 {len(config['keywords'])}개로 검색 시작...")
        for kw in config["keywords"]:
            print(f"    🔍 {kw}", end=" ", flush=True)
            found = search_cases(bc, build_id, kw, max_items=300)
            added = 0
            for key, item in found.items():
                if key not in all_items:
                    all_items[key] = item
                    added += 1
                else:
                    for k in item.get("keywords", []):
                        if k not in all_items[key].get("keywords", []):
                            all_items[key].setdefault("keywords", []).append(k)
            print(f"→ +{added} (누적 {len(all_items)})")
            time.sleep(0.5)

        # 검색 결과 저장
        search_cache.write_text(
            json.dumps({
                "query_type": qtype,
                "total": len(all_items),
                "searched_at": datetime.now().isoformat(),
                "items": list(all_items.values()),
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        grand_total["searched"] += len(all_items)
        print(f"  검색 완료: {len(all_items)}건 고유")

        if args.search_only:
            continue

        # Phase 2: 상세 수집 + Supabase 저장
        # 미수집 건만 필터
        pending = []
        for key, item in all_items.items():
            if key not in existing_keys:
                pending.append(item)
                grand_total["new"] += 1

        # 키워드 히트 수 높은 것 우선
        pending.sort(key=lambda x: -len(x.get("keywords", [])))
        pending = pending[:args.target]

        print(f"  미수집 건: {len(pending)}건 (기존 {len(all_items) - len(pending)}건 스킵)")
        print(f"  상세 수집 시작 (목표: {args.target}건)...")

        log_file = LOG_DIR / f"{qtype}_collect.log"
        fetched_count = 0
        error_count = 0

        for i, item in enumerate(pending):
            court = item["court"]
            case_number = item["case_number"]
            key = f"{court}_{case_number}"

            print(f"  [{i+1}/{len(pending)}] {case_number}", end=" ", flush=True)

            try:
                detail = fetch_detail_authenticated(bc, build_id, court, case_number)
                if not detail:
                    print("SKIP (no detail)")
                    error_count += 1
                    continue

                result = upsert_to_supabase(detail, config["reason_category"], item.get("keywords", []))
                existing_keys.add(key)
                fetched_count += 1
                print(f"→ {result}")

                # 로그 기록
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().isoformat()}] {case_number} → {result}\n")

            except Exception as e:
                error_count += 1
                print(f"ERR: {str(e)[:60]}")
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().isoformat()}] {case_number} → ERROR: {e}\n")

            time.sleep(args.delay)

        grand_total["fetched"] += fetched_count
        grand_total["errors"] += error_count
        grand_total["saved"] += fetched_count

        print(f"\n  {config['name']} 완료: +{fetched_count}건 저장, {error_count}건 에러")

    # 최종 요약
    print(f"\n{'='*60}")
    print(f"최종 요약")
    print(f"{'='*60}")
    print(f"  검색된 고유 건: {grand_total['searched']}")
    print(f"  미수집(신규): {grand_total['new']}")
    print(f"  수집 성공: {grand_total['fetched']}")
    print(f"  에러: {grand_total['errors']}")
    print(f"  완료 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
