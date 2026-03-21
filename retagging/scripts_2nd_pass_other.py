"""
other 6,369건 2차 판독 패스
- 현재 96%가 misconduct → holding_points 직독으로 재분류
- 주요 재분류 대상: procedure, worker_status, unfair_treatment,
  dismissal_validity, disciplinary_severity, renewal_expectation, redundancy
- 10배치마다 진행상황 출력
"""
import sys, json, re
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

ROOT    = Path('C:/dev/labor-decisions-search/retagging')
IN_DIR  = ROOT / 'input' / 'batches_38k'
OUT_DIR = ROOT / 'output' / 'reviewed'
LOG_DIR = ROOT / 'logs'

def clean(s):
    return re.sub(r'\s+', ' ', s or '').strip()

def ct(t, *words):
    return any(w in t for w in words)


# ──────────────────────────────────────────────
# PRIMARY 판정
# ──────────────────────────────────────────────

def classify_primary(h, t):
    """holding_points + source_text 기반 primary 재판정"""
    c = h + ' ' + t  # combined for some checks

    # ── 1. PROCEDURE: 각하/기각 절차적 이유 ──────────────────
    # 제척기간 도과
    if ct(h, '제척기간이 도과', '제척기간을 도과', '제척기간 도과',
          '신청기간이 지났', '구제신청기간이 경과', '신청기간이 경과',
          '기산일', '3개월이 지난'):
        return 'procedure'

    # 보정 불응 / 출석 거부 / 신청 의사 없음
    if ct(h, '보정요구에', '보정을 하지 않', '보정에 응하지 않', '보정 요구를',
          '신청 의사를 포기', '구제신청의 의사가 없', '구제신청 의사를 포기',
          '취하해달라는', '구제신청을 취하',
          '심문회의에도 출석하지 않', '출석 요구에도 2회 이상 불응',
          '2회에 걸쳐 보정', '3회 이상 신청취지 보정 요구',
          '4회에 걸쳐 보정요구',
          '불출석하는 등 구제신청 의사를 포기'):
        return 'procedure'

    # 구제이익 소멸 (복직명령·원직복직)
    if ct(h, '구제이익이 소멸', '구제실익이 없다', '구제이익이 없다',
          '구제신청의 이익이 소멸', '구제를 신청할 권리가 소멸',
          '복직명령으로 구제이익', '원직복직명령이', '구제이익이 없어',
          '사업장이 사실상 폐업하여 원직복직이 불가능'):
        return 'procedure'

    # 재심 기간 도과
    if ct(h, '재심신청의 제척기간', '재심신청 기간', '재심신청의 요건을 갖추지 못',
          '재심신청이 제척기간'):
        return 'procedure'

    # 노동위원회규칙 위반 각하
    if ct(h, '노동위원회규칙 제60조', '규칙 제60조', '각하 판정'):
        return 'procedure'

    # ── 2. WORKER_STATUS: 5인 미만 / 근로자성 ─────────────────
    if ct(h, '5인 미만', '5명 미만', '상시근로자 수가 5명 미만', '상시근로자 수가 5인 미만',
          '5인 미만 사업장', '5명 미만 사업장',
          '상시 5인 미만', '상시 5명 미만',
          '상시근로자 수는 4', '상시근로자 수가 4',
          '상시근로자 수가 3', '상시근로자 수가 2'):
        return 'worker_status'

    if ct(h, '근로기준법상 근로자에 해당하지 않', '근로기준법상의 근로자에 해당하지 않',
          '근로자에 해당하지 않아 구제신청', '근로자에 해당하지 않아 당사자',
          '근로자로 볼 수 없어', '근로자가 아니므로',
          '독립적인 사업자로', '프리랜서') \
       and not ct(h, '근로자에 해당한다', '근로자로 인정'):
        return 'worker_status'

    if ct(h, '사용자 적격이 인정되지', '사용자 적격이 없', '당사자 적격이 없',
          '신청인 적격이 없', '실질적인 사용자'):
        return 'worker_status'

    # ── 3. UNFAIR_TREATMENT: 공정대표의무 / 단체협약 / 교섭 ────
    if ct(h, '공정대표의무', '교섭대표노동조합', '교섭요구 노동조합',
          '근로시간면제', '공동교섭대표단', '소수 노동조합',
          '노동조합 운영비', '노동조합 사무실',
          '단체협약' , '임금동결은 교섭창구',
          '부당노동행위', '지배개입'):
        # 단체협약만 있을 때 세분화
        if ct(h, '단체협약') and not ct(h, '공정대표의무', '교섭대표노동조합',
                                         '교섭요구', '근로시간면제', '조합원 수',
                                         '부당노동행위', '지배개입',
                                         '노동조합 운영비', '노동조합 사무실'):
            # 단순 단체협약 해석/이행 → unfair_treatment
            return 'unfair_treatment'
        return 'unfair_treatment'

    # 의결 (노동조합법 위반 의결)
    if ct(h, '공무원노조법에 위반', '노동조합법에 위반', '법에 위반된다고 의결',
          '위반된다고 결정', '교섭대상에 해당하는지', '비교섭 사항'):
        return 'unfair_treatment'

    # ── 4. DISMISSAL_VALIDITY: 해고 부존재 / 합의해지 / 채용내정 ─
    if ct(h, '해고가 존재하지 않', '해고가 없었다', '해고가 있었다고 볼 수 없',
          '해고로 볼 수 없', '해고에 해당하지 않', '해고 부존재',
          '해고가 아닌', '해고가 없다고'):
        return 'dismissal_validity'

    if ct(h, '합의해지', '사직서를', '자진사직', '자진퇴사',
          '사직의 의사표시', '사직 의사표시') \
       and not ct(h, '부당해고', '부당한 해고', '해고는 정당'):
        return 'dismissal_validity'

    if ct(h, '채용내정이 성립하지 않', '채용내정의 의사표시', '근로계약이 성립되었다고 볼 수 없',
          '근로계약 체결 사실이 없어'):
        return 'dismissal_validity'

    if ct(h, '일용근로자에 해당하여 해고가 없었다', '1일 단위의 계약기간 만료'):
        return 'dismissal_validity'

    # 근로관계 종료(사직/합의) 판정 - 부당해고 아님
    if ct(h, '근로관계가 종료한 것', '근로관계 종료가 해고가 아', '근로계약이 만료'):
        if not ct(h, '부당해고', '부당한 해고', '부당하다'):
            return 'dismissal_validity'

    # ── 5. RENEWAL_EXPECTATION: 갱신기대권 / 계약만료 ───────────
    if ct(h, '갱신기대권', '갱신에 대한 기대'):
        return 'renewal_expectation'

    if ct(h, '촉탁 근로계약이 만료', '기간만료에 따라 근로계약이 종료',
          '계약기간 만료에 따라 근로계약', '촉탁계약이 만료') \
       and not ct(h, '부당해고', '부당한 해고'):
        return 'dismissal_validity'

    # ── 6. DISCIPLINARY_SEVERITY: 양정 과다 ──────────────────
    if ct(h, '징계양정이 과다', '양정이 과하', '양정이 과도', '양정이 적정하지',
          '징계양정이 과하', '양정의 적정성', '징계양정이 적정'):
        return 'disciplinary_severity'

    # ── 7. REDUNDANCY: 경영상 해고 / 폐업 ───────────────────
    if ct(h, '경영상 이유에 의한 해고', '긴박한 경영상', '정리해고',
          '위장폐업', '사업 폐지', '폐업 절차'):
        return 'redundancy'

    # ── 8. TRANSFER_VALIDITY: 대기발령 / 전보 ────────────────
    if ct(h, '대기발령') and not ct(h, '경영상 해고', '정리해고'):
        return 'transfer_validity'

    if ct(h, '전직', '전보', '근로조건을 위반') and ct(h, '업무변경', '이동'):
        return 'transfer_validity'

    # ── 9. PROCEDURE: 서면통지 단독 위반 ─────────────────────
    if ct(h, '서면통지') and not ct(h, '해고사유', '징계사유', '비위', '양정',
                                    '경영상', '부당', '정당한 이유'):
        return 'procedure'

    # ── 10. MISCONDUCT: 실제 비위행위 징계 (default for genuine cases) ─
    return 'misconduct'


