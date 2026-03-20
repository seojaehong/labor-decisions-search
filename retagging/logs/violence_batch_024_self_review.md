# violence_batch_024 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 21 |
| dismissal_validity | 4 |
| transfer_validity | 2 |
| misconduct | 1 |
| unfair_treatment | 2 |
### confidence 분포
| confidence | count |
|---|---:|
| high | 30 |

## 대표 보정 사례 (2~3건)
- id_3235: violence legacy bucket -> transfer_validity / 전직의 업무상 필요성과 생활상 불이익의 상당성 비교가 결론을 좌우해 transfer_validity를 primary로 조정.
- id_32401: violence legacy bucket -> disciplinary_severity / 징계사유 인정 후 정직의 과중성과 소급적용 여부가 결론을 좌우해 disciplinary_severity를 primary로 조정.
- id_33087: violence legacy bucket -> dismissal_validity / 수습근로자 본채용 거부의 정당성이 핵심이라 probation 사건의 dismissal_validity 구조로 재분류.

## 특이 사항
- exclusion_flags 사용 건수: 12건
- notes 기재 건수: 30건
- medium confidence: 0건
