"""BigCase 확장 수집 — Next.js data API 직접 활용

기존 검색 결과(search JSON)에서 상세 미수집 건을 fetchin 하고,
추가 검색으로 새 케이스도 확보.

목표: 카테고리당 2,000건 = 전체 16,000건

Usage:
    python scripts/bigcase_expand_collect.py --mode detail-only
    python scripts/bigcase_expand_collect.py --mode full
    python scripts/bigcase_expand_collect.py --category Q1_무단결근
"""
import sys
import os
import json
import argparse
import time
import re
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

REPO_DIR = Path(__file__).parent.parent
OUTPUT_DIR = REPO_DIR / "evaluation" / "bigcase_bulk"

BIGCASE_BASE = "https://bigcase.ai"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

CATEGORIES = {
    "Q1_무단결근": {
        "keywords": [
            "무단결근 해고", "무단결근 징계해고 정당", "결근 징계 부당해고",
            "무단결근 부당해고 인정", "결근 해고 취소", "장기결근 해고",
            "출근불량 해고", "근태불량 징계", "무단결근 취소",
            "결근 해고 판결", "출근거부 해고", "결근 부당해고",
            "결근 징계 판결", "결근 해고 정당성", "무단이탈 징계",
        ],
        "types": ["행정", "민사"],
    },
    "Q2_결근절차": {
        "keywords": [
            "무단결근 서면통지 위반", "해고 절차위반 부당", "서면통지 미비 해고",
            "해고 절차 위반 취소", "서면통지 부당해고 인정", "소명기회 미부여 해고",
            "인사위원회 미개최", "해고예고 위반", "징계절차 위반 부당해고",
            "해고 서면 미교부", "해고 사전통지 위반", "서면해고 부당",
            "해고 서면요건 미비",
        ],
        "types": ["행정", "민사"],
    },
    "Q3_괴롭힘성립": {
        "keywords": [
            "직장내괴롭힘 성립", "직장내괴롭힘 징계", "괴롭힘 인정 해고",
            "직장내괴롭힘 부당해고", "직장내괴롭힘 인정", "괴롭힘 손해배상",
            "폭언 괴롭힘", "업무상 적정범위", "우위성 괴롭힘",
            "직장 내 괴롭힘 성립요건", "근로기준법 76조의2", "괴롭힘 판단기준",
            "직장내 괴롭힘 민사", "괴롭힘 위자료", "직장내 따돌림 손해배상",
            "상사 폭언 괴롭힘", "갑질 손해배상", "직장내 괴롭힘 위법",
            "직장내괴롭힘 형사", "직장내괴롭힘 신고", "직장 내 따돌림 위자료",
            "직장내 괴롭힘", "직장 괴롭힘 판결", "근로자 괴롭힘 인정",
            "근로기준법 제76조의2", "괴롭힘 손해 배상", "사업장 괴롭힘 판결",
            "직장 내 괴롭힘 행위자", "직장 괴롭힘 피해자", "직장내 집단따돌림",
            "직장 내 괴롭힘 징계", "직장 내 괴롭힘 피해 배상",
        ],
        "types": ["행정", "민사", "형사"],
    },
    "Q4_괴롭힘보복": {
        "keywords": [
            "직장내괴롭힘 신고 보복", "괴롭힘 신고 불이익", "괴롭힘 신고 부당해고",
            "신고자 불이익", "보복 인사조치", "신고자 보호", "불이익취급 부당노동행위",
            "내부고발 보복", "신고 전보",
            "괴롭힘 신고 보복 해고", "피해자 보복 인사조치", "괴롭힘 신고 후 불이익",
        ],
        "types": ["행정", "민사", "형사"],
    },
    "Q5_수습해고": {
        "keywords": [
            "수습 본채용거부", "수습기간 해고", "본채용거부 취소",
            "시용 해고 정당", "수습 부당해고", "본채용 거부 정당성",
            "수습평가 해고", "시용기간 해약권", "수습 해고",
            "시용계약 해지", "수습근로자 해고", "수습 부당해고 취소",
            "시용 해고 부당", "수습 평가 해고", "시용기간 만료 해고",
            "수습 계약 해지 정당", "수습 해고 인정", "시용 채용 거부",
            "수습 계약 해지", "시용 기간 종료 해고", "본채용 거절 정당",
            "시용 근로자 해고", "본채용 거부 취소",
            "수습 불합격 해고 정당", "시용 기간 내 해고", "본채용 불합격 부당해고",
        ],
        "types": ["행정", "민사"],
    },
    "Q6_수습절차": {
        "keywords": [
            "수습 해고 서면통지", "본채용거부 절차", "시용 해고 절차위반",
            "본채용거부 서면통지 위반", "수습 소명기회", "수습 인사위원회",
            "시용 서면통지", "수습 해고예고",
            "시용 해고통보 절차", "수습 해고 사전통지", "본채용 거부 통보 방법",
            "수습 해고 서면통지 미비", "시용 해고 예고 위반", "수습 해고 절차 위반",
            "수습기간 해고 통보 하자", "시용 해고 불복",
            "수습 해고 통지", "수습 해고 해고예고", "수습 기간 해고 방법",
            "수습 해고 부당 절차", "시용기간 해고 부당 절차", "수습 근로자 해고 통보",
            "시용기간 해고 절차", "수습 해고 정당 절차", "시용 본채용 거부 통지",
            "시용 해고 사전 통지", "수습 부당해고 절차 위반",
            "수습 해고통보 방법", "시용 해고 서면 위반", "수습기간 해고 서면 미교부",
            "시용 해고 부당 절차위반", "수습근로자 해고 통지 방법",
            "시용 해고 서면요건", "시용 해약권 행사 방법",
        ],
        "types": ["행정", "민사"],
    },
    "Q7_저성과": {
        "keywords": [
            "저성과 해고", "업무능력부족 해고", "저성과 부당해고",
            "근무성적 불량 해고", "성과미달 해고", "인사평가 해고",
            "업무능력 부족 부당해고", "통상해고 업무능력",
            "업무능력 해고", "근무성적 해고", "근무불량 해고",
            "업무미달 해고", "직무능력 부족 해고", "성과 해고 부당",
            "근무불량 부당해고", "업무능력 미달 해고",
            "업무능력 미달 징계", "근무불량 징계 해고", "업무실적 불량 해고",
            "근무성적 불량 징계", "업무능력 부족 직권면직",
        ],
        "types": ["행정", "민사"],
    },
    "Q8_징계양정": {
        "keywords": [
            "징계양정 과다 부당해고", "징계 과중 해고", "해고 양정 사회통념",
            "징계양정 과다 취소", "징계 비례원칙", "사회통념상 상당성",
            "징계 재량권 일탈", "감봉 과다", "정직 과다",
            "징계 수위 부당", "징계처분 과다 부당", "징계 수준 적정성",
            "감봉 정직 과다 부당",
        ],
        "types": ["행정", "민사"],
    },
}


