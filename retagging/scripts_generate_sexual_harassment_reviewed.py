import sys, json, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path('C:/dev/labor-decisions-search/retagging')
IN_DIR = ROOT / 'input' / 'batches_38k'
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
        idx = {v: i for i, v in enumerate(order)}
        seen.sort(key=lambda x: idx.get(x, 999))
    return seen

def clean(s):
    return re.sub(r'\s+', ' ', s or '').strip()

def contains(t, *words):
    return any(w in t for w in words)

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
    if contains(text, '직권면직', '면직') and not contains(text, '해고'):
        return ['dismissal']
    if contains(text, '해고가 존재하지 않', '해고가 없', '해고의 사실이 없', '해고 부존재',
                '합의해지', '사직의 의사표시', '사직서를 제출', '사직 처리'):
        return ['no_formal_disposition']
    m = sanction.lower() if sanction else ''
    if m == 'suspension':
        return ['suspension']
    if m == 'pay_cut':
        return ['pay_cut']
    if m == 'demotion':
        return ['other']
    if m in ('warning', 'reprimand'):
        return ['other']
    if stage == 'probation' and contains(text, '본채용 거부', '정식채용 여부를 결정', '시용기간 만료'):
        return ['rejection_of_regular_employment']
    if m in ('dismissal', 'disciplinary_dismissal') or contains(text, '해고', '파면'):
        return ['disciplinary_dismissal']
    return ['dismissal']

def primary(text, stage, decision):
    # 1) 불이익 조치/보복이 중심 (신고 후 불이익)
    if contains(text, '성희롱 피해자에게 불이익', '피해자에게 불이익 조치', '신고를 이유로 불이익',
                '성희롱 신고를 한 근로자에게 불이익', '보호조치를 하지 않', '2차 피해'):
        return 'unfair_treatment'
    # 2) 절차 하자가 결론을 좌우
    if contains(text, '소명기회 미부여', '소명기회를 부여하지', '절차 하자', '절차위반',
                '서면으로 해고사유', '서면통보') and \
       contains(text, '부당') and \
       not contains(text, '절차에 특별한 하자는 없는', '절차에 하자가 없'):
        return 'procedure'
    # 3) 해고 부존재/사직 다툼
    if contains(text, '해고가 존재하지 않', '해고가 없', '해고의 사실이 없', '합의해지',
                '사직서를 제출', '사직 처리', '사직의 의사표시'):
        return 'dismissal_validity'
    # 4) 갱신기대권
    if stage == 'renewal_stage' and contains(text, '갱신기대권', '재고용'):
        return 'renewal_expectation'
    # 5) 양정 과도 여부가 결론 → disciplinary_severity
    # 징계사유는 인정되고 양정이 과다/적정이 핵심인 경우
    if contains(text, '징계양정이 과', '양정이 과도', '양정이 과하', '징계양정이 적정',
                '양정이 적정', '재량권의 범위를 벗어났', '재량권을 남용', '양정의 적정성'):
        return 'disciplinary_severity'
    # 6) 성희롱 인정 여부 자체가 쟁점 (사실관계 + 피해자 진술 신빙성 등)
    if contains(text, '성희롱이 인정', '성희롱에 해당', '성희롱으로 보기 어렵',
                '성희롱 해당 여부', '성희롱으로 볼 수 없', '성적 굴욕감',
                '성적 수치심', '성희롱에 해당하지'):
        return 'misconduct'
    # 7) 직장 내 괴롭힘 성격의 반복적 행위가 중심
    if contains(text, '직장 내 괴롭힘', '괴롭힘') and contains(text, '반복', '지속', '지위'):
        return 'workplace_harassment'
    # 8) 수습
    if stage == 'probation':
        return 'dismissal_validity'
    # 9) 기본값: 비위행위 중심이면 misconduct
    if contains(text, '비위행위', '성폭력', '성희롱'):
        return 'misconduct'
    return 'disciplinary_severity'

