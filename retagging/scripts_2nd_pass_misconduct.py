"""
misconduct_remaining 2nd pass
- notes는 이미 양질 → 유지
- secondary 빈 배열(4.2%) → holding_points 기반 보강
- confidence medium(10.4%) → holding 명확하면 high로
- exclusion_flags 과도한 것 정제
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

def derive_secondary(h, t, primary):
    arr = []
    combined = h + ' ' + t

    # 절차 하자
    if ct(combined, '절차', '서면통지', '소명기회', '징계위원회', '인사위원회') and primary != 'procedure':
        arr.append('procedure')

    # 양정
    if ct(h, '양정', '재량권', '과하', '과도') and primary != 'disciplinary_severity':
        arr.append('disciplinary_severity')

    # 부당노동행위/불이익취급
    if ct(combined, '부당노동행위', '불이익취급', '지배개입', '조합') and primary != 'unfair_treatment':
        arr.append('unfair_treatment')

    # misconduct 부수 (primary가 다른 경우)
    if ct(combined, '징계사유', '비위', '업무지시 불이행', '폭언', '폭행', '횡령', '허위') and primary != 'misconduct':
        arr.append('misconduct')

    # 해고 성립 여부
    if ct(h, '해고가 아니라', '사직', '합의해지', '해고 부존재') and primary != 'dismissal_validity':
        arr.append('dismissal_validity')

    # 전보/대기발령
    if ct(combined, '대기발령', '직위해제', '전보') and primary not in ('transfer_validity',):
        arr.append('transfer_validity')

    # primary 제거 + 중복 제거
    arr = list(dict.fromkeys([x for x in arr if x != primary]))
    return arr[:3]

def fix_confidence(h, primary, existing_conf, excl):
    # 이미 high면 유지
    if existing_conf == 'high':
        return 'high'
    # evidence_too_thin이 있으면 medium 유지
    if 'evidence_too_thin' in excl:
        return 'medium'
    # 명확한 판정 표현이 있으면 high
    if ct(h, '인정', '정당', '적정', '부당', '인정되지 않', '볼 수 없', '존재하지 않'):
        return 'high'
    # holding이 너무 짧으면 medium 유지
    if len(clean(h)) < 10:
        return 'medium'
    return 'high'

def fix_exclusions(h, t, primary, existing_excl):
    excl = list(existing_excl)
    combined = h + ' ' + t

    # not_really_harassment_case: misconduct 배치에서는 대부분 제거 대상
    if 'not_really_harassment_case' in excl:
        excl.remove('not_really_harassment_case')

    # evidence_too_thin: 실제 증거 부족 명시된 경우만 유지
    if 'evidence_too_thin' in excl and ct(h, '인정', '정당') and not ct(h, '부족', '없는', '볼 수 없'):
        excl.remove('evidence_too_thin')
    if ct(h, '피해자의 주장만으로는', '증명이 부족', '입증이 부족', '소명이 부족') and 'evidence_too_thin' not in excl:
        excl.append('evidence_too_thin')

    # procedure_dominant: procedure primary인 경우만
    if 'procedure_dominant' in excl and primary != 'procedure':
        excl.remove('procedure_dominant')
    if primary == 'procedure' and 'procedure_dominant' not in excl:
        excl.append('procedure_dominant')

    return list(dict.fromkeys(excl))

total_changed = 0
for b in range(1, 156):
    in_path = IN_DIR / f'misconduct_remaining_batch_{b:03d}.jsonl'
    rev_path = OUT_DIR / f'misconduct_remaining_batch_{b:03d}_reviewed.jsonl'

    if not rev_path.exists():
        continue
    if not in_path.exists():
        continue

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

        old_secondary = r.get('issue_type_secondary', [])
        old_conf = r.get('confidence', 'medium')
        old_excl = r.get('exclusion_flags', [])
        primary = r.get('issue_type_primary', '')

        # secondary가 비어있을 때만 보강 (기존 secondary 존중)
        if old_secondary:
            new_secondary = [x for x in old_secondary if x != primary][:3]
        else:
            new_secondary = derive_secondary(hp, src, primary)

        new_conf = fix_confidence(hp, primary, old_conf, old_excl)
        new_excl = fix_exclusions(hp, src, primary, old_excl)

        changed = (new_secondary != old_secondary or new_conf != old_conf or new_excl != old_excl)

        r['issue_type_secondary'] = new_secondary
        r['confidence'] = new_conf
        r['exclusion_flags'] = new_excl
        r['review_status'] = 'reviewed'

        if changed:
            batch_changes.append({'cid': cid, 'p': primary, 's': new_secondary,
                                   'c': new_conf, 'e': new_excl})
            total_changed += 1
        recs.append(r)

    rev_path.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n', encoding='utf-8')

    log_lines = [f'# misconduct_remaining_batch_{b:03d}_reviewed.jsonl 2nd pass', '',
                 f'변경 건수: {len(batch_changes)} / {len(recs)}', '']
    for ch in batch_changes[:3]:
        log_lines += [f"## {ch['cid']}", f"- primary: {ch['p']} | secondary: {ch['s']}",
                      f"- confidence: {ch['c']}", '']
    (LOG_DIR / f'misconduct_remaining_batch_{b:03d}_self_review.md').write_text(
        '\n'.join(log_lines).rstrip() + '\n', encoding='utf-8')

    if b % 10 == 0 or b == 155:
        print(f'batch_{b:03d}: {len(recs)}건, {len(batch_changes)}건 변경 [누적: {total_changed}]')

print(f'\n총 변경: {total_changed}건')
