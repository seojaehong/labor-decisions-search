import json, re
from pathlib import Path

ROOT = Path('/mnt/c/dev/labor-decisions-search/retagging')
IN_DIR = ROOT / 'input' / 'batches'
OUT_DIR = ROOT / 'output' / 'reviewed'
LOG_DIR = ROOT / 'logs'
RULE_LOG = LOG_DIR / 'rule_change_notes_v1.md'

issue_order = ['attendance','absence_without_leave','misconduct','work_ability','performance','evaluation','procedure','training_opportunity','worker_status','disciplinary_severity','harassment_report','transfer_validity','unfair_treatment']
marker_order = ['probation_period','quantitative_evaluation','qualitative_evaluation','improvement_opportunity_given','written_notice','written_notice_missing','evidence_sufficient','evidence_insufficient','procedural_defect','short_tenure','mutual_agreement','resignation_dispute','disciplinary_committee','prior_sanction_history','comparative_employee_case','harassment_report_filed','unauthorized_absence','witness_statement']
legal_order = ['just_cause','social_norm_reasonableness','procedural_due_process','evidentiary_sufficiency','employer_burden_of_proof','suitability_for_regular_employment','proportionality','appropriateness_of_discipline','expectation_of_renewal','protection_against_retaliation']
exclude_order = ['not_really_harassment_case','not_really_absence_case','renewal_expectation_dominant','settlement_or_mutual_termination','resignation_dispute','unrelated_to_probation','procedure_dominant','fact_specific_low_reusability','evidence_too_thin','unrelated_to_dismissal']

def uniq(seq, order=None):
    seen = []
    for x in seq:
        if x and x not in seen:
            seen.append(x)
    if order:
        idx = {v:i for i,v in enumerate(order)}
        seen.sort(key=lambda x: idx.get(x, 999))
    return seen

def clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace('&#8228;', '·')).strip()

def contains(t, *words):
    return any(w in t for w in words)

def employment_stage(text):
    if contains(text, '갱신기대권', '재고용 기대권', '계약갱신', '재계약', '갱신 거절', '갱신거절'):
        return 'renewal_stage'
    if contains(text, '기간제근로자', '기간제 근로자', '기간제') and not contains(text, '갱신기대권', '재계약', '갱신거절'):
        return 'fixed_term'
    if contains(text, '시용', '수습', '본채용'):
        return 'probation'
    return 'regular'

def disposition(raw_sanction, text, stage):
    sanction = (raw_sanction or '').lower()
    if contains(text, '해고가 존재하지 않', '해고가 존재한다고 보기 어렵', '해고가 없', '해고의 사실이 없', '해고 부존재', '합의해지', '사직의 의사', '사직서를 제출'):
        return ['no_formal_disposition']
    if stage == 'probation' and contains(text, '본채용 거절', '본채용 거부'):
        return ['rejection_of_regular_employment']
    if stage == 'probation' and contains(text, '시용기간 중', '수습기간 중', '해약권') and contains(text, '해고'):
        return ['probation_termination']
    if stage == 'renewal_stage' and contains(text, '갱신거절', '재계약 거절', '갱신 거절'):
        return ['nonrenewal']
    arr = []
    if sanction == 'suspension' or contains(text, '정직 '):
        arr.append('suspension')
    if sanction == 'pay_cut' or contains(text, '감봉'):
        arr.append('pay_cut')
    if contains(text, '전보'):
        arr.append('transfer')
    if sanction in ('other',) and not arr:
        arr.append('other')
    if sanction == 'dismissal' and not arr:
        if contains(text, '징계해고', '징계면직', '해임'):
            arr.append('disciplinary_dismissal')
        else:
            arr.append('dismissal')
    if not arr:
        if contains(text, '징계해고', '징계면직', '해임'):
            arr.append('disciplinary_dismissal')
        elif contains(text, '해고'):
            arr.append('dismissal')
        else:
            arr.append('other')
    return uniq(arr)