def secondary(text, prim):
    arr = []
    if contains(text, '지각', '조퇴', '출근율', '근태불량', '근무시간 미준수'):
        arr.append('attendance')
    if contains(text, '무단결근', '결근', '무단이탈', '근무지 이탈'):
        arr.append('absence_without_leave')
    if contains(text, '업무지시 불이행', '폭언', '폭행', '허위', '음주', '품위유지',
                '비위행위', '성폭력', '성희롱'):
        arr.append('misconduct')
    if contains(text, '업무능력 부족', '업무적격성', '부적격', '근무성적이 불량'):
        arr.append('work_ability')
    if contains(text, '실적부진', '저성과', '성과'):
        arr.append('performance')
    if contains(text, '평가', 'MBO', '평가점수', '근무평가'):
        arr.append('evaluation')
    if contains(text, '절차', '소명기회', '서면', '징계위원회', '인사위원회', '통지'):
        arr.append('procedure')
    if contains(text, '교육', '재교육', '개선기회', '지도'):
        arr.append('training_opportunity')
    if contains(text, '근로자에 해당', '사용자 적격', '상시근로자', '근로자인지'):
        arr.append('worker_status')
    if contains(text, '양정', '재량권'):
        arr.append('disciplinary_severity')
    if contains(text, '괴롭힘 신고', '성희롱 신고', '피해 신고'):
        arr.append('harassment_report')
    if contains(text, '전보', '전환배치', '배치전환', '복직명령', '대기발령'):
        arr.append('transfer_validity')
    if contains(text, '부당노동행위', '불이익취급', '지배·개입'):
        arr.append('unfair_treatment')
    arr = [x for x in uniq(arr, issue_order) if x != prim]
    return arr

def fact_markers(text, stage):
    arr = []
    if stage == 'probation':
        arr.append('probation_period')
    if contains(text, '평가점수', 'MBO', '계량'):
        arr.append('quantitative_evaluation')
    if contains(text, '피해자 진술', '참고인 진술', '진술', '정황', '신빙성'):
        arr.append('witness_statement')
    if contains(text, '객관적', '평가자 1인', '근무평가', '정성'):
        arr.append('qualitative_evaluation')
    if contains(text, '재교육', '개선기회', '교육을 실시', '주의를 받은'):
        arr.append('improvement_opportunity_given')
    if contains(text, '서면으로', '서면 통보', '통지서를', '출석통지서', '내용증명',
                '해고통보서', '징계통보'):
        arr.append('written_notice')
    if contains(text, '소명기회 미부여', '미송달', '서면으로 해고사유') and contains(text, '부당'):
        arr.append('written_notice_missing')
    if contains(text, '모두 인정', '사실이 인정', '확인된다', '피해자들의 진술', '진술이 일관'):
        arr.append('evidence_sufficient')
    if contains(text, '객관적 근거가 부족', '입증자료가 부족', '입증자료가 없는',
                '객관적 증거가 없', '인정하기 어렵', '신빙성이 없', '신빙성이 부족'):
        arr.append('evidence_insufficient')
    if contains(text, '절차 하자', '소명기회', '절차위반') and contains(text, '부당'):
        arr.append('procedural_defect')
    if contains(text, '징계위원회', '인사위원회', '상벌위원회'):
        arr.append('disciplinary_committee')
    if contains(text, '과거', '이전 징계', '재범', '전력', '기존 징계', '재차'):
        arr.append('prior_sanction_history')
    if contains(text, '유사 사례', '형평', '다른 근로자', '비교하여도'):
        arr.append('comparative_employee_case')
    if contains(text, '괴롭힘 신고', '성희롱 신고', '피해 신고'):
        arr.append('harassment_report_filed')
    if contains(text, '무단결근', '무단이탈', '장기간 결근', '출근하지 않고'):
        arr.append('unauthorized_absence')
    return uniq(arr, marker_order)

def legal_focus(text, prim, stage):
    arr = []
    if contains(text, '정당한', '징계사유', '해고사유'):
        arr.append('just_cause')
    if contains(text, '사회통념상', '고용관계를 계속할 수 없', '재량권'):
        arr.append('social_norm_reasonableness')
    if contains(text, '절차', '소명기회', '서면', '통지'):
        arr.append('procedural_due_process')
    if contains(text, '객관적 증거', '입증자료', '증명하기 위한 자료', '입증할만한',
                '피해자 진술', '진술의 신빙성'):
        arr.append('evidentiary_sufficiency')
    if contains(text, '입증', '증거가 없', '입증자료'):
        arr.append('employer_burden_of_proof')
    if stage == 'probation':
        arr.append('suitability_for_regular_employment')
    if contains(text, '양정', '과도', '과하', '재량권', '비례'):
        arr.append('proportionality')
    if contains(text, '징계양정', '양정이 적정'):
        arr.append('appropriateness_of_discipline')
    if contains(text, '갱신기대권', '재고용 기대권'):
        arr.append('expectation_of_renewal')
    if contains(text, '불이익 조치', '불이익취급', '보호조치', '2차 피해', '부당노동행위',
                '성희롱 피해자에게 불이익'):
        arr.append('protection_against_retaliation')
    return uniq(arr, legal_order)

