# contract_expiry_batch_006_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_006_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_13581` [dismissal_validity]
  - 변경: notes
  - notes: 해고의 효력을 다투던 중 근로계약기간의 만료로 근로계약관계가 종료되어 구제의 이익이 없다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유
- `id_13617` [discrimination]
  - 변경: notes
  - notes: 이 사건 사용자가 이 사건 근로자에게 행한 계약기간 종료 처분은 부당해고에 해당한다고 판정한 사례 — discrimination 판단이 핵심
- `id_13633` [discrimination]
  - 변경: notes
  - notes: 비교대상근로자에 비하여 명절휴가보전금, 교통보조비, 정액급식비, 가족수당을 지급하지 않은 것은 합리적인 이유 없는 차별이라고 판정한 사례 — d
- `id_13643` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약기간의 만료로 인해 부당해고 구제신청의 이익이 소멸되었다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_13649` [renewal_expectation]
  - 변경: notes
  - notes: 기간의 정함이 있는 근로계약이 기간만료로 종료되었으나 갱신기대권이 있다고 보기 어려워 해고가 존재하지 않는다고 판정한 사례 — 갱신기대권 성립 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
