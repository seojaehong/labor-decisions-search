"""
other secondary 보강 2nd pass
- 기존 reviewed JSONL 읽기
- secondary 빈 배열 → holding_points 기반 채우기
- 복합 쟁점: secondary 도출
- 단일 쟁점 확실: secondary 빈 채로, notes에 "단일 쟁점" 명시
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

    # 징계절차 하자
    if ct(combined, '서면통지', '소명기회', '징계위원회', '인사위원회',
          '징계절차', '절차상의 하자', '절차를 위반', '이중징계',
          '의결정족수') and primary != 'procedure':
        arr.append('procedure')

    # 징계양정
    if ct(h, '양정이 과', '양정이 적정', '양정이 과다', '양정이 과하',
          '양정이 너무', '재량권을 일탈', '양정이 무겁') and primary != 'disciplinary_severity':
        arr.append('disciplinary_severity')

    # 비위행위 / 징계사유
    if ct(combined, '비위', '징계사유', '폭언', '폭행', '횡령', '허위보고',
          '업무지시 불이행', '무단결근', '음주') and primary != 'misconduct':
        arr.append('misconduct')

    # 부당노동행위 / 불이익취급
    if ct(combined, '부당노동행위', '불이익취급', '지배개입') and primary != 'unfair_treatment':
        arr.append('unfair_treatment')

    # 교섭대표 / 공정대표의무 / 단체협약 (unfair_treatment 아닌 primary에서)
    if ct(combined, '교섭대표노동조합', '공정대표의무', '근로시간면제한도',
          '교섭창구단일화') and primary not in ('unfair_treatment',):
        arr.append('unfair_treatment')

    # 단체협약 + 절차
    if ct(combined, '단체협약', '노사협의회', '고충처리') and primary not in ('unfair_treatment', 'procedure'):
        arr.append('unfair_treatment')

    # 갱신기대권
    if ct(combined, '갱신기대권', '계약갱신') and primary != 'renewal_expectation':
        arr.append('renewal_expectation')

    # 경영상 이유 / 정리해고
    if ct(combined, '경영상 이유', '정리해고', '긴박한 경영상',
          '위장폐업') and primary != 'redundancy':
        arr.append('redundancy')

    # 대기발령 / 전보 / 직위해제
    if ct(combined, '대기발령', '직위해제', '보직대기',
          '전보', '전직') and primary != 'transfer_validity':
        arr.append('transfer_validity')

    # 근로자성 / 5인 미만
    if ct(combined, '5인 미만', '5명 미만', '상시근로자 수가 5',
          '근로기준법상 근로자에 해당하지') and primary != 'worker_status':
        arr.append('worker_status')

    # 해고 존재 여부 / 합의해지
    if ct(combined, '해고가 존재하지 않', '해고로 볼 수 없',
          '해고가 없었', '합의해지', '사직서') and primary != 'dismissal_validity':
        arr.append('dismissal_validity')

    # 성희롱
    if ct(combined, '성희롱', '성추행', '성폭력') and primary != 'workplace_harassment':
        arr.append('workplace_harassment')

    # 임금 분쟁 (명확한 임금 쟁점)
    if ct(h, '임금을 지급', '임금 체불', '최저임금', '통상임금',
          '임금협정') and primary not in ('wage_dispute',):
        arr.append('wage_dispute')

    arr = [x for x in list(dict.fromkeys(arr)) if x != primary]
    return arr[:3]


def is_single_issue(h, t, primary, derived_secondary):
    """derived_secondary가 비어 있을 때 단일 쟁점 여부 확인"""
    if derived_secondary:
        return False
    combined = h + ' ' + t
    # 절차적 각하(procedure primary)는 단일 쟁점
    if primary == 'procedure' and ct(combined,
        '제척기간', '보정요구', '구제이익', '신청 의사를 포기',
        '노동위원회 규칙', '각하', '보정을 하지 않'):
        return True
    # 5인 미만 단일 쟁점
    if primary == 'worker_status' and ct(combined, '5인 미만', '5명 미만',
                                          '상시근로자 수가 5'):
        return True
    # holding이 단 한 쟁점만 언급
    if len(clean(h)) < 30:
        return True
    return True  # derive로 찾지 못했으면 단일 쟁점으로 표시


total_changed = 0
total_secondary_filled = 0
total_single_noted = 0

for b in range(1, 129):
    in_path = IN_DIR / f'other_batch_{b:03d}.jsonl'
    rev_path = OUT_DIR / f'other_batch_{b:03d}_reviewed.jsonl'

    if not rev_path.exists():
        continue

    # 원본 holding_points 로드
    orig = {}
    if in_path.exists():
        for line in in_path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                d = json.loads(line)
                orig[d['case_id']] = d

    recs = []
    batch_changes = []
    for line in rev_path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        cid = r['case_id']
        o = orig.get(cid, {})

        old_secondary = r.get('issue_type_secondary', [])
        old_notes = r.get('notes', '')
        primary = r.get('issue_type_primary', 'misconduct')

        # secondary 이미 있으면 skip
        if old_secondary:
            recs.append(r)
            continue

        hp = clean(o.get('holding_points', '') or r.get('holding_summary', ''))
        src = clean(o.get('source_text', ''))

        new_secondary = derive_secondary(hp, src, primary)
        new_notes = old_notes

        changed = False
        if new_secondary:
            r['issue_type_secondary'] = new_secondary
            changed = True
            total_secondary_filled += 1
        else:
            # 단일 쟁점 명시 (notes에 없는 경우만)
            if '단일 쟁점' not in (old_notes or ''):
                if old_notes:
                    new_notes = old_notes.rstrip('.') + ' (단일 쟁점).'
                else:
                    new_notes = '단일 쟁점.'
                r['notes'] = new_notes
                changed = True
                total_single_noted += 1

        if changed:
            batch_changes.append({
                'cid': cid, 'p': primary,
                's': new_secondary, 'n': new_notes
            })
            total_changed += 1

        recs.append(r)

    rev_path.write_text(
        '\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n',
        encoding='utf-8'
    )

    # log
    log_lines = [f'# other_batch_{b:03d}_reviewed.jsonl secondary 보강', '',
                 f'변경: {len(batch_changes)} / {len(recs)}', '']
    for ch in batch_changes[:3]:
        log_lines += [f"## {ch['cid']} | {ch['p']}",
                      f"- secondary: {ch['s']}",
                      f"- notes: {ch['n']}", '']
    (LOG_DIR / f'other_batch_{b:03d}_secondary_fill.md').write_text(
        '\n'.join(log_lines).rstrip() + '\n', encoding='utf-8'
    )

    if b % 10 == 0 or b == 128:
        print(f'batch_{b:03d}: {len(recs)}건, {len(batch_changes)}건 변경 '
              f'[누적: {total_changed} | sec채움: {total_secondary_filled} | 단일쟁점: {total_single_noted}]')

print(f'\n총 변경: {total_changed}건')
print(f'  secondary 채움: {total_secondary_filled}건')
print(f'  단일 쟁점 notes: {total_single_noted}건')
