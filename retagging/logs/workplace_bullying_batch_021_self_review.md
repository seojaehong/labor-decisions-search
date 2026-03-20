# workplace_bullying_batch_021 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 24 |
| transfer_validity | 3 |
| procedure | 1 |
| renewal_expectation | 1 |
| absence_without_leave | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 30 |

## 대표 보정 사례 (2~3건)
- id_407475: workplace_bullying legacy bucket -> disciplinary_severity / 후속조치 이행과 경고의 적정성이 핵심이다.
- id_407587: workplace_bullying legacy bucket -> disciplinary_severity / 직인·공탁금·근태·괴롭힘이 섞인 복합 비위에 대한 해고 양정이 핵심이다.
- id_408113: transfer/harassment draft -> absence_without_leave / 전보 불응 이후의 장기 무단결근과 업무지시 불이행에 대한 징계해고가 핵심이다.

## 특이 사항
- `workplace_harassment` primary는 남기지 않고, 실제 판단축이 `양정`, `전보`, `절차`, `갱신기대권`, `무단결근`으로 갈리는 구조를 유지했다.
- notes를 30건 모두 채워 검색/검토용 설명력을 유지했다.
- 별도 수동 재검토 체크포인트는 `logs/manual_recheck_workplace_bullying_batch_021.md`에 전건 표로 남겼다.
