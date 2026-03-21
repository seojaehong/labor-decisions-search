# contract_expiry_batch_025_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_025_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_25135` [renewal_expectation]
  - 변경: notes
  - notes: 근로계약기간이 연장될 수 있는 평가점수를 받았음에도 정규직 심사에서 탈락되었다는 사유로 근로관계를 종료한 것은 부당하다고 판정한 사례 — 갱신기
- `id_25169` [discrimination]
  - 변경: notes
  - notes: 주 15시간 미만으로 근무한다는 이유로 주 40시간 근로하는 비교대상 근로자에 비하여 정액급식비를 지급하지 않은 것은 합리적 이유 없는 차별로 
- `id_2517` [renewal_expectation]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'disciplinary_severity', 'dismissal_validity']
  - notes: 근로자에 대한 출연정지 1월의 징계는 양정이 과하지 않으며, 갱신거절에 있어 합리적 이유가 있다고 판정한 사례 — 갱신기대권 성립 여부 및 갱신
- `id_25207` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약서에 계약기간 만료일이 기재되어 있지 않으나, 건설현장 근로계약 관행을 볼 때 작업이 완료되어 근로관계가 종료된 것은 해고에 해당되지 않
- `id_25233` [discrimination]
  - 변경: notes
  - notes: 비교대상근로자들에게 지급한 근속수당, 휴일근로수당, 생일축하금 등을 근로자들에게 합리적 사유 없이 미지급 한 것은 차별적 처우라고 인정한 사례 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
