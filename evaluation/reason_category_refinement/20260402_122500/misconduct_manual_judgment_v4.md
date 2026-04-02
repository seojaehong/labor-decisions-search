# misconduct v4 수기 판단 메모

## 총평

- v4는 `misconduct`의 블랙홀 성향을 더 줄였다.
- 특히 `violence`, `sexual_harassment`, `workplace_bullying`, `transfer`, `probation`과 충돌하는 사건들이 `keep`보다 `needs_review`로 더 많이 이동했다.
- 완전한 자동 분리는 아니지만, 일반 비위와 특수 비위를 섞어 보여주는 문제는 v3보다 완화되었다.

## v3 대비 핵심 변화

- `keep`: `7,069 -> 6,632`
- `remove`: `290 -> 278`
- `needs_review`: `6,399 -> 6,848`

해석:

- 특수비위를 성급히 일반 `misconduct`로 keep하지 않겠다는 방향이 더 강해졌다.
- 그 대신 자동 remove보다는 review가 늘었다.

## 좋아진 점

1. `성희롱`, `성추행`, `성비위`, `불륜`, `스토킹`이 포함된 사건이 keep에서 더 잘 빠진다.
2. `폭행`, `폭언`, `협박`, `쌍방 폭행` 같은 `violence` 성격 사건도 keep 누수가 줄었다.
3. `전보`, `대기발령`, `직위해제`, `본채용 거부`, `갱신거절`이 섞인 사건이 review 쪽으로 더 이동했다.
4. `음주운전`은 여전히 `subtype=dui`로 표시되어 별도 검토가 가능하다.

## 남은 혼선

### 1. review 증가

- `징계사유`, `양정`, `절차` 같은 일반 문구는 여전히 너무 강해서, 특수비위 사건이 review에 많이 남는다.
- 이는 현재 단계에선 의도된 보수적 처리로 볼 수 있다.

### 2. 음주운전 subtype의 범위

- `dui` 보조 신호는 유용하지만, `당연퇴직`, `통상해고`, `면허취소 후 해고` 같은 후속 처분 사건은 일반 misconduct보다 별도 취급이 더 자연스럽다.
- 차기 단계에서는 `dui`를 하위유형으로 유지하면서도 `termination-after-dui` 같은 결론 문맥 분리가 가능하다.

## 결론

- `misconduct`는 v4가 v3보다 더 안전하다.
- 특히 browse/list에서 특수비위를 일반 비위로 바로 노출하는 오염을 줄이는 데는 v4가 낫다.
- DB 반영 전 최종판으로 가려면 `dui`, `violence`, `sexual_harassment`, `workplace_bullying`의 review 사례를 한 번 더 줄이는 후속 단계가 필요하다.
