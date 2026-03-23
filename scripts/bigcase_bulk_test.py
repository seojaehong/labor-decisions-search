"""BigCase 400건으로 우리 AI 예측 테스트

사실관계에서 결론 제거 → AI 질문 → 예측 vs 실제 비교

Usage:
    python scripts/bigcase_bulk_test.py
    python scripts/bigcase_bulk_test.py --limit 10 --dry-run
"""
import sys
import os
import json
import re
import time
import urllib.request
import argparse

sys.stdout.reconfigure(encoding='utf-8')

INPUT_PATH = r"C:\dev\labor-decisions-search\evaluation\bigcase_bulk\all_details.jsonl"
OUTPUT_PATH = r"C:\dev\labor-decisions-search\evaluation\bigcase_bulk\ai_test_results.jsonl"
REPORT_PATH = r"C:\dev\labor-decisions-search\evaluation\bigcase_bulk\ai_test_report.md"
API_URL = "http://localhost:3002/api/sanction"

CONCLUSION_PATTERNS = [
    r'결과\s*요약', r'##\s*결과', r'원고.*기각', r'원고.*승',
    r'파기환송', r'항소.*기각', r'상고.*기각',
    r'부당하다[고.]', r'정당하다[고.]', r'위법하다',
    r'원심.*유지', r'원심.*취소', r'판결\s*주문',
]


def extract_facts_only(summary, full_text):
    """summary에서 사실관계만 추출 (결론 제거)"""
    text = summary or full_text or ''
    if not text:
        return ''

    lines = text.split('\n')
    facts_section = False
    facts_lines = []

    for line in lines:
        stripped = line.strip()

        # 사실관계 섹션 시작
        if '사실관계' in stripped or '사실 관계' in stripped:
            facts_section = True
            continue

        # 결론/판단 섹션 → 중단
        if any(k in stripped for k in ['핵심 쟁점', '법원의 판단', '결과 요약', '관련 판례', '관련 법령', '## 결론']):
            if facts_section:
                break

        if facts_section:
            # 결론 문구가 있는 줄 제거
            has_conclusion = any(re.search(p, stripped) for p in CONCLUSION_PATTERNS)
            if not has_conclusion and stripped:
                facts_lines.append(line)

    result = '\n'.join(facts_lines).strip()

    # 사실관계 섹션이 없으면 전체에서 결론 제거
    if len(result) < 50:
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            if any(k in stripped for k in ['결과 요약', '## 결론', '핵심 쟁점', '법원의 판단', '관련 판례']):
                continue
            has_conclusion = any(re.search(p, stripped) for p in CONCLUSION_PATTERNS)
            if not has_conclusion and stripped and not stripped.startswith('#'):
                clean_lines.append(line)
        result = '\n'.join(clean_lines).strip()

    return result[:2000]  # 토큰 제한


def interpret_result(summary):
    """summary에서 실제 판결 결과 추출"""
    if not summary:
        return 'unknown'

    text = summary[:500]

    if any(k in text for k in ['기각', '원고의 청구를 기각', '원고 패소', '항소를 기각', '상고를 기각']):
        return 'dismissed'
    if any(k in text for k in ['원고 승소', '취소', '파기환송', '인용', '원고의 청구를 인용', '부당하다고 판단']):
        return 'granted'
    if '정당' in text and ('인정' in text or '판단' in text):
        return 'dismissed'
    if '부당' in text and ('인정' in text or '판단' in text):
        return 'granted'

    return 'unknown'


def query_ai(question):
    """AI에 질문"""
    payload = json.dumps({
        'messages': [{'role': 'user', 'content': question}]
    }).encode('utf-8')

    req = urllib.request.Request(
        API_URL, data=payload,
        headers={'Content-Type': 'application/json'}
    )

    try:
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read().decode('utf-8'))
        return result.get('content', '')
    except Exception as e:
        return f"ERROR: {e}"


