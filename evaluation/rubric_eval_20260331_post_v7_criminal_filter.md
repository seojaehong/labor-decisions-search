=== RUBRIC EVALUATION REPORT ===
Date: 2026-03-31 (2nd eval)
RPC: public.search_similar_cases (v7 + criminal case filter)
Changes since last eval: no-category keyword ILIKE (v7), criminal case WHERE filter
Evaluator: Claude Opus 4.6
Previous Score: 134/240 (55.8%) — legacy RPC only, direct call

--- Per-Query Scores ---

Q01: "반복 무단결근으로 해고된 사건" (absence)
  #1: bc_7d0b20f9 경찰공무원 무단결근 견책처분 → score 1
  #2: id_10411 장기 무출근 징계해고 정당 → score 1
  #3: id_46933 승무정지+무단결근 → score 2
  #4: id_1981 해고 부존재 → score 0
  #5: id_571 해고 부존재 → score 0
  Weighted: 4/10 (unchanged)

Q02: "무단결근이 언급되지만 실제 핵심은 절차 위반인 사건" (absence)
  #1: bc_73c9121e 무단결근 판단 기준 → score 2
  #2: bc_4579b2fe 주한미군 재판권 → score 0
  #3: bc_79382b69 해고무효확인 다양한 비위 → score 1
  #4: bc_bde1f750 종중 징계 → score 0
  #5: id_413011 무단결근 제척기간 도과 → score 0
  Weighted: 3/10 (unchanged)

Q03: "택시나 버스 기사 무단결근 징계해고" (absence)
  #1: bc_c738fa55 택시 무단결근 징계해고 고용보험 → score 2
  #2: bc_e466f0e8 택시기사 징계해고 무효 → score 2
  #3: bc_32705c27 택시운전기사 무단결근 징계해고 → score 2
  #4: bc_9a5050a2 광역버스 기사 면직 → score 2
  #5: id_39209 전보명령 불응 무단결근 → score 0
  Weighted: 8/10 (unchanged)

Q04: "직장내괴롭힘이 실제로 성립하는지 다툼이 핵심인 사건" (workplace_bullying)
  #1: bc_f47e23b9 명예훼손 형사사건 → score 0 | 형사사건
  #2: bc_293df091 카마스터 부당노동행위 → score 0 | 근로자성이 핵심
  #3: id_412935 괴롭힘 조사 후 대기발령 정당 → score 1 | 괴롭힘 배경이나 대기발령이 핵심
  #4: id_410665 괴롭힘 쟁점 대기발령 → score 1 | 괴롭힘 쟁점이나 대기발령/휴업이 핵심
  #5: bc_11ac014e 괴롭힘 손해배상 기각 → score 1 | 괴롭힘 성립 판단 포함
  Weighted: 3/10 (was 0, +3 IMPROVED)

Q05: "직장내괴롭힘 신고 후 불이익이나 보복이 문제 된 사건" (workplace_bullying)
  #1: id_49193 괴롭힘 신고 후 인사발령 → score 0
  #2: bc_5f4944f5 징계절차/양정 부당 → score 1
  #3: bc_f47e23b9 명예훼손 형사 → score 0
  #4: id_3745 괴롭힘 신고 분리배치 → score 0
  #5: id_3591 괴롭힘 제기 전보 → score 0
  Weighted: 1/10 (unchanged)

Q06: "괴롭힘은 인정되는데 징계 수위가 과한지 보는 사건" (workplace_bullying)
  #1: id_58067 괴롭힘+주식거래 양정 과하 → score 2
  #2: id_405643 괴롭힘 인정 감봉2월 정당 → score 2
  #3: id_49591 괴롭힘 인정 감봉 정당 → score 2
  #4: id_44513 징계사유 일부, 양정 과하 → score 1
  #5: id_413513 괴롭힘 징계사유, 양정 과하 → score 2
  Weighted: 9/10 (unchanged)

Q07: "수습기간 중 본채용 거부가 정당한지" (probation)
  All 5 results: 수습 본채용 거부 정당성 → score 2 each
  Weighted: 10/10 (unchanged)