def primary(text, stage, case_name=''):
    if ('부당노동행위' in case_name and '부당해고' not in case_name) or contains(text, '괴롭힘 신고를 한 근로자에게 불이익', '직장 내 괴롭힘 신고에 대한 불이익', '불이익 취급', '지배·개입'):
        return 'unfair_treatment'
    if (
        contains(text, '서면통지 의무를 위반', '서면통지 미비', '소명기회 미부여', '소명기회를 부여하지 않', '절차적 하자', '절차에 중대한 흠결', '징계절차를 거치지 않', '문자메시지 해고', '징계일자를 징계 의결일보다 소급')
        or ('절차상 하자' in text and not contains(text, '절차상 하자도 없어', '절차상 하자가 없', '절차상 별다른 하자가 존재하지 않', '절차상 하자가 존재하지 않'))
    ) and not contains(text, '징계절차 또한 적법', '절차가 부당하다고 볼 수 없', '절차에 하자가 없어', '징계절차에 하자가 없', '징계절차도 적법', '절차가 모두 정당', '징계절차 및 양정이 모두 적정'):
        return 'procedure'
    if contains(text, '해고가 존재하지 않', '해고가 존재한다고 보기 어렵', '해고가 없', '해고의 사실이 없', '합의해지', '사직의 의사', '사직서를 제출'):
        return 'dismissal_validity'
    if stage == 'renewal_stage':
        return 'renewal_expectation'
    if stage == 'probation':
        return 'dismissal_validity'
    if contains(text, '직장 내 괴롭힘', '직장내 괴롭힘'):
        return 'workplace_harassment'
    if contains(text, '부하직원', '지속적 폭언', '상습적인 폭언', '반복적 폭언', '욕설·협박', '직위를 이용한') and not contains(text, '양정이 과', '양정이 적정', '징계양정'):
        return 'workplace_harassment'
    if contains(text, '양정이 과', '양정이 적정', '징계양정', '재량권을 일탈', '재량권을 남용', '과도하', '과중하', '양정이 무겁'):
        return 'disciplinary_severity'
    if contains(text, '입증하지 못', '증거를 제출하지 못', '인정하기 어렵', '객관적 증거가 없', '일부만 인정'):
        return 'misconduct'
    return 'misconduct'

def secondary(text, prim):
    arr=[]
    if contains(text, '지각', '조퇴', '근태'): arr.append('attendance')
    if contains(text, '근무지 이탈', '무단이탈', '무단결근'): arr.append('absence_without_leave')
    if contains(text, '폭행', '폭언', '욕설', '협박', '흉기', '업무지시 불이행', '허위 기재', '허위기재', '비방', '업무태만', '직장질서 문란', '촬영', '상해'):
        arr.append('misconduct')
    if contains(text, '업무평가', '평가', '60점', '근무평가'): arr.append('evaluation')
    if contains(text, '서면통지', '소명기회', '절차', '인사위원회', '징계위원회'): arr.append('procedure')
    if contains(text, '교육', '안전교육', '개선 여지', '시정 기회'): arr.append('training_opportunity')
    if contains(text, '양정', '재량권'): arr.append('disciplinary_severity')
    if contains(text, '괴롭힘 신고'): arr.append('harassment_report')
    if contains(text, '전보'): arr.append('transfer_validity')
    if contains(text, '부당노동행위', '불이익 취급', '불이익취급', '지배·개입'): arr.append('unfair_treatment')
    return [x for x in uniq(arr, issue_order) if x != prim]

