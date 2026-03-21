# misconduct_remaining_batch_067_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_067_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_399925` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고 징계절차상 하자는 없으나, 징계사유에 비하여 양정이 과하여 부당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한
- `id_399943` [unfair_treatment]
  - 변경: notes
  - notes: 근로자의 진정ㆍ고소와 같은 다수의 신고 제기 행위, 상급자에 대한 폭력적인 언행, 직장 내 현수막 게시 등의 비위행위의 동기와 경위, 조직 질서
- `id_399945` [unfair_treatment]
  - 변경: notes
  - notes: 근로자가 지속 반복적으로 배차간격 문제를 야기한 사실이 인정되고, 이에 대한 여러 차례 사용자의 개선 요구에도 불구하고 실질적으로 개선되지 않아
- `id_399965` [disciplinary_severity]
  - 변경: notes
  - notes: 대기발령은 정당하고, 징계사유 대부분이 불인정되어 해고의 징계양정이 과도하고, 징계처분 통지서를 받기 전까지 징계사유 중 일부를 근로자가 인지하
- `id_39997` [misconduct]
  - 변경: notes
  - notes: "기각"징계사유가 인정되고, 징계양정이 타당하며, 징계절차에 하자가 없다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
