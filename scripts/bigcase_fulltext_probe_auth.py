"""BigCase 전문 수집 가능성 프로브 — 인증(로그인) 포함 버전

기존 probe 스크립트가 비인증 상태로 돌아서 member_only 오류가 대부분이었음.
이 스크립트는 BigCaseClient로 먼저 로그인한 뒤 동일한 프로브를 수행.

Usage:
    # 이메일/비밀번호로 자동 로그인
    python scripts/bigcase_fulltext_probe_auth.py --email you@example.com --password yourpw

    # 브라우저 수동 로그인 (창 띄워서 직접 로그인)
    python scripts/bigcase_fulltext_probe_auth.py --manual-login

    # 이미 chrome_profile_bigcase에 세션 있으면 그냥 실행
    python scripts/bigcase_fulltext_probe_auth.py

    # 프로브 대상 건수 변경 (기본 20)
    python scripts/bigcase_fulltext_probe_auth.py --limit 50
"""
import sys
import os
import json
import argparse
import time
import re
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# legal-automation 경로 자동 탐색
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent

# 로컬 Windows 경로와 서버 경로 모두 지원
LEGAL_AUTO_CANDIDATES = [
    Path(r"C:\dev\neuro-coach\legal-automation"),
    Path.home() / "legal-automation",
    Path.home() / "dev" / "legal-automation",
]

legal_auto_path = None
for p in LEGAL_AUTO_CANDIDATES:
    if (p / "src" / "bigcase" / "client.py").exists():
        legal_auto_path = p
        break

if legal_auto_path:
    sys.path.insert(0, str(legal_auto_path))
    print(f"✅ legal-automation 경로: {legal_auto_path}")
else:
    print("❌ legal-automation 경로를 찾을 수 없습니다.")
    print("   --legal-auto 옵션으로 직접 지정해주세요.")
    print("   예: --legal-auto C:\\dev\\neuro-coach\\legal-automation")

OUTPUT_DIR = REPO_DIR / "evaluation" / "bigcase_bulk" / "probes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def classify_fulltext(detail, raw_next_data=None) -> dict:
    """수집된 상세 정보의 전문 품질 분류"""
    if not detail:
        return {"status": "no_detail", "member_only": False, "extracted_len": 0, "has_reasoning": False}

    full_text = detail.full_text or ""
    summary = detail.summary or ""
    extracted_len = len(full_text)

    # reasoning 포함 여부 (이유 본문이 있으면 진짜 전문)
    has_reasoning = "[이유]" in full_text and len(full_text) > 1000

    # member_only 감지: "로그인이 필요합니다" 또는 짧은 텍스트
    member_only = extracted_len < 200 and not summary

    if has_reasoning and extracted_len > 2000:
        status = "likely_full"
    elif has_reasoning or extracted_len > 800:
        status = "maybe_full"
    elif summary and len(summary) > 200:
        status = "ai_summary_only"
    elif extracted_len > 0:
        status = "summary_like"
    else:
        status = "empty"

    return {
        "status": status,
        "member_only": member_only,
        "extracted_len": extracted_len,
        "summary_len": len(summary),
        "has_reasoning": has_reasoning,
    }


def run_probe(client, case_ids: list, limit: int) -> list:
    """프로브 실행"""
    results = []

    for i, case_id in enumerate(case_ids[:limit]):
        court = case_id.get("court", "")
        case_number = case_id.get("case_number", "")
        bc_id = case_id.get("id", "")

        print(f"  [{i+1}/{min(len(case_ids), limit)}] {court} {case_number}", end=" ... ")

        try:
            detail = client.get_detail(court=court, case_number=case_number)
            classification = classify_fulltext(detail)

            result = {
                "bc_id": bc_id,
                "court": court,
                "case_number": case_number,
                **classification,
                "ai_summary_preview": (detail.summary or "")[:100] if detail else "",
            }
            results.append(result)
            print(f"{classification['status']} (len={classification['extracted_len']}, reasoning={classification['has_reasoning']})")

        except Exception as e:
            print(f"❌ {e}")
            results.append({
                "bc_id": bc_id,
                "court": court,
                "case_number": case_number,
                "status": "error",
                "error": str(e),
                "extracted_len": 0,
                "has_reasoning": False,
            })

        time.sleep(1.5)

    return results


def get_sample_cases(client, keywords: list, sample_size: int) -> list:
    """프로브용 샘플 판례 검색"""
    seen = {}
    for kw in keywords:
        if len(seen) >= sample_size:
            break
        try:
            result = client.search(query=kw, types=["행정", "민사"], limit=10)
            for item in result.items:
                key = f"{item.court}_{item.case_number}"
                if key not in seen:
                    seen[key] = {"id": key, "court": item.court, "case_number": item.case_number}
            time.sleep(1)
        except Exception as e:
            print(f"  검색 오류 ({kw}): {e}")

    return list(seen.values())[:sample_size]