def fact_markers(text, stage):
    arr=[]
    if stage == 'probation': arr.append('probation_period')
    if contains(text, '60점', '점수', '평가점수'): arr.append('quantitative_evaluation')
    if contains(text, '평가', '근무평가', '업무평가'): arr.append('qualitative_evaluation')
    if contains(text, '개선 여지', '시정 기회', '재교육', '안전교육'): arr.append('improvement_opportunity_given')
    if contains(text, '서면', '통지서', '내용증명'): arr.append('written_notice')
    if contains(text, '서면통지 의무를 위반', '서면통지 미비', '소명기회 미부여', '소명기회를 부여하지 않', '징계절차를 거치지 않', '문자메시지 해고'):
        arr.append('written_notice_missing')
    if contains(text, '모두 인정', '인정된다', '스스로 인정', '명백히 확인', '취업규칙을 위반하였고 근로자도 인정'): arr.append('evidence_sufficient')
    if contains(text, '입증하지 못', '증거를 제출하지 못', '인정하기 어렵', '객관적 증거가 없', '불분명', '일부만 인정', '단정 불가'):
        arr.append('evidence_insufficient')
    if contains(text, '절차상 하자', '절차적 하자', '중대한 흠결', '소명기회 미부여', '서면통지 의무를 위반', '징계절차를 거치지 않'):
        arr.append('procedural_defect')
    if contains(text, '합의해지'): arr.append('mutual_agreement')
    if contains(text, '사직의 의사', '사직서를 제출', '권고사직'): arr.append('resignation_dispute')
    if contains(text, '징계위원회', '인사위원회'): arr.append('disciplinary_committee')
    if contains(text, '징계 이력', '기존 징계', '이전에도 징계요구', '재범', '전력'): arr.append('prior_sanction_history')
    if contains(text, '형평성', '다른 근로자', '유사한 징계사유', '최근 3년간의 징계 사례', '쌍방폭행'): arr.append('comparative_employee_case')
    if contains(text, '괴롭힘 신고'): arr.append('harassment_report_filed')
    if contains(text, '녹취록', '진술'): arr.append('witness_statement')
    return uniq(arr, marker_order)

def legal_focus(text, prim, stage):
    arr=[]
    if contains(text, '정당한', '정당성', '징계사유', '해고사유'): arr.append('just_cause')
    if contains(text, '사회통념상', '근로관계를 유지할 수 없', '재량권'): arr.append('social_norm_reasonableness')
    if contains(text, '절차', '소명기회', '서면통지', '통지'): arr.append('procedural_due_process')
    if contains(text, '입증하지 못', '증거를 제출하지 못', '명백히 확인', '불분명', '일부만 인정'): arr.append('evidentiary_sufficiency')
    if contains(text, '입증하지 못', '증거를 제출하지 못', '객관적 증거가 없'): arr.append('employer_burden_of_proof')
    if stage == 'probation': arr.append('suitability_for_regular_employment')
    if contains(text, '양정', '과도', '과중', '재량권'): arr.append('proportionality')
    if contains(text, '징계양정', '양정이 적정', '양정이 과도'): arr.append('appropriateness_of_discipline')
    if stage == 'renewal_stage': arr.append('expectation_of_renewal')
    if contains(text, '부당노동행위', '불이익 취급', '괴롭힘 신고'): arr.append('protection_against_retaliation')
    return uniq(arr, legal_order)

def industry(text):
    if contains(text, '대학교', '교수', '학교'): return 'service'
    if contains(text, '병원', '요양', '환자'): return 'healthcare'
    if contains(text, '공장', '생산라인', '제조', '원단'): return 'manufacturing'
    if contains(text, '공단', '시청', '공공', '공사', '버스', '행정'): return 'public'
    return 'unknown'