# ──────────────────────────────────────────────
# SECONDARY 판정
# ──────────────────────────────────────────────

def classify_secondary(h, t, primary):
    arr = []
    c = h + ' ' + t

    # procedure primary → 실체 쟁점 부수
    if primary == 'procedure':
        if ct(h, '해고사유', '비위', '징계사유', '징계') and not ct(h, '보정', '제척'):
            arr.append('misconduct')
        if ct(h, '경영상'):
            arr.append('redundancy')
        if ct(h, '5인 미만', '5명 미만'):
            arr.append('worker_status')

    # worker_status primary → 실체 쟁점
    if primary == 'worker_status':
        if ct(h, '해고', '부당해고'):
            arr.append('dismissal_validity')

    # misconduct primary → 절차/양정 부수
    if primary == 'misconduct':
        if ct(h, '절차', '서면통지', '소명기회', '징계위원회'):
            arr.append('procedure')
        if ct(h, '양정', '과다', '과하'):
            arr.append('disciplinary_severity')
        if ct(h, '해고사유') and ct(h, '해고의 서면통지', '서면으로 통지'):
            arr.append('procedure')

    # disciplinary_severity primary
    if primary == 'disciplinary_severity':
        if ct(c, '징계사유', '비위', '업무'):
            arr.append('misconduct')
        if ct(c, '절차', '서면통지'):
            arr.append('procedure')

    # dismissal_validity primary
    if primary == 'dismissal_validity':
        if ct(h, '해고사유', '징계') and ct(h, '정당'):
            arr.append('misconduct')
        if ct(h, '서면통지', '절차'):
            arr.append('procedure')

    # redundancy primary
    if primary == 'redundancy':
        if ct(h, '서면통지', '절차'):
            arr.append('procedure')
        if ct(h, '해고사유', '징계'):
            arr.append('misconduct')

    # unfair_treatment primary
    if primary == 'unfair_treatment':
        if ct(h, '해고', '징계'):
            arr.append('misconduct')

    arr = list(dict.fromkeys([x for x in arr if x != primary]))
    return arr[:3]


