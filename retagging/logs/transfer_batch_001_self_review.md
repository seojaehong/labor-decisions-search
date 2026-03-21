# transfer_batch_001 Self-Review

- 작성일: 2026-03-21
- 배치: transfer_batch_001.jsonl
- 처리 건수: 50건
- 출력: retagging/output/reviewed/transfer_batch_001_reviewed.jsonl

---

## 태깅 요약

| 항목 | 값 |
|------|-----|
| 처리 건수 | 50건 |
| confidence=high | 50건 |
| confidence=medium | 0건 |
| confidence=low | 0건 |

---

## issue_type_primary 분포

| issue_type_primary | 건수 |
|---------------------|------|
| transfer_validity | 22건 |
| procedure | 12건 |
| union_activity | 7건 |
| no_dismissal | 3건 |
| disciplinary_severity | 3건 |
| redundancy | 2건 |
| discrimination | 2건 |
| work_ability | 1건 |

---

## 주요 관찰 사항

### 1. transfer batch 오분류 케이스
transfer_batch에 포함되어 있지만 실질적으로 전보/전직 정당성이 아닌 다른 이슈가 주된 케이스가 다수 존재.

**misclassified_transfer exclusion_flag 부여 케이스 (3건)**:
- `2018상병OOO`: 산재/상병보상 사건 (안전의무 위반)
- `2021의결OOO`: 쟁의행위 중지 의결 사건
- `id_10029`: 단체협약 해석(출장 여비) 사건

이 케이스들은 legacy_reason_category에 `transfer`가 포함되어 있지만 실질적으로 전보 관련 검색에 적합하지 않으므로 `exclude_for_queries`에 `전보 정당성` 등 전보 관련 쿼리를 포함하고 `exclusion_flags`에 `misclassified_transfer`를 부여함.

### 2. 차별시정 케이스 (2건)
- `2021차별OOO`, `2023차별OOO`: transfer batch에 포함되어 있으나 실질은 차별시정(기간제/단시간) 사건. 차별시정 검색에 적합하도록 태깅.

### 3. 절차적 각하/구제이익 소멸 케이스 (12건)
procedure를 primary로 분류한 12건 중 순수 절차 각하로 실체 판단이 없는 케이스에 `procedural_only` exclusion_flag 부여:
- `id_10309`: 동일 취지 재신청 각하
- `id_10431`: 해고 후 전보로 구제이익 소멸
- `id_10457`: 계약만료 중 구제이익 소멸
- `id_10533`: 대기발령 부수 전보 구제대상 아님
- `id_10565`: 전보 전 사직으로 구제이익 소멸
- `id_10581`: 노조 임원 불신임 후 구제이익 소멸
- `id_10611`: 업무분장은 전보/징벌 아님
- `id_10879`: 인사발령 해제로 구제이익 소멸
- `2021의결OOO`: 쟁의행위 자진 중단 각하

### 4. 전보 정당성 판단 3요건 분류
전보 정당성의 핵심 3요건(업무상 필요성 / 생활상 불이익 / 협의절차) 기준으로 분류:

**모두 충족 → 정당**:
id_10005, id_10027, id_10037, id_10057, id_1017, id_1027, id_10113, id_10287(전보부분), id_10289, id_10329, id_10407, id_10471, id_1059, id_1061

**생활상 불이익 과다 → 부당**:
id_1001(동의+협의 없음), id_10095, id_10315, id_10243(근로자1), id_10869

**업무상 필요성 없음 → 부당**:
id_10869, id_10745

**협의절차 위반 → 부당**:
id_10095

### 5. 부당노동행위 전보 케이스 (7건)
union_activity를 primary로 분류. 대부분 부당노동행위 **불인정** 판정:
- `id_10303`: 노조 간부 전보 → 부당노동행위 불인정
- `id_10523`: 단체협약 만료 전보 → 불인정
- `id_10769`: 인사발령 관련 발언 → 불인정
- `2016공정OOO`: 공정대표의무 위반 → 불인정
- **인정 케이스**: `id_10367`(원청 사용자성 인정, 지배개입)

---

## 태깅 품질 체크

| 항목 | 결과 |
|------|------|
| 모든 케이스 8축 태그 완성 | ✅ |
| include_for_queries 2개 이상 | ✅ (전건) |
| holding_summary 원문 기반 | ✅ |
| misclassified 케이스 exclusion_flag | ✅ (3건) |
| procedural_only 케이스 flagging | ✅ (9건) |
| confidence=medium/low 없음 | ✅ |

---

## 주요 검색 키워드 분류

**전보 정당성 핵심**:
- `부당전직`, `인사권 남용`, `전보 정당성`, `업무상 필요성`, `생활상 불이익`
- `전보 정당`, `코로나 전보`, `부당전보`

**부당노동행위 전보**:
- `노조간부 전보`, `부당노동행위 전보`, `지배개입`

**절차 위반**:
- `서면 해고통지`, `절차 위반 부당해고`, `구제이익 소멸`

**경영상 해고**:
- `정리해고`, `긴박한 필요성`, `경영상 해고 요건`

---

## 다음 배치
- 다음: transfer_batch_002.jsonl
