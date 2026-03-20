# absence_batch_020 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 7 |
| misconduct | 6 |
| procedure | 5 |
| absence_without_leave | 5 |
| unfair_treatment | 4 |
| renewal_expectation | 2 |
| dismissal_validity | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 27 |
| medium | 3 |

## 대표 보정 사례 (2~3건)
- id_27313: absence legacy bucket -> procedure / 결근이 언급되지만 실제 판단 중심은 결근 자체보다 다른 징계사유 또는 종료 구조에 있음.
- id_27369: absence legacy bucket -> unfair_treatment / 결근이 언급되지만 실제 판단 중심은 결근 자체보다 다른 징계사유 또는 종료 구조에 있음.
- id_27413: absence legacy bucket -> misconduct / 결근이 언급되지만 실제 판단 중심은 결근 자체보다 다른 징계사유 또는 종료 구조에 있음.

## 특이 사항
- exclusion_flags 사용 건수: 26건
- notes 기재 건수: 30건
- medium confidence: 3건
