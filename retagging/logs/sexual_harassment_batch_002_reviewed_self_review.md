# sexual_harassment_batch_002_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_002_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_14495` [disciplinary_severity]
  - 변경: notes
  - notes: 일부 성희롱 사실이 징계사유로 인정되나, 양정이 과하여 해고가 부당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_14651` [disciplinary_severity]
  - 변경: notes, secondary:[]→['misconduct']
  - notes: 성폭력 범죄 관련 유죄판결과 무단으로 하드 디스크 교체한 것에 대한 징계해고가 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 
- `id_14655` [misconduct]
  - 변경: notes
  - notes: 성희롱의 행위가 지속적이고 반복적으로 이루어진 것을 이유로 해임 처분한 것은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을
- `id_14703` [disciplinary_severity]
  - 변경: notes
  - notes: 성희롱 관리자에 대한 정직처분은 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_14859` [misconduct]
  - 변경: notes
  - notes: 사용자의 언론의 자유 범위내에서 이루어진 노동조합과 관련된 발언은 지배개입의 부당노동행위에 해당되지 않는다고 판정한 사례 — 비위행위 존재 및 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
