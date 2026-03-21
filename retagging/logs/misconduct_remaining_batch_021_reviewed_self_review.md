# misconduct_remaining_batch_021_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_021_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_21059` [unfair_treatment]
  - 변경: notes
  - notes: 징계사유는 인정되나 그에 대한 해고처분은 형평성에 어긋나 재량권의 남용에 해당하지만, 부당노동행위는 아니라고 판정한 사례 — 부당노동행위(불이익
- `id_21067` [disciplinary_severity]
  - 변경: notes
  - notes: 공기업 직원으로서 직무관련자로부터 향응 등을 제공받은 것을 사유로 해임한 것은 정당하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 
- `id_21071` [disciplinary_severity]
  - 변경: notes
  - notes: 예약일자 확인 소홀로 결혼식에 혼선을 초래한 근로자에 대한 정직 6월의 징계는 양정이 과하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 
- `id_21075` [unfair_treatment]
  - 변경: notes
  - notes: 노동조합 위원장이 파업지침을 통해 조합원들의 시간외근로 거부 및 연차휴가사용을 독려하여 쟁의행위를 주도한 결과 필수유지업무 협정서 상의 유지율이
- `id_21103` [disciplinary_severity]
  - 변경: notes
  - notes: 일부 징계사유의 정당성은 인정되나 양정이 과하여 부당해고라고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