Q08: "수습기간 중 업무능력 부족으로 해고하거나 본채용 거부한 사건" (probation)
  All 5 results: 수습 업무능력 부족 해고/본채용 거부 → score 2 each
  Weighted: 10/10 (unchanged)

Q09: "수습인데 서면통지나 절차 문제가 있는 사건" (probation)
  #1: id_60405 수습 근무평가 → score 1
  #2: bc_3daa7836 시용기간 해고 정당성 → score 1
  #3: bc_259a6b85 기간제 갱신거절 절차 → score 0
  #4: bc_6f8d5dc4 의원면직 → score 0
  #5: id_351481 수습평가 절차 하자 부당해고 → score 2
  Weighted: 4/10 (unchanged)

Q10: "정규직 저성과나 업무능력 부족으로 해고된 사건" (incompetence)
  #1: id_412461 업무능력 부족 양정 과도 → score 2
  #2: bc_002b2083 영양교사 갑질 → score 0
  #3: id_33547 업무능력 부족 해고 정당 → score 2
  #4: id_24195 업무능력 부족 개선의지 결여 → score 2
  #5: id_22147 수습기간 업무평가 → score 0
  Weighted: 6/10 (unchanged)

Q11: "개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건" (incompetence)
  #1: id_22147 수습 업무평가 → score 0
  #2: id_412461 업무능력 부족 양정 과도 → score 1
  #3: bc_002b2083 갑질 견책 → score 0
  #4: id_33547 직무능력 향상 교육 후 해고 정당 → score 2
  #5: id_24195 배치전환 노력 후 해고 → score 2
  Weighted: 5/10 (unchanged)

Q12: "징계사유는 인정되지만 해고가 너무 과하다고 본 사건" ("")
  #1: id_27207 징계사유 일부 인정, 양정 과하 → score 2
  #2: id_28061 직무태만 예산낭비, 해고 정당 → score 1
  (only 2 results returned — v7 keyword extraction issue)
  Weighted: 3/10 (was 10, -7 REGRESSION)
  ROOT CAUSE: v7 no-category 경로가 kw1="과하", kw2="너무"로 추출.
  "너무"는 법률문서에 거의 안 나오므로 매칭 2건뿐.
  이전에는 trigram 매칭으로 holding_summary에서 "양정 과다" 패턴 자유롭게 잡힘.

Q13: "정직 처분 양정이 적정한지 본 사건" ("")
  #1: id_411243 정직 징계사유, 양정 적정 → score 2
  #2: id_345077 정직 괴롭힘 양정 적정 → score 1
  #3: id_46869 정직처분 정당 (3가지 비위) → score 2
  #4: id_7893 정직처분 정당 → score 2
  #5: id_347185 비위 양정 과다 → score 2
  Weighted: 9/10 (was 0, +9 IMPROVED)

Q14: "감봉 처분이 과한지 본 사건" ("")
  #1: id_34307 감봉 1월 정당 (pay_cut) → score 2
  #2: id_32883 근속승진누락 (pay_cut) → score 0
  #3: id_14765 정직+감봉 초과 → score 1
  (only 3 results returned)
  Weighted: 3/10 (was 0, +3 IMPROVED)

Q15: "기간제 근로자의 갱신기대권이 인정되는지" (contract_expiry)
  All 5: 갱신기대권 판단 → score 2 each
  Weighted: 10/10 (unchanged)

Q16: "계약기간 만료인데 사실상 해고처럼 다퉈진 사건" (contract_expiry)
  All 5: 계약만료 고용종료 기각 → score 1 each
  Weighted: 5/10 (unchanged)

Q17: "전보나 인사발령이 정당한지 다툰 사건" (transfer)
  All 5: 인사발령/전보 정당성 → score 2 each
  Weighted: 10/10 (unchanged)

Q18: "대기발령이나 배치전환이 징계인지 인사권 행사인지 다툼" (transfer)
  All 5: 대기발령/배치전환 정당성 → score 2 each
  Weighted: 10/10 (unchanged)