def main():
    parser = argparse.ArgumentParser(description='BigCase 전문 프로브 (인증 포함)')
    parser.add_argument('--email', help='BigCase 이메일')
    parser.add_argument('--password', help='BigCase 비밀번호')
    parser.add_argument('--manual-login', action='store_true', help='브라우저에서 직접 로그인')
    parser.add_argument('--limit', type=int, default=20, help='프로브 건수 (기본 20)')
    parser.add_argument('--legal-auto', help='legal-automation 경로 직접 지정')
    args = parser.parse_args()

    # 경로 재지정
    if args.legal_auto:
        sys.path.insert(0, args.legal_auto)
        print(f"✅ 지정 경로: {args.legal_auto}")

    try:
        from src.bigcase.client import BigCaseClient
    except ImportError:
        print("\n❌ BigCaseClient를 import할 수 없습니다.")
        print("   --legal-auto 옵션으로 legal-automation 경로를 지정해주세요.")
        return

    # 키워드 샘플 (다양한 카테고리)
    SAMPLE_KEYWORDS = [
        "부당해고 정당성 인정", "징계해고 취소", "해고 부당 노동위",
        "직장내괴롭힘 해고", "무단결근 해고 정당", "수습 본채용거부",
    ]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"bigcase_probe_auth_{timestamp}.jsonl"
    report_path = OUTPUT_DIR / f"bigcase_probe_auth_{timestamp}_report.md"

    print(f"\n{'='*60}")
    print(f"BigCase 전문 프로브 (인증 포함) — {timestamp}")
    print(f"{'='*60}\n")

    # headless=False로 창 띄움 (manual-login 또는 세션 확인용)
    headless = not args.manual_login and not (args.email and args.password)

    with BigCaseClient(headless=headless) as client:

        # 로그인
        print("🔐 로그인 단계...")
        if args.email and args.password:
            success = client.login(email=args.email, password=args.password)
        elif args.manual_login:
            success = client.login()  # 브라우저 창에서 수동 로그인 대기
        else:
            # chrome_profile에 저장된 세션 확인
            success = client.login()

        if not success:
            print("❌ 로그인 실패 — 인증 없이 계속 진행합니다 (결과가 부정확할 수 있음)")
        else:
            print("✅ 로그인 성공!\n")

        # 샘플 판례 수집
        print(f"🔍 샘플 {args.limit}건 검색 중...")
        cases = get_sample_cases(client, SAMPLE_KEYWORDS, args.limit)
        print(f"   → {len(cases)}건 확보\n")

        if not cases:
            print("❌ 샘플 판례를 찾을 수 없습니다.")
            return

        # 프로브 실행
        print(f"📋 전문 수집 가능성 프로브 ({len(cases)}건):")
        print("-" * 60)
        results = run_probe(client, cases, args.limit)

    # 결과 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # 통계
    status_counts = {}
    has_reasoning_count = 0
    total_len = 0

    for r in results:
        status = r.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        if r.get("has_reasoning"):
            has_reasoning_count += 1
        total_len += r.get("extracted_len", 0)

    avg_len = total_len // len(results) if results else 0

    # 리포트 작성
    report_lines = [
        f"# BigCase 전문 프로브 리포트 (인증 포함)",
        f"",
        f"- 일시: {timestamp}",
        f"- 프로브 건수: {len(results)}",
        f"- 로그인: {'성공' if success else '실패/미시도'}",
        f"",
        f"## 상태 분포",
        f"",
    ]
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        report_lines.append(f"- {status}: {count}건")

    report_lines += [
        f"",
        f"## 핵심 지표",
        f"",
        f"- 이유 본문 포함(has_reasoning): {has_reasoning_count}/{len(results)}건",
        f"- 평균 추출 길이: {avg_len:,}자",
        f"",
        f"## 결론",
        f"",
    ]

    likely_or_maybe = status_counts.get("likely_full", 0) + status_counts.get("maybe_full", 0)
    ratio = likely_or_maybe / len(results) * 100 if results else 0

    if ratio >= 70:
        report_lines.append(f"✅ 전문 수집 가능 (likely_full + maybe_full = {ratio:.0f}%)")
        report_lines.append(f"   → 대량 재수집 권장")
    elif ratio >= 30:
        report_lines.append(f"⚠️ 부분 수집 가능 ({ratio:.0f}%)")
        report_lines.append(f"   → maybe_full 이상만 선별 수집 권장")
    else:
        report_lines.append(f"❌ 전문 수집 어려움 ({ratio:.0f}%)")
        report_lines.append(f"   → ai_summary 활용 방향으로 전환 권장")

    report_lines += [
        f"",
        f"## 샘플 결과",
        f"",
    ]
    for r in results[:10]:
        report_lines.append(
            f"- {r.get('court','')} {r.get('case_number','')}: "
            f"{r.get('status','')} (len={r.get('extracted_len',0)}, "
            f"reasoning={r.get('has_reasoning',False)})"
        )

    report_content = "\n".join(report_lines)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\n{'='*60}")
    print(report_content)
    print(f"{'='*60}")
    print(f"\n저장: {output_path}")
    print(f"리포트: {report_path}")


if __name__ == '__main__':
    main()
