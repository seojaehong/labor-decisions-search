#!/usr/bin/env python3
"""BigCase 레코드에 8축 태깅을 수행하는 스크립트.

reason_category + holding_points/summary 기반으로 rule-based 태깅.
AI 태깅 전 단계로, 빠르게 기본 태그를 채움.

Usage:
  export $(cat /home/ubuntu/work-orchestrator/repos/labor-law-guide/supabase/.env | xargs)
  python3 scripts/bigcase_retag.py [--dry-run] [--limit N]
"""

import requests, json, os, sys, re, time

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
DRY_RUN = '--dry-run' in sys.argv
LIMIT = None
for i, arg in enumerate(sys.argv):
    if arg == '--limit' and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])

headers_read = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
headers_write = {
    'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json', 'Prefer': 'return=minimal'
}

# reason_category → issue_type_primary 매핑
REASON_TO_PRIMARY = {
    'absence': 'absence_without_leave',
    'embezzlement': 'misconduct',
    'misconduct': 'misconduct',
    'no_dismissal': 'dismissal_validity',
    'redundancy': 'redundancy',
    'sexual_harassment': 'misconduct',
    'transfer': 'transfer_validity',
    'violence': 'disciplinary_severity',
    'workplace_bullying': 'workplace_harassment',
    'probation': 'dismissal_validity',
    'incompetence': 'work_ability',
    'contract_expiry': 'renewal_expectation',
    'union_activity': 'unfair_treatment',
    'discrimination': 'discrimination',
    'worker_status': 'worker_status',
    'other': 'other',
}

# 키워드 → 더 정밀한 primary 매핑
KEYWORD_PRIMARY_OVERRIDES = [
    (re.compile(r'횡령|배임|공금|착복|유용'), 'misconduct'),
    (re.compile(r'성희롱|성추행|성적\s*언동'), 'misconduct'),
    (re.compile(r'폭언|폭행|욕설|폭력|가혹'), 'disciplinary_severity'),
    (re.compile(r'절차.*위반|서면.*통지|소명.*기회'), 'procedure'),
    (re.compile(r'양정|과도|과중|비례'), 'disciplinary_severity'),
    (re.compile(r'갱신.*기대|계약.*만료'), 'renewal_expectation'),
    (re.compile(r'경영.*해고|정리해고|구조조정'), 'redundancy'),
    (re.compile(r'전보|배치.*전환|인사.*발령'), 'transfer_validity'),
    (re.compile(r'근로자.*지위|근로자성'), 'worker_status'),
    (re.compile(r'부당노동행위|노조|지배.*개입'), 'unfair_treatment'),
    (re.compile(r'수습|시용|본채용'), 'dismissal_validity'),
    (re.compile(r'무단결근|결근|근무태만'), 'absence_without_leave'),
    (re.compile(r'업무능력|저성과|성과.*부족'), 'work_ability'),
    (re.compile(r'직장.*내.*괴롭힘|따돌림'), 'workplace_harassment'),
    (re.compile(r'보복|불이익.*처분'), 'retaliation'),
]

# 키워드 → fact_markers
KEYWORD_FACTS = [
    (re.compile(r'서면\s*통지'), 'written_notice'),
    (re.compile(r'서면\s*통지.{0,10}(없|미|부재|하지)'), 'written_notice_missing'),
    (re.compile(r'소명\s*기회|변명.*기회|의견\s*진술'), 'disciplinary_committee'),
    (re.compile(r'인사위원회|징계위원회'), 'disciplinary_committee'),
    (re.compile(r'절차.*하자|절차.*위반'), 'procedural_defect'),
    (re.compile(r'무단결근|무단\s*결근'), 'unauthorized_absence'),
    (re.compile(r'반복.*결근|상습.*결근'), 'repeated_absence'),
    (re.compile(r'증거.*부족|입증.*부족'), 'evidence_insufficient'),
    (re.compile(r'공공기관|공단|공사|재단'), 'public_institution'),
    (re.compile(r'경고|시정.*요구'), 'warning_given'),
    (re.compile(r'개선.*기회|PIP|개선.*기간'), 'improvement_opportunity_given'),
]

