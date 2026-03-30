=== RUBRIC EVALUATION REPORT ===
Date: 2026-03-30
Model: Haiku (independent evaluator)
Total Queries: 24

--- Per-Query Results ---

Q01: "반복 무단결근으로 해고된 사건" (category: 무단결근)
  #1: bc_e62151d0 부당해고구제재심판결취소 → score 2 | reason: Core absence dismissal, legitimate procedure
  #2: bc_38c5e47c 시용기간 중 무단결근 본채용거부 → score 2 | reason: Probation absence, directly relevant
  #3: bc_82f94de1 해고 무효 확인 및 미지급임금 → score 1 | reason: Absence mentioned but procedure issue is core
  #4: bc_32705c27 택시운전기사 무단결근 징계해고 → score 2 | reason: Transport + absence, core issue
  #5: bc_3b920e8d 겸직 및 무단결근 징계해고 → score 1 | reason: Absence among multiple issues
  Precision@5: 4/5 | Weighted: 8/10

Q02: "무단결근이 언급되지만 실제 핵심은 절차 위반인 사건" (category: 무단결근)
  #1: id_15115 부당해고 구제신청 → score 2 | reason: Procedure focus with absence, matches intent
  #2: bc_ef80136b 징계위원 기피신청 절차 위반 → score 2 | reason: Pure procedure violation, no dismissal core
  #3: bc_3b905ccf 해고예고의무 위반 근로기준법 → score 1 | reason: Procedure (notice) but not absence-centered
  #4: bc_46e59bda 해고예고의무 위반 근로기준법 → score 1 | reason: Notice violation, different context
  #5: bc_43c45045 부당해고 재심판정 취소 → score 1 | reason: Procedure issue but dismissal is core
  Precision@5: 2/5 | Weighted: 6/10

Q03: "택시나 버스 기사 무단결근 징계해고" (category: 무단결근)
  #1: bc_32705c27 택시운전기사 무단결근 징계해고 → score 2 | reason: Exact match: taxi driver absence dismissal
  #2: bc_3b920e8d 겸직 및 무단결근 징계해고 → score 1 | reason: General absence, not transport industry
  #3: bc_2c4e9c0a 공무원 무단결근 감봉 → score 0 | reason: Public servant, not transportation
  #4: bc_445f5ace 택시 기사 해고 절차적 하자 → score 1 | reason: Taxi but procedure focus, not pure absence
  #5: id_15115 부당해고 구제신청 → score 1 | reason: General absence, not transport-specific
  Precision@5: 1/5 | Weighted: 5/10

Q04: "직장내괴롭힘이 실제로 성립하는지 다툼이 핵심인 사건" (category: 직장내괴롭힘)
  #1: bc_559a6691 직장 내 괴롭힘으로 위자료 청구 → score 2 | reason: Harassment establishment confirmed
  #2: bc_2e221184 직장 내 괴롭힘 손해배상 항소 → score 2 | reason: Harassment facts disputed and judged
  #3: bc_2cf7424f 상급자의 폭행 직장괴롭힘 사건 → score 1 | reason: Harassment but also criminal (assault)
  #4: bc_e818dc89 부당한 명령휴직 직장괴롭힘 → score 2 | reason: Harassment core issue, multiple harms
  #5: id_349929 부당해고 구제신청 → score 2 | reason: Harassment establishment dispute focus
  Precision@5: 4/5 | Weighted: 8/10

Q05: "직장내괴롭힘 신고 후 불이익이나 보복이 문제 된 사건" (category: 직장내괴롭힘)
  #1: bc_4e6d2a02 육아휴직 후 복직 불이익 조치 → score 1 | reason: Retaliation concept but different context
  #2: id_42979 괴롭힘 신고인보다 징계 → score 2 | reason: Retaliation against reporter focus
  #3: bc_2cf7424f 상급자의 폭행 직장괴롭힘 → score 1 | reason: Harassment but not retaliation framing
  #4: bc_559a6691 직장 내 괴롭힘 위자료 청구 → score 1 | reason: Harassment but not retaliation focus
  #5: bc_480323f5 직장내괴롭힘 보호의무 위반 자살 → score 0 | reason: Criminal harm level, not employment retaliation
  Precision@5: 1/5 | Weighted: 4/10

