# contract_expiry_batch_014_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_014_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_18387` [dismissal_validity]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 계약기간의 만료에 따라 근로계약관계를 종료한 것은 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_18407` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약의 기간만료에 따라 근로관계가 종료되었다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_18439` [dismissal_validity]
  - 변경: notes
  - notes: 무기계약 전환의 기대권은 인정되나, 무기계약 전환 거절에 합리적 이유가 있어 정당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성
- `id_18443` [dismissal_validity]
  - 변경: notes
  - notes: 근로자가 참여한 작업공사기간의 만료에 따라 근로관계가 종료되었을 뿐 부당한 해고는 아니라고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유
- `id_18459` [dismissal_validity]
  - 변경: notes
  - notes: 무기한 정직 처분 후 추가 비위행위 등 사정변경이 없었음에도 일정기간 내 복직명령이 없었다는 이유만으로 당연퇴직 한 것은 부당하다고 판정한 사례

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
