# manual recheck: workplace_bullying_batch_025

Batch 025 was reviewed case by case from the input JSONL and the final reviewed JSONL was aligned to the actual holding structure of each case.

## Case-by-case review

- `id_410457`: 직위해제·대기발령의 업무상 필요성과 생활상 불이익, 절차 적법성이 핵심이어서 `transfer_validity`로 유지.
- `id_410485`: 직장 내 괴롭힘 사실과 절차 하자, 양정 과다를 함께 보되 핵심은 징계양정의 과중 여부라 `disciplinary_severity`.
- `id_410489`: 괴롭힘 사실이 전제되고 징계양정과 절차가 모두 정당한 전형적 양정 사건이라 `disciplinary_severity`.
- `id_410509`: 성희롱과 직장 내 괴롭힘 비위가 인정되고 부당노동행위 여부도 함께 다뤄지지만 핵심은 징계해고의 정당성이라 `disciplinary_severity`.
- `id_410517`: 다수의 괴롭힘·성희롱·음주 비위에 대한 징계해고 사안으로, 양정과 절차가 핵심이라 `disciplinary_severity`.
- `id_410519`: 업무지시 불이행, 괴롭힘, 2차 가해, 업무방해가 누적된 징계해고 사건으로 `disciplinary_severity`.
- `id_410579`: 초기에는 보복성 불이익처럼 보일 수 있으나, 실제로는 문서조작·허위제출 비위에 대한 징계양정이 핵심이어서 `disciplinary_severity`.
- `id_410599`: 이중징계와 개별 징계사유 특정 가능성이 쟁점인 해고 사건으로 `disciplinary_severity`.
- `id_410665`: 대기발령과 정직의 정당성, 그리고 직장 내 괴롭힘·성희롱 비위의 징계양정이 함께 검토되어 `disciplinary_severity`.
- `id_410697`: 성희롱, 괴롭힘, 2차 가해, 조직 질서 문란이 모두 징계사유로 인정된 징계해고 사건이라 `disciplinary_severity`.
- `id_410701`: 보안규정 위반과 업무태만이 주축이고 괴롭힘은 일부 배경이므로 징계양정 중심의 `disciplinary_severity`.
- `id_410721`: 직장 내 괴롭힘과 감사 비위가 모두 인정되지만 결론은 해고 양정 과다 여부이므로 `disciplinary_severity`.
- `id_410789`: 팀 메신저를 통한 업무지시와 질책이 괴롭힘에 해당하더라도 핵심은 양정 과다이어서 `disciplinary_severity`.
- `id_410791`: 실제 해고가 존재하지 않는다고 본 사안이어서 `dismissal_validity`.
- `id_410863`: 폭언, 협박, 차용, 돌봄 지시 등 괴롭힘 행위에 대한 정직 1월의 양정 적정성이 핵심이라 `disciplinary_severity`.
- `id_410873`: 경영방침 위반, 비방, 소통 차단, 직장 내 괴롭힘이 얽혀 있으나 핵심은 징계해고의 양정이므로 `disciplinary_severity`.
- `id_410985`: 정보보안 규정 위반이 중심이고 괴롭힘은 오히려 부인된 배경이므로 `disciplinary_severity`와 `not_really_harassment_case` 유지.
- `id_411019`: 직장 내 괴롭힘 일부가 인정되지만 감봉과 보직해임의 양정·절차가 분리되어 검토되므로 `disciplinary_severity`.
- `id_411033`: 수습직원 및 팀원들에 대한 괴롭힘과 성희롱이 징계사유로 인정되고 정직 1월이 정당하므로 `disciplinary_severity`.
- `id_411115`: 발언 자체가 곧바로 괴롭힘 성립으로 이어지지 않는 사례라 `workplace_harassment`가 맞고, 양정으로 넘어가지 않는다.
- `id_411151`: 개인정보 열람·유포의 괴롭힘 행위가 객관적으로 입증되지 않아 징계사유 자체가 없으므로 `disciplinary_severity`.
- `id_411261`: 성희롱·괴롭힘 비위에 대한 징계해고 사건으로, 양정과 절차가 핵심이라 `disciplinary_severity`로 고치고 `disposition_type`도 dismissal로 맞춤.
- `id_411305`: 전보명령 불응과 그에 따른 정직·해고의 정당성이 핵심이므로 전보 명령의 성격을 반영한 `transfer_validity`.
- `id_411311`: 기간제 근로자성, 갱신기대권, 갱신거절 사유가 핵심이어서 `renewal_expectation`.
- `id_411321`: 직장 내 괴롭힘 사건 자체보다 노동조합 간부·조합원에 대한 불이익취급 여부가 핵심이므로 `unfair_treatment`.
- `id_411337`: 강등은 정당하고 훈계만 부당한 복합 사안이지만, 중심은 징계사유와 양정이므로 `disciplinary_severity`.
- `id_411369`: 대기발령 제척기간과 정직 사유·절차가 함께 문제된 사건으로, 전보성 조치보다 징계의 정당성이 더 크다고 보고 `disciplinary_severity`로 정리.
- `id_411381`: 하급자에 대한 신체적 폭력과 폭언이 직장 내 괴롭힘에 해당하고 정직 3개월의 양정이 정당하므로 `disciplinary_severity`.
- `id_411401`: 해고 통지가 형식적 서면에 불과해 일방적 해고가 존재하지 않는다고 본 사건이므로 `dismissal_validity`.
- `id_411447`: 타 직원의 비위를 신고하지 않은 행위는 징계사유가 아니므로, 신고의무 부존재와 징계사유 성립 여부를 중심으로 `disciplinary_severity`.

## Ambiguities noted during review

- `id_410457` and `id_411369` are borderline between transfer-like separation measures and disciplinary validity, but I kept the current split because the written holding still turns on the separation order / waiting-order structure.
- `id_411261` has a transfer-themed reasoning thread inside a dismissal case, so `transfer_validity` remains secondary only.
- `id_410985` is a denial-of-harassment case inside a discipline fact pattern, so it keeps the `not_really_harassment_case` exclusion flag.