Q06: "괴롭힘은 인정되는데 징계 수위가 과한지 보는 사건" (category: 직장내괴롭힘)
  #1: bc_559a6691 직장 내 괴롭힘 위자료 청구 → score 1 | reason: Harassment recognized but not discipline severity
  #2: bc_2b8eea9b 징계사유 인정되나 양정 과도 → score 2 | reason: Harassment + proportionality core
  #3: id_406575 직장내괴롭힘 징계양정 정당 → score 2 | reason: Harassment recognized, discipline severity examined
  #4: id_345701 직장내괴롭힘 정직 양정 과다 → score 2 | reason: Harassment + proportionality focus
  #5: id_20027 성희롱 괴롭힘 해고 양정 과하다 → score 2 | reason: Harassment recognized, dismissal severity questioned
  Precision@5: 4/5 | Weighted: 8/10

Q07: "수습기간 중 본채용 거부가 정당한지" (category: 수습)
  #1: bc_ac1f847b 수습기간 중 근로계약 해지 정당성 → score 2 | reason: Probation rejection validity core
  #2: bc_50f8a97d 수습기간 중 해고 절차적 정당성 → score 2 | reason: Probation rejection procedure examined
  #3: id_17275 수습기간 중 본채용 거부 정당 → score 2 | reason: Probation rejection validity exact match
  #4: id_31161 수습기간 중 업무평가 본채용 거부 → score 2 | reason: Probation evaluation + rejection
  #5: id_17675 수습근로자 업무능력 고려 해지 → score 2 | reason: Probation rejection based on competence
  Precision@5: 5/5 | Weighted: 10/10

Q08: "수습기간 중 업무능력 부족으로 해고하거나 본채용 거부한 사건" (category: 수습)
  #1: id_17275 수습기간 중 본채용 거부 정당 → score 2 | reason: Probation + incompetence core
  #2: id_31161 수습기간 근무실적 평가 본채용거부 → score 2 | reason: Probation + performance evaluation
  #3: id_17675 수습근로자 업무능력 고려 해지 → score 2 | reason: Probation + competence assessment
  #4: id_13937 시용기간 본채용 거부 서면통지 위반 → score 1 | reason: Probation but procedure focus
  #5: id_15853 시용기간 본채용 거부 서면통지 위반 → score 1 | reason: Probation but procedure violation
  Precision@5: 3/5 | Weighted: 8/10

Q09: "수습인데 서면통지나 절차 문제가 있는 사건" (category: 수습)
  #1: id_15099 수습기간 근무지 이탈 해고 정당 → score 1 | reason: Probation but not notice procedure
  #2: id_35799 수습근로자 평가 서면통지 위반 → score 2 | reason: Probation + notice procedure violation
  #3: id_31373 시용근로자 평가 없고 서면통지 위반 → score 2 | reason: Probation + notice procedure core
  #4: id_13693 수습계약 서면통지 의무 위반 → score 2 | reason: Probation + oral dismissal invalidity
  #5: id_60405 시용근로자 근무평가 본채용 거부 → score 1 | reason: Probation but substantive evaluation focus
  Precision@5: 3/5 | Weighted: 8/10

Q10: "정규직 저성과나 업무능력 부족으로 해고된 사건" (category: 근무태만)
  #1: bc_e7b2566d 부당해고 재심신청 업무능력 부족 → score 2 | reason: Regular employee incompetence core
  #2: bc_31af3f2d 부당노동행위 업무능력 부족 → score 1 | reason: Incompetence but labor practice focus
  #3: bc_91bf300e 업무 저성과 해고 정당성 → score 2 | reason: Regular employee low performance dismissal
  #4: id_15181 근무실적 평가 규정 위반 해고 → score 2 | reason: Regular employee performance dismissal
  #5: bc_3473e185 부당해고 무효 해고기간 임금 → score 1 | reason: General dismissal, not performance-specific
  Precision@5: 3/5 | Weighted: 8/10

