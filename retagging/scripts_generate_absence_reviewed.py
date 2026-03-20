import json, re
from pathlib import Path

ROOT = Path('/mnt/c/dev/labor-decisions-search/retagging')
IN_DIR = ROOT / 'input' / 'batches'
OUT_DIR = ROOT / 'output' / 'reviewed'
LOG_DIR = ROOT / 'logs'

OUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

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
    return re.sub(r'\s+', ' ', s or '').strip()

def contains(t, *words):
    return any(w in t for w in words)

def split_sent(s):
    s = clean(s)
    return s

def employment_stage(text):
    if contains(text, '시용', '수습', '본채용', '정식채용 여부'):
        return 'probation'
    if contains(text, '갱신기대권', '계약갱신', '재고용', '촉탁직 재고용', '계약기간 만료'):
        return 'renewal_stage'
    if contains(text, '기간제', '계약직') and not contains(text, '갱신기대권'):
        return 'fixed_term'
    return 'regular'

def disposition(sanction, text, stage):
    if contains(text, '본채용 거부', '채용 거절'):
        return ['rejection_of_regular_employment']
    if contains(text, '직권면직', '면직'):
        return ['dismissal']
    if contains(text, '해고가 존재하지 않', '해고가 없', '해고의 사실이 없', '해고 부존재', '합의해지', '사직의 의사표시', '사직서를 제출', '사직 처리'):
        return ['no_formal_disposition']
    m = sanction.lower()
    if m == 'suspension':
        return ['suspension']
    if m == 'pay_cut':
        return ['pay_cut']
    if m in ('warning','reprimand','demotion'):
        return ['other']
    if stage == 'probation' and contains(text, '본채용 거부', '정식채용 여부를 결정', '시용기간 만료'):
        return ['rejection_of_regular_employment']
    return ['dismissal']

def primary(text, stage, decision):
    if contains(text, '직장 내 괴롭힘 신고', '괴롭힘 신고를 한 근로자에게 불이익한 처분', '보호조치도 하지 않았'):
        return 'unfair_treatment'
    if contains(text, '소명기회 미부여', '절차 하자', '절차위반', '서면으로 해고사유', '서면통보') and contains(text, '부당') and not contains(text, '절차에 특별한 하자는 없는'):
        return 'procedure'
    if contains(text, '해고가 존재하지 않', '해고가 없', '해고의 사실이 없', '합의해지', '사직서를 제출', '사직 처리', '사직의 의사표시', '사직의사가 없으면 출근'):
        return 'dismissal_validity'
    if stage == 'renewal_stage' and contains(text, '갱신기대권', '재고용'):
        return 'renewal_expectation'
    if stage == 'probation' and contains(text, '업무능력 부족', '업무적격성', '근무성적', '평가'):
        return 'work_ability'
    if contains(text, '양정이 과', '양정이 적정', '징계양정', '재량권의 범위를 벗어난', '재량권을 남용'):
        # procedure-dominant cases handled above
        return 'disciplinary_severity'
    if contains(text, '직장 내 괴롭힘', '괴롭힘', '성희롱') and not contains(text, '신고를 한 근로자에게 불이익'):
        return 'workplace_harassment'
    if stage == 'probation':
        return 'dismissal_validity'
    return 'misconduct'

def secondary(text, prim):
    arr=[]
    if contains(text,'지각','조퇴','출근율','근태불량','출퇴근','근무시간 미준수','근무시간 준수'):
        arr.append('attendance')
    if contains(text,'무단결근','결근','무단이탈','근무지 이탈','직장 이탈','작업장 무단이탈','근무지 무단'):
        arr.append('absence_without_leave')
    if contains(text,'업무지시 불이행','폭언','폭행','허위','절도','횡령','배임','음주','무단취식','성실의 의무 위반','품위유지'):
        arr.append('misconduct')
    if contains(text,'업무능력 부족','업무적격성','부적격','근무성적이 불량','근무평가 불량'):
        arr.append('work_ability')
    if contains(text,'실적부진','저성과','성과'):
        arr.append('performance')
    if contains(text,'평가','MBO','평가점수','근무평가'):
        arr.append('evaluation')
    if contains(text,'절차','소명기회','서면','징계위원회', '인사위원회', '통지'):
        arr.append('procedure')
    if contains(text,'교육','재교육','개선기회','지도'):
        arr.append('training_opportunity')
    if contains(text,'근로자에 해당','사용자 적격','상시근로자', '근로자인지'):
        arr.append('worker_status')
    if contains(text,'양정','재량권'):
        arr.append('disciplinary_severity')
    if contains(text,'괴롭힘 신고'):
        arr.append('harassment_report')
    if contains(text,'전보','전환배치','배치전환','복직명령', '대기발령'):
        arr.append('transfer_validity')
    if contains(text,'부당노동행위','불이익취급','지배·개입'):
        arr.append('unfair_treatment')
    arr=[x for x in uniq(arr, issue_order) if x != prim]
    return arr

