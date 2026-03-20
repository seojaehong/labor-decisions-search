# absence_batch_027 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
| --- | ---: |
| `disciplinary_severity` | 15 |
| `dismissal_validity` | 6 |
| `absence_without_leave` | 3 |
| `procedure` | 2 |
| `transfer_validity` | 1 |
| `unfair_treatment` | 1 |
| `work_ability` | 1 |
| `worker_status` | 1 |

| confidence | count |
| --- | ---: |
| `high` | 29 |
| `medium` | 1 |

## 대표 보정 사례
- `id_33279`: 절차 중심 초안을 버리고 징계양정 적정성 중심으로 되돌렸다.
- `id_33463`: 무단결근이 아니라 서면통지 의무 위반이 핵심이라 `procedure`로 전환했다.
- `id_33859`: 전보, 정직, 본채용 거부가 한 사건에 섞여 있어 처분 유형을 복원했다.
- `id_34021`: 등기이사 해임안 의결을 해고로 볼 수 없다는 점을 명확히 반영했다.

## 특이 사항
- 복합 사건: `id_33501`, `id_33627`, `id_33859`, `id_33897`, `id_34005`, `id_34021`
- 진성 무단결근 사건: `id_33799`, `id_33853`, `id_33863`, `id_34097`
- 경계 사례는 `id_3411` 1건만 `medium`으로 유지했다.
