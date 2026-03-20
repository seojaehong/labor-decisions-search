# violence_batch_023 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 19 |
| misconduct | 4 |
| unfair_treatment | 2 |
| dismissal_validity | 2 |
| transfer_validity | 1 |
| procedure | 1 |
| work_ability | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 29 |
| medium | 1 |

## 대표 보정 사례 (2~3건)
- id_31669: violence legacy bucket -> transfer_validity / 인사명령의 업무상 필요성과 생활상 불이익이 핵심이었다.
- id_31739: violence legacy bucket -> procedure / 동일 비위에 대한 후행 정직은 이중징계 문제였다.
- id_32209: violence legacy bucket -> work_ability / 폭언 감봉과 본채용 거부가 함께 다뤄진 혼합 사건이었다.

## 특이 사항
- exclusion_flags 사용 건수: 13건
- notes 기재 건수: 30건
- medium confidence: 1건
- id_31767의 secondary에서 잘못 들어간 violence를 제거해 JSONL 검증 경고를 해소했다.
