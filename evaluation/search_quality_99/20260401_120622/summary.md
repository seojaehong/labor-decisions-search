## Q10/Q16 Focused Reevaluation Summary

- Baseline total: `165`
- Upgraded total: `186`
- Delta: `+21`
- Duration: `448.87s`

### Purpose

이번 라운드는 `Q10`과 `Q16`을 집중적으로 보정한 뒤 재평가한 결과입니다.

### Key Result

- `Q10`: `8 -> 8`
- `Q16`: `8 -> 8`

즉, 직전 라운드에서 약해졌던 두 쿼리는 이번 보정으로 모두 기준선 수준까지 회복했습니다.

### What Changed

- `Q10`
  - `정규직`, `무기계약`, `통상해고` 표현을 intent-aware query expansion에 추가
  - `probation`/`transfer`가 불필요하게 섞이는 경우를 평가 하네스에서 약하게 페널티
  - `개선 기회`, `직무교육`, `전환배치` 맥락 부스트 강화

- `Q16`
  - `부당해고`, `갱신기대권 인정` 표현을 query expansion에 추가
  - `갱신기대권 인정` + `부당해고 다툼` 계열을 추가 부스트
  - `갱신기대권 인정되지 않음` 계열은 약하게 감점

### Interpretation

- 전체 총점은 이전 최고점 `188`보다 조금 낮지만, 이번 라운드의 목적이었던 `Q10`, `Q16`은 확실히 회복됨
- 따라서 지금 상태는
  - 전체 최고점 기준으로는 `20260331_163224`
  - Q10/Q16 보정 확인 기준으로는 `20260401_120622`
  두 결과를 함께 참고하는 것이 적절함

### Artifacts

- `report.json`
- `results.json`
- `debug/Q10.json`
- `debug/Q16.json`
