"""BigCase 최대 확장 수집 전략

사안별 가능한 모든 판례를 수집.
키워드를 세분화하고, 검색 결과 전량 수집 후 상세 조회.
주기적 실행으로 신규 판례도 자동 보충.

Usage:
    # 전체 수집 (최초)
    python scripts/bigcase_max_collect.py --mode full

    # 신규 보충 (주기적)
    python scripts/bigcase_max_collect.py --mode incremental

    # 특정 영역만
    python scripts/bigcase_max_collect.py --category Q1_무단결근 --mode full

    # 검색만 (상세 조회 안 함)
    python scripts/bigcase_max_collect.py --mode search-only

    # 상세 미조회 건만 이어서
    python scripts/bigcase_max_collect.py --mode detail-only
"""
import sys
import os
import json
import argparse
import time
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\dev\neuro-coach\legal-automation")

from src.bigcase.client import BigCaseClient

OUTPUT_DIR = Path(r"C:\dev\labor-decisions-search\evaluation\bigcase_max")
DETAIL_DIR = OUTPUT_DIR / "details"
SEARCH_DIR = OUTPUT_DIR / "searches"

# 최대 확장 키워드 — 영역당 다양한 검색어로 커버리지 극대화
CATEGORIES = {
    "Q1_무단결근": {
        "keywords": [
            "무단결근 해고", "무단결근 징계해고", "결근 해고 정당",
            "무단결근 부당해고", "결근 징계 부당", "무단결근 취소",
            "장기결근 해고", "출근불량 해고", "근태불량 징계",
            "결근 서면경고", "무단이탈 해고",
        ],
        "types": ["행정", "민사"],
    },
    "Q2_결근절차": {
        "keywords": [
            "해고 서면통지 위반", "해고 절차위반 부당", "서면통지 미비 해고",
            "해고 절차 하자", "소명기회 미부여 해고", "인사위원회 미개최",
            "해고예고 위반", "해고통지 절차", "징계절차 위반 부당해고",
        ],
        "types": ["행정", "민사"],
    },
    "Q3_괴롭힘성립": {
        "keywords": [
            "직장내괴롭힘 성립", "직장내괴롭힘 인정", "괴롭힘 징계",
            "직장내괴롭힘 해고", "괴롭힘 손해배상", "직장내괴롭힘 판결",
            "직장내 성희롱 징계", "폭언 괴롭힘", "업무상 적정범위",
            "우위성 괴롭힘",
        ],
        "types": ["행정", "민사", "형사"],
    },
    "Q4_괴롭힘보복": {
        "keywords": [
            "괴롭힘 신고 보복", "신고자 불이익", "보복 인사조치",
            "괴롭힘 신고 해고", "신고자 보호", "불이익취급 부당노동행위",
            "내부고발 보복", "신고 전보", "괴롭힘 피해자 불이익",
        ],
        "types": ["행정", "민사", "형사"],
    },
    "Q5_수습해고": {
        "keywords": [
            "수습 해고", "시용 해고", "본채용거부", "수습기간 해고",
            "시용근로자 해고", "수습 부당해고", "본채용 거부 취소",
            "수습평가 해고", "시용기간 해약권",
        ],
        "types": ["행정", "민사"],
    },
    "Q6_수습절차": {
        "keywords": [
            "수습 서면통지", "본채용거부 절차", "시용 절차위반",
            "수습 해고예고", "수습 소명기회", "본채용거부 서면통지",
            "수습 인사위원회", "시용 해고 절차",
        ],
        "types": ["행정", "민사"],
    },
    "Q7_저성과": {
        "keywords": [
            "저성과 해고", "업무능력부족 해고", "근무성적 불량 해고",
            "성과미달 해고", "인사평가 해고", "PIP 해고",
            "업무능력 부족 부당해고", "저성과 징계", "통상해고 업무능력",
        ],
        "types": ["행정", "민사"],
    },
    "Q8_징계양정": {
        "keywords": [
            "징계양정 과다", "징계양정 부당", "해고 양정 과다",
            "징계 비례원칙", "사회통념상 상당성", "징계 재량권 일탈",
            "징계 과중 부당", "해고 양정 사회통념", "감봉 과다",
            "정직 과다",
        ],
        "types": ["행정", "민사"],
    },
}


def load_existing_cases():
    """이미 수집된 사건 목록"""
    existing = {}
    if DETAIL_DIR.exists():
        for f in DETAIL_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding='utf-8'))
                key = f"{data.get('court','')}_{data.get('case_number','')}"
                existing[key] = data
            except:
                pass
    return existing


def search_all_keywords(client, config, max_per_keyword=500):
    """키워드별 전량 검색"""
    all_items = {}

    for keyword in config["keywords"]:
        print(f"  검색: {keyword}", end=" ")
        page = 1
        collected = 0

        while collected < max_per_keyword:
            try:
                result = client.search(
                    query=keyword,
                    types=config.get("types"),
                    page=page,
                    limit=10,
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
                        "court": item.court,
                        "case_number": item.case_number,
                        "title": item.title,
                        "url": item.url,
                        "keywords": [keyword],
                    }
                    collected += 1
                elif keyword not in all_items[key]["keywords"]:
                    all_items[key]["keywords"].append(keyword)

            if len(result.items) < 10:
                break
            page += 1
            time.sleep(0.5)

        print(f"→ {collected}건 (누적 {len(all_items)})")

    return all_items


