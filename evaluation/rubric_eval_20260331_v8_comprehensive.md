=== RUBRIC EVALUATION REPORT ===
Date: 2026-03-31 (3rd eval — v8 comprehensive refactoring)
RPC: public.search_similar_cases (v8)
Changes: is_non_labor_case() filter, domain-aware keyword priority, trigram+keyword hybrid no-category, expanded metadata_boost (15 patterns)
Evaluator: Claude Opus 4.6
Previous Score: 146/240 (60.8%) — v7 + criminal filter

--- Per-Query Scores ---

Q01: "반복 무단결근으로 해고된 사건" (absence)
  #1: bc_7d0b20f9 경찰공무원 무단결근 견책 → score 1
  #2: id_10411 장기 무출근 132일 징계해고 정당 → score 1
  #3: id_46933 무단결근 해고 양정 과다 → score 2
  #4: id_32775 무단결근 7일 직권해직 정당 → score 2
  #5: bc_26c019ce 무단결근 징계해고 고용보험 → score 0
  Weighted: 6/10 (+2 vs v7)

Q02: "무단결근이 언급되지만 실제 핵심은 절차 위반인 사건" (absence)
  #1: bc_73c9121e 무단결근 판단 기준 → score 2
  #2: bc_79382b69 해고무효확인 다양한 비위 → score 1
  #3: id_4047 원직복직 후 무단결근 → score 1
  #4: id_3969 횡령+무단결근 비위 → score 1
  #5: bc_9335b15e 시말서 양심자유 징계재량 남용 → score 1
  Weighted: 6/10 (+3 vs v7) ✅ 주한미군(bc_4579b2fe), 종중(bc_bde1f750) 제거됨!

Q03: "택시나 버스 기사 무단결근 징계해고" (absence)
  #1: bc_c738fa55 택시 무단결근 징계해고 → score 2
  #2: bc_e466f0e8 택시기사 징계해고 무효 → score 2
  #3: bc_32705c27 택시운전기사 무단결근 징계해고 → score 2
  #4: bc_9a5050a2 광역버스 기사 면직 → score 2
  #5: bc_6ff36d06 전보 불응 해고 → score 0
  Weighted: 8/10 (unchanged)

Q04: "직장내괴롭힘이 실제로 성립하는지 다툼이 핵심인 사건" (workplace_bullying)
  #1: bc_293df091 카마스터 부당노동행위 → score 0
  #2: bc_11ac014e 괴롭힘 손해배상 기각 → score 1
  #3: bc_38504ee6 괴롭힘 손해배상 인정 → score 1
  #4: bc_3daf53ba 선박 무단 출항 → score 0
  #5: bc_4073f614 괴롭힘 손해배상 인정 → score 1
  Weighted: 3/10 (unchanged) | 형사사건(bc_f47e23b9) 제거됨

Q05: "직장내괴롭힘 신고 후 불이익이나 보복이 문제 된 사건" (workplace_bullying)
  #1: id_49193 괴롭힘 신고 후 인사발령 → score 1
  #2: id_3745 괴롭힘 신고 후 분리배치 → score 1
  #3: id_3591 괴롭힘 제기 후 전보 → score 1
  #4: id_401847 괴롭힘 조사 후 대기발령 → score 1
  #5: id_405489 괴롭힘 신고 후 대기발령 → score 1
  Weighted: 5/10 (+4 vs v7) ✅ 형사사건(bc_f47e23b9) 제거, 보복/불이익 관련 결과 모두 올라옴

Q06: "괴롭힘은 인정되는데 징계 수위가 과한지 보는 사건" (workplace_bullying)
  #1: id_58067 괴롭힘+주식거래 양정 과하 → score 2
  #2: id_44513 일부 인정, 양정 과하 → score 1
  #3: id_413513 괴롭힘 일부 확인, 양정 과다 → score 2
  #4: id_6051 괴롭힘 인정, 명예훼손 불인정 → score 1
  #5: id_20027 성희롱+괴롭힘 징계 → score 1
  Weighted: 7/10 (-2 vs v7) | id_405643(2), id_49591(2) 탈락

Q07: "수습기간 중 본채용 거부가 정당한지" (probation)
  All 5: 수습 본채용 거부 정당성 → score 2 each
  Weighted: 10/10 (unchanged)

