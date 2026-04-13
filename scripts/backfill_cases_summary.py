"""
cases.summary 백필 스크립트
- law.go.kr API에서 판례 원문(판결요지/판례내용) 가져오기
- 판결요지가 있으면 직접 사용, 없으면 판례내용에서 AI 요약 생성
- Supabase에 summary 업데이트
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import requests

REPO_DIR = Path(__file__).parent.parent
SUPABASE_URL = ""
SUPABASE_KEY = ""
LAWGO_OC = ""
BATCH_SIZE = 20
API_DELAY = 0.3  # law.go.kr rate limit


def load_env():
    global SUPABASE_URL, SUPABASE_KEY, LAWGO_OC
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip())
    SUPABASE_URL = os.environ.get("NEXT_PUBLIC_SUPABASE_URL") or os.environ.get("SUPABASE_URL", "")
    SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    LAWGO_OC = os.environ.get("LAWGO_OC") or os.environ.get("OC", "iceamericano9")


def supabase_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }


def fetch_null_summary_cases(limit=1000):
    """summary가 NULL인 cases를 가져온다."""
    url = f"{SUPABASE_URL}/rest/v1/cases"
    params = {
        "select": "id,case_number,title,url,court,case_type,verdict_type,decision_date",
        "summary": "is.null",
        "order": "id",
        "limit": str(limit),
    }
    r = requests.get(url, headers=supabase_headers(), params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def extract_lawgo_id(url_str: str) -> str | None:
    """law.go.kr URL에서 ID 추출."""
    m = re.search(r"ID=(\d+)", url_str or "")
    return m.group(1) if m else None


def fetch_lawgo_prec(prec_id: str) -> dict:
    """법제처 API에서 판례 데이터 가져오기."""
    url = "http://www.law.go.kr/DRF/lawService.do"
    params = {"OC": LAWGO_OC, "target": "prec", "ID": prec_id, "type": "JSON"}
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return r.json().get("PrecService", {})
    except Exception as e:
        print(f"  [WARN] law.go.kr fetch failed for {prec_id}: {e}", file=sys.stderr)
    return {}


def clean_html(text: str) -> str:
    """HTML 태그, 불필요한 공백 정리."""
    if not text:
        return ""
    text = text.replace("<br/>", "\n").replace("<br>", "\n")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_summary_from_content(content: str, title: str, max_len: int = 500) -> str:
    """판례내용에서 주문/이유 부분을 추출하여 요약으로 사용."""
    cleaned = clean_html(content)
    if not cleaned:
        return ""

    # 주문 부분 추출
    joomun = ""
    m = re.search(r"【\s*주\s*문\s*】\s*(.*?)(?=【|$)", cleaned, re.DOTALL)
    if m:
        joomun = m.group(1).strip()

    # 이유 첫 부분 추출
    reason = ""
    m = re.search(r"【\s*이\s*유\s*】\s*(.*?)(?=\n\n|\Z)", cleaned, re.DOTALL)
    if m:
        reason = m.group(1).strip()[:800]

    # 조합
    parts = []
    if joomun:
        parts.append(joomun[:200])
    if reason:
        parts.append(reason[:300])

    if parts:
        summary = " ".join(parts)
        if len(summary) > max_len:
            summary = summary[:max_len].rsplit(".", 1)[0] + "."
        return summary

    # fallback: 처음 500자
    return cleaned[:max_len].rsplit(".", 1)[0] + "." if len(cleaned) > max_len else cleaned


def generate_summary(prec_data: dict, case: dict) -> str:
    """판례 데이터에서 summary를 생성한다."""
    # 1순위: 판결요지
    verdict_summary = clean_html(prec_data.get("판결요지", ""))
    if verdict_summary and len(verdict_summary) > 20:
        return verdict_summary[:1000]

    # 2순위: 판시사항
    holding = clean_html(prec_data.get("판시사항", ""))
    if holding and len(holding) > 20:
        return holding[:1000]

    # 3순위: 판례내용에서 추출
    content = prec_data.get("판례내용", "")
    if content:
        return extract_summary_from_content(content, case.get("title", ""))

    # 최종 fallback: 제목 + 메타데이터
    parts = [case.get("title", "")]
    if case.get("court"):
        parts.append(case["court"])
    if case.get("verdict_type"):
        parts.append(case["verdict_type"])
    return " - ".join(p for p in parts if p)


def update_summary(case_id: str, summary: str) -> bool:
    """Supabase에 summary 업데이트."""
    url = f"{SUPABASE_URL}/rest/v1/cases"
    params = {"id": f"eq.{case_id}"}
    body = {"summary": summary}
    try:
        r = requests.patch(url, headers=supabase_headers(), params=params, json=body, timeout=15)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"  [ERR] update failed for {case_id}: {e}", file=sys.stderr)
        return False


def main():
    load_env()
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL / SUPABASE_SERVICE_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching cases with NULL summary...")
    cases = fetch_null_summary_cases(limit=2000)
    print(f"Found {len(cases)} cases to backfill")

    stats = {"total": len(cases), "lawgo_ok": 0, "ilabor_skip": 0, "updated": 0, "failed": 0, "no_data": 0}
    results = []

    for i, case in enumerate(cases):
        case_id = case["id"]
        url = case.get("url", "")

        if i > 0 and i % 50 == 0:
            print(f"Progress: {i}/{len(cases)} — updated: {stats['updated']}, failed: {stats['failed']}")

        lawgo_id = extract_lawgo_id(url)
        if not lawgo_id:
            # ilabor or no URL — generate from metadata only
            stats["ilabor_skip"] += 1
            title = case.get("title", "")
            court = case.get("court", "")
            vtype = case.get("verdict_type", "")
            meta_summary = " - ".join(p for p in [title, court, vtype] if p)
            if meta_summary and len(meta_summary) > 5:
                if update_summary(case_id, meta_summary):
                    stats["updated"] += 1
                    results.append({"id": case_id, "source": "metadata", "len": len(meta_summary)})
            continue

        # law.go.kr API에서 가져오기
        prec_data = fetch_lawgo_prec(lawgo_id)
        time.sleep(API_DELAY)

        if not prec_data:
            stats["no_data"] += 1
            continue

        summary = generate_summary(prec_data, case)
        if summary and len(summary) > 5:
            stats["lawgo_ok"] += 1
            if update_summary(case_id, summary):
                stats["updated"] += 1
                results.append({"id": case_id, "source": "lawgo", "len": len(summary)})
            else:
                stats["failed"] += 1
        else:
            stats["no_data"] += 1

    print(f"\n=== Backfill Complete ===")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    # 결과 저장
    out_path = REPO_DIR / "backfill_summary_results.json"
    out_path.write_text(json.dumps({"stats": stats, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    main()
