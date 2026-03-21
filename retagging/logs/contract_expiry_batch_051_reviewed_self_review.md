# contract_expiry_batch_051_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_051_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_349973` [renewal_expectation]
  - 변경: notes
  - notes: 근로자는 기간제법 제4조제1항의 예외 사유에 해당하는 기간제근로자로 근로계약의 갱신기대권이 존재한다고 보기 어려워 계약만료로 근로관계가 종료되었
- `id_349985` [renewal_expectation]
  - 변경: notes
  - notes: 기각(갱신기대권) — 갱신기대권 성립 여부 및 갱신거절 합리성이 핵심
- `id_34999` [renewal_expectation]
  - 변경: notes
  - notes: 근로관계가 종료 후 공백기간을 두고 공개채용절차를 통해 새로운 근로계약을 체결한 경우에도 업무가 상시적이고 연속하여 4차례 계속해서 근무한 점을
- `id_349995` [renewal_expectation]
  - 변경: notes
  - notes: 이 사건 촉탁직 근로관계는 이 사건 근로자의 사직원 제출로 인하여 상호 합의하에 계약기간 만료로 종료되었다 할 것이고, 이 사건 사용자가 부당노
- `id_350005` [dismissal_validity]
  - 변경: notes
  - notes: 근로계약관계가 이미 종료된 후 구제신청이 제기되어 구제이익이 존재하지 아니한다고 판정한 사례 — 해고 사실 자체의 존부 또는 처분 유효성이 쟁점

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
