# contract_expiry_batch_079_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_079_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_410757` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간 만료일 이후에 구제신청을 제기하여 구제이익이 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_410761` [dismissal_validity]
  - 변경: notes
  - notes: 본채용 거부에 객관적으로 합리적인 이유가 존재한다고 보기 어려우므로 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_41077` [unfair_treatment]
  - 변경: notes, secondary:['procedure', 'dismissal_validity']→['procedure', 'renewal_expectation', 'dismissal_validity']
  - notes: 근로계약기간 만료로 근로관계가 정당하게 종료되었고, 부당노동행위에도 해당하지 않는다고 판정한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 
- `id_410803` [renewal_expectation]
  - 변경: notes, secondary:['dismissal_validity']→['attendance', 'dismissal_validity']
  - notes: 근로자의 근로계약기간 만료일은 2025. 7. 2.이며, 정규직 전환 기대권이 인정되지 않으므로 근로계약기간 만료로 근로관계를 종료한 것은 정당
- `id_410805` [dismissal_validity]
  - 변경: notes
  - notes: 구제신청의 구제이익이 있고 해고가 존재하며 경영상 이유에 의한 해고의 요건을 갖추지 못하여 부당하다고 판정한 사례 — 해고 사실 자체의 존부 또

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
