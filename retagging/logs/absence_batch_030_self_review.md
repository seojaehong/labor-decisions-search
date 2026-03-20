# absence_batch_030 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 10 |
| misconduct | 6 |
| procedure | 5 |
| absence_without_leave | 5 |
| renewal_expectation | 2 |
| unfair_treatment | 1 |
| dismissal_validity | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 29 |
| medium | 1 |

## 대표 보정 사례 (2~3건)
- id_345231: absence legacy bucket -> disciplinary_severity / 결근이 언급되지만 실제 판단 중심은 결근 자체보다 다른 징계사유 또는 종료 구조에 있음.
- id_345277: absence legacy bucket -> disciplinary_severity / 결근이 언급되지만 실제 판단 중심은 결근 자체보다 다른 징계사유 또는 종료 구조에 있음.
- id_345323: absence legacy bucket -> misconduct / 결근이 언급되지만 실제 판단 중심은 결근 자체보다 다른 징계사유 또는 종료 구조에 있음.

## 특이 사항
- exclusion_flags 사용 건수: 27건
- notes 기재 건수: 30건
- medium confidence: 1건