# 키워드 → legal_focus
KEYWORD_LEGAL = [
    (re.compile(r'정당.*사유|정당한.*이유'), 'just_cause'),
    (re.compile(r'사회통념|사회.*통념'), 'social_norm_reasonableness'),
    (re.compile(r'비례|양정.*과다|과도.*처분'), 'proportionality'),
    (re.compile(r'절차.*적법|적법.*절차'), 'procedural_due_process'),
    (re.compile(r'증거.*충분|입증.*충분'), 'evidentiary_sufficiency'),
    (re.compile(r'사용자.*입증|입증.*책임'), 'employer_burden_of_proof'),
    (re.compile(r'갱신.*기대'), 'expectation_of_renewal'),
    (re.compile(r'보복.*금지|불이익.*금지'), 'protection_against_retaliation'),
    (re.compile(r'징계.*적정|징계.*상당'), 'appropriateness_of_discipline'),
]

# result → disposition_type
DISPOSITION_MAP = {
    'granted': ['dismissal'],
    'dismissed': ['dismissal'],
    'partial': ['dismissal'],
    'upheld': ['dismissal'],
    'overturned': ['dismissal'],
    'rejected': [],
}

# reason_category → employment_stage 힌트
REASON_STAGE = {
    'probation': 'probation',
    'contract_expiry': 'fixed_term',
}

def tag_record(rec):
    """단일 레코드에 8축 태그 생성"""
    text = ' '.join(filter(None, [
        rec.get('holding_points', ''),
        rec.get('holding_summary', ''),
        rec.get('key_issue', ''),
    ]))
    reasons = rec.get('reason_category', []) or []
    result = rec.get('decision_result', '')

    # 1. issue_type_primary
    primary = 'other'
    # 키워드 기반 (더 정밀)
    for pattern, p in KEYWORD_PRIMARY_OVERRIDES:
        if pattern.search(text):
            primary = p
            break
    # fallback: reason_category 기반
    if primary == 'other' and reasons:
        primary = REASON_TO_PRIMARY.get(reasons[0], 'other')

    # 2. issue_type_secondary
    secondary = set()
    for pattern, p in KEYWORD_PRIMARY_OVERRIDES:
        if pattern.search(text) and p != primary:
            secondary.add(p)
    secondary = list(secondary)[:3]

    # 3. fact_markers
    facts = []
    for pattern, f in KEYWORD_FACTS:
        if pattern.search(text):
            facts.append(f)
    facts = list(set(facts))[:5]

    # 4. legal_focus
    legal = []
    for pattern, l in KEYWORD_LEGAL:
        if pattern.search(text):
            legal.append(l)
    legal = list(set(legal))[:4]

    # 5. disposition_type
    disposition = DISPOSITION_MAP.get(result, ['dismissal'])

    # 6. employment_stage
    stage = 'unknown'
    for r in reasons:
        if r in REASON_STAGE:
            stage = REASON_STAGE[r]
            break
    if re.search(r'정규직|상용직', text):
        stage = 'regular'
    elif re.search(r'수습|시용', text):
        stage = 'probation'
    elif re.search(r'기간제|계약직', text):
        stage = 'fixed_term'

    return {
        'issue_type_primary': primary,
        'issue_type_secondary': secondary,
        'disposition_type': disposition,
        'fact_markers': facts,
        'legal_focus': legal,
        'employment_stage': stage,
        'tag_confidence': 'medium',
        'retag_version': 'bigcase-rule-v1',
    }


def main():
    total = 0
    updated = 0
    offset = 0

    while True:
        if LIMIT and total >= LIMIT:
            break

        r = requests.get(
            f'{SUPABASE_URL}/rest/v1/nlrc_decisions?id=like.bc_*&issue_type_primary=is.null&select=id,holding_points,holding_summary,key_issue,reason_category,decision_result&order=id&limit=500&offset={offset}',
            headers=headers_read, timeout=30
        )
        if r.status_code != 200:
            print(f'Read error: {r.status_code}')
            time.sleep(5)
            continue

        data = r.json()
        if not isinstance(data, list) or not data:
            break

        for rec in data:
            if LIMIT and total >= LIMIT:
                break
            total += 1
            tags = tag_record(rec)

            if DRY_RUN:
                if total <= 5:
                    print(f"{rec['id']}: {tags['issue_type_primary']} | facts={tags['fact_markers']} | legal={tags['legal_focus']}")
                updated += 1
            else:
                try:
                    r2 = requests.patch(
                        f'{SUPABASE_URL}/rest/v1/nlrc_decisions?id=eq.{rec["id"]}',
                        headers=headers_write, json=tags, timeout=10
                    )
                    if r2.status_code in (200, 204):
                        updated += 1
                except:
                    pass

        offset += 500
        if not DRY_RUN:
            print(f'{updated}/{total}...', flush=True)
            time.sleep(0.3)

    print(f'\nDone! Tagged: {updated}/{total}')
    if DRY_RUN:
        print('[DRY RUN]')


if __name__ == '__main__':
    main()
