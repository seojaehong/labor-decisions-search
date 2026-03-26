"""BigCase 신규 카테고리 확장 수집 — 카테고리당 2000건 목표

8개 신규 카테고리를 500건에서 2000건으로 확장:
  - sexual_harassment (성희롱)
  - violence (폭언/폭행)
  - embezzlement (횡령/배임)
  - misconduct (비위행위)
  - redundancy (경영상해고)
  - transfer (전보/인사이동)
  - contract_expiry (갱신기대권/계약만료)
  - no_dismissal (해고부존재/사직)

Usage:
    python3 scripts/bigcase_new_categories_expand.py
    python3 scripts/bigcase_new_categories_expand.py --mode full
    python3 scripts/bigcase_new_categories_expand.py --category sexual_harassment
    python3 scripts/bigcase_new_categories_expand.py --target 2000
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

# 확장 키워드 — 기존 500건 수집에 쓴 키워드에 15~30개 추가
CATEGORIES = {
    "sexual_harassment": {
        "keywords": [
            # 기존 키워드
            "성희롱 해고",
            "성희롱 징계",
            "직장내 성희롱",
            "성희롱 손해배상",
            "성희롱 부당해고",
            "성희롱 피해자 불이익",
            "성희롱 가해자 징계",
            "성희롱 신고 보복",
            # 확장 키워드
            "성희롱 피해자",
            "성희롱 가해자",
            "성희롱 2차피해",
            "성희롱 신고",
            "성희롱 보복",
            "성적 언동",
            "성희롱 예방",
            "성추행 징계",
            "성희롱 면직",
            "성희롱 파면",
            "성희롱 인사조치",
            "성희롱 행위자 징계",
            "성희롱 손해 배상",
            "성희롱 불이익",
            "성희롱 위자료",
            "직장 성희롱 손해배상",
            "성희롱 해고 정당",
            "성희롱 징계 취소",
            "성적 괴롭힘",
            "성희롱 인정 판결",
            "성희롱 사건 해고",
            "성추행 해고",
            "직장 성추행 징계",
        ],
        "types": ["행정", "민사", "형사"],
    },
    "violence": {
        "keywords": [
            # 기존 키워드
            "폭행 해고",
            "폭언 징계",
            "직장내 폭행",
            "폭행 부당해고",
            "폭언 해고 정당",
            "상습폭행 징계",
            "직장내 폭력 해고",
            # 확장 키워드
            "상해 해고",
            "협박 징계",
            "물리적 폭력 해고",
            "욕설 징계",
            "위협 해고",
            "가혹행위 징계",
            "신체적 폭력",
            "직장 폭력 부당해고",
            "상사 폭행 징계",
            "직장내 폭력 징계",
            "폭력 해고 정당",
            "폭행 면직",
            "폭언 폭행 해고",
            "직원 폭행 해고",
            "상습 폭언 징계",
            "폭행 징계 취소",
            "직장 폭언 손해배상",
            "신체적 위해 해고",
            "동료 폭행 해고",
            "폭력 징계 정당",
        ],
        "types": ["행정", "민사", "형사"],
    },
    "embezzlement": {
        "keywords": [
            # 기존 키워드
            "횡령 해고",
            "배임 해고",
            "횡령 징계해고",
            "업무상 횡령 해고 정당",
            "배임 부당해고",
            "횡령 비위 징계",
            "금품횡령 해고",
            # 확장 키워드
            "공금횡령",
            "배임수재",
            "사기 해고",
            "횡령 면직",
            "업무상배임 해고",
            "자금유용",
            "회사재산 유용",
            "금품 착복 해고",
            "비자금 징계",
            "공금 유용 해고",
            "업무상 배임 징계",
            "횡령 징계 취소",
            "횡령 파면",
            "배임 징계",
            "재산 횡령 해고",
            "공금 횡령 면직",
            "금전 착복 징계",
            "회사 자금 횡령",
            "업무상 배임 해고 정당",
            "횡령죄 해고",
        ],
        "types": ["행정", "민사", "형사"],
    },
    "misconduct": {
        "keywords": [
            # 기존 키워드
            "비위행위 해고",
            "비위 징계",
            "품위손상 해고",
            "비위 부당해고",
            "복무규정 위반 해고",
            "비위 면직",
            "겸직 징계",
            "음주 징계",
            # 확장 키워드
            "무면허운전 징계",
            "허위보고 해고",
            "직무태만 해고",
            "사생활 비위",
            "성실의무 위반",
            "근무지 이탈",
            "복무위반 징계",
            "질서문란 해고",
            "품위손상 징계",
            "겸직금지 위반",
            "음주운전 징계",
            "금지행위 위반 해고",
            "비위행위 면직",
            "직무 소홀 해고",
            "복무규정 위반 징계",
            "비위 파면",
            "징계사유 비위",
            "직원 비위행위",
            "품위 훼손 해고",
            "성실의무 위반 해고",
        ],
        "types": ["행정", "민사"],
    },
    "redundancy": {
        "keywords": [
            # 기존 키워드
            "경영상해고",
            "정리해고",
            "긴박한 경영상 필요",
            "정리해고 부당",
            "경영해고 절차",
            "해고회피노력",
            "정리해고 취소",
            "구조조정 해고",
            # 확장 키워드
            "해고기준 공정성",
            "정리해고 절차",
            "경영악화 해고",
            "인원감축",
            "사업폐지 해고",
            "통폐합 해고",
            "희망퇴직",
            "경영상 이유 해고",
            "잉여인력 해고",
            "경영상 해고 요건",
            "정리해고 요건",
            "경영위기 해고",
            "사업 축소 해고",
            "구조조정 부당해고",
            "정리해고 해고회피",
            "경영상 필요 해고",
            "인원 감축 해고",
            "사업장 폐쇄 해고",
            "경영 악화 해고 부당",
        ],
        "types": ["행정", "민사"],
    },
    "transfer": {
        "keywords": [
            # 기존 키워드
            "부당전보",
            "전보 인사이동 부당",
            "전직 부당",
            "배치전환 부당",
            "인사이동 부당해고",
            "전보명령 취소",
            "부당전직 인사이동",
            # 확장 키워드
            "좌천 인사",
            "보복전보",
            "직위해제",
            "대기발령",
            "직무배제",
            "직위변경",
            "부당배치전환",
            "보직변경 부당",
            "전보명령 무효",
            "인사발령 부당",
            "직위 강등",
            "좌천성 인사",
            "전보 취소",
            "보복성 전보",
            "전보명령 취소 소송",
            "인사이동 취소",
            "강제전보 부당",
            "전직명령 취소",
            "배치전환 취소",
            "인사발령 무효",
        ],
        "types": ["행정", "민사"],
    },
    "contract_expiry": {
        "keywords": [
            # 기존 키워드
            "갱신기대권",
            "계약만료 해고",
            "기간제 갱신기대권",
            "계약직 갱신거절",
            "기간만료 부당해고",
            "갱신기대권 인정",
            "반복갱신 해고",
            "계약해지 부당",
            # 확장 키워드
            "기간제법",
            "무기계약 전환",
            "2년 초과 기간제",
            "갱신거절 부당",
            "정규직 전환거부",
            "계약종료 부당",
            "기간제 차별",
            "계약만료 부당해고",
            "갱신기대권 침해",
            "기간제 갱신 거절",
            "반복 갱신 기대권",
            "계약직 기간 만료",
            "무기계약직 전환",
            "갱신기대권 판결",
            "기간제 부당해고",
            "계약 갱신 거절 부당",
            "기간제근로자 갱신",
            "계약직 부당해고",
            "기간제 계약 만료",
        ],
        "types": ["행정", "민사"],
    },
    "no_dismissal": {
        "keywords": [
            # 기존 키워드
            "해고부존재",
            "권고사직 부당",
            "사직 강요",
            "사직서 무효",
            "자발적 사직 여부",
            "사직 의사표시 하자",
            "사직 강요 부당해고",
            "합의해지 무효",
            # 확장 키워드
            "퇴직강요",
            "자진퇴사 여부",
            "사직 취소",
            "의원면직 강요",
            "당연퇴직 부당",
            "명예퇴직 강요",
            "사직서 강요",
            "권고사직 부당해고",
            "사직 강요 취소",
            "강압적 사직",
            "해고 아닌 사직",
            "합의해지 강요",
            "퇴직 강요 손해배상",
            "사직서 제출 강요",
            "자발 사직 인정",
            "의사에 반한 사직",
            "해고 부존재 확인",
            "사직 의사 무효",
            "강요 퇴직 부당해고",
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
    """기존 수집된 사건번호 세트 로드 (전체 파일)"""
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
    """카테고리 확장 수집"""
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
    cat_existing_keys = set()
    if detail_path.exists():
        for line in detail_path.read_text(encoding="utf-8").strip().split("\n"):
            if line:
                try:
                    r = json.loads(line)
                    cat_existing.append(r)
                    cat_existing_keys.add(f"{r['court']}_{r['case_number']}")
                except:
                    pass

    print(f"  현재 상세 수집: {len(cat_existing)}건")

    if len(cat_existing) >= target:
        print(f"  목표 달성! 스킵")
        return cat_existing

    # 상세 조회할 건 목록 (전체 미수집 + 이 카테고리 미수집)
    pending = []
    for key, item in search_items.items():
        if key not in cat_existing_keys:
            pending.append(item)

    # 키워드 수 많은 것 우선 (관련성 높음)
    pending.sort(key=lambda x: -len(x.get("keywords", [])))

    need = target - len(cat_existing)
    print(f"  상세 조회 대상: {len(pending)}건 (필요: {need}건)")

    fetched = []
    errors = 0
    skipped_dup = 0

    for i, item in enumerate(pending):
        if len(fetched) + len(cat_existing) >= target:
            print(f"\n  목표 {target}건 달성!")
            break

        court = item.get("court", "")
        case_number = item.get("case_number", "")
        key = f"{court}_{case_number}"

        # 다른 카테고리에 이미 있더라도 이 카테고리에는 추가 (카테고리별 중복 허용)
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

    # 카테고리 파일에 추가 (append — 기존 데이터 보존)
    all_cat_records = cat_existing + fetched
    with open(detail_path, "w", encoding="utf-8") as f:
        for r in all_cat_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n  수집 완료: +{len(fetched)}건 (에러 {errors}건) → 합계 {len(all_cat_records)}건")
    return all_cat_records


def merge_all_details():
    """카테고리별 파일을 all_details.jsonl로 병합 (Q* + 신규 카테고리)"""
    all_records = {}
    cat_counts = defaultdict(int)

    for f in sorted(OUTPUT_DIR.glob("*_details.jsonl")):
        # skip the merged output file itself
        if f.stem == "all_details":
            continue
        cat = f.stem.replace("_details", "")
        count_before = len(all_records)
        for line in f.read_text(encoding="utf-8").strip().split("\n"):
            if line:
                try:
                    d = json.loads(line)
                    # 카테고리 정보 설정
                    if "category" not in d or not d["category"]:
                        d["category"] = cat
                    # 카테고리별로 고유 키 (같은 사건번호가 여러 카테고리에 있을 수 있음)
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


def print_summary():
    """수집 현황 요약 출력"""
    print(f"\n{'='*60}")
    print("신규 카테고리 수집 현황")
    print(f"{'='*60}")
    total = 0
    for cat_key in CATEGORIES:
        detail_path = OUTPUT_DIR / f"{cat_key}_details.jsonl"
        count = 0
        if detail_path.exists():
            for line in detail_path.read_text(encoding="utf-8").strip().split("\n"):
                if line:
                    try:
                        json.loads(line)
                        count += 1
                    except:
                        pass
        print(f"  {cat_key}: {count}건")
        total += count
    print(f"{'='*60}")
    print(f"  합계: {total}건")
    return total


def main():
    parser = argparse.ArgumentParser(description="BigCase 신규 카테고리 확장 수집 (목표: 2000건/카테고리)")
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

    # 기존 수집 현황 (전체 파일 기준)
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

    # 수집 현황 요약
    if args.mode != "search":
        print_summary()

        # 전체 병합 (Q* + 신규 카테고리)
        print(f"\n전체 파일 병합 중...")
        total = merge_all_details()
        print(f"\n수집 완료! 전체: {total}건")


if __name__ == "__main__":
    main()