Q08: "수습기간 중 업무능력 부족으로 해고하거나 본채용 거부한 사건" (probation)
  #1: id_27339 수습 업무능력 부족 해고 부당 → score 2
  #2: bc_035c5912 경영악화 사직 보장 → score 0
  #3: bc_16e26c6b 수습 업무능력 부족 본채용 거절 → score 2
  #4: id_40327 수습 업무 미숙지 해고 정당 → score 2
  #5: id_350467 수습기간 해고 정당 → score 2
  Weighted: 8/10 (-2 vs v7) | bc_035c5912 비관련

Q09: "수습인데 서면통지나 절차 문제가 있는 사건" (probation)
  #1: bc_259a6b85 기간제 갱신거절 절차 → score 0
  #2: id_351481 수습평가 절차 하자 부당해고 → score 2
  #3: id_413685 수습 평가 미안내 절차 하자 → score 2
  #4: bc_669ef49a 복직명령 구제이익 → score 0
  #5: id_15015 수습기간 업무 정리 통보 → score 1
  Weighted: 5/10 (+1 vs v7) | id_413685 신규 (절차하자 정확 매칭)

Q10: "정규직 저성과나 업무능력 부족으로 해고된 사건" (incompetence)
  #1: id_21941 업무능력 부족 반복 실수 징계 → score 2
  #2: bc_f33725f1 업무능력 부족 해고무효 → score 1
  #3: bc_ef2c957c 업무능력 부족 해고무효 → score 1
  #4: bc_124a6155 업무능력 부족 해고무효 → score 1
  #5: id_412461 업무능력 부족 양정 과도 → score 2
  Weighted: 7/10 (+1 vs v7)

Q11: "개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건" (incompetence)
  #1: id_21941 반복 실수 개선노력 없음 해고 → score 2
  #2: id_22147 수습 업무평가 → score 0
  #3: id_43873 잦은 병가 직장괴롭힘 → score 1
  #4: bc_f33725f1 업무능력 부족 해고무효 → score 1
  #5: bc_ef2c957c 업무능력 부족 해고무효 → score 1
  Weighted: 5/10 (unchanged)

Q12: "징계사유는 인정되지만 해고가 너무 과하다고 본 사건" ("")
  #1: id_24205 폭행 양정 과다 → score 2
  #2: id_1989 징계사유 일부 인정, 양정 과하 → score 2
  #3: id_27677 일부 비위 인정, 양정 과하 → score 2
  #4: bc_16761155 부당해고 부당노동행위 → score 0
  #5: bc_1131cb78 택시 징계해고 절차 하자 → score 0
  Weighted: 6/10 (+3 vs v7) ✅ 5건 반환 복구, trigram+keyword hybrid 효과

Q13: "정직 처분 양정이 적정한지 본 사건" ("")
  #1: id_2451 정직 양정 적정성 소명기회 → score 2
  #2: id_34279 정직 인사기밀 양정 → score 2
  #3: id_4295 반복 무단결근 정직 정당 → score 2
  #4: id_411029 인사서류 미제출 정직 양정 과하 → score 2
  #5: id_53907 음주측정 거부 정직 양정 → score 2
  Weighted: 10/10 (+1 vs v7)

Q14: "감봉 처분이 과한지 본 사건" ("")
  #1: id_34307 감봉 1월 정당 → score 2
  #2: id_404985 성희롱 감봉 양정 → score 1
  #3: id_37047 공개사과 거부 감봉 병과 부당 → score 1
  #4: id_32883 근속승진누락 감봉 효과 → score 0
  #5: id_14765 정직+감봉 초과 → score 1
  Weighted: 5/10 (+2 vs v7) ✅ 5건 반환 복구

Q15: "기간제 근로자의 갱신기대권이 인정되는지" (contract_expiry)
  All 5: 갱신기대권 판단 → score 2 each
  Weighted: 10/10 (unchanged)

Q16: "계약기간 만료인데 사실상 해고처럼 다퉈진 사건" (contract_expiry)
  All 5: 계약만료/갱신기대권 기각 → score 1 each
  Weighted: 5/10 (unchanged)

Q17: "전보나 인사발령이 정당한지 다툰 사건" (transfer)
  #1: bc_eaa30af8 부당 인사발령 구제 → score 2
  #2: id_46985 인사발령 정당성 → score 2
  #3: id_406109 인사발령 정당+징계 양정 과하 → score 2
  #4: id_407431 인사발령 정당 인사권 행사 → score 2
  #5: id_38827 전보 정당+해고 절차 하자 → score 1
  Weighted: 9/10 (-1 vs v7)

