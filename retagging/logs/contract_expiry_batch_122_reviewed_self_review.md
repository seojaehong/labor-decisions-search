# contract_expiry_batch_122_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_122_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_7467` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로계약을 체결한 근로자로 볼 수 없고 근로계약 갱신기대권이 존재하지 않으므로 근로계약기간 만료로 근로관계를 종료한 것은 정
- `id_7479` [dismissal_validity]
  - 변경: notes
  - notes: 사내협력업체의 영업을 양도·양수하여 근로자 지위가 승계되었음에도 기간제 근로계약을 체결하고, 계약기간의 만료를 이유로 고용관계를 종료한 것은 부
- `id_7485` [discrimination]
  - 변경: notes, secondary:['procedure', 'dismissal_validity', 'renewal_expectation']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 갱신기대권이 존재하고 갱신거절의 합리적 이유가 없다고 판정한 사례 — discrimination 판단이 핵심
- `id_7489` [unfair_treatment]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 관리자가 노동조합 조합원에게 노동조합 탈퇴 종용의 발언을 한 행위는 지배·개입의 부당노동행위에 해당하나, 촉탁직 조합원들의 근로계약 종료가 사용
- `id_749` [unfair_treatment]
  - 변경: notes, conf:high→medium
  - notes: 사용자들이 도급계약 만료에 따라 현장 소속 근로자들과 근로관계를 종료한 것이 지배·개입 및 불이익취급의 부당노동행위에 해당되지 않는다고 판정한 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