Q11: "개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건" (category: 근무태만)
  #1: bc_e7b2566d 부당해고 재심신청 업무능력 부족 → score 1 | reason: Incompetence but no improvement opportunity documented
  #2: bc_31af3f2d 부당노동행위 업무능력 부족 → score 1 | reason: Incompetence but labor practice focus
  #3: id_15181 규정 위반 근무실적 평가 해고 → score 2 | reason: Multiple improvement chances given before dismissal
  #4: bc_3473e185 부당해고 무효 해고기간 임금 → score 0 | reason: General dismissal, no improvement opportunity mention
  #5: bc_4bf13781 영양교사 조리사 업무능력 부족 → score 0 | reason: Non-labor context (public servant reprimand)
  Precision@5: 1/5 | Weighted: 4/10

Q12: "징계사유는 인정되지만 해고가 너무 과하다고 본 사건" (category: empty)
  #1: id_47837 징계사유 인정 해고 양정 과다 → score 2 | reason: Misconduct recognized, dismissal severity excessive
  #2: id_55817 금품수수 징계사유 인정 양정 과하다 → score 2 | reason: Misconduct found, discipline too severe
  #3: id_48737 징계사유 모두 인정 양정 정당 → score 1 | reason: Misconduct recognized but proportionality upheld
  #4: id_48315 징계사유 대부분 인정 양정 적정 → score 1 | reason: Misconduct + proportionality but dismissal upheld
  #5: id_48237 무단결근 징계사유 인정 해고 정당 → score 0 | reason: Misconduct recognized, dismissal upheld as proper
  Precision@5: 2/5 | Weighted: 6/10

Q13: "정직 처분 양정이 적정한지 본 사건" (category: empty)
  #1: id_59397 징계사유 정직 1개월 양정 과다 → score 2 | reason: Suspension severity examined, found excessive
  #2: id_52717 징계사유 인정 정직 2개월 정당 → score 1 | reason: Suspension but discipline upheld as proper
  #3: id_52135 징계사유 정직 1개월 정당 → score 1 | reason: Suspension examined, upheld as proportionate
  #4: id_539 징계사유 정직 3개월 정당 → score 1 | reason: Suspension proportionality but upheld
  #5: id_43927 징계사유 일부 인정 정직 6월 과하다 → score 2 | reason: Suspension severity assessed, some excessive
  Precision@5: 2/5 | Weighted: 6/10

Q14: "감봉 처분이 과한지 본 사건" (category: empty)
  #1: bc_da30ec65 감봉 3월 처분 취소 청구 기각 → score 1 | reason: Pay cut severity examined but upheld
  #2: bc_3ac312ae 감봉 3월 처분 취소 → score 2 | reason: Pay cut severity found excessive, cancelled
  #3: bc_9bc01aad 감봉 1월 징계처분 취소 → score 2 | reason: Pay cut found disproportionate, cancelled
  #4: bc_e26298fd 감봉 3월 징계처분 취소 → score 2 | reason: Pay cut severity found excessive
  #5: bc_548f90f1 퇴직 처분 무효 임금 청구 → score 0 | reason: Retirement (not pay cut severity), general dismissal
  Precision@5: 3/5 | Weighted: 8/10