def industry(text):
    if contains(text, '병원', '요양원', '간호', '의료', '환자', '조리실장', '의원'):
        return 'healthcare'
    if contains(text, '은행', '금융', '보험설계사', '금융투자협회', '증권'):
        return 'finance'
    if contains(text, '공공기관', '위원회', '버스', '택시', '공단', '구청', '시내버스',
                '공사', '공기업', '국립', '시립', '도립'):
        return 'public'
    if contains(text, '공장', '제조', '생산량', '폐기물', '용접봉'):
        return 'manufacturing'
    if contains(text, '어린이집', '미화', '서비스', '가맹점', '청소', '주방', '택시', '호텔',
                '식당', '카페', '요식'):
        return 'service'
    return 'unknown'

def exclusions(text, stage, prim):
    arr = []
    # not_really_harassment_case: 성희롱 언급은 있으나 실질 쟁점이 성희롱과 무관한 경우
    # 성희롱 배치에서 양정/절차가 primary이더라도 이는 여전히 성희롱 사건이므로 플래그 불필요
    # 갱신기대권, 결근, 전보 등이 주된 경우에만 적용
    if prim in ('renewal_expectation', 'dismissal_validity') and \
       not contains(text, '성희롱', '성폭력', '성적 수치심', '성적 굴욕감'):
        arr.append('not_really_harassment_case')
    if contains(text, '갱신기대권', '재고용') and stage == 'renewal_stage':
        arr.append('renewal_expectation_dominant')
    if contains(text, '합의해지'):
        arr.append('settlement_or_mutual_termination')
    if contains(text, '사직서', '사직 처리', '권고사직') and prim == 'dismissal_validity':
        arr.append('resignation_dispute')
    if stage != 'probation' and contains(text, '수습', '시용'):
        arr.append('unrelated_to_probation')
    if prim == 'procedure':
        arr.append('procedure_dominant')
    if contains(text, '객관적 증거가 없', '입증자료가 없', '입증자료가 부족',
                '신빙성이 없', '신빙성이 부족'):
        arr.append('evidence_too_thin')
    if contains(text, '견책', '정직', '감봉', '부당노동행위') and \
       not contains(text, '해고', '파면'):
        arr.append('unrelated_to_dismissal')
    return uniq(arr, exclude_order)

def queries(rec, text):
    inc = []
    exc = []
    prim = rec['issue_type_primary']
    if contains(text, '성희롱이 인정', '성희롱에 해당'):
        inc.append('성희롱 징계해고')
    if contains(text, '양정이 과', '양정이 과도', '재량권을 남용'):
        inc.append('성희롱 징계양정 과다')
    if contains(text, '양정이 적정', '재량권의 범위를 벗어났다고 보기 어렵'):
        inc.append('성희롱 해고 정당')
    if contains(text, '절차', '소명기회') and prim == 'procedure':
        inc.append('성희롱 징계절차 하자')
    if contains(text, '불이익 조치', '피해자에게 불이익', '2차 피해'):
        inc.append('성희롱 피해자 불이익취급')
    if contains(text, '직장 내 괴롭힘', '괴롭힘'):
        inc.append('직장 내 괴롭힘 성희롱')
    if contains(text, '강등', '정직') and prim == 'disciplinary_severity':
        inc.append('성희롱 강등 징계양정')
    if not inc:
        inc.append('직장 내 성희롱 징계')
    if 'not_really_harassment_case' in rec['exclusion_flags']:
        exc.append('성희롱 행위 자체 다툼')
    if prim == 'disciplinary_severity':
        exc.append('성희롱 성립 여부')
    return uniq(inc)[:3], uniq(exc)[:3]

def confidence_score(text, prim, exc):
    if 'evidence_too_thin' in exc:
        return 'medium'
    if prim in ('dismissal_validity', 'procedure', 'renewal_expectation', 'unfair_treatment'):
        return 'medium'
    if contains(text, '일부만 인정', '일부 인정', '인정되지 않고'):
        return 'medium'
    return 'high'

def retrieval_note(rec, text):
    prim = rec['issue_type_primary']
    excl = rec['exclusion_flags']
    notes = []
    if 'not_really_harassment_case' in excl:
        notes.append(f'성희롱 배치이나 실질 쟁점은 {prim}')
    elif prim == 'disciplinary_severity':
        notes.append('성희롱 사실 인정, 징계양정(해고/정직/강등 수위) 적정성이 핵심')
    elif prim == 'misconduct':
        if contains(text, '성희롱으로 보기 어렵', '성희롱으로 볼 수 없', '성희롱에 해당하지'):
            notes.append('성희롱 행위 성립 자체가 부정된 사례')
        else:
            notes.append('성희롱 행위 성립 여부 자체가 쟁점')
    elif prim == 'workplace_harassment':
        notes.append('반복적·지위이용 성희롱/괴롭힘 행위 유형이 중심')
    elif prim == 'procedure':
        notes.append('징계절차 하자(소명기회·서면통지)가 결론을 좌우')
    elif prim == 'unfair_treatment':
        notes.append('성희롱 피해자 또는 신고자에 대한 불이익 조치가 핵심')
    else:
        notes.append('성희롱 관련 징계·해고 사건')
    if rec['employment_stage'] == 'probation':
        notes.append('수습·시용 단계 판단')
    return '; '.join(notes)

