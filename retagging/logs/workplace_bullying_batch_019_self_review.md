# workplace_bullying_batch_019 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 16 |
| dismissal_validity | 5 |
| transfer_validity | 4 |
| absence_without_leave | 1 |
| work_ability | 1 |
| workplace_harassment | 1 |
| worker_status | 1 |
| procedure | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 29 |
| medium | 1 |

## 대표 보정 사례 (2~3건)
- id_405489: retaliation 초안 -> transfer_validity / 대기발령의 업무상 필요성과 생활상 불이익을 비교하는 인사명령 사건으로 재정렬.
- id_405851: disciplinary_severity 초안 -> absence_without_leave / 병가 증빙 없이 23일 무단결근한 전형적 결근 사건으로 복원.
- id_406179: disciplinary_severity 초안 -> work_ability / 시용 평가와 본채용 거부의 공정성이 핵심이라 probation 축으로 정리.

## 특이 사항
- `not_really_harassment_case`는 괴롭힘이 배경에만 머무는 경우에만 유지했다.
- `workplace_harassment`가 실제 쟁점인 경우는 primary 또는 secondary로 남겼고, 배경만인 사건은 `notes`로 정리했다.
- `confidence=medium`은 다자 징계가 섞인 `id_406049` 1건만 유지했다.
