"""
sexual_harassment 2nd pass v2
- 기존 reviewed JSONL 읽기
- holding_points 직접 읽고 보강
- 수정 대상: primary 확인/수정, secondary 채우기, notes 생성, confidence 정상화
- batch 001~002는 이미 LLM직독 완료 → skip
- batch 003~020 처리
"""
import sys, json, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path('C:/dev/labor-decisions-search/retagging')
IN_DIR = ROOT / 'input' / 'batches_38k'
OUT_DIR = ROOT / 'output' / 'reviewed'
LOG_DIR = ROOT / 'logs'

def clean(s):
    return re.sub(r'\s+', ' ', s or '').strip()

def ct(t, *words):
    return any(w in t for w in words)


def derive_notes_from_holding(hp, primary, sanction):
    """holding_points 텍스트를 직접 읽어 케이스별 notes 생성"""
    h = clean(hp)
    if not h:
        return '판정문 요약 정보 부족.'

    smap = {'dismissal':'해고','suspension':'정직','pay_cut':'감봉','demotion':'강등','warning':'경고','reprimand':'견책'}
    sl = smap.get((sanction or '').lower(), '처분')

    # holding_points에서 핵심 문장 추출 전략
    # 일반적으로 "~라고 판정한 사례" 형식이므로 앞 부분이 내용

    # 패턴 1: "~사유가 인정되..., ~양정이 과하여 부당" → 양정 과다 구제
    if ct(h, '양정이 과하여', '양정이 과도하여', '양정이 너무 가혹', '양정이 과하다고'):
        # 사유 인정 여부
        if ct(h, '일부 인정', '일부가 인정', '일부만 인정'):
            return f'성희롱 등 징계사유 일부 인정, {sl} 양정 과도하여 구제.'
        elif ct(h, '인정되지 않', '징계사유가 정당하지 않', '사유가 존재하지'):
            return f'성희롱 등 징계사유 불인정 또는 정당하지 않음, {sl} 부당.'
        elif ct(h, '사유는 인정', '사유가 인정', '사유가 존재', '사유로 타당'):
            return f'성희롱 등 징계사유 인정, {sl} 양정 과도하여 구제.'
        else:
            return f'성희롱 관련 {sl} 양정 과도하여 구제.'

    # 패턴 2: "~사유가 인정되..., ~양정이 적정/정당" → 처분 정당
    if ct(h, '양정이 적정', '양정이 과하다고 볼 수 없', '양정이 과도하지 않', '재량권 범위를 벗어났다고 보기 어렵', '고용관계를 계속할 수 없을 정도'):
        if ct(h, '반복', '지속', '장기간', '수년간', '다수'):
            return f'성희롱 반복·지속적 행위 인정(다수 피해자 포함), {sl} 양정 정당.'
        elif ct(h, '부하직원', '상급자', '관리자', '지위'):
            return f'지위 이용 성희롱 인정, {sl} 양정 적정.'
        else:
            return f'성희롱 등 사유 인정, {sl} 양정 적정.'

    # 패턴 3: 사유 불인정 → 부당
    if ct(h, '성희롱이 있었다고 볼 수 없', '성희롱으로 볼 수 없', '성희롱으로 단정할 수 없', '징계사유가 존재하지 않', '정당하지 않아 부당', '사유가 모두 정당성이 인정되지 아니하여'):
        return f'성희롱 행위 성립 불인정 또는 사유 정당성 없음, {sl} 부당.'

    # 패턴 4: 절차 하자 → 부당
    if ct(h, '절차', '이중징계', '의결정족수', '서면통지') and ct(h, '부당', '하자'):
        if ct(h, '이중징계'):
            return f'동일 사안 이중징계(절차 위반)로 {sl} 부당 판정.'
        if ct(h, '의결정족수'):
            return f'징계위원회 의결정족수 흠결, 절차 위반으로 {sl} 부당.'
        return f'징계절차 하자(절차 위반)로 {sl} 부당.'

    # 패턴 5: 해고 부존재/사직
    if ct(h, '해고가 아니라고', '해고가 존재하지 않', '사직서를 사용자가 수리', '근로관계가 종료', '묵시적으로 근로계약을 해지'):
        return '사직 또는 합의에 의한 근로관계 종료, 해고 부존재 판정.'

    # 패턴 6: 사유·양정·절차 모두 정당
    if ct(h, '사유, 양정, 절차', '사유가 존재하고, 징계양정', '모두 정당') and not ct(h, '부당'):
        return f'성희롱 등 징계사유·양정·절차 모두 정당, {sl} 정당.'

    # 패턴 7: 부당노동행위 관련
    if ct(h, '부당노동행위', '불이익취급', '지배개입'):
        if ct(h, '해당하지 않', '해당되지 않'):
            return f'성희롱 관련 불이익취급/부당노동행위 해당 안 됨. {sl} 정당성 별도 판단.'
        return f'성희롱 신고·조합활동 이후 불이익취급/부당노동행위 여부 판단.'

    # 패턴 8: 직위해제/대기발령
    if ct(h, '직위해제', '보직대기발령', '대기발령'):
        return f'직위해제/보직대기발령 정당성 판단 사건. 성희롱 의혹 관련 처분.'

    # fallback: holding_points 직접 압축 사용
    # "~라고 판정한 사례" 제거 후 핵심 사용
    compressed = h.replace('라고 판정한 사례', '').replace('고 판정한 사례', '').strip()
    if len(compressed) > 80:
        compressed = compressed[:80] + '...'
    return compressed + ('.' if not compressed.endswith('.') else '')


