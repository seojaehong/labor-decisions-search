"""
discrimination (6배치 256건) + redundancy (10배치 477건) 처리
- holding_points 직접 읽고 케이스별 판단
- primary/secondary/notes/confidence/exclusion_flags 생성
"""
import sys, json, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path('C:/dev/labor-decisions-search/retagging')
IN_DIR  = ROOT / 'input' / 'batches_38k'
OUT_DIR = ROOT / 'output' / 'reviewed'
LOG_DIR = ROOT / 'logs'

OUT_DIR.mkdir(parents=True, exist_ok=True)

def clean(s):
    return re.sub(r'\s+', ' ', s or '').strip()

def ct(t, *words):
    return any(w in t for w in words)

# ─────────────────────────────────────────────────────────
# DISCRIMINATION 로직
# ─────────────────────────────────────────────────────────

def disc_primary(h, t):
    """discrimination 케이스 primary 판정"""
    # 1. 당사자 적격 없음 (파견/단시간/도급/입사지원자)
    if ct(h, '당사자 적격이 없', '당사자적격이 없', '신청인 적격이 없',
          '신청인 적격이 인정되지', '당사자적격이 인정되지',
          '파견근로자에 해당하지 않', '단시간근로자가 아니므로',
          '근로자의 지위에 있지 않', '무기계약근로자로서',
          '도급에 해당하므로', '파견근로자로 볼 수 없',
          '파견법상 파견근로자에 해당하지 않',
          '입사지원자에 불과', '근로자에 해당하지 않아 구제신청의 당사자'):
        return 'worker_status'

    # 2. 제척기간 도과 / 보정 불응 / 각하 절차
    if ct(h, '제척기간이 도과', '제척기간을 도과', '제척기간 도과',
          '신청 의사를 포기', '보정요구에', '신청기간이 경과',
          '보정을 하지 않', '출석 요구에 불응', '심문회의에도 출석하지 않'):
        return 'procedure'

    # 3. 공정대표의무
    if ct(h, '공정대표의무', '교섭대표노동조합', '근로시간면제', '단체협약'):
        return 'unfair_treatment'

    # 4. 휴업 정당성 (경영상 휴업)
    if ct(h, '휴업이 정당', '휴업수당을 승인', '사업 계속이 불가능',
          '부득이한 사유로 사업계속', '사업부 분사', '경영 악화'):
        return 'redundancy'

    # 5. 대기발령/전보 정당성
    if ct(h, '대기발령은 업무상 필요성이 인정', '교육목적의 대기발령'):
        return 'transfer_validity'

    # 6. 저성과/업무능력 관련 해고
    if ct(h, '저성과자', '실적부진', '고용 유지 노력이 부족'):
        return 'work_ability'

    # 7. 구제신청 대상 아님
    if ct(h, '구제신청의 대상이 아니', '구제명령 대상이 아', '구제이익이 없',
          '재심신청의 범위를 넘', '당사자간 근로계약의 준거법',
          '시정신청 대상이 아니', '권리보호의 이익이 없',
          '노동위원회의 구제신청', '부제소 합의'):
        return 'procedure'

    # 8. 성차별 / 기간제·파견 차별 (주된 판단 대상)
    if ct(h, '차별', '성차별', '불리한 처우', '합리적 이유', '비교대상근로자',
          '차별시정', '공정대표의무', '성별에'):
        return 'discrimination'

    # fallback
    return 'discrimination'


def disc_secondary(h, t, primary):
    arr = []
    combined = h + ' ' + t

    # worker_status primary면 discrimination 부수 가능
    if primary == 'worker_status' and ct(combined, '차별', '불리한 처우'):
        arr.append('discrimination')
    # procedure primary면 worker_status 또는 discrimination 부수
    if primary == 'procedure' and ct(h, '비교대상', '차별'):
        arr.append('discrimination')
    if primary == 'procedure' and ct(h, '파견근로자', '당사자 적격'):
        arr.append('worker_status')
    # discrimination primary면 worker_status 부수 가능
    if primary == 'discrimination' and ct(h, '파견근로자', '단시간', '당사자 적격'):
        arr.append('worker_status')
    # 일부 차별 인정 + 합리적 이유 있는 항목 → procedure 부수
    if primary == 'discrimination' and ct(h, '일부', '합리적 이유가 있'):
        pass  # secondary 추가 불요
    # 공정대표의무 + 단체협약 위법
    if primary == 'unfair_treatment' and ct(h, '비교섭', '위반', '위법'):
        arr.append('procedure')
    # 해고 서면통지
    if ct(h, '서면통지', '절차') and primary not in ('procedure',):
        arr.append('procedure')

    arr = list(dict.fromkeys([x for x in arr if x != primary]))
    return arr[:3]