Q15: "기간제 근로자의 갱신기대권이 인정되는지" (category: 갱신기대권)
  #1: bc_5ec76e7b 기간제 갱신기대권 인정 부당해고 → score 2 | reason: Renewal expectation core issue
  #2: bc_20ffd56e 기간제 갱신기대권 거절 합리적 이유 → score 2 | reason: Renewal expectation examined, rejected
  #3: bc_cae42353 기간제 갱신기대권 절차적 하자 → score 2 | reason: Renewal expectation + procedure examined
  #4: bc_ae507334 기간제 갱신기대권 인정되지 않음 → score 2 | reason: Renewal expectation verdict, not recognized
  #5: bc_09166594 기간제 갱신기대권 무기계약 전환 → score 2 | reason: Renewal expectation judgment
  Precision@5: 5/5 | Weighted: 10/10

Q16: "계약기간 만료인데 사실상 해고처럼 다퉈진 사건" (category: 갱신기대권)
  #1: id_14371 계약기간 만료 구제이익 소멸 → score 2 | reason: Contract expiry treated as dismissal issue
  #2: id_349995 사직원 계약기간 만료 → score 1 | reason: Contract expiry but resignation focus
  #3: id_11429 계약기간 만료 해고 부존재 → score 2 | reason: Contract expiry / dismissal distinction
  #4: id_411099 2차 근로계약 미성립 계약기간 만료 → score 1 | reason: Contract negotiation, not expiry as dismissal
  #5: id_31115 계약기간 만료 부당해고 인정 → score 2 | reason: Contract expiry treated as improper dismissal
  Precision@5: 3/5 | Weighted: 8/10

Q17: "전보나 인사발령이 정당한지 다툰 사건" (category: 전보)
  #1: id_1059 보직변경 인사발령 정당 정직 징계 → score 2 | reason: Transfer validity examined
  #2: id_16591 인사발령 강등 해당 안함 정당 → score 2 | reason: Transfer validity core
  #3: id_348595 인사발령 업무상 필요성 정당 → score 2 | reason: Transfer legitimacy judgment
  #4: bc_374b678c 해외주재원 국내 귀임 인사발령 → score 2 | reason: Transfer validity examined
  #5: id_349529 전직 업무상 필요성 정당 → score 2 | reason: Transfer necessity assessed
  Precision@5: 5/5 | Weighted: 10/10

Q18: "대기발령이나 배치전환이 징계인지 인사권 행사인지 다툼" (category: 전보)
  #1: bc_2d2ee3ef 부당 배치전환 임금차액 위자료 → score 2 | reason: Transfer vs discipline distinction
  #2: id_16945 배치전환 업무상 필요성 정당 → score 2 | reason: Transfer legitimacy examined
  #3: id_348383 보직해임 제재 또는 인사명령 → score 2 | reason: Transfer as discipline vs HR action
  #4: id_16863 배치전환 업무상 필요성 정당 → score 2 | reason: Transfer legitimacy core
  #5: id_43877 인사발령 징계기간 종료 원직복직 → score 2 | reason: Transfer as remedy vs new HR action
  Precision@5: 5/5 | Weighted: 10/10

Q19: "폭행이나 욕설 같은 비위 사실 자체가 인정되는지가 핵심" (category: 폭言)
  #1: id_47155 폭행 행위 징계사유 인정 → score 2 | reason: Misconduct establishment core
  #2: id_11633 욕설 폭언 징계사유 인정 일부 → score 2 | reason: Misconduct establishment focus
  #3: id_15419 욕설 폭언 근무지 무단이탈 징계 → score 2 | reason: Misconduct facts recognized
  #4: bc_b3af29ba 사용자 폭행 근로기준법 위반 → score 1 | reason: Criminal case (employer misconduct), not employee
  #5: id_11829 동료 폭행 징계사유 인정 양정 과하다 → score 2 | reason: Misconduct recognized, severity evaluated
  Precision@5: 4/5 | Weighted: 8/10