# ──────────────────────────────────────────────
# NOTES 생성
# ──────────────────────────────────────────────

def make_notes(h, primary):
    h = clean(h)
    if not h:
        # primary별 기본 메시지
        defaults = {
            'procedure': '절차적 사유로 각하/기각된 사건.',
            'worker_status': '근로자성 또는 사업장 규모 요건 불충족.',
            'unfair_treatment': '공정대표의무 또는 단체협약 관련 사건.',
            'dismissal_validity': '해고 성립 여부 자체가 다투어진 사건.',
            'misconduct': '비위행위 등 징계사유 정당성이 쟁점.',
            'disciplinary_severity': '징계양정 과다 여부가 핵심.',
            'renewal_expectation': '갱신기대권 존부가 핵심 쟁점.',
            'redundancy': '경영상 이유에 의한 해고 요건 충족 여부.',
            'transfer_validity': '전보/대기발령 정당성이 쟁점.',
        }
        return defaults.get(primary, '판정 요약 정보 부족.')

    # "라고 판정한 사례", "고 판정한 사례" 등 제거
    note = re.sub(r'(라고|고|으로|으로서|다고|다는) (판정한|결정한|의결한|본|인정한) 사례\.?$', '', h).strip()
    note = re.sub(r'판정한 사례\.?$', '', note).strip()
    note = re.sub(r'결정한 사례\.?$', '', note).strip()

    if len(note) < 5:
        note = h

    # 너무 길면 첫 문장 또는 앞 120자
    if len(note) > 120:
        # 마침표로 자르기 시도
        first = note.split('.')[0].strip()
        if len(first) >= 15:
            note = first
        else:
            note = note[:120] + '...'

    if not note.endswith('.'):
        note += '.'
    return note


# ──────────────────────────────────────────────
# CONFIDENCE
# ──────────────────────────────────────────────

def make_confidence(h, primary, excl):
    if 'evidence_too_thin' in excl:
        return 'medium'
    if ct(h, '인정', '정당', '각하', '부당', '볼 수 없', '해당하지 않',
          '존재하지 않', '적법', '위반', '도과', '미만'):
        return 'high'
    if len(clean(h)) < 10:
        return 'medium'
    return 'high'


