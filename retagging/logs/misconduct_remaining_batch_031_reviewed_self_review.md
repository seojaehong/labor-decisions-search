# misconduct_remaining_batch_031_reviewed 2nd-pass self-review

- 배치: `misconduct_remaining_batch_031_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_27141` [disciplinary_severity]
  - 변경: notes
  - notes: 근로자에게 부과한 정직 1개월의 처분은 징계사유에 비하여 징계양정이 과다하다고 판정한 사례 — 징계양정(제재 수위)의 적정성이 핵심 쟁점
- `id_27147` [disciplinary_severity]
  - 변경: notes
  - notes: 주차요금 징수업무 담당자가 885건의 주차요금 총 1,863,200원을 횡령한 행위에 대하여 징계해고는 정당하다고 판정한 사례 — 징계양정(제재
- `id_27155` [disciplinary_severity]
  - 변경: notes
  - notes: 항공사의 VIP 고객 정보를 외부로 유출한 것을 징계사유로 삼은 것은 정당하나 비위행위의 정도에 비하면 양정이 과하다고 판정한 사례 — 징계양정
- `id_27157` [misconduct]
  - 변경: notes
  - notes: 징계사유가 인정되고, 징계양정에 하자가 없으므로 정직처분은 정당하다고 판정한 사례 — 비위행위 존재 및 중대성이 해고 정당성을 직접 좌우
- `id_27159` [misconduct]
  - 변경: notes
  - notes: 배차 제외는 승무정지의 징계처분에 해당하고 징계사유의 정당성이 인정되지 아니하여 부당하며, 정직은 징계사유의 정당성이 인정되지 아니하여 부당하다

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