Q20: "폭행은 있었지만 해고까지는 과하다고 본 사건" (category: 폭言)
  #1: id_24205 동료 폭언 폭행 책임 일부 해고 과하다 → score 2 | reason: Violence + proportionality core
  #2: id_38087 동료 쌍방폭행 징계 양정 과하다 → score 2 | reason: Violence recognized, dismissal excessive
  #3: id_18545 폭행 발생 사용자 책임도 양정 과하다 → score 2 | reason: Violence severity and proportionality
  #4: bc_e7c637b7 해고 보복성 폭행 특수협박 → score 0 | reason: Criminal case (post-dismissal retaliation)
  #5: bc_8e74f579 직장 해고 앙심 망치 폭행 → score 0 | reason: Criminal case (post-dismissal violence)
  Precision@5: 3/5 | Weighted: 6/10

Q21: "욕설이나 직장질서 문란이 반복되어 징계해고된 사건" (category: 폭言)
  #1: id_17095 비위행위 반복 신뢰관계 해쳐 징계 → score 2 | reason: Repeated misconduct + dismissal
  #2: id_411717 욕설 폭언 직장질서 위반 징계 정당 → score 2 | reason: Repeated speech misconduct
  #3: id_12013 폭언 욕설 직장질서 문란 징계 정당 → score 2 | reason: Misconduct and workplace disruption
  #4: id_16927 이력서 허위 직장질서 위반 징계 과하다 → score 1 | reason: Mixed misconduct, not pure speech
  #5: bc_ccae8fa4 동료 모욕 상해 징계해고 정당 → score 1 | reason: Harassment + injury, broader than speech
  Precision@5: 3/5 | Weighted: 8/10

Q22: "근로자성이 실제 핵심 쟁점인 사건" (category: 근로자성)
  #1: id_346709 해고절차 적법 해고사유 양정 과도 → score 0 | reason: Dismissal validity, not worker status
  #2: id_407107 근로계약 갱신 거절 건강상 문제 → score 0 | reason: Renewal expectation, not worker status
  #3: id_51041 전보 정당성 노동조합 지배개입 → score 0 | reason: Transfer + union rights, not worker status
  #4: id_29961 해고처분 존재 해고사유 미인정 → score 0 | reason: Dismissal validity, not worker status
  #5: id_36513 사용자 복직명령 구제이익 없음 → score 0 | reason: Remedy, not worker status determination
  Precision@5: 0/5 | Weighted: 0/10

Q23: "괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건" (category: 직장내괴롱힘)
  #1: id_348225 괴롭힘 사실 입증 자료 부재 전직 → score 2 | reason: No harassment found, transfer for failed claim
  #2: id_348245 괴롭힘 입증 자료 부족 전보 → score 2 | reason: No harassment established, conflict escalation
  #3: id_411165 대기발령 필요성 미인정 → score 1 | reason: Alleged harassment claim but needs more context
  #4: id_16261 대기발령 업무상 필요성 미인정 → score 1 | reason: Harassment claim but other dispute focus
  #5: id_346833 직장내괴롱힘 아님 징계사유 인정 안됨 → score 2 | reason: Harassment not recognized, conflict from false claim
  Precision@5: 3/5 | Weighted: 8/10

Q24: "여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건" (category: empty)
  #1: bc_e2f32941 기간제 갱신기대권 인정 여부 → score 0 | reason: Renewal expectation, not composite misconduct
  #2: id_20335 해고의 의사표시 미인정 → score 0 | reason: Dismissal existence, not composite cause
  #3: id_406769 근무평정 구제대상 여부 → score 0 | reason: Performance evaluation, not composite misconduct
  #4: id_24665 근로계약 종료사유 자진사직 → score 0 | reason: Resignation vs dismissal distinction
  #5: id_23277 해고 존재 단정 불가 → score 0 | reason: Dismissal existence disputed, not cause analysis
  Precision@5: 0/5 | Weighted: 0/10

--- Summary Metrics ---
Average Precision@5: 2.75/5 (55%)
Average Weighted Score@5: 6.75/10 (67.5%)
Total Score: 162/240 (67.5%)
Queries with Precision@5 = 1.0: 4/24 (Q07, Q15, Q17, Q18)
Queries with any 0-score result: 11/24