def get_build_id():
    """bigcase.ai 현재 build ID 조회"""
    url = BIGCASE_BASE + "/"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    resp = urllib.request.urlopen(req, timeout=15)
    data = resp.read().decode("utf-8", errors="replace")
    match = re.search(r'"buildId"\s*:\s*"([^"]+)"', data)
    if match:
        return match.group(1)
    raise RuntimeError("Could not find build ID")


def search_cases(build_id, query, max_items=1000):
    """키워드로 판례 검색 (페이지네이션 처리)"""
    q_encoded = urllib.parse.quote(query)
    items = {}
    page = 1

    while len(items) < max_items:
        url = f"{BIGCASE_BASE}/_next/data/{build_id}/search/case.json?q={q_encoded}&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode("utf-8"))
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
                        "url": f"{BIGCASE_BASE}/cases/{urllib.parse.quote(court)}/{urllib.parse.quote(case_number)}",
                    }
                else:
                    if query not in items[key]["keywords"]:
                        items[key]["keywords"].append(query)

            if len(lst) < 10 or len(items) >= total:
                break

            page += 1
            time.sleep(0.3)

        except Exception as e:
            print(f"    검색 에러 (page={page}): {e}")
            break

    return items


def fetch_detail(build_id, court, case_number):
    """판례 상세 조회"""
    court_encoded = urllib.parse.quote(court)
    case_encoded = urllib.parse.quote(case_number)
    url = f"{BIGCASE_BASE}/_next/data/{build_id}/cases/{court_encoded}/{case_encoded}.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    resp = urllib.request.urlopen(req, timeout=20)
    data = json.loads(resp.read().decode("utf-8"))
    return data.get("pageProps", {}).get("caseDetail")


