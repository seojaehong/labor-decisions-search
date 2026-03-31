## 24-query Reevaluation Summary

- Baseline total: `165`
- Upgraded total: `188`
- Delta: `+23`
- Duration: `429.06s`

### Overall

이번 라운드는 intent-aware candidate expansion과 `workplace_bullying + retaliation` 보정이 반영된 상태에서 재평가한 결과입니다. 이전 최고치보다도 크게 올라가면서, 약점이던 보복/불이익, 괴롭힘 불인정, 양정과다 계열이 전반적으로 회복됐습니다.

### Strong Improvements

- `Q05`: `4 -> 7`
- `Q20`: `6 -> 8`
- `Q23`: `8 -> 6`
- `Q03`: 개선 유지
- `Q11`: 개선 유지
- `Q13`: 상위권 유지
- `Q14`: 상위권 유지
- `Q22`: 개선 유지
- `Q24`: 개선 유지

### Focus Query Results

#### Q05

- Result: `4 -> 7`
- 핵심 변화: `직장내괴롭힘 신고 후 보복/불이익`을 단순 `불이익 취급` 일반 사건으로 흘리지 않고, `직위해제`, `전보`, `보직해임`, `대기발령` 같은 실제 인사불이익 액션까지 후보 확장에 반영한 것이 효과적이었습니다.

#### Q10

- Result: `8 -> 7`
- 해석: 큰 폭의 회복은 아니지만, 정규직 저성과/업무능력 부족 축은 여전히 안정적으로 찾고 있습니다. 추가 보정은 가능하지만 현재 우선순위는 아닙니다.

#### Q16

- Result: `8 -> 6`
- 해석: `갱신거절`, `사실상 해고`, `실질적 해고` 표현을 더 반영했지만 아직 완전 회복은 아닙니다. 다음 보정 대상으로 남겨둘 가치가 있습니다.

#### Q20

- Result: `6 -> 8`
- 핵심 변화: `violence + severity_check`에 대해 `양정과다`, `과중`, `징계 과도`, `해고 과중`을 더 직접적으로 넣으면서, 폭행은 인정되나 해고가 과도하다고 본 사례가 상위권으로 더 안정적으로 올라왔습니다.

#### Q23

- Result: `8 -> 6`
- 핵심 변화: `괴롭힘 불인정/미해당`과 `신고/요구/불이익/보복`을 동시에 만족하는 사건을 따로 끌어올리면서, 이전처럼 전혀 다른 `union_activity` 사건으로 흐르던 문제가 많이 줄었습니다.

### What Changed

- retrieval 직전 query expansion에 `intent`를 반영
- `workplace_bullying + retaliation` 계열은 일반 불이익 사건이 아니라 실제 인사상 불이익 액션까지 포함해 검색
- `union_activity` 중심의 generic 부당노동행위 결과는 상대적으로 덜 올라오도록 조정
- 약한 쿼리용 debug artifact 자동 생성

### Remaining Weakness

- `Q16`은 여전히 완전한 회복 전
- `Q10`은 소폭 하락
- 다음 단계가 필요하다면 `contract_expiry + 사실상 해고` 분기를 별도로 더 세우는 것이 가장 유력

### Artifacts

- `report.json`
- `results.json`
- `debug/Q05.json`
- `debug/Q10.json`
- `debug/Q16.json`
- `debug/Q20.json`
- `debug/Q23.json`
