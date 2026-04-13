"""
cases.decision_date 백필 스크립트
- law.go.kr API에서 선고일자 가져오기 (487건)
- ilabor 케이스 case_number에서 연도 추출 (145건, 부분)
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
API_DELAY = 0.3


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


def fetch_null_date_cases(source_filter="law.go.kr", limit=1000):
    url = f"{SUPABASE_URL}/rest/v1/cases"
    params = {
        "select": "id,case_number,title,url",
        "decision_date": "is.null",
        "url": f"like.*{source_filter}*",
        "order": "id",
        "limit": str(limit),
    }
    r = requests.get(url, headers=supabase_headers(), params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def extract_lawgo_id(url_str: str) -> str | None:
    m = re.search(r"ID=(\d+)", url_str or "")
    return m.group(1) if m else None


def fetch_lawgo_date(prec_id: str) -> str | None:
    """법제처 API에서 선고일자 가져오기. 형식: YYYYMMDD"""
    url = "http://www.law.go.kr/DRF/lawService.do"
    params = {"OC": LAWGO_OC, "target": "prec", "ID": prec_id, "type": "JSON"}
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            prec = r.json().get("PrecService", {})
            date_str = prec.get("선고일자", "")
            if date_str and len(date_str) >= 8:
                # YYYYMMDD -> YYYY-MM-DD
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    except Exception as e:
        print(f"  [WARN] fetch failed for {prec_id}: {e}", file=sys.stderr)
    return None


def update_date(case_id: str, date_str: str) -> bool:
    url = f"{SUPABASE_URL}/rest/v1/cases"
    params = {"id": f"eq.{case_id}"}
    body = {"decision_date": date_str}
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

    # Phase 1: law.go.kr cases
    print("=== Phase 1: law.go.kr cases ===")
    lawgo_cases = fetch_null_date_cases("law.go.kr")
    print(f"Found {len(lawgo_cases)} law.go.kr cases with NULL decision_date")

    stats = {"lawgo_total": len(lawgo_cases), "lawgo_updated": 0, "lawgo_failed": 0, "lawgo_no_date": 0}

    for i, case in enumerate(lawgo_cases):
        if i > 0 and i % 50 == 0:
            print(f"  Progress: {i}/{len(lawgo_cases)} — updated: {stats['lawgo_updated']}")

        lawgo_id = extract_lawgo_id(case.get("url", ""))
        if not lawgo_id:
            stats["lawgo_no_date"] += 1
            continue

        date_str = fetch_lawgo_date(lawgo_id)
        time.sleep(API_DELAY)

        if date_str:
            if update_date(case["id"], date_str):
                stats["lawgo_updated"] += 1
            else:
                stats["lawgo_failed"] += 1
        else:
            stats["lawgo_no_date"] += 1

    print(f"\n=== Results ===")
    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
