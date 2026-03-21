# no_dismissal_batch_099 self review

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
| high | 49 |
| medium | 1 |

## 대표 사례 (2~3건)
- id_46883: dismissal_validity / 근로자의 사직서 제출이 사용자의 강요나 압박에 의한 것이라고 볼 수 없어 해고가 존재하지 않는다고 판정한 사례 — 해고가 실제로 존재했는지(사직·합의해지·당연퇴직 vs 실질적 해고
- id_47269: worker_status / 신청인은 회사로부터 위임받은 사무를 처리하는 비등기 임원으로서 근로기준법에서 정한 근로자에 해당한다고 보기 어려워 당사자 적격이 없다고 판정한 사례 — 근로자성(사용종속관계) 판단
- id_46961: procedure / 사용자에게 구제신청의 당사자 적격이 있고, 해고의 서면통지 의무를 위반하여 부당하다고 판정한 사례 — 해고예고·서면통지·소명기회 등 절차 하자가 판정을 좌우

## 특이 사항
- exclusion_flags 사용 건수: 30건
- medium confidence: 1건
