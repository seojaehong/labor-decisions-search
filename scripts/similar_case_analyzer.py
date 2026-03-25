"""유사 사례 비교 + 승패 요인 분석

사용자 입력 → 유사 사건 매칭 → 이긴 사건 vs 진 사건 비교 → 체크리스트

Usage:
    python scripts/similar_case_analyzer.py "직원이 3일간 무단결근했습니다"
    python scripts/similar_case_analyzer.py --interactive
"""
import sys
import os
import json
import re
import argparse
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

BIGCASE_DIR = Path(r"C:\dev\labor-decisions-search\evaluation\bigcase_bulk")
MERGED_PATH = Path(r"C:\dev\labor-decisions-search\retagging\output\merged\merged_42k_v1.jsonl")

# 승패 요인 키워드
FACTOR_KEYWORDS = {
    'written_notice': ['서면통지', '서면으로 통지', '서면 통보'],
    'hearing_opportunity': ['소명기회', '소명 기회', '변명의 기회', '의견 진술'],
    'disciplinary_committee': ['인사위원회', '징계위원회', '심의위원회'],
    'proportionality': ['양정', '비례', '사회통념', '과하다', '과도하다', '과중'],
    'work_rules': ['취업규칙', '근로계약', '단체협약', '인사규정'],
    'prior_warning': ['경고', '시정요구', '개선기회', '주의'],
    'tenure': ['근속연수', '재직기간', '근무기간'],
    'remorse': ['반성', '개선 의사', '사과', '시정'],
    'fairness': ['형평', '비교', '동일 사유', '다른 직원'],
    'procedural_defect': ['절차 위반', '절차 하자', '절차적 하자', '절차상 하자'],
    'evidence': ['입증', '증거', '증명', '소명'],
}

FACTOR_LABELS = {
    'written_notice': '서면통지',
    'hearing_opportunity': '소명기회 부여',
    'disciplinary_committee': '인사위원회/징계위원회',
    'proportionality': '징계양정 비례성',
    'work_rules': '취업규칙/규정 근거',
    'prior_warning': '사전 경고/개선기회',
    'tenure': '근속연수 고려',
    'remorse': '반성/개선 의사',
    'fairness': '형평성 비교',
    'procedural_defect': '절차 위반/하자',
    'evidence': '입증/증거',
}


def load_bigcase_records():
    """빅케이스 판례 로드"""
    records = []
    for f in BIGCASE_DIR.glob("Q*_details.jsonl"):
        with open(f, 'r', encoding='utf-8') as fh:
            for line in fh:
                try:
                    records.append(json.loads(line))
                except:
                    pass
    return records


def extract_facts(summary):
    """summary에서 사실관계 추출"""
    lines = summary.split('\n')
    in_facts = False
    facts = []
    for line in lines:
        if '사실관계' in line or '기초사실' in line:
            in_facts = True
            continue
        if in_facts and any(k in line for k in ['핵심 쟁점', '법원의 판단', '결과 요약', '관련 판례', '## 결론']):
            break
        if in_facts and line.strip():
            facts.append(line)
    return '\n'.join(facts).strip()


def get_label(summary):
    """판결 결과 라벨"""
    text = summary[:500]
    if any(k in text for k in ['기각', '원고의 청구를 기각', '항소를 기각', '상고를 기각']):
        return 'dismissed'
    if any(k in text for k in ['원고 승소', '취소', '파기환송', '인용', '부당하다고 판단']):
        return 'granted'
    if '정당' in text:
        return 'dismissed'
    if '부당' in text:
        return 'granted'
    return 'unknown'


def extract_factors(text):
    """텍스트에서 승패 요인 추출"""
    found = {}
    for factor_key, keywords in FACTOR_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                # 긍정/부정 판단
                idx = text.find(kw)
                context = text[max(0, idx-30):idx+len(kw)+30]
                negative = any(neg in context for neg in ['않', '없', '미', '불', '위반', '하자', '결여'])
                found[factor_key] = not negative
                break
    return found


def compute_similarity(query, facts_text):
    """간단한 키워드 유사도"""
    query_tokens = set(re.findall(r'[가-힣]{2,}', query))
    facts_tokens = set(re.findall(r'[가-힣]{2,}', facts_text))
    if not query_tokens:
        return 0
    overlap = query_tokens & facts_tokens
    return len(overlap) / len(query_tokens)