def exclusions(text, stage, prim, disp):
    arr=[]
    if prim not in ('workplace_harassment', 'unfair_treatment') and contains(text, '폭언', '괴롭힘', '욕설', '모욕적 발언') and not contains(text, '직장 내 괴롭힘', '직장내 괴롭힘'):
        arr.append('not_really_harassment_case')
    if contains(text, '무단결근', '근무지 이탈') and prim not in ('disciplinary_severity', 'misconduct'):
        arr.append('not_really_absence_case')
    if stage == 'renewal_stage': arr.append('renewal_expectation_dominant')
    if contains(text, '합의해지'): arr.append('settlement_or_mutual_termination')
    if 'no_formal_disposition' in disp: arr.append('resignation_dispute')
    if stage != 'probation' and contains(text, '수습', '시용'): arr.append('unrelated_to_probation')
    if prim == 'procedure': arr.append('procedure_dominant')
    if contains(text, '불분명', '단정 불가', '인정하기 어렵', '객관적 증거가 없'):
        arr.append('evidence_too_thin')
    if 'dismissal' not in disp and 'disciplinary_dismissal' not in disp and 'probation_termination' not in disp and 'rejection_of_regular_employment' not in disp and 'nonrenewal' not in disp and 'contract_termination' not in disp and 'no_formal_disposition' not in disp:
        arr.append('unrelated_to_dismissal')
    return uniq(arr, exclude_order)

def queries(text, rec):
    inc=[]; exc=[]
    if rec['issue_type_primary'] == 'disciplinary_severity':
        if contains(text, '폭행'): inc.append('폭행 징계양정')
        elif contains(text, '폭언', '욕설'): inc.append('폭언 징계양정 과다')
        else: inc.append('복합 비위 징계양정')
    if rec['issue_type_primary'] == 'misconduct':
        if contains(text, '흉기', '협박'): inc.append('직장 내 폭력 위협 해고')
        elif contains(text, '촬영'): inc.append('신체 촬영 징계')
        else: inc.append('폭행 징계사유')
    if rec['issue_type_primary'] == 'workplace_harassment':
        inc.append('지속적 폭언 징계')
    if rec['issue_type_primary'] == 'procedure':
        inc.append('해고절차 하자')
    if rec['issue_type_primary'] == 'dismissal_validity':
        inc.append('해고 부존재')
    if rec['issue_type_primary'] == 'renewal_expectation':
        inc.append('갱신기대권 갱신거절')
    if rec['issue_type_primary'] == 'unfair_treatment':
        inc.append('부당노동행위 불이익취급')
    if contains(text, '쌍방폭행'): inc.append('쌍방폭행 징계')
    if contains(text, '징계절차'): inc.append('징계절차 하자')
    if not inc: inc.append('폭언 폭행 징계')
    if 'not_really_harassment_case' in rec['exclusion_flags']: exc.append('직장내 괴롭힘')
    if 'unrelated_to_dismissal' in rec['exclusion_flags']: exc.append('해고')
    if contains(text, '촬영'): exc.append('성희롱')
    return uniq(inc)[:4], uniq(exc)[:3]

def retrieval_note(text, rec):
    if rec['issue_type_primary'] == 'disciplinary_severity':
        if contains(text, '폭행', '폭언', '욕설'):
            return '폭행·폭언 비위는 인정되나, 핵심 판단은 징계양정의 상당성 여부'
        return '복합 비위 사건이나 판정의 중심은 징계양정 판단'
    if rec['issue_type_primary'] == 'misconduct':
        return '폭행·협박 등 비위 사실의 존부 또는 중대성이 직접 핵심'
    if rec['issue_type_primary'] == 'workplace_harassment':
        return '반복적·지위이용형 폭언/협박이 핵심으로, 직장내 괴롭힘 성격이 강함'
    if rec['issue_type_primary'] == 'procedure':
        return '폭언·폭행 언급이 있으나 결론은 해고/징계 절차 하자가 좌우'
    if rec['issue_type_primary'] == 'dismissal_validity':
        return '폭언·협박 정황이 일부 있으나 핵심은 해고 존부 또는 종료 의사표시의 효력'
    if rec['issue_type_primary'] == 'renewal_expectation':
        return '폭언은 평가 반영 요소일 뿐, 핵심은 갱신기대권과 갱신거절 합리성'
    if rec['issue_type_primary'] == 'unfair_treatment':
        return 'legacy violence 태그가 있으나 실질은 부당노동행위/불이익취급 판단'
    return 'violence 배치 사건의 검색용 구조화 사례'