def extract_prediction(ai_response):
    """AI 답변에서 예측 방향 추출"""
    text = ai_response

    granted_signals = ['부당하다', '부당해고', '양정이 과하', '양정 과다',
                       '부당 가능성', '부당해고로 판정될 가능성', '해고가 부당',
                       '인용 가능성이 높', '근로자 승', '부당할 가능성']
    dismissed_signals = ['정당하다', '정당한 해고', '해고 정당', '기각 가능성',
                         '정당 가능성', '해고가 정당', '징계가 정당',
                         '사용자 승', '정당할 가능성']

    g = sum(1 for s in granted_signals if s in text)
    d = sum(1 for s in dismissed_signals if s in text)

    if g > d:
        return 'granted'
    elif d > g:
        return 'dismissed'
    return 'unclear'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=999)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--category', help='특정 영역만')
    args = parser.parse_args()

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        records = [json.loads(l) for l in f]

    if args.category:
        records = [r for r in records if r.get('category') == args.category]
    records = records[:args.limit]

    print(f"테스트: {len(records)}건")

    results = []
    for i, record in enumerate(records):
        cat = record.get('category', '')
        case_num = record.get('case_number', '')
        actual = interpret_result(record.get('summary', ''))

        facts = extract_facts_only(record.get('summary', ''), record.get('full_text', ''))

        print(f"[{i+1}/{len(records)}] {cat} | {case_num} | 실제: {actual}", end=' ')

        if len(facts) < 30:
            print("⏭️ 사실관계 부족")
            continue

        if args.dry_run:
            print(f"(dry-run) {len(facts)}자")
            results.append({
                'category': cat, 'case_number': case_num,
                'actual': actual, 'facts_length': len(facts),
            })
            continue

        question = f"""다음 상황에서 해고(또는 징계)가 정당한지 판단해주세요.

{facts}

이 상황에서 근로자가 구제신청을 하면 인용(근로자 승)될 가능성이 높은지, 기각(사용자 승)될 가능성이 높은지 분석해주세요."""

        ai_response = query_ai(question)
        prediction = extract_prediction(ai_response)
        match = prediction == actual if actual != 'unknown' else None
        icon = '✅' if match else '❌' if match is False else '❓'

        print(f"→ {prediction} {icon}")

        results.append({
            'category': cat, 'case_number': case_num,
            'court': record.get('court', ''),
            'actual': actual, 'prediction': prediction,
            'match': match,
            'facts_length': len(facts),
            'response_excerpt': ai_response[:200],
        })

        time.sleep(1)

    # 저장
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # 리포트
    if not args.dry_run:
        judged = [r for r in results if r.get('match') is not None]
        correct = sum(1 for r in judged if r['match'])
        total = len(judged)

        report = f"""# BigCase 400건 AI 예측 테스트 리포트

- 전체: {len(results)}건
- 판정 가능: {total}건
- 적중: {correct}건 ({correct * 100 // max(total, 1)}%)

## 영역별

| 영역 | 적중 | 전체 | 비율 |
|------|:---:|:---:|:---:|
"""
        from collections import Counter
        for cat in sorted(set(r['category'] for r in results)):
            cat_judged = [r for r in judged if r['category'] == cat]
            cat_correct = sum(1 for r in cat_judged if r['match'])
            report += f"| {cat} | {cat_correct} | {len(cat_judged)} | {cat_correct * 100 // max(len(cat_judged), 1)}% |\n"

        report += f"\n## 예측 분포\n\n"
        pred_dist = Counter(r.get('prediction', '') for r in results)
        for k, v in pred_dist.most_common():
            report += f"- {k}: {v}건\n"

        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n{'='*60}")
        print(f"적중률: {correct}/{total} ({correct * 100 // max(total, 1)}%)")
        print(f"{'='*60}")
        for cat in sorted(set(r['category'] for r in results)):
            cat_judged = [r for r in judged if r['category'] == cat]
            cat_correct = sum(1 for r in cat_judged if r['match'])
            print(f"  {cat}: {cat_correct}/{len(cat_judged)}")

    print(f"\n저장: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