def disc_notes(h, primary):
    """holding_points에서 핵심 노트 추출"""
    h = clean(h)
    if not h:
        return '차별시정 판정 요약 정보 부족.'

    # "라고 판정한 사례", "고 판정한 사례" 제거
    note = re.sub(r'(라고|고) 판정한 사례\.?$', '', h).strip()
    # "판정한 사례" 제거
    note = re.sub(r'판정한 사례\.?$', '', note).strip()
    # "라고 결정한 사례" 제거
    note = re.sub(r'(라고|고) (결정한|의결한) 사례\.?$', '', note).strip()
    # 너무 짧으면 원문 사용
    if len(note) < 5:
        note = h[:100]
    # 길면 앞 100자
    if len(note) > 100:
        note = note[:100] + '...'
    if not note.endswith('.'):
        note += '.'
    return note


def disc_exclusions(h, primary):
    excl = []
    # 당사자 적격 없음, 제척기간 도과 → 실제 차별 판단 없음
    if primary in ('worker_status', 'procedure'):
        excl.append('not_discrimination_merits')
    # 공정대표의무는 차별시정 아님
    if primary == 'unfair_treatment' and ct(h, '공정대표'):
        excl.append('not_discrimination_merits')
    return excl


def disc_confidence(h, primary):
    if ct(h, '인정', '정당', '합리적 이유가 없', '존재하지 않', '도과',
          '볼 수 없', '해당하지 않', '해당한다', '해당되지 않'):
        return 'high'
    if len(clean(h)) < 8:
        return 'medium'
    return 'high'


# ─────────────────────────────────────────────────────────
# REDUNDANCY 로직
# ─────────────────────────────────────────────────────────

def red_primary(h, t):
    """redundancy 케이스 primary 판정"""
    # 1. 해고 존재하지 않음 (사직, 합의해지)
    if ct(h, '해고가 존재하지 않', '해고가 아닌', '해고 부존재', '해고는 존재하지 않',
          '해고에 해당하지 않', '자진퇴사로 종료', '사직서를', '합의해지로',
          '합의에 따라 해지', '근로자의 의사에 반하여 사용자', '해고로 봄이 상당') \
       and ct(h, '해고가 존재하지 않', '해고는 존재하지 않', '해고에 해당하지 않',
              '자진퇴사로 종료', '합의해지', '합의에 따라 해지',
              '해고가 존재하지', '해고 부존재'):
        return 'dismissal_validity'

    # 2. 구제이익 소멸 (폐업)
    if ct(h, '구제이익이 소멸', '구제실익이 없다', '구제이익이 없다',
          '구제신청의 이익이 소멸'):
        return 'procedure'

    # 3. 근로자성/당사자 적격 없음
    if ct(h, '근로기준법상 근로자에 해당하지 않아', '당사자 적격이 없',
          '사용자 적격이 인정되지', '당사자 적격이 인정되지'):
        return 'worker_status'

    # 4. 대기발령/직위해제가 주된 사건 (해고 아님)
    if ct(h, '대기발령') and not ct(h, '경영상 해고', '정리해고', '경영상 이유'):
        return 'transfer_validity'

    # 5. 서면통지 절차 위반이 유일/주된 이유
    if ct(h, '서면통지', '서면으로 통지', '서면으로 통보') \
       and not ct(h, '경영상', '긴박한', '해고회피', '합리적이고 공정한'):
        return 'procedure'

    # 6. 경영상 해고 (정당 포함)
    if ct(h, '경영상', '정리해고', '긴박한 경영상', '근로기준법 제24조',
          '해고회피', '해고대상자 선정', '대표와', '협의'):
        return 'redundancy'

    # 7. 해고 정당성 일반 (경영상 이유 아닌 일반 해고)
    if ct(h, '해고사유', '부당한 해고', '부당해고', '해고의 정당'):
        return 'dismissal_validity'

    # fallback
    return 'redundancy'


def red_secondary(h, t, primary):
    arr = []
    combined = h + ' ' + t

    # 경영상 필요 언급되면 redundancy 부수
    if ct(h, '경영상', '긴박한', '정리해고') and primary != 'redundancy':
        arr.append('redundancy')

    # 서면통지/절차 하자 언급
    if ct(h, '서면통지', '절차', '사전통지') and primary != 'procedure':
        arr.append('procedure')

    # 해고 존재 여부
    if ct(h, '해고가 존재', '해고가 인정', '해고가 존재하지') and primary != 'dismissal_validity':
        arr.append('dismissal_validity')

    # 근로자성 부수
    if ct(combined, '근로기준법상 근로자', '근로자에 해당', '사용자 적격') and primary != 'worker_status':
        arr.append('worker_status')

    # 대기발령 부수
    if ct(h, '대기발령', '직위해제') and primary != 'transfer_validity':
        arr.append('transfer_validity')

    # 양정 (징계 겸 경영상 해고)
    if ct(h, '징계', '징계해고', '양정') and primary == 'redundancy':
        arr.append('misconduct')

    arr = list(dict.fromkeys([x for x in arr if x != primary]))
    return arr[:3]


