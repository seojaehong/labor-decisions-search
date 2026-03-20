# absence_batch_025 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 10 |
| misconduct | 6 |
| transfer_validity | 3 |
| absence_without_leave | 3 |
| dismissal_validity | 3 |
| procedure | 2 |
| renewal_expectation | 2 |
| worker_status | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 25 |
| medium | 5 |

## 대표 보정 사례 (2~3건)
- id_31377: absence legacy bucket -> procedure / 휴직 상태라 무단결근이 아니고 직권면직 절차와 사유가 함께 무너진다.
- id_31545: absence legacy bucket -> disciplinary_severity / 단발성 무단결근과 경미한 비위는 인정되지만 고정배제는 양정이 과하다.
- id_3217: absence legacy bucket -> transfer_validity / 부당전보가 먼저이고, 그 전보를 둘러싼 무단결근과 해고는 파생 쟁점이다.

## 특이 사항
- exclusion_flags 사용 건수: 27건
- notes 기재 건수: 30건
- medium confidence: 5건
