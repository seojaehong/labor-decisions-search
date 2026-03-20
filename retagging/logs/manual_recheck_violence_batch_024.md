# manual recheck: violence_batch_024

Batch reviewed manually, case by case, against the source input and the tagging schema.

## Cases checked

- id_32329: 폭행·폭언 비위가 인정되고 제재 수위가 결론을 좌우해 `disciplinary_severity` 유지.
- id_32337: 입소자 폭행 사실 인정 후 정직 1개월의 적정성이 쟁점이라 `disciplinary_severity` 유지.
- id_3235: 전직 명령의 업무상 필요성과 생활상 불이익의 상당성 비교가 핵심이라 `transfer_validity`로 조정.
- id_32351: 영내폭행·가혹행위 자체와 제재 양정이 함께 문제되는 전형적 징계양정 사건이라 `disciplinary_severity` 유지.
- id_32357: 폭행·협박 비위는 전제이고, 결론은 징계양정과 절차의 종합 판단이라 `disciplinary_severity`로 조정.
- id_32363: 전보/전직 명령의 업무상 필요성까지 함께 다뤄지는 복합 사건이지만, 폭행 비위 이후 처분의 실질은 징계양정 중심이라 `disciplinary_severity` 유지.
- id_3239: 후배 폭행 사실 인정 후 해고 양정이 문제된 사건이라 `disciplinary_severity` 유지.
- id_32399: 징계사유와 절차가 모두 인정되어도 결론은 양정 적정성에 달려 `disciplinary_severity` 유지.
- id_32401: 징계사유는 인정되지만 정직 과중성과 소급적용이 결론을 좌우해 `disciplinary_severity`로 조정.
- id_32427: 권한 없는 채용기준 개입 등 비위는 인정되나 핵심은 징계 수위라 `disciplinary_severity` 유지.
- id_32435: 해고 존재가 아니라 사직의 진의가 쟁점이므로 `dismissal_validity`로 조정.
- id_32567: 형사판결을 이유로 한 당연면직 규정의 적용 가능성이 핵심이라 `dismissal_validity`로 조정.
- id_32593: 폭행·폭언 사유는 전제이고, 양정 남용 여부가 핵심이라 `disciplinary_severity` 유지.
- id_32767: 증정품 현금화와 폭언 메일을 포함한 비위는 인정되나 해고 양정이 핵심이라 `disciplinary_severity` 유지.
- id_32809: 절차 문구가 있으나 실질은 징계양정 적정성 판단이 중심이라 `disciplinary_severity`로 조정.
- id_32839: 인사명령의 업무상 필요성과 생활상 불이익 비교형량이 핵심이라 `transfer_validity`로 조정.
- id_32841: 비위 인정과 징계양정 적정성이 함께 결론을 지배해 `disciplinary_severity` 유지.
- id_32885: 일부 사유는 독립 징계사유가 아니어도 양정에 참작되는 사건이라 `disciplinary_severity` 유지.
- id_32907: 해고 양정 과중 여부가 핵심이라 `disciplinary_severity` 유지.
- id_32943: 성희롱과 폭행이 결합된 중대한 비위로 해고 양정이 핵심이므로 `disciplinary_severity` 유지.
- id_32981: 업무코칭 거부, 소란, 방해행위에 대한 징계 수위가 핵심이라 `disciplinary_severity` 유지.
- id_32993: 사직서의 비진의 여부와 해고 부존재가 핵심이므로 `dismissal_validity`로 조정.
- id_32995: 절차 흠결 치유 후 재징계의 적법성과 양정이 핵심이라 `disciplinary_severity` 유지.
- id_33087: 수습(시용) 본채용 거부의 정당성이 핵심이므로 `dismissal_validity`로 조정.
- id_33061: 폭행 해고와 부당노동행위 판단이 함께 걸린 사건이라 `unfair_treatment` 유지.
- id_3307: 폭행 해고와 부당노동행위 판단이 함께 걸린 사건이라 `unfair_treatment` 유지.
- id_33097: 일부 사유 인정 후 양정 과중 여부가 핵심이라 `disciplinary_severity` 유지.
- id_33193: 폭력행위는 인정되나 해고는 과중하다고 본 사건이라 `disciplinary_severity` 유지.
- id_33195: 징계사유, 양정, 절차가 모두 문제되는 전형적 징계양정 사건이라 `disciplinary_severity` 유지.
- id_33241: 동료 간 3차례 폭행사건을 이유로 한 징계해고로 비위 자체가 핵심이라 `misconduct` 유지.

## Ambiguities

- `id_32567`은 자동면직 규정의 적용 범위가 핵심이라 `dismissal_validity`로 봤지만, 형사비위 중심으로 읽을 여지도 있었다.
- `id_32809`은 절차 문구가 강하게 보이지만, 실제로는 징계양정 적정성이 더 중심이라고 판단해 `disciplinary_severity`로 옮겼다.
- `id_32435`와 `id_32993`은 둘 다 해고 부존재/사직 진의가 핵심이라 dismissal 계열로 재분류했다.
- `id_3235`와 `id_32839`은 violence 표면값보다 전직 명령의 상당성 판단이 핵심인 예외 사건으로 보았다.
- `id_33087`은 probation 본채용 거부 사건이라 일반 폭행 사건과 달리 `dismissal_validity` 축으로 보는 것이 맞았다.