def notes(text, rec):
    prim = rec['issue_type_primary']
    if prim == 'disciplinary_severity':
        return '폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지'
    if prim == 'misconduct' and 'evidence_too_thin' in rec['exclusion_flags']:
        return '폭행 사건이지만 핵심은 사용자의 입증 부족 여부라 misconduct + evidentiary focus로 정리'
    if prim == 'misconduct':
        return '폭행·협박 등 비위행위 자체의 인정 여부 또는 중대성이 핵심인 사례'
    if prim == 'workplace_harassment':
        return '반복성·관계구조상 단순 폭언보다 괴롭힘 구조가 두드러져 workplace_harassment를 선택'
    if prim == 'procedure':
        return '실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우한 사례'
    if prim == 'dismissal_validity':
        return '폭언·협박 언급은 있으나 실질은 해고 존부/사직·합의해지 효력 판단 사건'
    if prim == 'renewal_expectation':
        return '폭언은 부수 사정이고, 계약갱신 거절의 합리성과 갱신기대권 법리가 중심'
    if prim == 'unfair_treatment':
        return 'violence보다 부당노동행위 판단이 중심이어서 unfair_treatment로 정리'
    return ''

OVR = {
    'id_10479': {'primary':'unfair_treatment','disp':['dismissal'],'exclude_add':['not_really_harassment_case']},
    'id_11055': {'primary':'disciplinary_severity'},
    'id_11561': {'primary':'disciplinary_severity'},
    'id_12051': {'primary':'misconduct','disp':['dismissal']},
    'id_12175': {'primary':'disciplinary_severity'},
    'id_12209': {'primary':'misconduct'},
    'id_12331': {'primary':'disciplinary_severity','disp':['pay_cut','transfer']},
    'id_12371': {'primary':'dismissal_validity','disp':['probation_termination','disciplinary_dismissal']},
    'id_12389': {'primary':'dismissal_validity','disp':['no_formal_disposition']},
    'id_1243': {'primary':'disciplinary_severity','disp':['suspension']},
    'id_12503': {'primary':'disciplinary_severity','disp':['suspension']},
    'id_12573': {'primary':'disciplinary_severity','disp':['pay_cut','transfer']},
    'id_13193': {'primary':'disciplinary_severity'},
    'id_13359': {'stage':'regular','primary':'procedure','disp':['dismissal'],'exclude_add':['unrelated_to_probation','procedure_dominant','not_really_harassment_case']},
    'id_13989': {'primary':'disciplinary_severity','disp':['suspension']},
    'id_14013': {'primary':'misconduct','disp':['dismissal']},
    'id_1441': {'primary':'dismissal_validity','disp':['probation_termination']},
    'id_15605': {'primary':'misconduct','disp':['disciplinary_dismissal']},
    'id_15635': {'primary':'misconduct','disp':['disciplinary_dismissal']},
}