def analyze(query, records, top_n=10):
    """유사 사례 분석"""
    # 유사도 계산
    scored = []
    for r in records:
        summary = r.get('summary', '')
        facts = extract_facts(summary)
        if len(facts) < 50:
            continue

        sim = compute_similarity(query, facts + summary)
        label = get_label(summary)
        factors = extract_factors(summary)

        scored.append({
            'record': r,
            'similarity': sim,
            'label': label,
            'factors': factors,
            'facts': facts,
        })

    scored.sort(key=lambda x: -x['similarity'])
    top = scored[:top_n]

    # 승패 분리
    wins = [s for s in top if s['label'] == 'granted']
    losses = [s for s in top if s['label'] == 'dismissed']

    # 요인 비교
    win_factors = Counter()
    lose_factors = Counter()
    for s in wins:
        for k, v in s['factors'].items():
            win_factors[f"{FACTOR_LABELS[k]}={'있음' if v else '없음'}"] += 1
    for s in losses:
        for k, v in s['factors'].items():
            lose_factors[f"{FACTOR_LABELS[k]}={'있음' if v else '없음'}"] += 1

    return {
        'query': query,
        'total_matched': len(scored),
        'top_n': len(top),
        'wins': wins,
        'losses': losses,
        'win_factors': win_factors,
        'lose_factors': lose_factors,
    }


def print_report(result):
    """분석 결과 출력"""
    print(f"\n{'='*60}")
    print(f"유사 사례 분석: {result['query']}")
    print(f"{'='*60}")
    print(f"매칭: {result['total_matched']}건 중 상위 {result['top_n']}건")
    print(f"인용(근로자 승): {len(result['wins'])}건")
    print(f"기각(사용자 승): {len(result['losses'])}건")

    if result['wins']:
        print(f"\n--- 근로자가 이긴 사건 ---")
        for i, s in enumerate(result['wins'][:3]):
            r = s['record']
            print(f"  [{i+1}] {r.get('court','')} {r.get('case_number','')}")
            print(f"      {s['facts'][:120]}...")
            print(f"      요인: {', '.join(FACTOR_LABELS[k] + '=' + ('O' if v else 'X') for k,v in s['factors'].items())}")

    if result['losses']:
        print(f"\n--- 사용자가 이긴 사건 ---")
        for i, s in enumerate(result['losses'][:3]):
            r = s['record']
            print(f"  [{i+1}] {r.get('court','')} {r.get('case_number','')}")
            print(f"      {s['facts'][:120]}...")
            print(f"      요인: {', '.join(FACTOR_LABELS[k] + '=' + ('O' if v else 'X') for k,v in s['factors'].items())}")

    # 체크리스트
    print(f"\n--- 체크리스트 ---")
    all_factors = set(list(result['win_factors'].keys()) + list(result['lose_factors'].keys()))
    for factor in sorted(all_factors):
        w = result['win_factors'].get(factor, 0)
        l = result['lose_factors'].get(factor, 0)
        if w > 0 or l > 0:
            direction = "→ 인용 경향" if '없음' in factor and w > l else "→ 기각 경향" if '있음' in factor and l > w else ""
            print(f"  {factor}: 인용{w}건 / 기각{l}건 {direction}")


def main():
    parser = argparse.ArgumentParser(description='유사 사례 비교 분석')
    parser.add_argument('query', nargs='?', help='상황 설명')
    parser.add_argument('--interactive', action='store_true')
    parser.add_argument('--top-n', type=int, default=10)
    args = parser.parse_args()

    records = load_bigcase_records()
    print(f"판례 DB: {len(records)}건")

    if args.interactive:
        while True:
            query = input("\n상황 설명 (q=종료): ").strip()
            if query.lower() == 'q':
                break
            result = analyze(query, records, args.top_n)
            print_report(result)
    elif args.query:
        result = analyze(args.query, records, args.top_n)
        print_report(result)
    else:
        # 데모
        demos = [
            "직원이 3일간 무단결근 후 해고했습니다",
            "수습기간 중 업무능력 부족으로 본채용을 거부했습니다",
            "직장내 괴롭힘 신고 후 전보 발령을 받았습니다",
        ]
        for q in demos:
            result = analyze(q, records, args.top_n)
            print_report(result)


if __name__ == '__main__':
    main()