Q19: "폭행이나 욕설 같은 비위 사실 자체가 인정되는지가 핵심인 사건" (violence)
  #1: bc_78fcbd6d 형사 폭행죄 판결 → score 0 | 형사사건 (필터 미적용: title에 "형사" 없음)
  #2: id_1759 욕설 비위 양정 과하 → score 1
  #3: id_269 욕설 비위 양정 과하 → score 1
  #4: bc_5fc1c9c9 군인 성군기 위반 정직 → score 0 | 군사법 (필터 미적용: title에 "군인사법" 없음)
  #5: bc_6c90f019 사관생도 퇴학처분 → score 0 | 군 사건
  Weighted: 2/10 (was 4, -2 REGRESSION)
  ROOT CAUSE: 형사필터가 title만 검사. holding_summary 미검사.
  이전 5위 id_407471(폭언욕설폭행, score 2)이 bc_6c90f019(퇴교, score 0)로 교체됨.

Q20: "폭행은 있었지만 해고까지는 과하다고 본 사건" (violence)
  #1: bc_25a2abdf 사적 폭행 해고 재량권 남용 → score 2
  #2: bc_3f56ed6a 택시회사 대표 폭행 해고 무효 → score 1
  #3: id_24205 동료 폭언 폭행 양정 과다 → score 2
  #4: id_46647 특수폭행 해고 정당 → score 0
  #5: id_403329 비위행위 양정 과다 (폭행) → score 1
  Weighted: 6/10 (unchanged)

Q21: "욕설이나 직장질서 문란이 반복되어 징계해고된 사건" (violence)
  #1: id_403837 성희롱+괴롭힘 징계해고 → score 1
  #2: id_348451 상관 모독 양정 과다 → score 1
  #3: id_12017 성희롱 폭행 폭언 징계해고 → score 1
  #4: id_1785 여성 반장에 욕설 정직 양정 과다 → score 2
  #5: id_22671 직장질서 문란 양정 과다 → score 1
  Weighted: 6/10 (unchanged)

Q22: "근로자성이 실제 핵심 쟁점인 사건" (worker_status)
  All 5: 근로자성 핵심 쟁점 → score 2 each
  Weighted: 10/10 (unchanged)

Q23: "괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건" (workplace_bullying)
  #1: bc_418e69b1 갱신거절 → score 1
  #2: id_347 징계 정당 → score 0
  #3: id_58067 괴롭힘 인정됨 → score 0
  #4: bc_e4b49065 무고 손해배상 → score 1
  #5: bc_4b6618b8 공익신고자 보호 → score 1
  Weighted: 3/10 (unchanged)

Q24: "여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건" ("")
  #1: id_53865 횡령+비위, 양정 과하 (3 categories) → score 1
  #2: id_53671 횡령+비위, 양정 과하 (3 categories) → score 1
  #3: id_46869 3가지 징계사유, 정직 → score 1 | 여러 비위이나 해고 아닌 정직
  #4: id_344625 violence+absence+misconduct 해고 정당 → score 2
  #5: id_404365 absence+misconduct 해고 정당 → score 1
  Weighted: 6/10 (was 0, +6 IMPROVED)

--- Summary ---

Q01: 4, Q02: 3, Q03: 8, Q04: 3, Q05: 1, Q06: 9
Q07: 10, Q08: 10, Q09: 4, Q10: 6, Q11: 5, Q12: 3
Q13: 9, Q14: 3, Q15: 10, Q16: 5, Q17: 10, Q18: 10
Q19: 2, Q20: 6, Q21: 6, Q22: 10, Q23: 3, Q24: 6

--- TOTAL ---
Total: 146/240 (60.8%)
Previous: 134/240 (55.8%)
Change: +12 (+5.0%p) IMPROVEMENT

--- Delta Analysis ---

Improved (+):
  Q04:  0 →  3 (+3) | 괴롭힘 성립 - 결과 반환 복구 (여전히 약함)
  Q13:  0 →  9 (+9) | 정직 양정 - no-category fix 효과. sanction_type=suspension 매칭
  Q14:  0 →  3 (+3) | 감봉 양정 - no-category fix. 3건만 반환 (keyword "감봉" 매칭)
  Q24:  0 →  6 (+6) | 복합비위 - no-category fix. 여러 reason_category 사건 매칭