def fetch_details(client, items_dict, existing, max_details=9999):
    """상세 조회 — 이미 있는 건 스킵"""
    pending = []
    for key, item in items_dict.items():
        if key not in existing:
            pending.append((key, item))

    pending = sorted(pending, key=lambda x: -len(x[1]["keywords"]))[:max_details]

    print(f"  상세 조회: {len(pending)}건 (기존 {len(existing)}건 스킵)")

    fetched = []
    for i, (key, item) in enumerate(pending):
        print(f"  [{i+1}/{len(pending)}] {item['court']} {item['case_number']}", end=" ")

        try:
            detail = client.get_detail(court=item['court'], case_number=item['case_number'])
            if detail:
                record = {
                    "court": item["court"],
                    "case_number": item["case_number"],
                    "title": detail.title or item["title"],
                    "date": detail.date or "",
                    "case_type": detail.case_type or "",
                    "result": detail.result if hasattr(detail, 'result') else '',
                    "summary": detail.summary or "",
                    "full_text": detail.full_text or "",
                    "keywords": item["keywords"],
                    "url": item.get("url", ""),
                    "collected_at": datetime.now().isoformat(),
                }

                # 개별 파일 저장
                safe_name = re.sub(r'[^\w가-힣-]', '_', f"{item['court']}_{item['case_number']}")
                detail_path = DETAIL_DIR / f"{safe_name}.json"
                detail_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')

                fetched.append(record)
                print("✅")
            else:
                print("❌")
        except Exception as e:
            print(f"❌ {e}")

        time.sleep(1.5)

    return fetched


def main():
    parser = argparse.ArgumentParser(description='BigCase 최대 확장 수집')
    parser.add_argument('--category', help='특정 영역만')
    parser.add_argument('--mode', choices=['full', 'incremental', 'search-only', 'detail-only'],
                        default='full', help='수집 모드')
    parser.add_argument('--max-per-keyword', type=int, default=500, help='키워드당 최대 검색')
    parser.add_argument('--max-details', type=int, default=9999, help='최대 상세 조회')
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    SEARCH_DIR.mkdir(parents=True, exist_ok=True)

    categories = CATEGORIES
    if args.category:
        if args.category in CATEGORIES:
            categories = {args.category: CATEGORIES[args.category]}
        else:
            print(f"카테고리: {list(CATEGORIES.keys())}")
            return

    existing = load_existing_cases()
    print(f"기존 수집: {len(existing)}건")

    total_new = 0

    with BigCaseClient(headless=True) as client:
        for cat_key, config in categories.items():
            print(f"\n{'='*60}")
            print(f"영역: {cat_key} ({len(config['keywords'])}개 키워드)")
            print(f"{'='*60}")

            # 검색
            if args.mode != 'detail-only':
                items = search_all_keywords(client, config, args.max_per_keyword)

                # 검색 결과 저장
                search_path = SEARCH_DIR / f"{cat_key}_search.json"
                search_path.write_text(json.dumps({
                    "category": cat_key,
                    "total_unique": len(items),
                    "searched_at": datetime.now().isoformat(),
                    "items": list(items.values()),
                }, ensure_ascii=False, indent=2), encoding='utf-8')
                print(f"  검색 완료: {len(items)}건 고유")
            else:
                # 기존 검색 결과 로드
                search_path = SEARCH_DIR / f"{cat_key}_search.json"
                if search_path.exists():
                    data = json.loads(search_path.read_text(encoding='utf-8'))
                    items = {f"{i['court']}_{i['case_number']}": i for i in data.get("items", [])}
                else:
                    print(f"  검색 결과 없음 — 스킵")
                    continue

            # 상세 조회
            if args.mode != 'search-only':
                new_details = fetch_details(client, items, existing, args.max_details)
                total_new += len(new_details)

                # 영역별 JSONL
                cat_jsonl = OUTPUT_DIR / f"{cat_key}_all.jsonl"
                # 기존 + 신규 합치기
                cat_records = []
                for key, data in existing.items():
                    if any(kw in str(data.get('keywords', [])) for kw in config['keywords'][:3]):
                        cat_records.append(data)
                cat_records.extend(new_details)

                with open(cat_jsonl, 'w', encoding='utf-8') as f:
                    for r in cat_records:
                        r['category'] = cat_key
                        f.write(json.dumps(r, ensure_ascii=False) + '\n')

                print(f"  신규 {len(new_details)}건 | 영역 합계 {len(cat_records)}건")

                # existing 갱신
                for r in new_details:
                    key = f"{r['court']}_{r['case_number']}"
                    existing[key] = r

    # 전체 합산
    print(f"\n{'='*60}")
    print(f"수집 완료")
    print(f"{'='*60}")
    print(f"신규: {total_new}건")
    print(f"전체 보유: {len(existing)}건")

    # 전체 JSONL
    all_path = OUTPUT_DIR / "all_cases.jsonl"
    with open(all_path, 'w', encoding='utf-8') as f:
        for data in existing.values():
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    print(f"저장: {all_path}")


if __name__ == '__main__':
    main()
