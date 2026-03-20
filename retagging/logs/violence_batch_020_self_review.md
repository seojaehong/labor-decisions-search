# violence_batch_020 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 15 |
| misconduct | 4 |
| dismissal_validity | 3 |
| workplace_harassment | 2 |
| renewal_expectation | 2 |
| transfer_validity | 1 |
| retaliation | 1 |
| work_ability | 1 |
| absence_without_leave | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 28 |
| medium | 2 |

## 대표 보정 사례 (2~3건)
- id_28937: violence legacy bucket -> transfer_validity / 배치전환 적법성과 전보 거부 후 무단결근이 함께 핵심이다.
- id_29039: violence legacy bucket -> dismissal_validity / 해고 존재와 구제이익 소멸이 핵심인 사건이다.
- id_29137: violence legacy bucket -> work_ability / 시용기간 중 교통사고가 본채용 거절의 합리적 이유가 된다.

## 특이 사항
- exclusion_flags 사용 건수: 19건
- notes 기재 건수: 30건
- medium confidence: 2건
- 폭행·협박 사건뿐 아니라 전보, 구제이익 소멸, 시용 본채용 거절, 고용승계 거부 같은 비폭력 프레임을 분리해 두었다.
