# workplace_bullying_batch_022 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 16 |
| transfer_validity | 7 |
| retaliation | 3 |
| workplace_harassment | 1 |
| renewal_expectation | 1 |
| dismissal_validity | 1 |
| procedure | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 30 |

## 대표 보정 사례 (2~3건)
- id_408319: manual recheck -> dismissal_validity / 사직 수리로 종료된 사건이라 전보가 아니라 해고 부존재와 사직 종료가 핵심.
- id_408333: manual recheck -> transfer_validity / 괴롭힘으로 인한 피해 회복과 직장질서 유지 목적의 배치전환이 핵심.
- id_408371: manual recheck -> retaliation / 성희롱 발생 신고와 무관한 대기발령·징계해고인지가 핵심.

## 특이 사항
- exclusion_flags 사용 건수: 29건
- notes 기재 건수: 30건
- medium confidence: 0건
- 최종 분포는 `transfer_validity`와 `retaliation`이 함께 주도하되, 실제 핵심 결론은 전보/대기발령/사직 종료 같은 인사명령 축에 더 많이 걸려 있다.
