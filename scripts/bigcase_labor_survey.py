"""
BigCase 노동 판례 전수 규모 파악 스크립트

키워드별로 BigCase 검색 → totalCount 확인 → 전체 목록 수집 → 중복 제거
결과: 수집 가능한 노동 판례 총 건수 + case_id 목록 (JSONL)

Usage:
    # 규모 파악만 (빠름)
    python scripts/bigcase_labor_survey.py --survey-only

    # 전체 목록 수집 (페이지네이션)
    python scripts/bigcase_labor_survey.py

    # 기존 DB와 비교해서 신규 건만 출력
    python scripts/bigcase_labor_survey.py --diff-db
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
OUTPUT_DIR = REPO_DIR / "evaluation" / "bigcase_bulk" / "survey"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
NEXT_DATA_RE = re.compile(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)

# 노동 관련 검색 키워드 (포괄적)
LABOR_KEYWORDS = [
    # 해고
    "부당해고", "징계해고", "해고무효", "해고 정당성", "정리해고", "경영상해고",
    "수습 본채용거부", "본채용 거부", "해고부존재",
    # 임금/급여
    "임금체불", "체불임금", "퇴직금", "연장근로수당", "야간근로수당",
    "휴일근로수당", "통상임금", "평균임금", "최저임금", "성과급",
    "상여금", "수당 청구",
    # 근로관계
    "근로자성", "사용자성", "근로계약", "기간제", "파견근로",
    "도급 위장", "특수고용", "플랫폼노동",
    # 괴롭힘/차별
    "직장내괴롭힘", "직장 내 괴롭힘", "성희롱", "성차별",
    "폭언", "폭행", "따돌림",
    # 징계
    "징계 정당", "징계 부당", "감봉", "정직", "견책",
    "비위행위", "횡령", "배임",
    # 인사
    "전보", "전직", "인사이동", "배치전환",
    "직위해제", "대기발령",
    # 산재/안전
    "산업재해", "업무상재해", "산재 인정", "업무상 질병",
    "과로사", "자살 업무상",
    # 노동조합
    "부당노동행위", "노동조합", "단체교섭", "쟁의행위",
    "노조법", "부당해고 구제",
    # 계약/기간
    "갱신기대권", "무기계약", "정규직 전환",
    "계약해지", "계약만료",
    # 기타
    "노동위원회", "중앙노동위원회", "재심판정",
    "구제신청", "원직복직", "금전보상",
    "취업규칙", "인사규정",
]

# BigCase 사건 종류 (노동 관련)
CASE_TYPES_LABOR = ["민사", "행정"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BigCase 노동 판례 전수 규모 파악")
    parser.add_argument("--survey-only", action="store_true", help="키워드별 건수만 파악 (목록 수집 안 함)")
    parser.add_argument("--diff-db", action="store_true", help="기존 DB와 비교해서 신규 건 식별")
    parser.add_argument("--max-pages", type=int, default=50, help="키워드당 최대 페이지 (기본 50)")
    parser.add_argument("--delay", type=float, default=0.3, help="요청 간 딜레이")
    parser.add_argument("--keywords", nargs="+", help="특정 키워드만 검색")
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


def build_cookie_session() -> requests.Session:
    session = requests.Session()
    refresh_token = os.environ.get("BIGCASE_REFRESH_TOKEN", "")
    user_id = os.environ.get("BIGCASE_USER_ID", "")
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    if refresh_token:
        session.cookies.set("refreshToken", refresh_token, domain="bigcase.ai", path="/")
    if user_id:
        session.cookies.set("userId", user_id, domain="bigcase.ai", path="/")
    session.cookies.set("hasMembership", os.environ.get("BIGCASE_HAS_MEMBERSHIP", "true"), domain="bigcase.ai", path="/")
    session.cookies.set("keepLogin", "true", domain="bigcase.ai", path="/")
    access_token = os.environ.get("BIGCASE_ACCESS_TOKEN")
    if access_token:
        session.cookies.set("accessToken", access_token, domain="bigcase.ai", path="/")
    return session


def extract_next_data(html: str) -> dict[str, Any] | None:
    match = NEXT_DATA_RE.search(html)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        return None


def search_bigcase(
    session: requests.Session,
    query: str,
    types: list[str] | None = None,
    page: int = 1,
) -> tuple[int, list[dict[str, Any]]]:
    """
    BigCase 검색. Returns (total_count, items).
    items: [{"case_id", "court", "case_number", "case_expression", "case_type", "url"}, ...]
    """
    params = [f"q={quote(query)}"]
    if page > 1:
        params.append(f"page={page}")
    if types:
        params.append(f"types={','.join(types)}")

    url = f"https://bigcase.ai/search/case?{'&'.join(params)}"

    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"

    next_data = extract_next_data(resp.text)
    if not next_data:
        return 0, []

    page_props = next_data.get("props", {}).get("pageProps", {})
    total_count = page_props.get("totalItems", 0)
    items_data = page_props.get("list", [])

    items = []
    for item in items_data:
        case_id = str(item.get("case_id", ""))
        court = item.get("court", "")
        case_number = item.get("case_number", "")
        if not case_id:
            continue
        items.append({
            "case_id": case_id,
            "court": court,
            "case_number": case_number,
            "case_expression": item.get("case_expression", ""),
            "case_type": item.get("case_type", ""),
            "url": f"https://bigcase.ai/cases/{court}/{case_number}" if court and case_number else "",
        })

    return total_count, items


def fetch_existing_decision_urls() -> set[str]:
    """DB에서 기존 bigcase URL 목록"""
    service_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    supabase_url = os.environ.get("SUPABASE_URL", "")
    if not service_key or not supabase_url:
        print("  ⚠️ Supabase 키 없음 — DB 비교 건너뜀")
        return set()

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
    }
    urls: set[str] = set()
    offset = 0
    while True:
        resp = requests.get(
            f"{supabase_url}/rest/v1/nlrc_decisions",
            headers=headers,
            params={"select": "url", "url": "ilike.*bigcase.ai*", "limit": "1000", "offset": str(offset)},
            timeout=60,
        )
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break
        for row in chunk:
            if row.get("url"):
                urls.add(row["url"])
        if len(chunk) < 1000:
            break
        offset += 1000

    return urls


def main() -> None:
    load_env_file()
    args = parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    session = build_cookie_session()
    keywords = args.keywords or LABOR_KEYWORDS

    print(f"{'=' * 60}")
    print(f"BigCase 노동 판례 전수 규모 파악")
    print(f"키워드: {len(keywords)}개")
    print(f"모드: {'survey-only' if args.survey_only else 'full listing'}")
    print(f"{'=' * 60}\n")

    # Phase 1: 키워드별 건수 파악
    keyword_stats: list[dict[str, Any]] = []
    all_cases: dict[str, dict[str, Any]] = {}  # case_id → info (중복 제거)

    for i, kw in enumerate(keywords, 1):
        try:
            total_count, items = search_bigcase(session, kw, CASE_TYPES_LABOR, page=1)
            new_count = 0
            for item in items:
                cid = item["case_id"]
                if cid not in all_cases:
                    all_cases[cid] = item
                    new_count += 1

            keyword_stats.append({
                "keyword": kw,
                "total_count": total_count,
                "page1_items": len(items),
                "new_unique": new_count,
            })
            print(f"  [{i}/{len(keywords)}] \"{kw}\" → {total_count:,}건 (page1: {len(items)}, 신규: {new_count})")

        except Exception as e:
            print(f"  [{i}/{len(keywords)}] \"{kw}\" → ERROR: {e}")
            keyword_stats.append({"keyword": kw, "total_count": 0, "error": str(e)})

        time.sleep(args.delay)

    print(f"\n--- Phase 1 완료 ---")
    print(f"키워드 {len(keywords)}개 검색")
    print(f"1페이지 기준 고유 판례: {len(all_cases):,}건")
    print(f"키워드별 총건수 합계(중복 포함): {sum(s.get('total_count', 0) for s in keyword_stats):,}건")

    # 상위 키워드 출력
    top_keywords = sorted(keyword_stats, key=lambda x: x.get("total_count", 0), reverse=True)[:15]
    print(f"\n📊 상위 키워드:")
    for s in top_keywords:
        print(f"  {s['keyword']}: {s.get('total_count', 0):,}건")

    if args.survey_only:
        # survey 결과 저장
        survey_path = OUTPUT_DIR / f"labor_survey_{timestamp}.json"
        with open(survey_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
                "keywords_count": len(keywords),
                "unique_cases_page1": len(all_cases),
                "keyword_stats": keyword_stats,
            }, f, ensure_ascii=False, indent=2)
        print(f"\n저장: {survey_path}")
        return

    # Phase 2: 전체 목록 수집 (페이지네이션)
    print(f"\n--- Phase 2: 전체 목록 수집 ---")

    for i, kw in enumerate(keywords, 1):
        stat = keyword_stats[i - 1] if i <= len(keyword_stats) else {}
        total = stat.get("total_count", 0)
        if total <= 10:
            continue  # 1페이지로 충분

        total_pages = min((total + 9) // 10, args.max_pages)
        print(f"  [{i}/{len(keywords)}] \"{kw}\" → {total:,}건, {total_pages}페이지 수집...")

        for page in range(2, total_pages + 1):
            try:
                _, items = search_bigcase(session, kw, CASE_TYPES_LABOR, page=page)
                new_count = 0
                for item in items:
                    cid = item["case_id"]
                    if cid not in all_cases:
                        all_cases[cid] = item
                        new_count += 1
                if not items:
                    break  # 더 이상 결과 없음
            except Exception as e:
                print(f"    page {page} error: {e}")
                break
            time.sleep(args.delay)

        if i % 10 == 0:
            print(f"    → 현재 고유 판례: {len(all_cases):,}건")

    print(f"\n--- Phase 2 완료 ---")
    print(f"전체 고유 판례: {len(all_cases):,}건")

    # Phase 3: DB 비교 (선택)
    new_cases = all_cases
    if args.diff_db:
        print(f"\n--- Phase 3: DB 비교 ---")
        existing_urls = fetch_existing_decision_urls()
        print(f"  기존 DB: {len(existing_urls):,}건")
        new_cases = {
            cid: info for cid, info in all_cases.items()
            if info.get("url") and info["url"] not in existing_urls
        }
        print(f"  신규 (DB에 없는): {len(new_cases):,}건")

    # 결과 저장
    listing_path = OUTPUT_DIR / f"labor_cases_{timestamp}.jsonl"
    with open(listing_path, "w", encoding="utf-8") as f:
        for case in new_cases.values():
            f.write(json.dumps(case, ensure_ascii=False) + "\n")

    report_path = OUTPUT_DIR / f"labor_survey_{timestamp}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "keywords_count": len(keywords),
            "total_unique_cases": len(all_cases),
            "new_cases": len(new_cases) if args.diff_db else len(all_cases),
            "keyword_stats": keyword_stats,
            "top_keywords": top_keywords,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"📋 최종 결과:")
    print(f"  전체 고유 판례: {len(all_cases):,}건")
    if args.diff_db:
        print(f"  신규 (DB 미등록): {len(new_cases):,}건")
    print(f"  목록 저장: {listing_path}")
    print(f"  리포트 저장: {report_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
