# absence_batch_024 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 16 |
| dismissal_validity | 5 |
| absence_without_leave | 4 |
| procedure | 2 |
| renewal_expectation | 1 |
| transfer_validity | 1 |
| work_ability | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 30 |

## 대표 보정 사례 (2~3건)
- id_30703: absence legacy bucket -> procedure / 무단결근은 있었지만 결론은 소명기회 미부여 등 절차 하자가 좌우한다.
- id_30731: absence legacy bucket -> absence_without_leave / 승인된 병가 범위를 벗어난 장기 무단결근과 출근 지시 불응이 직접 해고사유다.
- id_31007: procedure draft -> absence_without_leave / 산재 종료 후 출근 거부와 장기 무단결근이 직접 해고사유다.

## 특이 사항
- exclusion_flags 사용 건수: 44건
- notes 기재 건수: 30건
- medium confidence: 0건