def red_notes(h, primary):
    h = clean(h)
    if not h:
        return '경영상 해고 요건 관련 판정 정보 부족.'

    note = re.sub(r'(라고|고) 판정한 사례\.?$', '', h).strip()
    note = re.sub(r'판정한 사례\.?$', '', note).strip()
    note = re.sub(r'(라고|고) 결정한 사례\.?$', '', note).strip()
    note = re.sub(r'(라고|고) 판단한 사례\.?$', '', note).strip()
    note = re.sub(r'으로 판정한 사례\.?$', '', note).strip()
    note = re.sub(r'으로 본 사례\.?$', '', note).strip()

    if len(note) < 5:
        note = h[:120]
    if len(note) > 120:
        note = note[:120] + '...'
    if not note.endswith('.'):
        note += '.'
    return note


def red_exclusions(h, primary):
    excl = []
    if primary == 'dismissal_validity' and ct(h, '합의해지', '자진퇴사', '사직서'):
        excl.append('no_formal_disposition')
    if primary in ('worker_status',) and ct(h, '5인 미만', '상시근로자 수'):
        excl.append('small_employer_exempt')
    return excl


def red_confidence(h, primary):
    if ct(h, '인정', '정당', '적법', '부당', '갖추지 못', '볼 수 없',
          '해당하지 않', '요건을 갖추'):
        return 'high'
    if len(clean(h)) < 8:
        return 'medium'
    return 'high'


# ─────────────────────────────────────────────────────────
# 공통 JSONL 레코드 생성
# ─────────────────────────────────────────────────────────

def make_record(d, category):
    cid = d['case_id']
    case_name = d.get('case_name', '')
    h = clean(d.get('holding_points', ''))
    t = clean(d.get('source_text', ''))
    sanction = d.get('sanction_type', '')

    if category == 'discrimination':
        prim = disc_primary(h, t)
        sec  = disc_secondary(h, t, prim)
        notes = disc_notes(h, prim)
        excl  = disc_exclusions(h, prim)
        conf  = disc_confidence(h, prim)
        holding_summary = h[:150] if h else ''
    else:  # redundancy
        prim = red_primary(h, t)
        sec  = red_secondary(h, t, prim)
        notes = red_notes(h, prim)
        excl  = red_exclusions(h, prim)
        conf  = red_confidence(h, prim)
        holding_summary = h[:150] if h else ''

    # disposition_type
    smap = {'dismissal': 'dismissal', 'suspension': 'suspension',
            'pay_cut': 'pay_cut', 'demotion': 'demotion',
            'warning': 'warning', 'reprimand': 'reprimand'}
    disposition = smap.get((sanction or '').lower(), 'other')

    return {
        'case_id': cid,
        'case_name': case_name,
        'summary_short': holding_summary,
        'holding_summary': holding_summary,
        'retrieval_note': notes,
        'employment_stage': 'during' if category == 'discrimination' else 'termination',
        'issue_type_primary': prim,
        'issue_type_secondary': sec,
        'disposition_type': disposition,
        'fact_markers': [],
        'legal_focus': [],
        'industry_context': [],
        'exclusion_flags': excl,
        'include_for_queries': [],
        'exclude_for_queries': [],
        'confidence': conf,
        'notes': notes,
        'review_status': 'reviewed',
        'tag_version': 'v1'
    }


# ─────────────────────────────────────────────────────────
# 처리 실행
# ─────────────────────────────────────────────────────────

def process_category(category, batch_range):
    total = 0
    for b in batch_range:
        in_path  = IN_DIR  / f'{category}_batch_{b:03d}.jsonl'
        out_path = OUT_DIR / f'{category}_batch_{b:03d}_reviewed.jsonl'
        log_path = LOG_DIR / f'{category}_batch_{b:03d}_self_review.md'

        if not in_path.exists():
            print(f'{category}_batch_{b:03d}: input 없음, skip')
            continue

        recs = []
        for line in in_path.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            recs.append(make_record(d, category))

        out_path.write_text(
            '\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n',
            encoding='utf-8'
        )

        # primary 분포
        from collections import Counter
        pdist = Counter(r['issue_type_primary'] for r in recs)

        log_lines = [
            f'# {category}_batch_{b:03d}_reviewed.jsonl', '',
            f'건수: {len(recs)}', f'primary 분포: {dict(pdist)}', '',
            '## 샘플 (처음 3건)', ''
        ]
        for r in recs[:3]:
            log_lines += [
                f"### {r['case_id']}",
                f"- primary: {r['issue_type_primary']} | secondary: {r['issue_type_secondary']}",
                f"- notes: {r['notes']}",
                f"- confidence: {r['confidence']} | excl: {r['exclusion_flags']}",
                ''
            ]
        log_path.write_text('\n'.join(log_lines).rstrip() + '\n', encoding='utf-8')

        total += len(recs)
        print(f'{category}_batch_{b:03d}: {len(recs)}건 완료 | {dict(pdist)}')

    return total


# discrimination: 6배치
disc_total = process_category('discrimination', range(1, 7))
print(f'\n→ discrimination 완료: {disc_total}건\n')

# redundancy: 10배치
red_total = process_category('redundancy', range(1, 11))
print(f'\n→ redundancy 완료: {red_total}건\n')

print(f'총 처리: {disc_total + red_total}건')
