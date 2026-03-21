# misconduct_remaining_batch_019_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_019_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_20081` [misconduct]
  - 변경: notes
  - notes: 징계사유가 존재하지 않는다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_20083` [disciplinary_severity]
  - 변경: notes
  - notes: 시설 생활인에 대한 용의지도 의무 불이행에 대한 징계사유가 인정되어 경고장을 발부한 징계처분은 정당하다고 판정한 사례 — 비위 인정이나 해고·징
- `id_20089` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유 중 세입·세출결산표 허위기재 방관의 사유만이 인정되고 양정이 과하여 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁
- `id_20113` [procedure]
  - 변경: notes, conf:medium→high
  - notes: 근로자의 비위행위가 징계사유에는 해당되나, 절차상 하자가 있고 징계양정도 과하다고 판정한 사례 — 징계·해고 절차 하자가 결론을 직접 좌우
- `id_20123` [unfair_treatment]
  - 변경: notes
  - notes: 비위행위에 대해 훈계적 차원에서 이루어진 경고는 구제신청 대상에 해당되지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
