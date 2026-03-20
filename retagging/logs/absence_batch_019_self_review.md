# absence_batch_019 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 9 |
| dismissal_validity | 7 |
| procedure | 6 |
| absence_without_leave | 4 |
| transfer_validity | 2 |
| unfair_treatment | 1 |
| misconduct | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 29 |
| medium | 1 |

## 대표 보정 사례 (2~3건)
- id_26243: absence legacy bucket -> transfer_validity / 무단결근은 부당전보와 해고의 파생 결과일 뿐이고, 핵심은 전보의 업무상 필요성과 생활상 불이익이다.
- id_26751: absence legacy bucket -> dismissal_validity / 결근 자체보다 복직명령의 진정성과 구제이익 소멸 여부가 중심이다.
- id_27267: procedure draft -> absence_without_leave / 반복 무단결근 자체가 직접 해고사유가 된 전형적 결근 사건이다.

## 특이 사항
- `absence` 배치명과 달리 실제 진성 결근 사건은 4건만 유지했다.
- 해고 존재/복직명령/구제이익 소멸 구조의 사건이 많아 `dismissal_validity`와 `procedure` 비중이 높다.
- 복합 처분 사건인 `id_26781`은 정기자 임용취소, 감봉, 부당노동행위가 함께 얽혀 있어 `medium`으로 유지했다.