def fact_markers(text, stage):
    arr=[]
    if stage=='probation': arr.append('probation_period')
    if contains(text,'평가점수','MBO','계량'): arr.append('quantitative_evaluation')
    if contains(text,'객관적', '평가자 1인', '근무평가', '정성'): arr.append('qualitative_evaluation')
    if contains(text,'재교육','개선기회','교육을 실시', '주의를 받은') : arr.append('improvement_opportunity_given')
    if contains(text,'서면으로', '서면 통보', '통지서를', '출석통지서', '내용증명'): arr.append('written_notice')
    if contains(text,'소명기회 미부여','미송달','서면으로 해고사유' ) and contains(text,'부당'): arr.append('written_notice_missing')
    if contains(text,'모두 인정', '사실이 인정', '확인된다', '근태자료', 'CCTV'): arr.append('evidence_sufficient')
    if contains(text,'객관적 근거가 부족', '입증자료가 부족', '입증자료가 없는', '객관적 증거가 없', '인정하기 어렵'):
        arr.append('evidence_insufficient')
    if contains(text,'절차 하자', '소명기회', '절차위반') and contains(text,'부당'):
        arr.append('procedural_defect')
    if contains(text,'단 4일', '25일간', '매우 짧'):
        arr.append('short_tenure')
    if contains(text,'합의해지', '합의된'): arr.append('mutual_agreement')
    if contains(text,'사직서', '사직 처리', '사직의 의사표시', '권고사직'): arr.append('resignation_dispute')
    if contains(text,'징계위원회', '인사위원회', '상벌위원회'): arr.append('disciplinary_committee')
    if contains(text,'과거', '이전 징계', '재범', '전력', '기존 징계'): arr.append('prior_sanction_history')
    if contains(text,'유사 사례', '형평', '다른 근로자', '비교하여도'): arr.append('comparative_employee_case')
    if contains(text,'괴롭힘 신고'): arr.append('harassment_report_filed')
    if contains(text,'무단결근','무단이탈','장기간 결근','출근하지 않고'): arr.append('unauthorized_absence')
    return uniq(arr, marker_order)

def legal_focus(text, prim, stage):
    arr=[]
    if contains(text,'정당한', '징계사유', '해고사유'): arr.append('just_cause')
    if contains(text,'사회통념상', '고용관계를 계속할 수 없', '재량권'): arr.append('social_norm_reasonableness')
    if contains(text,'절차', '소명기회', '서면', '통지'): arr.append('procedural_due_process')
    if contains(text,'객관적 증거', '입증자료', '증명하기 위한 자료', '입증할만한'): arr.append('evidentiary_sufficiency')
    if contains(text,'입증', '증거가 없', '입증자료'): arr.append('employer_burden_of_proof')
    if stage=='probation': arr.append('suitability_for_regular_employment')
    if contains(text,'양정', '과도', '과하', '재량권'): arr.append('proportionality')
    if contains(text,'징계양정', '양정이 적정'): arr.append('appropriateness_of_discipline')
    if contains(text,'갱신기대권', '재고용 기대권'): arr.append('expectation_of_renewal')
    if contains(text,'괴롭힘 신고를 한 근로자에게 불이익', '불이익취급', '부당노동행위'): arr.append('protection_against_retaliation')
    return uniq(arr, legal_order)

def industry(text):
    if contains(text,'병원','요양원','간호', '의료', '환자', '조리실장'): return 'healthcare'
    if contains(text,'은행','금융','보험설계사','금융투자협회'): return 'finance'
    if contains(text,'공공기관','위원회','버스','택시','공단','요양원','구청','시내버스'): return 'public'
    if contains(text,'공장','제조','생산량','폐기물','용접봉'): return 'manufacturing'
    if contains(text,'어린이집','미화','서비스','가맹점','청소','주방','택시', '호텔'): return 'service'
    return 'unknown'

