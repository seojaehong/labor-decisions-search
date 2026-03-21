# misconduct_remaining_batch_030_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_030_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_26495` [disciplinary_severity]
  - 변경: notes
  - notes: 사용자가 유인물 무단 배포 등으로 행한 징계에 대하여 우리 위원회의 최초 판정 등에 따라 징계양정을 상당 수준 감경하여 재징계처분한 것은 정당하
- `id_26515` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 교통사고, 승객 중도하차, 신용카드 가장매출 등의 징계사유 중 일부 징계사유의 정당성이 인정되고, 인정된 징계사유 만으로도 승무정지 75일의 징
- `id_26521` [unfair_treatment]
  - 변경: notes
  - notes: 인정(근로자1, 3 부당정직, 불이익취급 부당노동행위)각하(근로자2, 4 부당정직), 기각(지배,개입 부당노동행위) — 부당노동행위(불이익취급·
- `id_26527` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 공공기관 근로자의 금품·향응 수수, 고객정보 유출 등에 따른 해임처분은 정당하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_26549` [dismissal_validity]
  - 변경: notes, conf:medium→high
  - notes: 근로자가 사용자에게 사직의 의사를 표시하고 사용자가 이를 수리함으로써 근로관계가 종료된 것이므로 해고가 존재하지 않는다고 판정한 사례 — 해고 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