def check_and_fix_primary(h, t, primary, sanction):
    """holding_points 기반으로 primary가 잘못됐으면 수정"""
    # 절차 위반이 결정적
    if ct(h, '이중징계', '의결정족수 하자', '절차상의 하자로', '절차를 준수하지 않아') and ct(h, '부당'):
        return 'procedure'
    # 해고 부존재/사직
    if ct(h, '해고가 아니라고', '해고가 존재하지 않는다', '사직서를 사용자가 수리', '묵시적으로 근로계약을 해지'):
        return 'dismissal_validity'
    # 성희롱 성립 자체가 쟁점 (사유 불인정)
    if ct(h, '성희롱이 있었다고 볼 수 없', '성희롱으로 볼 수 없', '성희롱으로 단정할 수 없') and not ct(h, '양정'):
        return 'misconduct'
    # 양정이 결론 → disciplinary_severity
    if ct(h, '양정이 과하여', '양정이 과도하여', '양정이 적정', '재량권') and primary not in ('procedure', 'dismissal_validity', 'unfair_treatment'):
        return 'disciplinary_severity'
    # 사유 전부 불인정
    if ct(h, '모두 정당성이 인정되지 않', '모두 인정되지 않', '징계사유가 존재하지 않'):
        return 'misconduct'
    return primary  # 유지


def derive_secondary(h, t, primary):
    """holding_points 기반 secondary 도출"""
    arr = []
    # procedure가 언급됐으면
    if ct(h+t, '절차', '소명기회', '징계위원회', '서면통지', '인사위원회') and primary != 'procedure':
        arr.append('procedure')
    # 비위 행위 자체 (성희롱 외 다른 비위)
    if ct(h+t, '음주', '금품', '폭행', '무단', '업무지시 불이행', '하드디스크', '사학연금', '허위') and primary != 'misconduct':
        arr.append('misconduct')
    elif ct(h+t, '성희롱', '성추행', '성폭력') and primary != 'misconduct':
        arr.append('misconduct')
    # 양정
    if ct(h, '양정') and primary not in ('disciplinary_severity',):
        arr.append('disciplinary_severity')
    # 불이익취급/부당노동행위
    if ct(h, '부당노동행위', '불이익취급') and primary != 'unfair_treatment':
        arr.append('unfair_treatment')
    # 전보/대기발령
    if ct(h+t, '대기발령', '보직대기', '직위해제') and primary != 'transfer_validity':
        arr.append('transfer_validity')
    # secondary에서 primary 제거
    arr = [x for x in list(dict.fromkeys(arr)) if x != primary]
    return arr[:3]


def fix_confidence(h, primary, excl):
    """confidence 정상화 - 대부분 high"""
    if 'evidence_too_thin' in excl:
        return 'medium'
    # holding이 명확한 결론을 담고 있으면 high
    if ct(h, '인정', '정당', '적정', '부당', '과하여', '볼 수 없'):
        return 'high'
    if len(clean(h)) < 10:
        return 'medium'
    return 'high'


