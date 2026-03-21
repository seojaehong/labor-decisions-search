# misconduct_remaining_batch_027_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_027_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_2439` [misconduct]
  - 변경: notes, secondary:['disciplinary_severity']→['procedure', 'disciplinary_severity']
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 견책의 징계가 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정
- `id_24395` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 공공기관 근로자의 금품·향응 수수, 고객정보 유출 등에 따른 해임처분은 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_24401` [disciplinary_severity]
  - 변경: notes
  - notes: 공공기관 소속 근로자가 퇴직자 출신의 직무관련자를 상대로 금품수수, 고객정보 유출 및 무단열람, 사적 접촉 등을 한 것에 대하여 정직 1월은 정
- `id_24405` [misconduct]
  - 변경: notes
  - notes: 사용자에게 고용승계 의무가 인정되고, 비위행위 등 특별한 귀책사유의 유무에 따라 고용승계 거부가 정당 또는 부당하다 — 비위행위 존재 및 중대성
- `id_24409` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자의 금품·향응 수수, 고객정보 유출 및 무단열람, 직무관련자와 사적 접촉 등의 비위행위에 대한 징계해고는 정당하다고 판정한 사례 — 징계양

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
