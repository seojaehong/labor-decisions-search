# violence_batch_019 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 14 |
| dismissal_validity | 6 |
| misconduct | 4 |
| transfer_validity | 3 |
| procedure | 1 |
| unfair_treatment | 1 |
| workplace_harassment | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 28 |
| medium | 2 |


## 대표 보정 사례 (2~3건)
- id_28073: resignation/termination dispute -> dismissal_validity / 사직서 제출로 근로관계가 종료되어 해고가 존재하지 않는다.
- id_28171: transfer-like standby order -> transfer_validity / 대기발령의 업무상 필요성과 생활상 불이익 비교형량이 핵심이다.
- id_28553: violence bucket -> workplace_harassment / 성추행 성립과 해고 양정, 절차가 모두 핵심이다.

## 특이 사항
- exclusion_flags 사용 건수: 11건
- notes 기재 건수: 30건
- medium confidence: 2건
- violence 배치이지만 실제로는 전보, 사직/합의 종료, 부당노동행위처럼 비폭력 쟁점인 케이스를 별도 축으로 분리했다.
