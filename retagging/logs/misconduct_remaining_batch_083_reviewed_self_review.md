# misconduct_remaining_batch_083_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_083_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_407785` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고 비위행위의 정도를 고려할 때 해고의 징계는 징계양정이 과도하지 않으며 징계절차상 하자가 없으므로 정당하다고 판정한 사례 — 
- `id_40779` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 인정되고, 비위행위에 비해 양정이 과하다고 볼 수 없으며, 징계 절차상 하자도 없어 정직 처분이 정당하다고 판정한 사례 — 비위 인정
- `id_407803` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 징계사유가 인정되고, 징계절차상 하자도 없으나, 징계처분이 형평의 원칙에 반하여 부당한 징계라고 판정한 사례 — 징계·해고 절차 하자가 결론을 
- `id_407809` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 1차 해고는 임금상당액이 모두 지급되어 구제이익이 없고, 2차 해고는 사유와 절차 모두 부당하다고 판단한 사례 — 징계·해고 절차 하자가 결론을
- `id_40781` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 버스 운행 중 휴대폰 사용이라는 징계사유가 인정되고, 감봉 6개월의 처분은 양정이 과도하지 않으며, 절차에 하자가 없어 정당하다고 판정한 사례 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