def load_existing_keys():
    """기존 수집된 사건번호 세트 로드"""
    keys = set()
    for f in OUTPUT_DIR.glob("*_details.jsonl"):
        for line in f.read_text(encoding="utf-8").strip().split("\n"):
            if line:
                try:
                    d = json.loads(line)
                    keys.add(f"{d['court']}_{d['case_number']}")
                except:
                    pass
    return keys


def load_search_items(cat_key):
    """기존 검색 결과 로드"""
    search_path = OUTPUT_DIR / f"{cat_key}_search.json"
    if not search_path.exists():
        return {}
    d = json.loads(search_path.read_text(encoding="utf-8"))
    items = {}
    for item in d.get("items", []):
        key = f"{item['court']}_{item['case_number']}"
        items[key] = item
    return items


def save_search_items(cat_key, items_dict):
    """검색 결과 저장"""
    search_path = OUTPUT_DIR / f"{cat_key}_search.json"
    search_path.write_text(
        json.dumps(
            {
                "category": cat_key,
                "total_unique": len(items_dict),
                "searched_at": datetime.now().isoformat(),
                "items": list(items_dict.values()),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def collect_category(build_id, cat_key, config, existing_keys, target=2000, mode="full"):
    """카테고리 수집"""
    print(f"\n{'='*60}")
    print(f"영역: {cat_key} (목표: {target}건)")
    print(f"{'='*60}")

    # 기존 검색 결과 로드
    search_items = load_search_items(cat_key)
    print(f"  기존 검색 결과: {len(search_items)}건")

    # 추가 검색 (full 모드이거나, 기존 결과가 부족한 경우)
    if mode in ("full", "search") and len(search_items) < target * 2:
        print(f"  추가 검색 시작...")
        for keyword in config["keywords"]:
            print(f"    검색: {keyword}", end=" ", flush=True)
            new_items = search_cases(build_id, keyword, max_items=500)
            added = 0
            for key, item in new_items.items():
                if key not in search_items:
                    search_items[key] = item
                    added += 1
                else:
                    for kw in item["keywords"]:
                        if kw not in search_items[key].get("keywords", []):
                            search_items[key].setdefault("keywords", []).append(kw)
            print(f"→ +{added}건 (누적 {len(search_items)})")
            time.sleep(0.5)

        save_search_items(cat_key, search_items)
        print(f"  검색 완료: {len(search_items)}건 고유")

    if mode == "search":
        return []

    # 현재 카테고리에 수집된 건수 확인
    detail_path = OUTPUT_DIR / f"{cat_key}_details.jsonl"
    cat_existing = []
    if detail_path.exists():
        for line in detail_path.read_text(encoding="utf-8").strip().split("\n"):
            if line:
                try:
                    cat_existing.append(json.loads(line))
                except:
                    pass

    print(f"  현재 상세 수집: {len(cat_existing)}건")

    if len(cat_existing) >= target:
        print(f"  목표 달성! 스킵")
        return cat_existing

    # 상세 조회할 건 목록 (기존 미수집)
    pending = []
    for key, item in search_items.items():
        if key not in existing_keys:
            pending.append(item)

    # 키워드 수 많은 것 우선 (관련성 높음)
    pending.sort(key=lambda x: -len(x.get("keywords", [])))

    need = target - len(cat_existing)
    pending = pending[:need + 50]  # 여유분 추가
    print(f"  상세 조회 대상: {len(pending)}건 (필요: {need}건)")

    fetched = []
    errors = 0
    for i, item in enumerate(pending):
        if len(fetched) + len(cat_existing) >= target:
            print(f"\n  목표 {target}건 달성!")
            break

        court = item.get("court", "")
        case_number = item.get("case_number", "")
        key = f"{court}_{case_number}"

        print(f"  [{i+1}/{len(pending)}] {court} {case_number}", end=" ", flush=True)

        try:
            detail = fetch_detail(build_id, court, case_number)
            if detail:
                record = {
                    "court": court,
                    "case_number": case_number,
                    "title": detail.get("case_expression") or item.get("title", ""),
                    "date": detail.get("judgment_date", ""),
                    "case_type": detail.get("case_type", ""),
                    "result": detail.get("outcome", ""),
                    "summary": detail.get("ai_full_summary_md", ""),
                    "full_text": detail.get("fulltext", ""),
                    "keywords": item.get("keywords", []),
                    "url": item.get("url", f"{BIGCASE_BASE}/cases/{urllib.parse.quote(court)}/{urllib.parse.quote(case_number)}"),
                    "category": cat_key,
                    "collected_at": datetime.now().isoformat(),
                }
                fetched.append(record)
                existing_keys.add(key)
                print(f"OK ({detail.get('outcome', '?')})")
            else:
                errors += 1
                print("SKIP (no detail)")
        except Exception as e:
            errors += 1
            print(f"ERR: {str(e)[:50]}")

        time.sleep(0.8)

    # 카테고리 파일에 추가
    all_cat_records = cat_existing + fetched
    with open(detail_path, "w", encoding="utf-8") as f:
        for r in all_cat_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n  수집 완료: +{len(fetched)}건 (에러 {errors}건) → 합계 {len(all_cat_records)}건")
    return all_cat_records


def merge_all_details():
    """카테고리별 파일을 all_details.jsonl로 병합 (중복 제거)"""
    all_records = {}
    cat_counts = defaultdict(int)

    for f in sorted(OUTPUT_DIR.glob("*_details.jsonl")):
        cat = f.stem.replace("_details", "")
        if not cat.startswith("Q"):
            continue
        for line in f.read_text(encoding="utf-8").strip().split("\n"):
            if line:
                try:
                    d = json.loads(line)
                    d["category"] = cat  # 카테고리 재설정
                    key = f"{cat}_{d['court']}_{d['case_number']}"
                    if key not in all_records:
                        all_records[key] = d
                        cat_counts[cat] += 1
                except:
                    pass

    all_path = OUTPUT_DIR / "all_details.jsonl"
    with open(all_path, "w", encoding="utf-8") as f:
        for record in all_records.values():
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"\n{'='*60}")
    print(f"최종 병합 완료: {len(all_records)}건")
    print(f"{'='*60}")
    for cat, count in sorted(cat_counts.items()):
        print(f"  {cat}: {count}건")
    print(f"저장: {all_path}")
    return len(all_records)


def main():
    parser = argparse.ArgumentParser(description="BigCase 확장 수집")
    parser.add_argument("--category", help="특정 영역만")
    parser.add_argument(
        "--mode",
        choices=["full", "search", "detail-only"],
        default="full",
        help="수집 모드 (full=검색+상세, search=검색만, detail-only=상세만)",
    )
    parser.add_argument("--target", type=int, default=2000, help="카테고리당 목표 건수")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build ID 조회
    print("Build ID 조회...", end=" ", flush=True)
    try:
        build_id = get_build_id()
        print(f"OK: {build_id}")
    except Exception as e:
        print(f"실패: {e}")
        return

    # 기존 수집 현황
    existing_keys = load_existing_keys()
    print(f"기존 고유 수집: {len(existing_keys)}건")

    categories = CATEGORIES
    if args.category:
        if args.category in CATEGORIES:
            categories = {args.category: CATEGORIES[args.category]}
        else:
            print(f"카테고리 목록: {list(CATEGORIES.keys())}")
            return

    total_collected = 0
    for cat_key, config in categories.items():
        records = collect_category(
            build_id, cat_key, config, existing_keys,
            target=args.target, mode=args.mode
        )
        total_collected += len(records)

    # 전체 병합
    if args.mode != "search":
        total = merge_all_details()
        print(f"\n수집 완료! 전체: {total}건")


if __name__ == "__main__":
    main()
