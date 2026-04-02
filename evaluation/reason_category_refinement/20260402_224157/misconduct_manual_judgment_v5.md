# misconduct v5 수기 판단 메모

## 총평

v5는 `misconduct`를 일반 비위행위의 코어로 더 잘 좁혔다. 특수 비위(`violence`, `embezzlement`, `sexual_harassment`, `workplace_bullying`)와 인사처분/채용단계(`transfer`, `probation`) 누수가 `keep`보다 `lean_remove`로 이동한 점이 핵심이다.

## 유지 타당

- `비위행위`, `징계사유`, `취업규칙/복무규정 위반`
- `허위 보고`, `거짓 기재`, `지시 불이행`, `무단결근`, `무단외출`
- `주의의무/성실의무/복무의무 위반`

## 제거 또는 이관 타당

- `폭행`, `상해`, `욕설`, `폭언`, `위협` -> `violence`
- `횡령`, `배임`, `공금`, `법인카드`, `유용` -> `embezzlement`
- `성희롱`, `성추행` -> `sexual_harassment`
- `직장 내 괴롭힘` -> `workplace_bullying`
- `전보`, `대기발령`, `직위해제` -> `transfer`
- `본채용 거부`, `시용`, `수습` -> `probation`

## 음주운전 subtype 판단

- `dui`
  - 음주운전 자체가 징계사유로 언급되는 일반 비위형
- `dui_termination`
  - `당연퇴직`, `면허취소`, `운전직`, `통상해고`가 결합된 후속 처분형

실무상 음주운전은 `misconduct`의 하위유형으로 유지하는 방향이 타당하다. 다만 browse/list 주카테고리에서는 일반 비위와 바로 섞지 않고, 하위유형으로 남기는 편이 좋다.

## review_sub_bucket 해석

- `lean_remove`
  - 이미 다른 특수 비위나 인사처분 축으로 갈 근거가 강하다.
  - 다음 라운드 자동 이관 1순위다.
- `lean_keep`
  - 일반 비위에 가깝지만 요약 품질이나 혼합 문맥 때문에 review로 남은 케이스다.
- `ambiguous`
  - `근무태만`, `업무 미이행`, `징계양정`처럼 행위 위반과 성과/절차 문맥이 섞인 사례다.

## 다음 보정 포인트

1. `lean_remove`를 `violence / sexual_harassment / workplace_bullying / embezzlement / transfer / probation`로 자동 이관하는 규칙을 검토한다.
2. `dui`와 `dui_termination`는 별도 표시 정책을 두고 일반 `misconduct`와 분리한다.
3. `ambiguous` 중 `근무태만/업무 미이행`은 `incompetence`와의 경계 규칙을 더 세운다.
