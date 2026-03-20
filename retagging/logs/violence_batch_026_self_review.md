# violence_batch_026 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 20 |
| misconduct | 5 |
| unfair_treatment | 4 |
| renewal_expectation | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 29 |
| medium | 1 |

## 대표 보정 사례 (2~3건)
- id_33871: violence legacy bucket -> disciplinary_severity / 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지.
- id_33999: violence legacy bucket -> disciplinary_severity / 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지.
- id_34007: violence legacy bucket -> unfair_treatment / 표면 주제보다 종료 구조 또는 보복·전보 판단이 더 중심인 경계 사례.

## 특이 사항
- exclusion_flags 사용 건수: 20건
- notes 기재 건수: 30건
- medium confidence: 1건