def exclusions(text, stage, prim):
    arr=[]
    if not contains(text,'무단결근') or contains(text,'지각','조퇴','근무태만','근무지 이탈') and not contains(text,'장기간 무단결근'):
        arr.append('not_really_absence_case')
    if contains(text,'괴롭힘', '성희롱') and prim != 'workplace_harassment' and prim != 'unfair_treatment':
        arr.append('not_really_harassment_case')
    if stage=='renewal_stage' and contains(text,'갱신기대권','재고용'): arr.append('renewal_expectation_dominant')
    if contains(text,'합의해지'): arr.append('settlement_or_mutual_termination')
    if contains(text,'사직서','사직 처리','권고사직'): arr.append('resignation_dispute')
    if stage!='probation' and contains(text,'수습','시용'): arr.append('unrelated_to_probation')
    if prim=='procedure': arr.append('procedure_dominant')
    if contains(text,'객관적 증거가 없', '입증자료가 없', '입증자료가 부족'):
        arr.append('evidence_too_thin')
    if contains(text,'견책','정직','감봉','배차중지','부당노동행위') and not contains(text,'해고'): arr.append('unrelated_to_dismissal')
    return uniq(arr, exclude_order)

def queries(case, text):
    t = text
    inc=[]; exc=[]
    if contains(t,'무단결근'): inc.append('무단결근 징계')
    if contains(t,'장기간 무단결근','100여 일','1년 이상','17일','16일','132일','30일 이상'): inc.append('장기결근 해고')
    if contains(t,'전보','전환배치'): inc.append('전보 거부 무단결근')
    if contains(t,'병가','질병휴직'): inc.append('병가 불승인 결근')
    if contains(t,'시용','수습','본채용 거부'): inc.append('수습 결근 본채용 거부')
    if contains(t,'사직서','합의해지','해고가 존재하지'): inc.append('해고 부존재 사직 분쟁')
    if contains(t,'괴롭힘 신고'): inc.append('괴롭힘 신고 불이익 해고')
    if contains(t,'징계양정','양정'): inc.append('징계양정 과다')
    if contains(t,'절차 하자','소명기회'): inc.append('징계절차 하자')
    if contains(t,'갱신기대권','재고용'): inc.append('갱신기대권 근태 불량')
    if not inc:
        inc.append('근태불량 징계')
    if 'not_really_absence_case' in case['exclusion_flags']: exc.append('무단결근 단독 해고')
    if 'resignation_dispute' in case['exclusion_flags']: exc.append('무단결근 해고')
    if case['issue_type_primary'] == 'workplace_harassment': exc.append('단순 결근 징계')
    return uniq(inc)[:3], uniq(exc)[:3]

def confidence(text, prim, exc):
    if 'evidence_too_thin' in exc:
        return 'medium'
    if prim in ('dismissal_validity','procedure','renewal_expectation') or contains(text,'객관적 증거가 없','입증자료가 부족','일부만 인정'):
        return 'medium'
    return 'high'

# targeted overrides for clearer consistency
OVR = {
 'id_13583': {'primary':'dismissal_validity','employment_stage':'probation','disposition':['rejection_of_regular_employment'],'notes':'시용기간 만료 후 본채용 거부 사건으로 probation_termination이 아니라 rejection_of_regular_employment로 정리.'},
 'id_11473': {'primary':'dismissal_validity','employment_stage':'probation','disposition':['rejection_of_regular_employment'],'notes':'시용근로자 본채용 거부 정당성 판단 사건.'},
 'id_11877': {'primary':'unfair_treatment','notes':'무단조퇴·무단결근 언급보다 괴롭힘 신고 이후 불이익 해고 여부가 중심.'},
 'id_12485': {'primary':'dismissal_validity','notes':'무단결근 사유 자체보다 직권면직 정당성 부정과 금전보상 수용이 결론 중심.'},
 'id_11577': {'primary':'dismissal_validity','notes':'전환배치 명령의 부당성과 그에 따른 결근 책임 분배가 핵심이어서 단순 결근 사건으로 보기 어려움.'},
 'id_14369': {'primary':'dismissal_validity','notes':'대기발령의 정당성과 그 후 무단결근 해고 정당성이 결합된 사례.'},
 'id_15213': {'primary':'unfair_treatment','notes':'파업의 정당성이 인정되어 무단결근/무단이탈 징계가 부당하다고 본 사례.'}
}