--- Critical Issues Found ---

1. **WORKER STATUS (Q22): COMPLETE FAILURE (0/10)**
   - Search returned dismissal cases, not worker status determination cases
   - None of the 5 results address the core legal issue: whether employee vs contractor/independent
   - System does not appear to have worker status (근로자성) cases indexed or retrievable
   - All results scored 0

2. **COMPOSITE MISCONDUCT (Q24): COMPLETE FAILURE (0/10)**
   - Query for multiple misconduct + final dismissal validity returned unrelated results
   - Results discuss renewal expectation, resignation, performance review, dismissal existence
   - No cases showing multiple concurrent breach factors with holistic proportionality judgment
   - All results scored 0

3. **HARASSMENT RETALIATION (Q05): WEAK (4/10)**
   - Only 1 result directly matched retaliation-after-report theme
   - Query returned general harassment cases, not retaliation-specific ones
   - Embedding may conflate "harassment" with "retaliation" incorrectly

4. **IMPROVEMENT OPPORTUNITY (Q11): WEAK (4/10)**
   - Query seeking "개선기회나 경고를 주고도" (given improvement chance then dismissed)
   - Only 1 result clearly showed multiple improvement attempts before dismissal
   - Most results discuss performance issues without documented improvement period

5. **CRIMINAL VS LABOR CASES LEAKING:**
   - Q19: Result bc_b3af29ba is criminal employer case, not employee misconduct
   - Q20: Results bc_e7c637b7, bc_8e74f579 are criminal retaliation cases, not workplace dismissal
   - These should score 0 (no labor dismissal law application)

6. **CATEGORY STRING TYPO (Q23):**
   - Query used '직장내괴롱힘' (with typo: 롱 instead of 롭)
   - RPC may have auto-corrected or results indicate flexible matching
   - Results were still relevant, but typo may indicate fragile string matching

7. **ABSENCE + TRANSPORT SPECIFICITY (Q03): WEAK (5/10)**
   - Only 1 transport industry case returned first
   - Query specificity (택시나 버스 기사) is high but matching is weak
   - System struggles to combine category + industry filters

--- Diagnostic Patterns ---

**Strong Performance (8-10/10):**
- Q07, Q15, Q17, Q18: All highly structured legal categories (probation, renewal expectation, transfer)
- These have clear metadata and consistent case law

**Moderate Performance (6-8/10):**
- Q01, Q04, Q06, Q10, Q12, Q13, Q14, Q16, Q21: Mixed results
- Usually 2-3 out of 5 results match query intent
- Proportionality/severity queries perform better than procedural ones

**Weak Performance (4-6/10):**
- Q02, Q03, Q05, Q11, Q20, Q23: Nuance lost
- Procedure-focused queries struggle
- Contextual modifiers (transport, retaliation, improvement) weakly matched

**Failed Performance (0-4/10):**
- Q22, Q24: Zero relevant results
- System lacks indexed cases for worker status determination
- Composite misconduct holistic judgment pattern not recognized

--- Final Score ---
**162/240 = 67.5/100**

**Interpretation:**
The search system performs adequately for straightforward legal categories (dismissal, probation, transfer, harassment establishment) but struggles with:
1. Procedural nuances (procedure violation within absence, notice requirements)
2. Contextual modifiers (transport industry, improvement opportunity, retaliation)
3. Missing entire case law areas (worker status, composite misconduct holistic review)
4. Embedding conflates related but distinct legal questions
5. Criminal cases leaked into labor law searches

**Recommendation for Improvement:**
- Index worker status (근로자성) cases separately
- Tag cases by contextual factors (industry, procedure type, precedent pattern)
- Strengthen embedding to distinguish retaliation from general harassment
- Filter out non-labor criminal cases at RPC level
- Add composite case markers for multi-breach holistic judgment cases
