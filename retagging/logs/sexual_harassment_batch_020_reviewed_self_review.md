# sexual_harassment_batch_020_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_020_reviewed`
- 2차 패스 처리 건수: 43
- 실질 변경 건수: 43
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_6829` [disciplinary_severity]
  - 변경: notes
  - notes: 취업규칙에서 정한 징계 사유가 인정되며, 징계 양정과 절차상의 하자가 없으므로 해고는 정당하고, 불이익 취급의 부당노동행위에 해당하지 않는다고 
- `id_683` [misconduct]
  - 변경: notes
  - notes: 임금 등 경제적 불이익만 있고 법률상 불이익이 없으며, 동일한 사유로 후속처분인 징계해고가 있어 인사대기 명령은 실효되었으므로 구제이익이 없다고
- `id_6851` [misconduct]
  - 변경: notes
  - notes: 사용자가 근로자의 징계사유로 삼은 성추행과 언어적 성희롱 행위는 피해자의 사유서 및 진술만으로 근로자가 위 행위를 하였다고 보기 어려워 근로자의
- `id_6913` [disciplinary_severity]
  - 변경: notes
  - notes: 징계사유가 존재하고, 징계양정도 적정하며, 징계절차에도 하자가 없어 정당하다고 판정한 사례 — 비위 인정이나 해고·징계 수위가 과중한지 여부가 
- `id_6961` [misconduct]
  - 변경: notes, secondary:['procedure', 'disciplinary_severity']→['procedure', 'disciplinary_severity', 'workplace_harassment']
  - notes: 전부 기각직위해제는 구제이익이 존재하나, 업무상 필요성이 인정되고, 생활상 불이익이 크지 않아 정당하며, 감봉 1개월 징계는 사유가 인정되고, 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
