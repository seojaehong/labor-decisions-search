"""BigCase 수집 판례로 우리 AI에 질문 + 예측 비교

사실관계에서 결론/판단 문구를 제거하고 순수 사실만 전달.

Usage:
    python scripts/bigcase_test_query.py
    python scripts/bigcase_test_query.py --limit 3 --dry-run
"""
import sys
import os
import json
import re
import time
import urllib.request
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

INPUT_DIR = r"C:\dev\labor-decisions-search\evaluation\bigcase_test"
OUTPUT_PATH = r"C:\dev\labor-decisions-search\evaluation\bigcase_test\ai_predictions.jsonl"
API_URL = "http://localhost:3002/api/sanction"

# 결론/판단 문구 — 사실관계에서 제거
CONCLUSION_PATTERNS = [
    r'부당하다[고.]',
    r'정당하다[고.]',
    r'부당해고[에로]',
    r'부당노동행위[에로]',
    r'양정이?\s*과[하다]',
    r'해고[가는]\s*무효',
    r'원고\s*승소',
    r'원고\s*패소',
    r'기각',
    r'인용',
    r'취소',
    r'환송',
    r'판정[했한]',
    r'판단[했한]',
    r'결론적으로',
    r'따라서\s*이\s*사건',
    r'위법[하이]',
    r'적법[하이]',
    r'정당성[이이]\s*인정',
    r'정당성[이이]\s*부정',
    r'사회통념상\s*상당',
    r'재량권\s*[남일]',
]


def sanitize_facts(facts_text):
    """사실관계에서 결론/판단 문구 제거"""
    if not facts_text:
        return ''

    lines = facts_text.split('\n')
    clean_lines = []

    for line in lines:
        # 결론 패턴이 포함된 줄은 제거
        has_conclusion = False
        for pattern in CONCLUSION_PATTERNS:
            if re.search(pattern, line):
                has_conclusion = True
                break

        if not has_conclusion:
            clean_lines.append(line)

    result = '\n'.join(clean_lines).strip()

    # 너무 짧아지면 원본 사용 (결론 제거가 과도한 경우)
    if len(result) < 50 and len(facts_text) > 100:
        return facts_text

    return result


def build_question(record):
    """판례 사실관계에서 AI 질문 생성"""
    facts = sanitize_facts(record.get('facts', ''))
    if not facts:
        # facts가 없으면 ai_summary에서 사실관계 부분만
        facts = sanitize_facts(record.get('ai_summary', ''))
    if not facts or len(facts) < 30:
        return None

    # 질문 형태로 변환
    question = f"""다음 상황에서 해고(또는 징계)가 정당한지 판단해주세요.

{facts}

이 상황에서 근로자가 구제신청을 하면 인용(근로자 승)될 가능성이 높은지, 기각(사용자 승)될 가능성이 높은지 분석해주세요."""

    return question


def query_ai(question):
    """우리 AI에 질문"""
    payload = json.dumps({
        'messages': [{'role': 'user', 'content': question}]
    }).encode('utf-8')

    req = urllib.request.Request(
        API_URL, data=payload,
        headers={'Content-Type': 'application/json'}
    )

    try:
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read().decode('utf-8'))
        return result.get('content', '')
    except Exception as e:
        return f"ERROR: {e}"


def extract_prediction(ai_response):
    """AI 답변에서 예측 방향 추출"""
    text = ai_response.lower()

    # 인용(근로자 승) 신호
    granted_signals = [
        '부당하다', '부당해고', '부당한 해고', '양정이 과하',
        '양정 과다', '인용', '근로자 승', '부당 가능성',
        '부당해고로 판정될 가능성', '해고가 부당',
    ]
    # 기각(사용자 승) 신호
    dismissed_signals = [
        '정당하다', '정당한 해고', '해고 정당', '기각',
        '사용자 승', '정당 가능성', '해고가 정당',
        '징계가 정당',
    ]

    granted_count = sum(1 for s in granted_signals if s in text)
    dismissed_count = sum(1 for s in dismissed_signals if s in text)

    if granted_count > dismissed_count:
        return 'granted'
    elif dismissed_count > granted_count:
        return 'dismissed'
    else:
        return 'unclear'


def interpret_actual_result(result_text):
    """실제 판결에서 근로자 승/패 판단"""
    if not result_text:
        return 'unknown'

    text = result_text.strip()

    # 근로자 승 (해고 취소 = 노동위 인용 = 사용자 패소)
    if any(k in text for k in ['원고승', '1심취소', '파기환송', '원고항소인용', '원고일부승', '원고항소일부인용']):
        return 'granted'

    # 근로자 패 (해고 유지 = 노동위 기각 = 사용자 승소)
    if any(k in text for k in ['원고패', '상고기각', '원고항소기각']):
        return 'dismissed'

    # 벌금 (형사 — 사용자 유죄 = 근로자 승)
    if '벌금' in text:
        return 'granted'

    return 'unknown'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=999)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--category', help='특정 영역만')
    args = parser.parse_args()

    # 수집 데이터 로드
    input_path = os.path.join(INPUT_DIR, 'all_bigcase_test.jsonl')
    with open(input_path, 'r', encoding='utf-8') as f:
        records = [json.loads(l) for l in f]

    if args.category:
        records = [r for r in records if r.get('category') == args.category]

    records = records[:args.limit]
    print(f"테스트 대상: {len(records)}건")

    results = []
    for i, record in enumerate(records):
        cat = record.get('category', '')
        case_num = record.get('case_number', '')
        actual = interpret_actual_result(record.get('result', ''))

        print(f"[{i+1}/{len(records)}] {cat} | {case_num} | 실제: {actual}", end=' ')

        question = build_question(record)
        if not question:
            print("⏭️ 사실관계 부족")
            continue

        if args.dry_run:
            print(f"(dry-run) 질문 {len(question)}자")
            results.append({
                **record,
                'actual_label': actual,
                'question_length': len(question),
                'dry_run': True,
            })
            continue

        # AI 질문
        ai_response = query_ai(question)
        prediction = extract_prediction(ai_response)
        match = '✅' if prediction == actual else '❌' if actual != 'unknown' else '❓'

        print(f"→ 예측: {prediction} {match}")

        results.append({
            'category': cat,
            'case_number': case_num,
            'court': record.get('court', ''),
            'actual_result': record.get('result', ''),
            'actual_label': actual,
            'ai_prediction': prediction,
            'match': prediction == actual if actual != 'unknown' else None,
            'question_length': len(question),
            'ai_response_length': len(ai_response),
            'ai_response_excerpt': ai_response[:300],
        })

        time.sleep(1)

    # 저장
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # 요약
    print(f"\n{'='*60}")
    print(f"테스트 결과 요약")
    print(f"{'='*60}")

    if not args.dry_run:
        total_judged = [r for r in results if r.get('match') is not None]
        correct = sum(1 for r in total_judged if r['match'])
        print(f"전체: {len(results)}건")
        print(f"판정 가능: {len(total_judged)}건")
        print(f"적중: {correct}건 ({correct * 100 // max(len(total_judged), 1)}%)")

        from collections import Counter
        for cat in sorted(set(r['category'] for r in results)):
            cat_results = [r for r in total_judged if r['category'] == cat]
            cat_correct = sum(1 for r in cat_results if r['match'])
            print(f"  {cat}: {cat_correct}/{len(cat_results)}")

    print(f"\n저장: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