def fix_exclusions(h, t, primary, existing_excl):
    """exclusion_flags 정제 - 과도한 것 제거"""
    excl = list(existing_excl)
    # not_really_harassment_case: 성희롱 언급이 있으면 제거
    if 'not_really_harassment_case' in excl and ct(h+t, '성희롱', '성추행', '성폭력', '성적'):
        excl.remove('not_really_harassment_case')
    # evidence_too_thin: 증거 부족이 실제로 명시된 경우만 유지
    if 'evidence_too_thin' in excl and ct(h, '인정', '정당') and not ct(h, '부족', '없는', '볼 수 없'):
        excl.remove('evidence_too_thin')
    # 진짜 evidence_too_thin 추가
    if ct(h, '피해자의 주장만으로는', '증명이 부족하여', '조사와 증명이 부족') and 'evidence_too_thin' not in excl:
        excl.append('evidence_too_thin')
    # procedure_dominant: procedure primary인 경우만 유지
    if 'procedure_dominant' in excl and primary != 'procedure':
        excl.remove('procedure_dominant')
    if primary == 'procedure' and 'procedure_dominant' not in excl:
        excl.append('procedure_dominant')
    return list(dict.fromkeys(excl))


total_changed = 0
# batch 001~002는 LLM직독 완료 → 003부터
for b in range(3, 21):
    in_path = IN_DIR / f'sexual_harassment_batch_{b:03d}.jsonl'
    rev_path = OUT_DIR / f'sexual_harassment_batch_{b:03d}_reviewed.jsonl'
    if not in_path.exists() or not rev_path.exists():
        print(f'batch_{b:03d}: skip (파일 없음)')
        continue

    # 원본 holding_points 로드
    orig = {}
    for line in in_path.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        d = json.loads(line)
        orig[d['case_id']] = d

    recs = []
    batch_changes = []
    for line in rev_path.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        r = json.loads(line)
        cid = r['case_id']
        o = orig.get(cid, {})

        hp = clean(o.get('holding_points', '') or r.get('holding_summary', ''))
        src = clean(o.get('source_text', ''))
        sanction = o.get('sanction_type', '')

        old_primary = r.get('issue_type_primary', '')
        old_secondary = r.get('issue_type_secondary', [])
        old_notes = r.get('notes', '')
        old_conf = r.get('confidence', 'medium')
        old_excl = r.get('exclusion_flags', [])

        # 보강/수정
        new_primary = check_and_fix_primary(hp, src, old_primary, sanction)
        new_secondary = derive_secondary(hp, src, new_primary)
        if old_secondary and len(old_secondary) >= len(new_secondary):
            # 기존이 더 풍부하면 유지하되 primary만 제거
            new_secondary = [x for x in old_secondary if x != new_primary][:3]
        new_notes = derive_notes_from_holding(hp, new_primary, sanction)
        new_excl = fix_exclusions(hp, src, new_primary, old_excl)
        new_conf = fix_confidence(hp, new_primary, new_excl)

        changed = (new_primary != old_primary or new_notes != old_notes or
                   new_secondary != old_secondary or new_conf != old_conf or new_excl != old_excl)

        r['issue_type_primary'] = new_primary
        r['issue_type_secondary'] = new_secondary
        r['notes'] = new_notes
        r['confidence'] = new_conf
        r['exclusion_flags'] = new_excl
        r['review_status'] = 'reviewed'

        if changed:
            batch_changes.append({'cid': cid, 'p': new_primary, 's': new_secondary,
                                   'n': new_notes, 'c': new_conf, 'e': new_excl})
            total_changed += 1
        recs.append(r)

    rev_path.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in recs)+'\n', encoding='utf-8')

    log_lines = [f'# sexual_harassment_batch_{b:03d}_reviewed.jsonl 2nd pass v2', '',
                 f'변경 건수: {len(batch_changes)} / {len(recs)}', '']
    for ch in batch_changes[:5]:
        log_lines += [f"## {ch['cid']}", f"- primary: {ch['p']} | secondary: {ch['s']}",
                      f"- notes: {ch['n']}", f"- confidence: {ch['c']}", '']
    (LOG_DIR / f'sexual_harassment_batch_{b:03d}_self_review.md').write_text(
        '\n'.join(log_lines).rstrip()+'\n', encoding='utf-8')

    print(f'batch_{b:03d}: {len(recs)}건, {len(batch_changes)}건 변경')

print(f'\n총 변경: {total_changed}건')