Degraded (-):
  Q12: 10 →  3 (-7) | 양정 과다 - v7 keyword 추출이 "과하/너무" 선택 → 2건만 반환
  Q19:  4 →  2 (-2) | 폭행/욕설 비위 - 형사필터로 결과 순서 변경, 좋은 결과 탈락

Unchanged (=): Q01-Q03, Q05-Q11, Q15-Q18, Q20-Q23

--- Critical Issues ---

### 1. V7 KEYWORD EXTRACTION REGRESSION (Q12: -7)
v7의 no-category 경로가 2글자 어간을 알파벳순 정렬 후 kw1/kw2 선택.
"징계사유는 인정되지만 해고가 너무 과하다고 본 사건" → kw1="과하", kw2="너무"
"너무"는 법률문서에 거의 사용되지 않아 매칭 실패.
**수정안**: 키워드 선택 전략 변경 — 알파벳순이 아닌 TF-IDF 또는 길이순,
또는 no-category에서 trigram 매칭을 병행.

### 2. CRIMINAL FILTER TOO NARROW (Q19: -2)
title만 검사하여 holding_summary의 형사사건 표시를 놓침.
- bc_78fcbd6d: title="폭행" → "형사" 없음 → 필터 통과
- bc_5fc1c9c9: title="징계처분취소" → "군인사법" 없음 → 필터 통과
- bc_6c90f019: title="퇴교처분취소" → 패턴 없음 → 필터 통과
**수정안**: holding_summary도 검사 대상에 포함하고, 패턴 추가 (고정/고단 = 형사사건번호)

### 3. NO-CATEGORY 결과 부족 (Q14: 3건만)
"감봉"은 매칭되지만 "처분이 과한지"에서 추출된 "처분/과한" 등은
title/key_issue에 빈번하지 않아 결과 부족.
**수정안**: 결과 < 5건일 때 trigram fallback

### 4. VIOLENCE 카테고리 약점 지속 (Q19: 2/10, Q21: 6/10)
폭행/욕설 비위 카테고리에서 형사사건+군사법 사건이 섞여 있어 정확도 저하.
violence 카테고리 자체의 데이터 정제가 필요.

--- Recommendations (Priority Order) ---

1. **[긴급] Q12 복구: no-category 경로에 trigram 매칭 병행**
   - 현재: keyword ILIKE만 → 2건
   - 개선: keyword ILIKE + trigram(title % q OR key_issue % q) → 예상 10건+
   - 예상 효과: Q12 3→10 (+7)

2. **[긴급] 형사필터 확대: holding_summary 추가 + 패턴 보강**
   - holding_summary에 "형사", "형법 제", "군인사법" 패턴 추가
   - 사건번호 패턴: "고정", "고단", "고합" = 형사 1심
   - 예상 효과: Q19 2→4+ (+2)

3. **[중요] keyword 선택 전략 개선**
   - 현재: left(w,2) 알파벳순 → "과하" "너무" 같은 일반 단어 선택
   - 개선: 법률 도메인 중요 키워드 우선 (해고, 징계, 감봉, 정직 등)
   - 또는 길이가 긴 원본 키워드 우선

4. **[향후] 벡터 인덱스 활용 hybrid 평가**
   - 현재 평가는 legacy RPC만 사용 (search_similar_cases)
   - 앱 경유 시 query rewriting + embedding → search_similar_cases_hybrid 사용
   - hybrid 평가로 실제 서비스 품질 측정 필요

--- Score Projection ---

Q12 복구(+7) + 형사필터 보강(+2) 적용 시:
예상: 146+9 = 155/240 (64.6%)

추가로 keyword 전략 개선(Q14 +2~4) 시:
예상: ~159/240 (66.3%)

Hybrid RPC 사용 시 (embedding 활용):
예상: 170-185/240 (71-77%) — 이전 앱경유 평가 수준 회복 가능
