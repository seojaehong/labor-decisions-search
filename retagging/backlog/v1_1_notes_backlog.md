# v1.1 Notes Backlog

## 성격

- 긴급 수정 아님
- 메인 업로드 흐름과 분리
- 다음 세션에서 바로 착수 가능한 `notes 보강 작업 큐`

## 대상 요약

### A. confidence=`medium` + notes 공란

- 총 `34건`
- 우선순위 `P1`
- 이유:
  - confidence가 `medium`이면 애매성 근거가 notes에 반드시 남는 편이 좋음
  - merged 기준 품질 설명력과 디버깅 가치를 가장 크게 올림

### B. workplace_bullying 001~005 blank notes

- 총 `129건`
- 이 중 A와 겹치는 건 `28건`
- 순수 추가 작업량은 `101건`
- 우선순위 `P2`
- 이유:
  - 초반 배치 공란 notes 정리
  - 주제군별 설명 품질 일관성 확보

## 권장 작업 순서

1. `P1` `34건` 먼저 처리
2. 그중 `workplace_bullying 001~005`와 겹치는 `28건`은 한 번에 같이 닫기
3. 이후 `P2`의 나머지 `101건` 처리

## 작업 방식 초안

### 공통 원칙

- notes는 길게 쓰기보다 `왜 이 primary로 잡았는지`를 한 문장으로 명확히 남긴다
- retrieval_note를 그대로 복붙하지 말고, `판단 근거` 문장으로 바꾼다
- 아래 구조를 기본 템플릿으로 사용한다

### notes 기본 템플릿

- `배경상 [주제] 언급은 있으나, 결론 중심은 [실제 핵심 쟁점]이라 [primary]로 정리.`
- `괴롭힘/결근/수습 등 표면 사유보다 [판단구조]가 결론을 좌우해 [primary]를 유지.`
- `복합 사건이나 [경계 사유]가 있어 confidence=medium으로 두고 후속 검토 여지를 남김.`

### primary별 권장 notes 문구 초안

- `disciplinary_severity`
  - `표면상 [주제] 사건이지만 실제 결론은 징계 수위의 상당성 판단이어서 disciplinary_severity로 정리.`
- `unfair_treatment`
  - `괴롭힘 사실 자체보다 신고 이후 불이익 처우·전보·인사조치의 정당성이 중심이라 unfair_treatment로 정리.`
- `dismissal_validity`
  - `배경 갈등과 별개로 최종 쟁점은 근로관계 종료의 존부·정당성이어서 dismissal_validity를 유지.`
- `procedure`
  - `실체 사유보다 서면통지·소명기회 등 절차 하자가 결론을 좌우해 procedure로 정리.`
- `renewal_expectation`
  - `괴롭힘 배경은 있으나 핵심은 갱신거절·전환거절의 합리성과 기대권 판단이라 renewal_expectation으로 정리.`
- `misconduct`
  - `괴롭힘 자체보다 복합 비위의 존부와 입증 여부가 핵심이라 misconduct로 정리.`
- `workplace_harassment`
  - `핵심은 괴롭힘 성립 여부와 그에 대한 사용자 조치 판단이라 workplace_harassment로 정리.`

## 작업 단위 제안

### 세션 1

- `34건` medium blank notes 전부
- 목표:
  - merged 품질 설명력 보강
  - medium 해석 가능성 확보

### 세션 2

- `workplace_bullying_batch_001~003`
- 목표:
  - 초반 bullying 배치 공란 감소

### 세션 3

- `workplace_bullying_batch_004~005`

## P1 대상: confidence=`medium` + notes blank 34건

### [absence_batch_001_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/absence_batch_001_reviewed.jsonl)

- `id_11047` | `disciplinary_severity` | 무단결근/근무지 이탈이 핵심 또는 주요 징계사유

### [probation_batch_003_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_003_reviewed.jsonl)

- `id_13355` | `misconduct` | 업무지시 불이행·허위기재 등 비위성 사유가 중심이 된 수습·시용 중 종료 사건
- `id_14245` | `dismissal_validity` | 시용·수습 관련성은 있으나 실질 쟁점에 따라 본채용 거부의 정당성이 문제 된 사건

### [probation_batch_004_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_004_reviewed.jsonl)

- `id_14829` | `dismissal_validity` | 시용·수습 관련성은 있으나 실질 쟁점에 따라 해고의 정당성이 문제 된 사건
- `id_15099` | `misconduct` | 업무지시 불이행·허위기재 등 비위성 사유가 중심이 된 해고 사건

### [probation_batch_005_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/probation_batch_005_reviewed.jsonl)

- `id_16299` | `procedure` | 해고의 절차 하자가 결론을 좌우한 사건

### [workplace_bullying_batch_001_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_001_reviewed.jsonl)

