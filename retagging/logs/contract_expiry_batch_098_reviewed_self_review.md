# contract_expiry_batch_098_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_098_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_49069` [unfair_treatment]
  - 변경: notes
  - notes: 근로자에게 정규직 전환기대권은 인정되나 정규직 전환거절에 합리적 이유가 있어 근로관계 종료는 정당하고, 불이익 취급의 부당노동행위에 해당하지 않
- `id_4907` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약 기간 만료로 근로관계가 종료된 것으로 해고는 존재하지 않는다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점
- `id_49081` [dismissal_validity]
  - 변경: notes
  - notes: □ 홍○○ 팀장의 2022. 6. 18. 07:39 “그동안 고생하셨습니다.”의 문자를 근거로 이 사건 근로자11인 홍○○ 팀장은 자진하여 퇴사
- `id_49099` [discrimination]
  - 변경: notes
  - notes: 차별적 처우 시정신청의 제척기간을 도과하였다고 판정한 사례 — discrimination 판단이 핵심
- `id_49117` [renewal_expectation]
  - 변경: notes, conf:high→medium
  - notes: 근로자1은 기간제법 기간제한의 예외 사유에 해당하여 2년 후 무기계약 근로자로 전환되었다고 볼 수 없고, 근로자들은 위·수탁관리계약의 종료와 함

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
