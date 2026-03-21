# no_dismissal_batch_129 self review

## 처리 결과
- 입력: 50건
- 출력: 50건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| dismissal_validity | 48 |
| worker_status | 1 |
| procedure | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 49 |
| medium | 1 |

## 대표 사례 (2~3건)
- id_61311: dismissal_validity / 근로자가 사직서를 제출하고, 사용자가 이를 수리함으로써 근로계약관계가 종료된 것으로 해고가 존재하지 않는다고 판정한 사례 — 해고가 실제로 존재했는지(사직·합의해지·당연퇴직 vs 
- id_61335: worker_status / 신청인이 근로기준법상 근로자에 해당하지 않아 구제신청의 당사자 적격이 없다고 판정한 사례 — 근로자성(사용종속관계) 판단이 구제신청 적격과 결론을 좌우
- id_61381: procedure / 근로자의 어떠한 행위가 징계사유로 된 것인지 특정하기 어렵고, 해고사유의 서면통지 의무를 위반하여 부당하다고 판정한 사례 — 해고예고·서면통지·소명기회 등 절차 하자가 판정을 좌우

## 특이 사항
- exclusion_flags 사용 건수: 28건
- medium confidence: 1건
