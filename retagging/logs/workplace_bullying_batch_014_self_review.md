# workplace_bullying_batch_014 self-review

## 배치 개요
- 총 30건 (id_399931 ~ id_401073)
- 괴롭힘 배치이나 실질 쟁점 분포가 다양함

## 분류 통계

### issue_type_primary 분포
| primary | 건수 | 비고 |
|---------|------|------|
| workplace_harassment | 10 | 괴롭힘 성립/불성립이 핵심 쟁점 |
| disciplinary_severity | 12 | 양정 과다 여부가 핵심 |
| transfer_validity | 5 | 전보/대기발령/직위해제 정당성 |
| misconduct | 2 | 횡령/비위가 실질 (괴롭힘은 배경) |
| dismissal_validity | 2 | 사유 부존재/해고부존재 |
| renewal_expectation | 1 | 갱신기대권이 실질 |

### not_really_harassment_case 플래그 부여 (4건)
| case_id | 사유 |
|---------|------|
| id_400153 | 갱신기대권 사건, 괴롭힘은 사용자 주장 사유로만 언급+입증 부족 |
| id_400347 | 예산 횡령·허위진술 강요가 핵심, 괴롭힘(출장동행) 배척 |
| id_400469 | 겸직금지·노조·양정이 핵심, 본문에 괴롭힘 실질 쟁점 없음 |
| id_40075 | 자금 편취(사기죄 실형)가 유일 쟁점, 괴롭힘 관련 내용 전무 |
| id_400611 | 사직서 진의 인정, 괴롭힘 성립 판단 없음 (resignation_dispute 병행) |

### 괴롭힘 성립 vs 불성립 판단 사례
| 유형 | 건수 | 대표 case_id |
|------|------|-------------|
| 괴롭힘 성립 인정 | 12 | id_399983, id_400231, id_400277, id_400535 등 |
| 괴롭힘 불성립 | 3 | id_400071(사적갈등), id_400937(우위성불인정), id_400299(일부불인정) |
| 괴롭힘 판단 자체 없음/배경 | 5 | id_400153, id_400347, id_40075, id_400469, id_400611 |

### 양정 판단 분포 (징계 정당 vs 과다)
| 양정 판단 | 건수 |
|-----------|------|
| 양정 정당 | 12 |
| 양정 과다 (부당) | 12 |
| 양정 미판단 (사유 불인정 등) | 6 |

## 주요 태깅 판단 기록

### id_399931
- primary: disciplinary_severity (성희롱이 주 비위, 따돌림은 병행)
- workplace_harassment를 secondary에 배치; 성희롱 단독 태그가 없어 harassment로 통합

### id_400071
- primary: workplace_harassment (괴롭힘 성립 요건 불충족이 핵심 판단)
- exclusion_flags: emotional_conflict_not_harassment (사적 갈등→괴롭힘 아님)
- 우위성·업무관련성 불인정을 명시한 중요 판례

### id_400153
- primary: renewal_expectation (갱신기대권이 결정적)
- not_really_harassment_case + renewal_expectation_dominant 이중 플래그
- 괴롭힘은 사용자 측 갱신거절 사유 주장 중 하나에 불과

### id_400273
- primary: disciplinary_severity (무관용 원칙 한계 명시)
- "비위행위의 경중을 고려하지 않고 일률적으로 해고하는 것은 재량남용" — 검색 가치 높음

### id_400277
- primary: workplace_harassment (원행위+2차가해+조사불응이 복합)
- 괴롭힘 자체가 핵심이고 2차 가해·조사방해가 양정 정당성 근거

### id_400375
- 경고 처분의 구제신청 대상 적격(그 밖의 징벌) 판단이 특징적
- primary: workplace_harassment

### id_400937
- 우위성 불인정으로 괴롭힘 불성립 + 징계위 전원 외부위원 구성=절차 위반
- 이중 위법 사례로 검색 가치 높음

### id_400961
- sanction_type이 pay_cut이나 본문에서 "견책이 가장 가벼운 징계"라 기재
- 감봉 선례 언급이 있어 legacy sanction_type(pay_cut)을 disposition_type에 유지

## 품질 체크리스트
- [x] 모든 case_id가 입력과 1:1 대응 (30건)
- [x] review_status: "pending" 통일
- [x] tag_version: "v1" 통일
- [x] issue_type_primary는 스키마 허용값만 사용
- [x] 괴롭힘이 배경인 사건에 not_really_harassment_case 부여
- [x] 사적 갈등 사건에 emotional_conflict_not_harassment 부여
- [x] include_for_queries/exclude_for_queries에 한글 검색어 포함
- [x] confidence 전건 high (원문이 충분히 명확)
