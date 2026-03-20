# violence_batch_022 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 21 |
| dismissal_validity | 5 |
| workplace_harassment | 2 |
| procedure | 1 |
| renewal_expectation | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 26 |
| medium | 4 |
| low | 0 |

## 대표 보정 사례 (2~3건)
- id_31083: 폭행 사유가 있어도 결론은 소명기회와 서면통지 하자가 좌우하므로 procedure primary로 정리했다.
- id_3109: 직장 내 괴롭힘이 핵심이어서 감봉 2개월의 적정성보다 harassment 축을 primary로 두었다.
- id_31517: 수습기간 중 폭행과 불화가 시용 해지 정당성의 중심이어서 dismissal_validity로 정리했다.
- id_3155: violence 배치에 섞여 있지만 실제 쟁점은 갱신기대권 부존재이므로 renewal_expectation을 primary로 두었다.
- id_31629: 우발적 반말과 욕설만으로는 해고 정당사유가 되지 않아 dismissal_validity로 정리했다.

## 특이 사항
- medium confidence: 4건
- notes 기재 건수: 30건
- exclusion_flags 사용 건수: 17건
- violence 배치이지만 해고 부존재, 사직서 제출, 갱신기대권처럼 종료 구조가 핵심인 경계 사례가 섞여 있다.
- 절차 하자 사건(예: 서면통지·소명기회)과 직장 내 괴롭힘/성희롱 사건은 primary 축을 실질 쟁점 기준으로 재고정했다.
