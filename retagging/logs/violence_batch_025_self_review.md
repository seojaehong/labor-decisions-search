# violence_batch_025 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 21 |
| dismissal_validity | 5 |
| transfer_validity | 2 |
| retaliation | 1 |
| procedure | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 28 |
| medium | 2 |

## 대표 보정 사례 (2~3건)
- id_3325: violence legacy bucket -> retaliation / 폭행 진정 제기 후 복직 뒤 보복성 강등·정직이 핵심인 사례.
- id_33289: violence legacy bucket -> transfer_validity / 폭행 재발 방지를 위한 전직의 업무상 필요성과 생활상 불이익 비교형량이 핵심인 사례.
- id_33501: violence legacy bucket -> procedure / 폭행 해고는 사유와 양정이 인정되지만 서면통지·소명기회 흠결이 결론을 좌우한 사례.

## 특이 사항
- `notes`는 전건 기재 유지.
- `disciplinary_severity`와 `dismissal_validity`가 중심이고, 보복성 조치나 전보 정당성 사례는 별도 프레임으로 분리했다.
- `medium`은 2건만 유지했다.
