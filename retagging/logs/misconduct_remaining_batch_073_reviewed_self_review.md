# misconduct_remaining_batch_073_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_073_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_402923` [disciplinary_severity]
  - 변경: notes
  - notes: '배우자 명의 업체와의 부당 거래 등’의 징계사유가 인정되고, 징계양정도 징계재량권을 남용하였다고 볼 수 없으며, 징계절차의 위법이 있다고도 볼
- `id_402933` [misconduct]
  - 변경: notes
  - notes: 근로자들이 사용자의 스타트 미팅 참여 지시를 정당한 사유 없이 불이행한 사실이 확인되어 징계사유가 존재하고, 감봉의 징계처분이 정당하다고 판정한
- `id_402935` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 모두 인정되고, 징계양정이 과도하지 않으며, 징계절차가 위법하지 않아 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 
- `id_402937` [disciplinary_severity]
  - 변경: notes
  - notes: 동료 근로자에 대한 폭언 및 욕설 등의 행위를 하여 위화감을 조성하고 정신적 고통을 가한 행위, 정당한 이유 없이 근무지를 이탈하고 사용자의 승
- `id_402939` [procedure]
  - 변경: notes
  - notes: 사용자가 주장하는 징계사유 중 일부만 인정되고 비위의 정도와 과실이 징계양정 기준에 부합하지 않아 양정이 과하므로 강등은 부당하다고 판정한 사례

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