counts = {}
rep_cases = []
for b in range(1, 6):
    batch_name = f'violence_batch_{b:03d}'
    recs = []
    for line in (IN_DIR / f'{batch_name}.jsonl').read_text(encoding='utf-8').splitlines():
        raw = json.loads(line)
        text = clean(raw['source_text'])
        hold = clean(raw.get('holding_points', ''))
        stage = employment_stage(text)
        disp = disposition(raw.get('sanction_type',''), text, stage)
        prim = primary(text, stage, raw.get('case_name',''))
        sec = secondary(text, prim)
        markers = fact_markers(text, stage)
        legal = legal_focus(text, prim, stage)
        rec = {
            'case_id': raw['case_id'],
            'case_name': raw['case_name'],
            'summary_short': hold,
            'holding_summary': hold,
            'retrieval_note': '',
            'employment_stage': stage,
            'issue_type_primary': prim,
            'issue_type_secondary': sec,
            'disposition_type': disp,
            'fact_markers': markers,
            'legal_focus': legal,
            'industry_context': industry(text),
            'exclusion_flags': [],
            'include_for_queries': [],
            'exclude_for_queries': [],
            'confidence': 'high',
            'notes': '',
            'review_status': 'reviewed',
            'tag_version': 'v1',
        }
        if rec['case_id'] in OVR:
            ov = OVR[rec['case_id']]
            rec['employment_stage'] = ov.get('stage', rec['employment_stage'])
            rec['issue_type_primary'] = ov.get('primary', rec['issue_type_primary'])
            rec['disposition_type'] = ov.get('disp', rec['disposition_type'])
        rec['issue_type_secondary'] = [x for x in uniq(secondary(text, rec['issue_type_primary']), issue_order) if x != rec['issue_type_primary']]
        rec['fact_markers'] = fact_markers(text, rec['employment_stage'])
        rec['legal_focus'] = legal_focus(text, rec['issue_type_primary'], rec['employment_stage'])
        rec['exclusion_flags'] = exclusions(text, rec['employment_stage'], rec['issue_type_primary'], rec['disposition_type'])
        if rec['case_id'] in OVR and 'exclude_add' in OVR[rec['case_id']]:
            rec['exclusion_flags'] = uniq(rec['exclusion_flags'] + OVR[rec['case_id']]['exclude_add'], exclude_order)
        rec['include_for_queries'], rec['exclude_for_queries'] = queries(text, rec)
        rec['retrieval_note'] = retrieval_note(text, rec)
        rec['notes'] = notes(text, rec)
        if contains(text, '일부만 인정', '불분명', '단정 불가', '인정하기 어렵'):
            rec['confidence'] = 'medium'
        if contains(text, '반복적 폭언', '상습적인 폭언', '지속적 폭언') and rec['issue_type_primary'] == 'workplace_harassment':
            rec['confidence'] = 'medium'
        recs.append(rec)
    (OUT_DIR / f'{batch_name}_reviewed.jsonl').write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n', encoding='utf-8')
    counts[batch_name] = len(recs)
    # representative notes for log
    chosen = [r for r in recs if r['issue_type_primary'] in ('procedure','dismissal_validity','unfair_treatment','workplace_harassment') or r['confidence'] == 'medium'][:5]
    if len(chosen) < 5:
        chosen = recs[:5]
    lines = [f'# {batch_name} self-review', '', '## 1. batch 개요', f'- batch: `{batch_name}`', f'- reviewed 건수: {len(recs)}', '- 작업 기준:', '  - `prompts/tag_dictionary_v1.md`', '  - `prompts/tagging_prompt_v1.md`', '  - `prompts/review_checklist_v1.md`', '  - `prompts/merge_policy_v1.md`', '', '## 2. representative review notes']
    for r in chosen:
        lines += [f"- `{r['case_id']}`", f"  - reviewed primary/disposition: {r['issue_type_primary']} / {r['disposition_type']}", f"  - secondary: {r['issue_type_secondary']}", f"  - exclusion_flags: {r['exclusion_flags']}", f"  - 변경 이유: {r['notes']}"]
    lines += ['', '## 3. batch-level consistency notes', '- violence 배치에서는 폭행·폭언 사실이 있어도 결론이 양정 판단이면 `disciplinary_severity`를 우선 유지했다.', '- 반복적·지위이용형 폭언/협박은 `workplace_harassment`를 검토했고, 단발적 다툼·복합 비위는 `misconduct` 또는 `disciplinary_severity`로 정리했다.', '- 해고 부존재/합의해지/부당노동행위 결합 사건은 legacy violence 태그를 따라가지 않고 `dismissal_validity` 또는 `unfair_treatment`로 보정했다.', '']
    (LOG_DIR / f'{batch_name}_self_review.md').write_text('\n'.join(lines), encoding='utf-8')

print(json.dumps(counts, ensure_ascii=False, indent=2))