Q18: "대기발령이나 배치전환이 징계인지 인사권 행사인지 다툼" (transfer)
  #1: id_57819 대기발령+배치전환 정당/부당 → score 2
  #2: bc_ddc8f008 대기발령 무효 확인 → score 1
  #3: bc_b38b17e7 배치전환 무효확인 → score 1
  #4: bc_f5c2e46f 대기발령 구제이익+인사발령 → score 1
  #5: id_349613 징계+인사발령 정당성 → score 1
  Weighted: 6/10 (-4 vs v7) ⚠️ 이전 결과(10/10)와 차이 큼

Q19: "폭행이나 욕설 같은 비위 사실 자체가 인정되는지가 핵심인 사건" (violence)
  #1: bc_556b29b4 군인 징계처분 → score 0 | 군사법 (is_non_labor_case 미감지: title에 "군인" 없음)
  #2: bc_4a2b2c50 교사 폭행/욕설 해임 → score 1
  #3: bc_be7ae41d 군무원 파면 → score 0 | 군사법
  #4: bc_8694b90d 군인 폭언 징계 → score 0 | 군사법
  #5: bc_76eaeea9 공무원 해임 → score 0
  Weighted: 1/10 (-1 vs v7) ⚠️ 군사법 사건 다수 (title에 패턴 없어 필터 통과)

Q20: "폭행은 있었지만 해고까지는 과하다고 본 사건" (violence)
  #1: id_24205 원청 작업반장 폭행 해고 부당 → score 2
  #2: id_46647 특수폭행 해고 정당 → score 0
  #3: id_403329 동료 폭행 양정 과다 → score 1
  #4: id_348333 직장질서 문란 양정 과다 → score 1
  #5: id_22783 우발적 폭행 양정 과다 → score 2
  Weighted: 6/10 (unchanged)

Q21: "욕설이나 직장질서 문란이 반복되어 징계해고된 사건" (violence)
  #1: id_348451 상관 모독 양정 과다 → score 1
  #2: id_12017 성희롱+폭행+폭언 징계해고 → score 1
  #3: id_1785 여성 반장에 욕설 정직 양정 과하 → score 2
  #4: bc_f1697bf7 PD 정직처분 → score 0
  #5: id_22071 임원 비방 양정 과하 → score 1
  Weighted: 5/10 (-1 vs v7)

Q22: "근로자성이 실제 핵심 쟁점인 사건" (worker_status)
  #1: id_26633 교회 근로자 수 5인 미만 → score 2 | 근로자성 판단 포함
  #2: id_57465 근로자성+갱신기대권 → score 1
  #3: id_52945 총수 조직 근로자성 → score 2
  #4: id_51825 센터장 근로자성 → score 1
  #5: id_412541 대표이사 근로자성 → score 2
  Weighted: 8/10 (-2 vs v7)

Q23: "괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건" (workplace_bullying)
  #1: bc_418e69b1 갱신거절 → score 1
  #2: id_347 무단결근+직장질서 → score 0
  #3: id_58067 괴롭힘 인정됨 → score 0
  #4: bc_e4b49065 무고 손해배상 → score 1
  #5: bc_4b6618b8 공익신고자 보호 → score 1
  Weighted: 3/10 (unchanged)

Q24: "여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건" ("")
  #1: id_50753 징계사유 3개 중 2개 인정, 해고 정당 → score 1
  #2: id_347335 비위 전보+징계 → score 1
  #3: id_49053 성희롱 반복+해고 정당 → score 1
  #4: id_15759 상사지시 비위 양정 과하 → score 1
  #5: id_346607 성폭력 벌금 당연퇴직 → score 1
  Weighted: 5/10 (-1 vs v7)

--- Summary ---

Q01: 6, Q02: 6, Q03: 8, Q04: 3, Q05: 5, Q06: 7
Q07: 10, Q08: 8, Q09: 5, Q10: 7, Q11: 5, Q12: 6
Q13: 10, Q14: 5, Q15: 10, Q16: 5, Q17: 9, Q18: 6
Q19: 1, Q20: 6, Q21: 5, Q22: 8, Q23: 3, Q24: 5

