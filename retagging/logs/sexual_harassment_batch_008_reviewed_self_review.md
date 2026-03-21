# sexual_harassment_batch_008_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_008_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_37089` [disciplinary_severity]
  - 변경: notes
  - notes: 하급자의 외모를 평가한 발언을 지속적으로 하여 직장 내 성희롱을 한 근로자에 대한 감봉 3월의 징계는 정당하다고 판정 — 징계양정(제재 수위)의
- `id_37101` [unfair_treatment]
  - 변경: notes
  - notes: 협력업체의 여직원에게 행한 언행은 언어적 성희롱에 해당되어 징계사유가 되나, 징계이력이 없고 의도적으로 이루어졌다고 보기 어려운 점 등으로 해고
- `id_37183` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자가 해고통지서의 수령을 거부하였으나, 해고통보서가 근로자에게 적법하게 도달된 것으로 보아 해고가 정당하다고 판정한 사례 — 징계양정(제재 
- `id_37239` [disciplinary_severity]
  - 변경: notes, secondary:['procedure']→['misconduct', 'procedure']
  - notes: 성희롱 등의 징계사유가 인정되고, 징계양정이 적정하며, 절차상 하자도 없어 징계처분은 정당하다고 판단한 사례 — 비위 인정이나 해고·징계 수위가
- `id_37305` [disciplinary_severity]
  - 변경: notes
  - notes: 풍기문란, 성희롱 및 성폭행의 징계사유 모두가 인정되고 해고의 양정은 적정하며 징계절차에도 하자가 없으므로 해고는 정당하다고 판정한 사례 — 징

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