# ──────────────────────────────────────────────
# EXCLUSION FLAGS
# ──────────────────────────────────────────────

def make_exclusions(h, primary):
    excl = []
    if primary in ('procedure', 'worker_status') \
       and not ct(h, '해고사유', '비위', '징계', '양정'):
        excl.append('no_substantive_ruling')
    if primary == 'unfair_treatment':
        excl.append('collective_bargaining_focus')
    return excl


# ──────────────────────────────────────────────
# 레코드 생성
# ──────────────────────────────────────────────

def make_record(orig_d, existing_r):
    h = clean(orig_d.get('holding_points', '') or existing_r.get('holding_summary', ''))
    t = clean(orig_d.get('source_text', ''))
    sanction = orig_d.get('sanction_type', '')

    prim = classify_primary(h, t)
    sec  = classify_secondary(h, t, prim)
    notes = make_notes(h, prim)
    conf  = make_confidence(h, prim, [])
    excl  = make_exclusions(h, prim)

    smap = {'dismissal':'dismissal','suspension':'suspension','pay_cut':'pay_cut',
            'demotion':'demotion','warning':'warning','reprimand':'reprimand'}
    disposition = smap.get((sanction or '').lower(), 'other')

    r = dict(existing_r)  # 기존 필드 보존
    r['issue_type_primary']   = prim
    r['issue_type_secondary'] = sec
    r['notes']                = notes
    r['confidence']           = conf
    r['exclusion_flags']      = excl
    r['holding_summary']      = h[:150] if h else ''
    r['review_status']        = 'reviewed'
    r['tag_version']          = 'v1'
    return r


# ──────────────────────────────────────────────
# 처리 실행
# ──────────────────────────────────────────────

total_changed = 0
total_recs = 0
overall_pdist = Counter()

for b in range(1, 129):
    in_path  = IN_DIR  / f'other_batch_{b:03d}.jsonl'
    rev_path = OUT_DIR / f'other_batch_{b:03d}_reviewed.jsonl'
    log_path = LOG_DIR / f'other_batch_{b:03d}_self_review.md'

    if not in_path.exists() or not rev_path.exists():
        continue

    # 원본 holding_points 로드
    orig = {}
    for line in in_path.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        d = json.loads(line)
        orig[d['case_id']] = d

    # 기존 reviewed 읽기 + 재분류
    recs = []
    batch_changed = 0
    for line in rev_path.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        existing_r = json.loads(line)
        cid = existing_r['case_id']
        o = orig.get(cid, {})

        new_r = make_record(o, existing_r)
        old_prim = existing_r.get('issue_type_primary', '')
        if new_r['issue_type_primary'] != old_prim:
            batch_changed += 1
            total_changed += 1

        recs.append(new_r)
        overall_pdist[new_r['issue_type_primary']] += 1

    total_recs += len(recs)

    rev_path.write_text(
        '\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n',
        encoding='utf-8'
    )

    # 로그
    pdist = Counter(r['issue_type_primary'] for r in recs)
    log_lines = [
        f'# other_batch_{b:03d}_reviewed.jsonl 2nd pass', '',
        f'건수: {len(recs)} | 재분류: {batch_changed}건',
        f'primary 분포: {dict(pdist)}', '',
        '## 샘플 (처음 3건)', ''
    ]
    for r in recs[:3]:
        log_lines += [
            f"### {r['case_id']}",
            f"- primary: {r['issue_type_primary']} | secondary: {r['issue_type_secondary']}",
            f"- notes: {r['notes'][:80]}",
            ''
        ]
    log_path.write_text('\n'.join(log_lines).rstrip() + '\n', encoding='utf-8')

    if b % 10 == 0 or b == 128:
        print(f'batch_{b:03d}: {len(recs)}건 | 재분류 {batch_changed}건 | 누적 {total_changed}/{total_recs}')

print(f'\n=== 최종 primary 분포 ===')
for k, v in overall_pdist.most_common():
    print(f'  {k}: {v} ({v/total_recs*100:.1f}%)')
print(f'\n총 재분류: {total_changed}/{total_recs}건')
