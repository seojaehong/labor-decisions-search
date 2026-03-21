# no_dismissal_batch_096 self review

## 처리 결과
- 입력: 50건
- 출력: 50건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| dismissal_validity | 48 |
| procedure | 1 |
| worker_status | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 46 |
| medium | 4 |

## 대표 사례 (2~3건)
- id_44869: dismissal_validity / 근로자와 사용자의 근로관계는 합의해지에 의해 종료되었으므로 해고는 존재하지 않는다고 판정한 사례 — 해고가 실제로 존재했는지(사직·합의해지·당연퇴직 vs 실질적 해고) 여부가 결론
- id_45343: worker_status / 근로기준법상 근로자에 해당하지 않아 구제신청의 당사자적격이 없다고 판정한 사례 — 근로자성(사용종속관계) 판단이 구제신청 적격과 결론을 좌우
- id_44919: procedure / 근로관계가 사용자의 일방적 의사에 의해 종료되었으므로 해고에 해당하고, 해고의 서면통지 의무를 위반하여 부당하다고 판정한 사례 — 해고예고·서면통지·소명기회 등 절차 하자가 판정을

## 특이 사항
- exclusion_flags 사용 건수: 24건
- medium confidence: 4건
