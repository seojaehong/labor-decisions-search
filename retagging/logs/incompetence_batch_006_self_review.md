# incompetence_batch_006 Self Review

## 배치 개요
- 입력: 30건 (id_37033 ~ id_40429)
- 출력: 30건 전량 태깅 완료
- 작업일: 2026-03-20

## 분류 통계

### employment_stage
| 단계 | 건수 |
|------|------|
| probation | 19 |
| regular | 9 |
| renewal_stage | 2 |

### issue_type_primary
| 유형 | 건수 |
|------|------|
| work_ability | 17 |
| dismissal_validity | 4 |
| disciplinary_severity | 3 |
| procedure | 2 |
| transfer_validity | 2 |
| misconduct | 1 |
| performance | 1 |
| renewal_expectation | 1 (id_403985는 갱신기대권이 실질 쟁점) |

### disposition_type (중복 포함)
| 유형 | 건수 |
|------|------|
| rejection_of_regular_employment | 15 |
| dismissal | 5 |
| disciplinary_dismissal | 5 |
| suspension | 4 |
| transfer | 2 |
| no_formal_disposition | 1 |

### decision_result
| 결과 | 건수 |
|------|------|
| dismissed (기각) | 14 |
| granted (인용) | 11 |
| upheld (초심유지) | 4 |
| overturned (초심취소) | 1 |

## 중점 점검 사항 판단 기록

### 1. work_ability vs dismissal_validity 구분
- **work_ability**: 업무능력 자체의 평가·입증이 판단의 핵심인 17건
  - 수습 본채용 거부 사건 대부분 (평가기준 존부, 평가 객관성, 개선기회 부여 등)
- **dismissal_validity**: 업무능력이 사유로 적시되었으나 사용자의 전반적 입증 실패가 핵심인 4건
  - id_38101: 상시근로자 수 선결 + 해고사유 전반 입증 실패
  - id_400221: 4개 징계사유 전부 부정 (구조적 인력부족 문제)
  - id_400339: 허위학력 + 업무능력 모두 사유 부정
  - id_403863: 사유 입증 실패 + 절차 전면 미준수

### 2. 수습 사건 구분 (employment_stage)
- **probation으로 분류한 19건**: 시용/수습 근로계약이 명시적으로 인정된 사건
- **regular로 분류한 사건 중 수습 이력 언급**:
  - id_37669: 수습기간 평가 후 본채용된 뒤의 전보 → regular (본채용 이후 사건)
  - id_38957: 수습기간 중이나 사직 의사의 진의가 핵심 → probation 유지 (맥락상 수습 중)
- **id_404161**: 시용기간 경과 후 계속 근무 → 본채용 간주. employment_stage는 probation으로 유지 (시용기간 법적 성격이 쟁점)

### 3. 갱신기대권 사건 식별
- **id_403985**: 갱신기대권 인정 + 인사고과 기반 갱신거절 정당
  - issue_type_primary: renewal_expectation
  - exclusion_flags: renewal_expectation_dominant
  - incompetence 레거시 태그는 인사고과 점수 미달이 갱신거절 사유일 뿐

### 4. disciplinary_severity 과잉 포착 주의
- **disciplinary_severity로 분류한 3건**:
  - id_39431: 정직 3월 - 비밀녹음+거래처불만+업무저조 → 양정 적정 판단이 핵심
  - id_39689: 정직 1월 - 사적활동+보안위반+최하위 성과 → 양정 적정
  - id_401981: 정직 - 업무지시 불이행·허위보고이나 중하지 않아 양정 과다
- **징계 사건이나 disciplinary_severity로 분류하지 않은 것**:
  - id_400087: 저성과자 PIP 후 해고 → performance가 핵심 (양정보다 사유 존부)
  - id_401587: 교육거부+무단결근 → misconduct가 핵심 (업무능력 아님)
  - id_400221: 징계사유 전부 부정 → dismissal_validity

### 5. exclusion_flags 부여 기준
- **not_really_performance_case** (7건): 업무능력이 명목상 사유이거나 보조적인 경우
  - id_37669 (전보가 핵심), id_38101 (법인격 부인이 핵심), id_38957 (사직 진의가 핵심)
  - id_39431, id_39689, id_401981 (비위행위가 주 징계사유)
  - id_400339 (허위학력이 병합), id_400879 (직위해제/전보가 핵심)
  - id_401587 (불복종·무단결근이 핵심)
- **procedure_dominant** (2건): 절차 하자로 부당 결론
  - id_403677 (서면통지 미이행), id_404161 (서면통지 미이행)
- **renewal_expectation_dominant** (1건): id_403985
- **resignation_dispute** (1건): id_38957

## 신뢰도 분포
| 신뢰도 | 건수 |
|--------|------|
| high | 30 |
| medium | 0 |
| low | 0 |

전건 high: 판정문 원문에서 쟁점 구분·판단 결론이 명확하여 태깅 판단에 모호함이 없었음.

## 특이 사건 메모
- **id_37423 / id_40327**: 동일 사건 초심/재심 쌍. 재심에서 초심 유지(수습해고 정당).
- **id_404161**: 시용기간 경과 후 본채용 간주 법리 + 기간제 vs 본채용 선결 쟁점.
- **id_400879**: 직위해제의 법적 성격(사실상 전보) 인정 → 구제이익 있음.
- **id_400339**: 금전보상명령 2,157만원 포함.