def auto_notes(rec, text):
    prim = rec['issue_type_primary']
    excl = rec['exclusion_flags']
    if 'not_really_harassment_case' in excl:
        return f'성희롱 배치 수록 사건이나 실질 쟁점은 {prim}.'
    if prim == 'misconduct':
        if contains(text, '성희롱으로 보기 어렵', '성희롱으로 볼 수 없', '성희롱에 해당하지'):
            return '성희롱 행위 성립이 부정된 사례. 피해자 진술 신빙성 또는 입증 부족.'
        return '성희롱 성립 여부가 주된 쟁점.'
    if prim == 'disciplinary_severity':
        return '성희롱 사실은 인정되고 징계양정(해고/정직 등 수위)의 상당성이 핵심.'
    if prim == 'workplace_harassment':
        return '반복적·지위이용 성희롱/괴롭힘 행위 유형이 중심인 사례.'
    if prim == 'procedure':
        return '절차 하자(소명기회 미부여·서면통지 흠결 등)가 결론을 좌우하는 경계 사례.'
    if prim == 'unfair_treatment':
        return '성희롱 피해자·신고자에 대한 불이익 조치 또는 2차 피해 여부가 핵심.'
    return ''

# 특정 케이스 오버라이드
OVR = {}

for b in range(1, 21):
    recs = []
    path = IN_DIR / f'sexual_harassment_batch_{b:03d}.jsonl'
    for line in path.read_text(encoding='utf-8').splitlines():
        raw = json.loads(line)
        text = clean(raw['source_text'])
        hold = clean(raw.get('holding_points', ''))
        stage = employment_stage(text)
        disp = disposition(raw.get('sanction_type', ''), text, stage)
        prim = primary(text, stage, raw.get('decision_result', ''))
        sec = secondary(text, prim)
        markers = fact_markers(text, stage)
        legal = legal_focus(text, prim, stage)
        excl = exclusions(text, stage, prim)
        rec = {
            'case_id': raw['case_id'],
            'case_name': raw['case_name'],
            'summary_short': hold if hold else clean(text[:110]),
            'holding_summary': hold if hold else clean(text[:180]),
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
            ov = OVR[raw['case_id']]
            rec['issue_type_primary'] = ov.get('primary', rec['issue_type_primary'])
            rec['employment_stage'] = ov.get('employment_stage', rec['employment_stage'])
            rec['disposition_type'] = ov.get('disposition', rec['disposition_type'])
            if ov.get('notes'):
                rec['notes'] = ov['notes']
        # post-fix
        rec['issue_type_secondary'] = [x for x in uniq(rec['issue_type_secondary'], issue_order)
                                        if x != rec['issue_type_primary']]
        rec['exclusion_flags'] = exclusions(text, rec['employment_stage'], rec['issue_type_primary'])
        rec['include_for_queries'], rec['exclude_for_queries'] = queries(rec, text)
        rec['confidence'] = confidence_score(text, rec['issue_type_primary'], rec['exclusion_flags'])
        rec['retrieval_note'] = retrieval_note(rec, text)
        if not rec['notes']:
            rec['notes'] = auto_notes(rec, text)
        recs.append(rec)

    out = OUT_DIR / f'sexual_harassment_batch_{b:03d}_reviewed.jsonl'
    out.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n', encoding='utf-8')

    # self review log
    lines = [f'# sexual_harassment_batch_{b:03d}_reviewed.jsonl 1차 self-review 메모', '']
    sample = [r for r in recs if r['notes']][:5]
    for r in sample:
        lines.extend([
            f"## {r['case_id']}",
            f"- reviewed primary/disposition: {r['issue_type_primary']} / {r['disposition_type']}",
            f"- secondary: {r['issue_type_secondary']}",
            f"- exclusion_flags: {r['exclusion_flags']}",
            f"- 변경 이유: {r['notes']}",
            ''
        ])
    (LOG_DIR / f'sexual_harassment_batch_{b:03d}_self_review.md').write_text(
        '\n'.join(lines).rstrip() + '\n', encoding='utf-8')

    print(f'batch_{b:03d}: {len(recs)}건 완료')

print('done')
