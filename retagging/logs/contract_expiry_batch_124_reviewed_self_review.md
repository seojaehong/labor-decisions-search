# contract_expiry_batch_124_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_124_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_8473` [discrimination]
  - 변경: notes
  - notes: 기간의 정함이 없는 근로자임에도 사용자가 계약기간 만료를 이유로 근로관계를 종료한 것은 부당해고라고 판정한 사례 — discrimination 
- `id_8485` [renewal_expectation]
  - 변경: notes
  - notes: 촉탁직 재고용 기대권이 인정되고, 촉탁직 재고용 거절에 합리적인 이유가 없어 촉탁직 재고용 거절은 부당한 해고이나, 불이익 취급 및 지배·개입의
- `id_8487` [renewal_expectation]
  - 변경: notes
  - notes: 고용이 승계되었다고 볼 만한 사정이 없어 근로자들은 기간제근로자에 해당하고, 근로자들에게 근로계약 갱신기대권이 인정된다고 볼 수 없다고 판정한 
- `id_8489` [dismissal_validity]
  - 변경: notes, secondary:[]→['misconduct', 'disciplinary_severity']
  - notes: 기자회견을 통해 사용자의 명예를 실추할 만한 표현을 사용한 행위는 징계사유로 인정되나, 그 비위행위에 비하여 해고는 징계양정이 과하여 부당하다고
- `id_8507` [dismissal_validity]
  - 변경: notes, secondary:['worker_status']→['misconduct', 'worker_status']
  - notes: 사용자에게 구제신청의 당사자 적격이 인정되며, 기간의 정함이 없는 근로자에 대한 ‘근로계약 만료’ 통지에 정당한 사유가 없어 부당한 해고로 판정

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
