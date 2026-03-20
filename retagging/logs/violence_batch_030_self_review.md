# violence_batch_030 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 23 |
| renewal_expectation | 3 |
| misconduct | 3 |
| dismissal_validity | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 29 |
| medium | 1 |

## 대표 보정 사례 (2~3건)
- id_347781: violence legacy bucket -> disciplinary_severity / 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지.
- id_34779: violence legacy bucket -> disciplinary_severity / 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지.
- id_347891: violence legacy bucket -> disciplinary_severity / 폭행·폭언 사실 자체보다 제재 수위가 결론을 좌우해 disciplinary_severity를 primary로 유지.

## 특이 사항
- exclusion_flags 사용 건수: 22건
- notes 기재 건수: 30건
- medium confidence: 1건
