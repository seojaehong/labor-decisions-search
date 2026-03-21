# transfer_batch_002 Self-Review

- 작성일: 2026-03-21
- 배치: transfer_batch_002.jsonl
- 처리 건수: 50건
- 출력: retagging/output/reviewed/transfer_batch_002_reviewed.jsonl

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
| transfer_validity | 23건 |
| procedure | 12건 |
| disciplinary_severity | 4건 |
| no_dismissal | 4건 |
| redundancy | 3건 |
| work_ability | 1건 |
| discrimination | 1건 |
| contract_expiry | 1건 |
| union_activity | 1건 |

---

## 주요 관찰 사항

### 1. 오분류 케이스 (misclassified_transfer, 2건)

- `id_11585`: 기간제 상여수당 차별시정 사건 — legacy transfer 분류이나 실질은 차별시정(discrimination)
- `id_11603`: 무기계약 전환 기대권 사건 — 실질은 계약만료(contract_expiry) 사건

두 케이스 모두 `exclusion_flags: ["misclassified_transfer"]`를 부여하고 전보 관련 쿼리를 `exclude_for_queries`에 추가.

### 2. 절차적 각하 케이스 (procedural_only, 3건)

- `id_10915`: 원직복직으로 구제이익 소멸 각하
- `id_1139`: 제척기간 도과 + 원직복직 복합 각하
- `id_1171`: 제척기간 도과 + 해고 부존재 각하

### 3. 전보 정당성 판단 3요건 분류

**정당 (3요건 충족)**:
id_10897, id_10969, id_11133(전보부분), id_11167, id_11171, id_11317, id_11357, id_11375(전직부분), id_11479, id_11517, id_1155, id_11599, id_11669, id_11727

**부당 — 3요건 전부 미충족**:
id_11067, id_11127, id_11161, id_11271, id_11547

**부당 — 업무상 필요성 없음**:
id_11145(전직부분), id_1191

**부당 — 보복성 (권고사직 거부 후)**:
id_1113, id_11547

**부분 구제 (직위해제 정당 + 전직 부당)**:
id_11145

### 4. 부당노동행위 관련 케이스

- `id_11241`: 배치전환 부당 인정, 부당노동행위 불인정
- `id_11247`: 경영상 해고 부당 + 부당노동행위 인정 (긴박한 필요성 없음 + 반노조)
- `id_11607`: 노조 가입 직후 전보 → 부당노동행위(불이익취급) 인정

### 5. 주목할 만한 판단

- `id_11603`: 무기계약 전환 기대권 형성 + 거절 합리적 이유 인정 → 이례적 판정 (기대권은 인정, 그러나 거절 합리성도 인정)
- `id_11357`: 이동 전례로 근무장소 특정 부정 → 전직 정당 (근무장소 유동성 법리)
- `id_11897`: 경영상 해고 요건 미충족 + 사전 배치전환도 부당 → 복합 구제

---

## 태깅 품질 체크

| 항목 | 결과 |
|------|------|
| 모든 케이스 8축 태그 완성 | ✅ |
| include_for_queries 2개 이상 | ✅ (전건) |
| holding_summary 원문 기반 | ✅ |
| misclassified 케이스 exclusion_flag | ✅ (2건) |
| procedural_only 케이스 flagging | ✅ (3건) |
| confidence=medium/low 없음 | ✅ |

---

## 주요 검색 키워드 분류

**전보 정당성 핵심**:
- `전보 정당성`, `업무상 필요성`, `생활상 불이익`, `부당전보`, `전보 3요건`
- `원거리 전보`, `인력순환 전보`, `조직개편 전보`, `코로나 전보`

**보복성 전보**:
- `권고사직 거부 후 전보`, `사직 권고 거부 전보`, `보복성 전보`

**절차 위반**:
- `서면통지 없는 해고`, `구두 해고`, `징계절차 위반`, `권고사직 해고`

**부당노동행위**:
- `노조 가입 후 전보`, `부당노동행위 전보`, `불이익취급`

**계약/고용형태**:
- `무기계약 전환 기대권`, `기간제 차별시정`, `육아휴직 중 전보`

---

## 다음 배치
- 다음: transfer_batch_003.jsonl