- `id_10819` | `renewal_expectation` | 괴롭힘 배경이 있으나 핵심은 전환·갱신거절의 합리성인 사건
- `id_10929` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_10989` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건
- `id_11021` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_11245` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_11761` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건

### [workplace_bullying_batch_002_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_002_reviewed.jsonl)

- `id_11999` | `misconduct` | 괴롭힘 외 복합 비위와 징계사유 존부가 중심인 사건
- `id_12075` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건
- `id_12333` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_12359` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_12423` | `procedure` | 괴롭힘 관련 사실보다 절차 하자가 결론을 좌우한 사건
- `id_12583` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건
- `id_12679` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건

### [workplace_bullying_batch_003_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_003_reviewed.jsonl)

- `id_1513` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_1763` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_18983` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건
- `id_1989` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_21941` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_21959` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건
- `id_22973` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건

### [workplace_bullying_batch_004_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_004_reviewed.jsonl)

- `id_2383` | `renewal_expectation` | 괴롭힘 배경이 있으나 핵심은 전환·갱신거절의 합리성인 사건
- `id_253` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_2605` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_2941` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건

### [workplace_bullying_batch_005_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_005_reviewed.jsonl)

- `id_343745` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_343775` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_343955` | `disciplinary_severity` | 괴롭힘 언급이 있으나 결론 중심은 징계양정 판단인 사건
- `id_344161` | `unfair_treatment` | 괴롭힘 신고·보호조치·전보 등 불이익 처우 또는 인사조치가 중심인 사건

## P2 대상: workplace_bullying 001~005 blank notes 전체 129건

### [workplace_bullying_batch_001_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_001_reviewed.jsonl) — 21건

- `id_10819`
- `id_10901`
- `id_10913`
- `id_10929`
- `id_10963`
- `id_10989`
- `id_10991`
- `id_10995`
- `id_11021`
- `id_11137`
- `id_11245`
- `id_11277`
- `id_11339`
- `id_11387`
- `id_11595`
- `id_11619`
- `id_11693`
- `id_11717`
- `id_11761`
- `id_11829`
- `id_11877`

### [workplace_bullying_batch_002_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_002_reviewed.jsonl) — 26건

- `id_11911`
- `id_11981`
- `id_11999`
- `id_12013`
- `id_12065`
- `id_12075`
- `id_12117`
- `id_12171`
- `id_12189`
- `id_12333`
- `id_12335`
- `id_12359`
- `id_12383`
- `id_12423`
- `id_12485`
- `id_12491`
- `id_12497`
- `id_12573`
- `id_12583`
- `id_12593`
- `id_12609`
- `id_12667`
- `id_12679`
- `id_13297`
- `id_1331`
- `id_1409`

### [workplace_bullying_batch_003_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_003_reviewed.jsonl) — 28건

- `id_1513`
- `id_1521`
- `id_1551`
- `id_1577`
- `id_16071`
- `id_1611`
- `id_1615`
- `id_1643`
- `id_1757`
- `id_1763`
- `id_1813`
- `id_18237`
- `id_18545`
- `id_1855`
- `id_18983`
- `id_1987`
- `id_1989`
- `id_199`
- `id_20027`
- `id_2077`
- `id_2111`
- `id_213`
- `id_21815`
- `id_21941`
- `id_21959`
- `id_2267`
- `id_22973`
- `id_2313`

### [workplace_bullying_batch_004_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_004_reviewed.jsonl) — 29건

- `id_2351`
- `id_23811`
- `id_2383`
- `id_24097`
- `id_2475`
- `id_2491`
- `id_253`
- `id_255`
- `id_2573`
- `id_2591`
- `id_2605`
- `id_2629`
- `id_265`
- `id_26813`
- `id_2837`
- `id_2861`
- `id_28809`
- `id_2915`
- `id_2941`
- `id_2951`
- `id_2971`
- `id_2999`
- `id_3109`
- `id_31357`
- `id_3187`
- `id_32351`
- `id_33465`
- `id_3349`
- `id_33627`

### [workplace_bullying_batch_005_reviewed.jsonl](C:/dev/labor-decisions-search/retagging/output/reviewed/workplace_bullying_batch_005_reviewed.jsonl) — 25건

- `id_3381`
- `id_343629`
- `id_343679`
- `id_343685`
- `id_343745`
- `id_343775`
- `id_343921`
- `id_343955`
- `id_343983`
- `id_344023`
- `id_344145`
- `id_344149`
- `id_344161`
- `id_344265`
- `id_344297`
- `id_344413`
- `id_344423`
- `id_344557`
- `id_344573`
- `id_344583`
- `id_344621`
- `id_344653`
- `id_344695`
- `id_344815`
- `id_344869`

## 다음 세션 한 줄 지시문

- `P1`: medium + notes blank 34건 먼저 보강
- `P2`: workplace_bullying 001~005 blank notes 나머지 101건 보강
- 기준본은 유지하고 notes만 보충
- 메인 업로드 흐름과 merge 결과는 건드리지 않음
