# absence_batch_023 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 14 |
| absence_without_leave | 5 |
| dismissal_validity | 3 |
| procedure | 2 |
| renewal_expectation | 2 |
| misconduct | 1 |
| transfer_validity | 1 |
| unfair_treatment | 1 |
| worker_status | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 28 |
| medium | 2 |

## 대표 보정 사례 (2~3건)
- id_29751: unfair_treatment draft -> worker_status / 수습근로자의 근태불량과 관리부실을 이유로 한 본채용 거부 사건.
- id_29861: misconduct draft -> transfer_validity / 전보 사유로 근태불량 등이 주장되지만 핵심은 업무상 필요성과 절차 적정성이다.
- id_30563: absence draft -> dismissal_validity / 당사자 적격과 해고 존재가 부정되고 전보명령만 정당한 사건.

## 특이 사항
- `absence` 배치명과 달리 본채용 거부, 전보, 갱신기대권, 해고 존재 여부가 함께 섞여 있어 primary를 실제 판단 구조 기준으로 넓게 재배치했다.
- 진성 무단결근 사건과 배경성 결근 사건을 다시 나눠, `not_really_absence_case`와 `evidence_too_thin`을 구분했다.
- `disciplinary_severity`와 `procedure`가 함께 나오는 사건은, 절차보다 양정이 결론을 좌우하는 경우만 primary를 유지했다.
