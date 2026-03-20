# absence_batch_026 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 14 |
| absence_without_leave | 7 |
| renewal_expectation | 3 |
| worker_status | 2 |
| dismissal_validity | 2 |
| work_ability | 1 |
| unfair_treatment | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 30 |

## 대표 보정 사례 (2~3건)
- id_32199: procedure legacy -> disciplinary_severity / 복합 비위에 대한 정직 2개월의 양정과 절차 적정성이 핵심이다.
- id_32287: misconduct legacy -> worker_status / 결근 공제는 간접 사정일 뿐이고, 실제 판단 중심은 근로자성 부정이다.
- id_32781: disciplinary_severity legacy -> dismissal_validity / 징계사유 자체가 입증되지 않아 실체 판단이 먼저 무너지는 사건이다.

## 특이 사항
- exclusion_flags 사용 건수: 25건
- notes 기재 건수: 30건
- medium confidence: 0건
- 재분류의 중심축은 `absence_without_leave` 자체보다 `disciplinary_severity`, `worker_status`, `renewal_expectation`, `dismissal_validity` 쪽으로 이동한 사례가 많았다.
