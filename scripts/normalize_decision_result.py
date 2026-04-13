#!/usr/bin/env python3
"""
decision_result 정규화 스크립트
42종 난립 → 8개 표준값으로 통합

사용법:
  python3 normalize_decision_result.py --dry-run   # 매핑만 출력
  python3 normalize_decision_result.py --apply      # DB 업데이트
"""

import os
import sys
import json
import argparse

try:
    from supabase import create_client
except ImportError:
    print("pip install supabase 필요")
    sys.exit(1)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://mewqgevgdgghhatqtuos.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# 정규화 매핑: 원래값 → 표준값
# 실제 분포 기반 (2026-04-04 조사, 15,742건)
NORMALIZE_MAP = {
    # 근로자 패 = 해고 정당 (dismissed 8,193 + 원고패 269 + rejected 396)
    "dismissed": "dismissed",      # 유지 (영문 표준)
    "원고패": "dismissed",
    "rejected": "dismissed",

    # 근로자 승 = 해고 무효 (granted 4,021 + 원고승 64)
    "granted": "granted",          # 유지 (영문 표준)
    "원고승": "granted",

    # 일부 인용 (partial 1,150)
    "partial": "partial",          # 유지

    # 원심 유지 (upheld 957)
    "upheld": "upheld",            # 유지

    # 파기환송 (overturned 383 + 파기환송 2 + 파기(자판)류)
    "overturned": "overturned",    # 유지
    "파기환송": "overturned",

    # 미분류 (unknown 254 + 빈값 2 + "-" 1)
    "unknown": "unknown",          # 유지
    "": "unknown",
    "-": "unknown",

    # 헌법재판 (합헌 2 + 헌법불합치 1)
    "합헌": "constitutional",
    "헌법불합치": "constitutional",

    # 무죄
    "무죄": "acquitted",
    "선고유예": "acquitted",
}

# 형사판결(벌금/징역) — 패턴 매칭으로 처리
CRIMINAL_PATTERNS = ["벌금", "징역", "집행유예", "파기(자판)"]


def main():
    parser = argparse.ArgumentParser(description="decision_result 정규화")
    parser.add_argument("--dry-run", action="store_true", help="매핑만 출력")
    parser.add_argument("--apply", action="store_true", help="DB 업데이트 실행")
    args = parser.parse_args()

    if not SUPABASE_KEY:
        print("SUPABASE_KEY 환경변수 필요")
        sys.exit(1)

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # 현재 분포 조회
    print("[현재 decision_result 분포]")
    rpc_data = None
    try:
        resp = supabase.rpc("exec_sql", {
            "query": """
            SELECT decision_result, count(*) as cnt
            FROM nlrc_decisions
            WHERE id LIKE 'bc_%'
            GROUP BY decision_result
            ORDER BY cnt DESC
            """
        }).execute()
        rpc_data = resp.data
    except Exception:
        pass

    if not rpc_data:
        # Fallback: fetch distinct values
        print("(RPC 미지원, 직접 조회)")
        resp = supabase.table("nlrc_decisions") \
            .select("decision_result") \
            .like("id", "bc_%") \
            .limit(1000) \
            .execute()
        from collections import Counter
        counts = Counter(row["decision_result"] for row in (resp.data or []))
        for val, cnt in counts.most_common():
            mapped = NORMALIZE_MAP.get(val, f"기타({val})")
            print(f"  {val:30s} → {mapped:15s} ({cnt}건)")
    else:
        for row in resp.data:
            val = row["decision_result"]
            cnt = row["cnt"]
            mapped = NORMALIZE_MAP.get(val, f"기타({val})")
            print(f"  {val:30s} → {mapped:15s} ({cnt}건)")

    if args.dry_run or not args.apply:
        print("\n[dry-run] --apply 플래그로 실행하세요")
        return

    # Apply normalization
    print("\n[정규화 적용 중...]")
    updated = 0

    # 1. Exact match normalization
    for original, normalized in NORMALIZE_MAP.items():
        if original == normalized:
            continue
        resp = supabase.table("nlrc_decisions") \
            .update({"decision_result": normalized}) \
            .like("id", "bc_%") \
            .eq("decision_result", original) \
            .execute()
        count = len(resp.data or [])
        if count > 0:
            print(f"  {original} → {normalized}: {count}건")
            updated += count

    # 2. Criminal pattern normalization (벌금/징역/파기(자판))
    for pattern in CRIMINAL_PATTERNS:
        resp = supabase.table("nlrc_decisions") \
            .update({"decision_result": "criminal"}) \
            .like("id", "bc_%") \
            .like("decision_result", f"%{pattern}%") \
            .execute()
        count = len(resp.data or [])
        if count > 0:
            print(f"  *{pattern}* → criminal: {count}건")
            updated += count

    print(f"\n[완료] {updated}건 정규화됨")


if __name__ == "__main__":
    main()