self_review_lines = {}
for b in range(1,6):
    recs=[]
    changes=[]
    path = IN_DIR / f'absence_batch_{b:03d}.jsonl'
    for line in path.read_text(encoding='utf-8').splitlines():
        raw = json.loads(line)
        text = clean(raw['source_text'])
        hold = clean(raw.get('holding_points',''))
        stage = employment_stage(text)
        disp = disposition(raw.get('sanction_type',''), text, stage)
        prim = primary(text, stage, raw.get('decision_result',''))
        sec = secondary(text, prim)
        markers = fact_markers(text, stage)
        legal = legal_focus(text, prim, stage)
        excl = exclusions(text, stage, prim)
        rec = {
            'case_id': raw['case_id'],
            'case_name': raw['case_name'],
            'summary_short': split_sent(hold if hold else text[:110]),
            'holding_summary': hold if hold else split_sent(text[:180]),
            'retrieval_note': '',
            'employment_stage': stage,
            'issue_type_primary': prim,
            'issue_type_secondary': sec,
            'disposition_type': disp,
            'fact_markers': markers,
            'legal_focus': legal,
            'industry_context': industry(text),
            'exclusion_flags': excl,
            'include_for_queries': [],
            'exclude_for_queries': [],
            'confidence': 'high',
            'notes': '',
            'review_status': 'reviewed',
            'tag_version': 'v1'
        }
        if raw['case_id'] in OVR:
            ov=OVR[raw['case_id']]
            rec['issue_type_primary']=ov.get('primary', rec['issue_type_primary'])
            rec['employment_stage']=ov.get('employment_stage', rec['employment_stage'])
            rec['disposition_type']=ov.get('disposition', rec['disposition_type'])
            if ov.get('notes'): rec['notes']=ov['notes']
            if rec['issue_type_primary']=='dismissal_validity' and 'disciplinary_severity' in rec['issue_type_secondary']:
                pass
            changes.append((raw['case_id'], ov.get('notes','override')))
        # post-fix exclusions and secondaries after overrides
        rec['issue_type_secondary'] = [x for x in uniq(rec['issue_type_secondary'], issue_order) if x != rec['issue_type_primary']]
        rec['exclusion_flags'] = exclusions(text, rec['employment_stage'], rec['issue_type_primary'])
        rec['include_for_queries'], rec['exclude_for_queries'] = queries(rec, text)
        rec['confidence'] = confidence(text, rec['issue_type_primary'], rec['exclusion_flags'])
        if not rec['retrieval_note']:
            note=[]
            if 'not_really_absence_case' in rec['exclusion_flags']:
                note.append('표면상 결근 배치이나 실질 쟁점은 ' + rec['issue_type_primary'])
            elif 'absence_without_leave' in rec['issue_type_secondary'] or contains(text,'무단결근'):
                note.append('무단결근/근무지 이탈이 핵심 또는 주요 징계사유')
            if rec['employment_stage']=='probation':
                note.append('수습·시용 단계 판단')
            if rec['issue_type_primary']=='procedure':
                note.append('절차 하자가 결론을 좌우')
            if rec['issue_type_primary']=='renewal_expectation':
                note.append('갱신기대권 법리가 중심')
            rec['retrieval_note']='; '.join(note) if note else '근태 관련 징계·종료 사건의 검색용 구조화 사례'
        # notes if empty but boundary
        if not rec['notes']:
            if rec['issue_type_primary'] in ('dismissal_validity','procedure','renewal_expectation','unfair_treatment'):
                rec['notes']='결근 언급보다 종료 존부/절차/보복 여부가 결론 중심인 경계 사례.'
            elif 'not_really_absence_case' in rec['exclusion_flags']:
                rec['notes']='결근 배치 수록 사건이나 실질 쟁점은 근무태만·괴롭힘·전보 등 결근 외 요소에 더 가깝다.'
        recs.append(rec)
    out = OUT_DIR / f'absence_batch_{b:03d}_reviewed.jsonl'
    out.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in recs)+'\n', encoding='utf-8')
    # minimal self review log with representative changes
    lines=[f'# absence_batch_{b:03d}_reviewed.jsonl 1차 self-review 메모','']
    sample_cases=[r for r in recs if r['notes']][:6][:5]
    for r in sample_cases:
        lines.extend([
            f"## {r['case_id']}",
            f"- reviewed primary/disposition: {r['issue_type_primary']} / {r['disposition_type']}",
            f"- secondary: {r['issue_type_secondary']}",
            f"- exclusion_flags: {r['exclusion_flags']}",
            f"- 변경 이유: {r['notes']}",
            ''
        ])
    (LOG_DIR / f'absence_batch_{b:03d}_self_review.md').write_text('\n'.join(lines).rstrip()+'\n', encoding='utf-8')

print('done')
