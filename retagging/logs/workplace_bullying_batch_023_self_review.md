# workplace_bullying_batch_023 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| workplace_harassment | 9 |
| transfer_validity | 7 |
| disciplinary_severity | 6 |
| misconduct | 2 |
| unfair_treatment | 2 |
| work_ability | 1 |
| procedure | 1 |
| absence_without_leave | 1 |
| dismissal_validity | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 27 |
| medium | 3 |

## 대표 보정 사례 (2~3건)
- id_408951: work_ability / probation 프레임을 유지하되, 연장된 수습과 본채용 거절의 절차 문제를 함께 반영했다.
- id_409197: 조합 가입을 이유로 한 불이익 평가인지가 핵심이라 `unfair_treatment`로 정리했다.
- id_409295: 임금 역전 문제 제기가 괴롭힘이 아니라는 점을 중심으로 `dismissal_validity`로 정리했다.

## 특이 사항
- exclusion_flags 사용 건수: 20건
- notes 기재 건수: 30건
- medium confidence: 3건
- 전반적으로 괴롭힘 자체가 성립하는 사건과, 전보·직위해제·정직처럼 인사명령의 필요성이 문제 되는 사건이 함께 섞여 있어 프레임 분리가 중요했다.