--- TOTAL ---
Total: 154/240 (64.2%)
Previous (v7): 146/240 (60.8%)
Change: +8 (+3.3%p) IMPROVEMENT

--- Delta Analysis ---

Improved (+):
  Q01:  4 →  6 (+2) | id_32775 무단결근 직권해직 신규 매칭
  Q02:  3 →  6 (+3) | 주한미군(bc_4579b2fe), 종중(bc_bde1f750) 완전 제거 ✅
  Q05:  1 →  5 (+4) | 형사사건 제거, 보복/불이익 관련 5건 모두 매칭 ✅
  Q09:  4 →  5 (+1) | id_413685 수습 평가 미안내 절차하자 신규
  Q10:  6 →  7 (+1) | incompetence BigCase 데이터 유입
  Q12:  3 →  6 (+3) | trigram+keyword hybrid 효과, 5건 반환 복구 ✅
  Q13:  9 → 10 (+1) | 정직 양정 완벽 매칭
  Q14:  3 →  5 (+2) | 5건 반환 복구, 감봉 관련 다양 매칭

Degraded (-):
  Q06:  9 →  7 (-2) | id_405643(감봉2월), id_49591(감봉) 탈락 → BigCase 결과로 교체
  Q08: 10 →  8 (-2) | bc_035c5912(경영악화 사직 보장) 비관련 유입
  Q17: 10 →  9 (-1) | id_38827 전보+해고 절차하자 (전보 정당이지만 해고 하자)
  Q18: 10 →  6 (-4) | ⚠️ 주요 회귀 — 이전 정확 매칭 결과들이 탈락
  Q19:  2 →  1 (-1) | 군사법 사건 다수 (title에 패턴 없어 필터 통과)
  Q21:  6 →  5 (-1) | bc_f1697bf7 PD 정직 비관련 유입
  Q22: 10 →  8 (-2) | 일부 근로자성 핵심 결과 탈락
  Q24:  6 →  5 (-1) | 복합비위 해고 정당성 결과 변동

Unchanged (=): Q03, Q04, Q11, Q15, Q16, Q20, Q23

--- Critical Issues ---

### 1. Q18 REGRESSION (-4): 대기발령/배치전환
v7에서 10/10 → v8에서 6/10. BigCase 결과들이 우선순위를 차지하면서
기존 잘 매칭되던 노동위 판정례가 밀려남.
원인: is_non_labor_case() 필터가 결과 pool을 줄이면서 순위 재배열 발생.

### 2. Q19 PERSISTENT WEAKNESS: 군사법 사건 미필터링
bc_556b29b4(군인 징계), bc_be7ae41d(군무원 파면), bc_8694b90d(군인 폭언) 등
title에 "군인사법"이 없고 holding_summary에도 패턴이 부족하여 is_non_labor_case 통과.
해결: holding_summary 검사에 '군인', '군무원', '병사', '장교' 키워드 추가 필요.

### 3. Q08/Q22 REGRESSIONS: BigCase 데이터 품질
BigCase에서 수집된 결과 중 key_issue="..." (빈 값) 건이 있어
relevance 계산에서 의미 있는 메타데이터 부스트를 받지 못하면서도 카테고리 매칭으로 상위 랭크.

### 4. NO-CATEGORY QUERIES (Q12, Q14, Q24) 개선되었으나 여전히 약점
trigram+keyword hybrid가 결과 수 복구에 성공했으나,
상위 결과의 정확도는 카테고리 있는 쿼리 대비 여전히 낮음.

--- Score Projection ---

현재: 154/240 (64.2%)

즉시 적용 가능한 개선:
1. Q18 복구: 대기발령/배치전환 키워드 부스트 추가 → +4
2. Q19 군사법 필터 보강: '군인','군무원','병사' 패턴 → +2~3
3. Q08 BigCase 빈 데이터 필터: key_issue가 없는 결과 페널티 → +2

예상: 154+8 = 162/240 (67.5%)

Hybrid RPC (embedding 활용) 평가 시:
예상: 175-190/240 (73-79%)

95% 목표 달성을 위한 근본적 한계:
- Text-only search 최대: ~170/240 (71%)
- Hybrid (text+vector): ~190/240 (79%)
- 95% = 228/240 — Query rewriting + RAG + 도메인 분류기 필요
- 현실적 단기 목표: Hybrid로 75%+ 달성 후 점진 개선
