"""BigCase 대량 수집 — bigcase_harassment_pipeline 활용

BigCaseClient를 직접 사용해서 영역별 100건씩 검색 + 상세 수집.

Usage:
    python scripts/bigcase_bulk_collect.py
    python scripts/bigcase_bulk_collect.py --category Q1_무단결근 --search-limit 50 --detail-limit 20
    python scripts/bigcase_bulk_collect.py --search-only
"""
import sys
import os
import json
import argparse
import time
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\dev\neuro-coach\legal-automation")

from src.bigcase.client import BigCaseClient
from src.bigcase.models import BigCaseItem, BigCaseDetail

OUTPUT_DIR = Path(r"C:\dev\labor-decisions-search\evaluation\bigcase_bulk")

CATEGORIES = {
    "Q1_무단결근": {
        "keywords": ["무단결근 해고", "무단결근 징계해고 정당", "결근 징계 부당해고"],
        "types": ["행정", "민사"],
    },
    "Q2_결근절차": {
        "keywords": ["무단결근 서면통지 위반", "해고 절차위반 부당", "서면통지 미비 해고"],
        "types": ["행정", "민사"],
    },
    "Q3_괴롭힘성립": {
        "keywords": ["직장내괴롭힘 성립", "직장내괴롭힘 징계", "괴롭힘 인정 해고"],
        "types": ["행정", "민사"],
    },
    "Q4_괴롭힘보복": {
        "keywords": ["직장내괴롭힘 신고 보복", "괴롭힘 신고 불이익", "신고자 보복 인사조치"],
        "types": ["행정", "민사", "형사"],
    },
    "Q5_수습해고": {
        "keywords": ["수습 본채용거부", "시용 해고 정당", "수습기간 해고"],
        "types": ["행정", "민사"],
    },
    "Q6_수습절차": {
        "keywords": ["수습 해고 서면통지", "본채용거부 절차", "시용 해고 절차위반"],
        "types": ["행정", "민사"],
    },
    "Q7_저성과": {
        "keywords": ["저성과 해고", "업무능력부족 해고", "근무성적 불량 해고"],
        "types": ["행정", "민사"],
    },
    "Q8_징계양정": {
        "keywords": ["징계양정 과다 부당해고", "징계 과중 해고", "해고 양정 사회통념"],
        "types": ["행정", "민사"],
    },
}


def collect_search(client, category_key, config, search_limit):
    """검색 단계 — 키워드별 판례 수집"""
    all_items = {}
    keywords = config["keywords"]
    types_list = config.get("types")

    for keyword in keywords:
        print(f"  검색: {keyword}", end=" ")
        page = 1
        collected = 0

        while collected < search_limit:
            try:
                result = client.search(
                    query=keyword,
                    types=types_list,
                    page=page,
                    limit=min(10, search_limit - collected),
                )
            except Exception as e:
                print(f"에러: {e}")
                break

            if not result.items:
                break

            for item in result.items:
                key = f"{item.court}_{item.case_number}"
                if key not in all_items:
                    all_items[key] = {
                        "item": item,
                        "keywords": [keyword],
                    }
                    collected += 1
                elif keyword not in all_items[key]["keywords"]:
                    all_items[key]["keywords"].append(keyword)

            if len(result.items) < 10:
                break
            page += 1
            time.sleep(1)

        print(f"→ {collected}건 (누적 {len(all_items)})")

    return all_items


def collect_details(client, items_dict, detail_limit):
    """상세 조회 단계"""
    sorted_items = sorted(
        items_dict.values(),
        key=lambda x: -len(x["keywords"])
    )[:detail_limit]

    details = []
    for i, bucket in enumerate(sorted_items):
        item = bucket["item"]
        print(f"  [{i+1}/{len(sorted_items)}] {item.court} {item.case_number}", end=" ")

        try:
            detail = client.get_detail(court=item.court, case_number=item.case_number)
            if detail:
                details.append({
                    "court": item.court,
                    "case_number": item.case_number,
                    "title": detail.title or item.title,
                    "date": detail.date or item.date,
                    "case_type": detail.case_type or item.case_type,
                    "result": detail.result if hasattr(detail, 'result') else '',
                    "summary": detail.summary or '',
                    "full_text": detail.full_text or '',
                    "keywords": bucket["keywords"],
                    "url": item.url,
                })
                result_text = detail.result if hasattr(detail, 'result') else '?'
                print(f"✅ {result_text}")
            else:
                print("❌ 상세 없음")
        except Exception as e:
            print(f"❌ {e}")

        time.sleep(2)

    return details


def main():
    parser = argparse.ArgumentParser(description='BigCase 대량 수집')
    parser.add_argument('--category', help='특정 영역만')
    parser.add_argument('--search-limit', type=int, default=100, help='키워드당 검색 건수')
    parser.add_argument('--detail-limit', type=int, default=50, help='영역당 상세 조회 건수')
    parser.add_argument('--search-only', action='store_true', help='검색만 (상세 조회 안 함)')
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    categories = CATEGORIES
    if args.category:
        if args.category in CATEGORIES:
            categories = {args.category: CATEGORIES[args.category]}
        else:
            print(f"카테고리: {list(CATEGORIES.keys())}")
            return

    all_details = []

    with BigCaseClient(headless=True) as client:
        for cat_key, config in categories.items():
            print(f"\n{'='*60}")
            print(f"영역: {cat_key}")
            print(f"{'='*60}")

            # 검색
            items = collect_search(client, cat_key, config, args.search_limit)

            # 검색 결과 저장
            search_path = OUTPUT_DIR / f"{cat_key}_search.json"
            with open(search_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "category": cat_key,
                    "total_unique": len(items),
                    "searched_at": datetime.now().isoformat(),
                    "items": [
                        {
                            "court": b["item"].court,
                            "case_number": b["item"].case_number,
                            "title": b["item"].title,
                            "keywords": b["keywords"],
                        }
                        for b in items.values()
                    ]
                }, f, ensure_ascii=False, indent=2)

            if args.search_only:
                print(f"  검색만 완료: {len(items)}건")
                continue

            # 상세 조회
            print(f"\n  상세 조회 (최대 {args.detail_limit}건)")
            details = collect_details(client, items, args.detail_limit)

            # 상세 저장
            detail_path = OUTPUT_DIR / f"{cat_key}_details.jsonl"
            with open(detail_path, 'w', encoding='utf-8') as f:
                for d in details:
                    d["category"] = cat_key
                    f.write(json.dumps(d, ensure_ascii=False) + '\n')

            all_details.extend(details)
            print(f"  저장: {detail_path} ({len(details)}건)")

    # 전체 저장
    all_path = OUTPUT_DIR / "all_details.jsonl"
    with open(all_path, 'w', encoding='utf-8') as f:
        for d in all_details:
            f.write(json.dumps(d, ensure_ascii=False) + '\n')

    # 요약
    print(f"\n{'='*60}")
    print(f"수집 완료: {len(all_details)}건")
    print(f"{'='*60}")
    for cat_key in categories:
        count = sum(1 for d in all_details if d.get('category') == cat_key)
        print(f"  {cat_key}: {count}건")
    print(f"저장: {all_path}")


if __name__ == '__main__':
    main()
