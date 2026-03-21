import json, sys
sys.stdout.reconfigure(encoding='utf-8')

records = []

# union_activity: 공무원노조법 단체협약 무효 패턴 (12건)
records.append({
    "id": "id_58325",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "다면평가운영협의=임용권", "복지예산편성협의=예산편성", "공무원노조법시행령4조2호4호위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법시행령4조2호", "교섭사항비교섭사항구분"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "다면평가임용권비교섭", "복지예산편성비교섭"],
    "exclude_for_queries": [],
    "summary_short": "다면평가운영협의=임용권+복지예산편성협의=예산편성=공무원노조법시행령4조위반=단체협약효력없음",
    "holding_summary": "단체협약상 다면평가 실시와 평가항목 구성 등 운영에 필요한 사항을 노조와 협의하는 것은 공무원의 채용·승진·전보 등 임용권에 관한 사항으로 비교섭 대상이며 공무원노조법 제8조제1항 및 시행령 제4조제2호에 위반된다. 조합원 복지예산 편성을 노조와 사전 협의하도록 한 것은 정책결정과 기관의 예산편성에 관한 사항으로 공무원노조법 시행령 제4조 각호에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효 패턴. 다면평가=임용권 비교섭. 복지예산=예산편성 비교섭.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

records.append({
    "id": "id_58337",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "단협16조1항=임용권", "단협18조=예산편성", "공무원노조법시행령4조2호4호위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법시행령4조", "교섭사항비교섭사항구분"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "임용권비교섭", "예산편성비교섭"],
    "exclude_for_queries": [],
    "summary_short": "단협16조1항=임용권+단협18조=예산편성=공무원노조법시행령4조2호4호위반=단체협약효력없음",
    "holding_summary": "단체협약 제16조제1항과 제18조는 공무원의 채용·승진·전보 등 임용권에 관한 사항과 예산의 편성·집행에 관한 사항을 규정한 내용이므로 교섭사항에 해당한다고 볼 수 없다. 공무원노조법 제8조제1항 및 시행령 제4조 제2호, 제4호에 각각 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효 패턴 연속. 임용권·예산편성 비교섭 사항 확인.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

records.append({
    "id": "id_58339",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "단협13조1항=노동조합간부전보=임용권", "공무원노조법시행령4조2호위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법시행령4조2호", "노동조합간부전보임용권"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "노동조합간부전보임용권비교섭"],
    "exclude_for_queries": [],
    "summary_short": "단협13조1항=노동조합간부전보=임용권행사=공무원노조법시행령4조2호위반=단체협약효력없음",
    "holding_summary": "단체협약 제13조제1항은 노동조합 간부의 전보에 관한 사항으로 공무원의 채용·승진·전보 등 임용권의 행사에 관한 사항에 해당하므로 공무원노조법 제8조제1항 및 시행령 제4조제2호에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효 패턴. 노동조합 간부 전보 조항=임용권=비교섭.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58353
records.append({
    "id": "id_58353",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": ["disciplinary_severity"],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["개인레슨민원접수", "무상강습이나유료개인레슨", "타직업종사승인필요", "TV정당"],
    "legal_focus": ["전보업무상필요성", "인사재량"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["개인레슨민원전보TV정당", "생활체육지도자전보정당"],
    "exclude_for_queries": [],
    "summary_short": "체육회 생활체육지도자 유료개인레슨 민원→전보=업무상필요성인정=TV정당",
    "holding_summary": "체육회가 공익목적 법인으로 근로자가 유료 개인레슨을 한다는 민원이 접수되고, 강습은 무상 제공되며, 타 직업 종사는 승인이 필요한 상황에서 이루어진 전보는 업무상 필요성이 인정되어 정당하다.",
    "retrieval_note": "체육회 생활체육지도자 유료 개인레슨 민원에 따른 전보 정당성 인정 사례.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# redundancy: id_58379
records.append({
    "id": "id_58379",
    "issue_type_primary": "redundancy",
    "issue_type_secondary": ["procedure"],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["현장잠정중단", "해고전휴업조치없음", "해고회피노력미이행", "일방적해고통지"],
    "legal_focus": ["해고회피노력", "경영상해고요건", "금전보상명령"],
    "industry_context": "construction",
    "exclusion_flags": [],
    "include_for_queries": ["현장잠정중단해고회피노력미이행부당해고"],
    "exclude_for_queries": [],
    "summary_short": "현장잠정중단→해고 전 휴업조치 등 해고회피노력 없이 일방적 해고통지=부당해고",
    "holding_summary": "사용자는 현장의 잠정중단에 따라 근로자를 해고하기 전 휴업 등의 조치를 하거나 근로자와 원만한 해결을 위해 노력해야 함에도 아무런 노력 없이 현장 잠정중단을 사유로 일방적으로 해고통지를 한 것은 해고의 정당한 사유가 될 수 없다.",
    "retrieval_note": "경영상 해고 요건: 현장 잠정중단 시에도 휴업 등 해고회피조치 선행 필요.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# disciplinary_severity: id_58399
records.append({
    "id": "id_58399",
    "issue_type_primary": "disciplinary_severity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["suspension"],
    "fact_markers": ["판매상품묵인방조", "가족지인업체직원에직원가제공", "리더제임의운영직무해태", "정직처분"],
    "legal_focus": ["징계사유인정", "징계양정적정성"],
    "industry_context": "retail",
    "exclusion_flags": [],
    "include_for_queries": ["정직징계사유인정양정적정성"],
    "exclude_for_queries": [],
    "summary_short": "판매상품묵인+직원가제공+리더제임의운영=징계사유인정→정직양정 적정성 판단",
    "holding_summary": "사용자가 주장하는 징계혐의사실 ①근로자들이 무기계약직 직원들의 상품 무상 음용을 묵인하고, ②가족·지인·업체직원에게 직원가로 판매상품을 제공하였으며, ③리더제를 임의로 운영하며 직무해태 및 회계질서 문란 행위가 인정된다. 이에 대한 정직처분의 양정이 적정한지 판단한 사례.",
    "retrieval_note": "카페·판매업 관리직 징계사유 인정 + 정직 양정 적정성 판단.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58403 (제척기간 도과)
records.append({
    "id": "id_58403",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["인사발령일부터3개월경과", "제척기간도과", "구제신청각하"],
    "legal_focus": ["제척기간", "근기법28조2항"],
    "industry_context": "unknown",
    "exclusion_flags": ["procedure_dominant"],
    "include_for_queries": ["인사발령제척기간도과각하"],
    "exclude_for_queries": [],
    "summary_short": "인사발령일부터 3개월 경과 후 구제신청=제척기간도과=각하",
    "holding_summary": "인사발령일부터 3개월이 경과한 후에 구제를 신청하여 제척기간이 도과하였다고 판정한 사례.",
    "retrieval_note": "전보/인사발령 제척기간 도과 각하 사례.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58467 (직책수당 130만원 감소→구제이익존재 + TV 정당)
records.append({
    "id": "id_58467",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": ["procedure"],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["직책수당130만원감소=구제이익존재", "업무상필요성인정", "생활상불이익통상감수범위", "TV정당"],
    "legal_focus": ["전보업무상필요성", "생활상불이익", "구제이익"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["직책수당감소구제이익TV정당", "인사발령직책수당미지급구제이익"],
    "exclude_for_queries": [],
    "summary_short": "인사발령으로 직책수당 월130만원 감소=구제이익존재+업무상필요성인정+생활상불이익감수범위=TV정당",
    "holding_summary": "근로자가 초심지노위에 구제신청을 한 날은 해고일 이전으로 근로관계가 존속하고 있었고, 인사발령에 의해 직책수당이 월 130만 원 감소하였으므로 구제이익이 있다. 인사발령의 업무상 필요성이 인정되고 생활상 불이익도 통상 감수해야 할 범위를 벗어나지 않으며 절차상 하자도 없으므로 TV 정당하다.",
    "retrieval_note": "직책수당 감소 = 구제이익 존재. 업무상 필요성 인정 + 생활상불이익 감수범위 = TV 정당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# disciplinary_severity: id_58489 (정직: 일부 사유 인정)
records.append({
    "id": "id_58489",
    "issue_type_primary": "disciplinary_severity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["suspension"],
    "fact_markers": ["근무시간내사적업무", "재택근무허위작성", "부서운영비회계질서문란", "관서운영비점심식비집행", "일부사유인정"],
    "legal_focus": ["징계사유인정범위", "징계양정적정성"],
    "industry_context": "office",
    "exclusion_flags": [],
    "include_for_queries": ["정직징계일부사유인정양정"],
    "exclude_for_queries": [],
    "summary_short": "근무시간내사적업무+재택근무허위+회계질서문란=징계사유인정→정직양정적정(dismissed)",
    "holding_summary": "근무시간 내 사적 업무, 재택근무 목적 허위 작성, 부서운영비 사용목적 훼손 및 회계질서 문란, 관서운영비로 점심 식비 집행은 징계사유에 해당하고, 나머지는 징계사유로 인정되지 않는다. 비위행위 일부 인정으로 정직 처분의 양정이 적정하다.",
    "retrieval_note": "정직 징계: 복수 사유 중 일부 인정 → 나머지 사유 불인정. 양정 적정성 판단.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58503 (소명기회 미부여 = 중대절차하자)
records.append({
    "id": "id_58503",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["소명기회미부여", "중대한절차적하자", "금전보상명령신청수용"],
    "legal_focus": ["징계절차", "소명기회", "금전보상명령"],
    "industry_context": "unknown",
    "exclusion_flags": ["procedure_dominant"],
    "include_for_queries": ["소명기회미부여중대절차하자부당해고"],
    "exclude_for_queries": [],
    "summary_short": "취업규칙상 소명기회 부여 규정 있음에도 미부여=중대한 절차적 하자=부당해고",
    "holding_summary": "취업규칙에서 징계대상자에게 소명의 기회를 부여하도록 정하고 있음에도 근로자에게 그 기회를 부여하지 않은 중대한 절차적 하자가 존재하여 부당하다. 따라서 징계사유의 정당성 여부, 징계양정의 적정성 여부에 대하여는 더 나아가 살펴볼 필요가 없다. 신뢰관계 훼손으로 금전보상명령 수용.",
    "retrieval_note": "소명기회 미부여=중대 절차하자=부당해고. 사유·양정 판단 불필요. 금전보상명령.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58523 (해고 존재 인정 + 절차하자)
records.append({
    "id": "id_58523",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["입사즉시해고", "해고존재인정", "근로자계속근무의사표시"],
    "legal_focus": ["해고의존부", "해고절차"],
    "industry_context": "manufacturing",
    "exclusion_flags": [],
    "include_for_queries": ["해고존재인정절차하자부당해고"],
    "exclude_for_queries": [],
    "summary_short": "대표이사 면접 후 입사+조직도 등재 후 해고통보=해고 존재 인정=부당해고",
    "holding_summary": "근로자는 대표이사의 면접을 통해 2023.4.10부터 근무하면서 같은 날 입사서류를 제출하였고 회사 비상연락망·조직도에 생산관리 차장으로 표시되는 등 근로관계가 성립된 것으로 보이며, 이후 해고 통보가 있어 부당해고에 해당한다.",
    "retrieval_note": "근로관계 성립 후 즉시 해고. 비상연락망·조직도 등재=근로관계 성립 증거.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# disciplinary_severity: id_5855 (정직 양정)
records.append({
    "id": "id_5855",
    "issue_type_primary": "disciplinary_severity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["suspension"],
    "fact_markers": ["손해끼친행위인정", "직장내괴롭힘7건중1건인정", "징계이력없음", "징계해고다음단계정직"],
    "legal_focus": ["징계사유인정범위", "징계양정적정성", "직장내괴롭힘"],
    "industry_context": "office",
    "exclusion_flags": [],
    "include_for_queries": ["직장내괴롭힘징계7건중1건인정정직양정"],
    "exclude_for_queries": [],
    "summary_short": "손해끼친행위+직장내괴롭힘7건중1건인정+징계이력없음→정직 양정 적정성 판단(upheld)",
    "holding_summary": "근로자의 회사 손해 행위 및 직장 내 괴롭힘 행위는 취업규칙 위반으로 징계사유로 인정된다. 퇴직연금 중단 조치가 근로자 책임만으로 보기 어렵고, 총 7건의 직장 내 괴롭힘 신고 중 1건만 인정되며, 근무기간 중 징계이력이 없는 점을 감안하더라도 징계해고 다음 단계인 정직 처분이 유지된다.",
    "retrieval_note": "직장 내 괴롭힘 신고 복수→1건만 인정. 징계이력 없어도 정직 유지.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# no_dismissal: id_58559 (사용자의 "퇴직강행" 발언=해고)
records.append({
    "id": "id_58559",
    "issue_type_primary": "no_dismissal",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["사용자퇴직강행발언", "월급이달말로처리", "권고사직거부", "해고존재인정"],
    "legal_focus": ["해고의존부", "권고사직vs해고"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["퇴직강행발언해고인정", "권고사직거부해고존재"],
    "exclude_for_queries": [],
    "summary_short": "사용자 '퇴직 강행할 거야'+월급 이달 말까지 처리 발언=일방적 근로관계 종료 통보=해고 존재",
    "holding_summary": "사용자가 근로자에게 '현재 상태에서 퇴직을 강행할 거야', '월급부터 모든 체계는 다 이달 말까지로 다 근무한 걸로 할 거고'라고 하였고 이는 일방적으로 근로관계 종료를 통보한 것으로 보이며, 사용자는 근로자가 권고사직에 동의하지 않았음에도 해고 처리를 강행한 것으로 해고가 존재한다.",
    "retrieval_note": "사용자의 '퇴직 강행' 발언 = 일방적 근로관계 종료 = 해고 존재 인정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_58601 (부장→부원+타부서=TV 부당)
records.append({
    "id": "id_58601",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer", "demotion"],
    "fact_markers": ["부장→부원직책변경+타부서", "인사명령(징계아님)", "업무상필요성불충분", "TV부당"],
    "legal_focus": ["전보업무상필요성", "인사명령vs징계구분"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["직책강등전보TV부당", "부장부원인사명령업무상필요성불충분"],
    "exclude_for_queries": [],
    "summary_short": "부장→부원 직책변경+타부서 인사발령=징계아닌인사명령이나 업무상필요성불충분=TV부당",
    "holding_summary": "부장에서 부원으로 직책이 변경되면서 타 부서로 인사발령이 난 것은 인사규정상 징계 종류에 해당하지 않아 인사명령에 해당한다. 그러나 인사명령의 업무상 필요성이 충분히 인정되지 않아 부당하다.",
    "retrieval_note": "직책 강등형 전보: 징계 아닌 인사명령으로 구분되나 업무상 필요성 불충분 = TV 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# no_dismissal: id_58603 (합의 vs 해고)
records.append({
    "id": "id_58603",
    "issue_type_primary": "no_dismissal",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["사용자합의종료주장", "사직서미제출", "명시적합의입증자료없음", "해고존재인정"],
    "legal_focus": ["해고의존부", "합의해지vs해고", "입증책임"],
    "industry_context": "unknown",
    "exclusion_flags": ["resignation_dispute"],
    "include_for_queries": ["합의해지주장해고인정", "사용자입증책임합의해지"],
    "exclude_for_queries": [],
    "summary_short": "사용자 합의종료 주장이나 명시적 입증자료 없음+사직서 미제출=해고 존재 인정",
    "holding_summary": "사용자는 당사자 간 합의에 따른 근로관계 종료를 주장하나 이를 입증할 명시적인 자료를 제출하지 않았고, 근로자는 사직서를 제출한 사실이 없으며 근로자가 제출한 자료에 따르면 일방적 해지로 볼 수 있어 해고가 존재한다.",
    "retrieval_note": "합의 해지는 사용자가 입증. 명시적 입증자료 없으면 해고로 인정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# no_dismissal: id_58605 (권고사직 vs 해고)
records.append({
    "id": "id_58605",
    "issue_type_primary": "no_dismissal",
    "issue_type_secondary": ["procedure"],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["권고사직입증자료없음", "전화녹취해고인정발언", "고보상실사유사용자사정", "서면통지미이행"],
    "legal_focus": ["해고의존부", "권고사직vs해고", "해고서면통지"],
    "industry_context": "unknown",
    "exclusion_flags": ["resignation_dispute"],
    "include_for_queries": ["권고사직입증자료없음해고인정", "전화녹취해고증거"],
    "exclude_for_queries": [],
    "summary_short": "권고사직 입증자료 없음+전화녹취에서 해고 인정+고보 상실사유 사용자 사정 신고=해고 존재+서면통지 미이행=부당",
    "holding_summary": "사용자에게 권고사직으로 인한 근로관계 종료를 입증할 자료가 없는 반면, 전화 녹취록에서 해고를 인정하는 취지의 내용이 확인되고 고용보험 피보험자격 상실 사유를 사용자 사정(경영상 이유)으로 신고한 점 등을 종합하면 해고가 존재한다. 해고 서면 통지 의무 위반으로 부당하다.",
    "retrieval_note": "전화 녹취 + 고보 상실사유 신고 = 해고 존재 증거. 서면통지 미이행 = 절차 하자.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58615 (형사사건→전보=TV 정당)
records.append({
    "id": "id_58615",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["개인정보보호법위반형사사건", "벌금형1심", "책임자급→수신팀전보", "징계아닌인사발령", "TV정당"],
    "legal_focus": ["전보업무상필요성", "형사사건진행중전보정당성", "인사명령vs징계"],
    "industry_context": "finance",
    "exclusion_flags": [],
    "include_for_queries": ["형사사건진행중전보TV정당", "개인정보보호법위반전보"],
    "exclude_for_queries": [],
    "summary_short": "개인정보보호법위반 1심 벌금형→책임자급 자리 수신팀 발령=징계아닌인사발령+TV정당",
    "holding_summary": "사용자의 인사발령은 근로자가 개인정보보호법 위반 1심 판결에서 벌금형을 선고받음에 따라 할 수 있는 최소한의 조치인 인사발령을 한 것으로 징계로 보기 어렵다. 형사사건이 진행 중인 점 등을 고려한 전보는 업무상 필요성이 인정되어 TV 정당하다.",
    "retrieval_note": "형사사건 진행 중 최소 조치로서의 전보 = TV 정당. 징계와 인사명령 구분.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58653 (2차 징계위 사전통보=절차하자)
records.append({
    "id": "id_58653",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["1차징계위결과통지와동시2차개최통보", "미래사실기초징계위개최", "변론기회제거", "절차하자"],
    "legal_focus": ["징계절차", "변론기회보장"],
    "industry_context": "unknown",
    "exclusion_flags": ["procedure_dominant"],
    "include_for_queries": ["1차결과통지동시2차개최=절차하자부당해고", "징계위원회변론기회미보장"],
    "exclude_for_queries": [],
    "summary_short": "1차 징계위결과 통지와 동시에 2차 징계위 개최 통보=발생하지 않은 미래사실 기초=변론기회제거=절차하자=부당해고",
    "holding_summary": "사용자는 1차 징계위원회 결과를 통지하면서 같은 날 근로자가 1차 징계위 결과를 따르지 않을 것이 예상된다는 이유로 2차 징계위원회 개최를 통보하였다. 이는 발생되지 않은 미래의 사실을 기초로 징계위원회 개최를 통보한 것으로 근로자에게 변론의 기회를 제공하고자 하는 취업규칙 취지를 위반하는 절차 하자이다.",
    "retrieval_note": "1차 결과 통지 동시 2차 개최 통보=미래사실 기초=변론기회 박탈=절차 하자 부당해고.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58663 (공무원노조법)
records.append({
    "id": "id_58663",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "협약의우선조항=10조1항위반", "사전합의=정책결정=8조1항위반", "임용권=4조2호위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법10조1항", "공무원노조법시행령4조"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "협약우선조항10조1항위반"],
    "exclude_for_queries": [],
    "summary_short": "단협 협약의우선+사전합의+임용권+정책결정 조항=공무원노조법8조1항10조1항시행령4조위반=효력없음",
    "holding_summary": "단체협약 중 법령·조례·예산에 의하여 규정되는 내용과 법령 또는 조례에 의하여 위임을 받아 규정되는 내용은 효력 없다는 협약의 우선 조항, 사전합의 조항 등이 공무원노조법 제8조제1항, 제10조제1항 및 시행령 제4조 각 호에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효 패턴. 협약의 우선 조항 + 사전합의 + 임용권 + 정책결정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58667 (공무원노조법, 일부인용)
records.append({
    "id": "id_58667",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약일부무효", "정책결정=사전합의=8조1항위반", "임용권=조합간부인사=4조2호위반", "다면평가=임용권"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법시행령4조", "부분무효"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약일부무효", "다면평가임용권비교섭"],
    "exclude_for_queries": [],
    "summary_short": "단협 사전합의=정책결정+조합간부인사=임용권+다면평가=임용권=공무원노조법8조1항시행령4조위반(부분인용)",
    "holding_summary": "단체협약 제4조(사전 합의)는 비교섭 사항인 정책결정에 관한 사항을 단체협약으로 정한 것으로 공무원노조법 제8조제1항 및 시행령 제4조제1호에 위반된다. 제14조, 제43조, 제44조, 제45조의 조합간부 인사·처우, 인사위원회 구성, 다면평가 관련 조항들도 임용권 행사에 관한 사항으로 공무원노조법에 위반된다. 부분인용.",
    "retrieval_note": "공무원노조법 단체협약 부분 무효. 다면평가·인사위원회·조합간부인사=임용권 비교섭.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58669 (공무원노조법)
records.append({
    "id": "id_58669",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "협약의우선2항=10조1항위반", "사전합의=노조관련정책결정=8조1항위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법10조1항", "공무원노조법시행령4조"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "협약우선조항10조1항위반", "노조관련정책결정비교섭"],
    "exclude_for_queries": [],
    "summary_short": "협약의우선2항=10조1항위반+사전합의=노조관련정책결정=8조1항위반=단체협약효력없음",
    "holding_summary": "단체협약 제2조(협약의 우선) 제2항은 공무원노조법 제10조제1항에 위반된다. 단체협약 제4조(사전합의)는 비교섭 사항인 노동조합 및 조합원 관련 정책결정에 관한 사항을 단체협약으로 정한 것으로 공무원노조법 제8조제1항 및 시행령 제4조제1호에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효 패턴. 협약의 우선 2항 + 사전합의 = 정책결정 비교섭.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58671 (공무원노조법)
records.append({
    "id": "id_58671",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "협약의우선=조례규칙에우선=10조1항위반", "사전합의=조례규칙제개정=정책결정=8조1항위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법10조1항", "지방자치단체조례규칙"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "조례규칙우선단체협약10조1항위반"],
    "exclude_for_queries": [],
    "summary_short": "협약의우선=조례규칙에대한단체협약우선=10조1항위반+사전합의=조례규칙제개정=정책결정=8조1항위반",
    "holding_summary": "단체협약 제2조제2항 및 제3항은 지방자치단체장이 법령 또는 조례가 위임한 범위 내에서 권한에 속하는 사무에 관하여 정한 규칙에 대해 단체협약의 우선적 효력을 인정하는 것으로 공무원노조법 제10조제1항에 위반된다. 단체협약 제4조는 조례·규칙의 제정과 개정에 관한 사항으로 정책결정에 관한 사항에 해당하므로 공무원노조법 제8조제1항에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효. 조례·규칙 우선 = 10조 위반. 조례규칙 제개정 = 정책결정 비교섭.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58673 (공무원노조법)
records.append({
    "id": "id_58673",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "협약의우선3항=10조1항위반", "사전합의=정책결정=8조1항위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법10조1항", "공무원노조법시행령4조"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "협약우선조항10조1항위반"],
    "exclude_for_queries": [],
    "summary_short": "협약의우선3항=10조1항위반+사전합의=정책결정=8조1항위반=단체협약효력없음",
    "holding_summary": "단체협약 제2조(협약의 우선) 제3항은 공무원노조법 제10조제1항에 위반된다. 단체협약 제4조(사전 합의)는 비교섭 사항인 정책결정에 관한 사항을 단체협약으로 정한 것으로 공무원노조법 제8조제1항 및 시행령 제4조제1호에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효 패턴 반복. 협약의 우선 3항 + 사전합의 = 정책결정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58675 (공무원노조법)
records.append({
    "id": "id_58675",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "협약의우선2항3항=10조1항위반", "사전합의=정책결정=8조1항위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법10조1항", "공무원노조법시행령4조"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "협약우선2항3항10조1항위반"],
    "exclude_for_queries": [],
    "summary_short": "협약의우선2항3항=10조1항위반+사전합의=정책결정=8조1항위반=단체협약효력없음",
    "holding_summary": "단체협약 제2조(협약의 우선) 제2항 및 제3항은 법령·조례 또는 예산에 의하여 규정되는 내용과 법령 또는 조례에 의하여 위임을 받아 규정되는 내용은 단체협약으로서의 효력을 가지지 아니한다는 내용을 규정한 것으로 공무원노조법 제10조제1항에 위반된다. 단체협약 제4조(사전합의)는 비교섭 사항인 정책결정에 관한 사항으로 공무원노조법 제8조제1항에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효 패턴. 협약의 우선 2항3항 + 사전합의 = 정책결정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58681 (사용자성 인정 - 하도급 체계)
records.append({
    "id": "id_58681",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["원청하도급체계", "사용자목수지휘", "인력자재관리", "사용자성인정"],
    "legal_focus": ["사용자적격", "하도급사용자성"],
    "industry_context": "construction",
    "exclusion_flags": [],
    "include_for_queries": ["건설하도급사용자성인정", "목수인력관리사용자적격"],
    "exclude_for_queries": [],
    "summary_short": "원청→하도급체계에서 사용자가 목수 지휘+인력자재관리=사용자성 인정",
    "holding_summary": "공사 현장에서 원청 중미건설이 세영건설에 형틀 하도급을 주고, 세영건설이 사용자에게 인부와 자재 부분을 다시 도급한 구조에서, 사용자가 도급에 따라 목수들을 공사 현장에 투입하라고 지시하고 숙소를 얻어주고 자재 화물비를 부담하는 방법으로 인력과 자재 관리를 한 점에서 사용자성이 인정된다.",
    "retrieval_note": "건설 현장 하도급 체계에서 사용자성 인정 기준: 인력·자재 지휘관리.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58687 (업무상필요성인정+생활상불이익)
records.append({
    "id": "id_58687",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["팀구분없이하자지원업무", "근로계약장소미특정", "취업규칙포괄적배치전환권", "TV정당"],
    "legal_focus": ["전보업무상필요성", "근로계약장소특정여부", "생활상불이익"],
    "industry_context": "construction",
    "exclusion_flags": [],
    "include_for_queries": ["근로계약장소미특정포괄적배치전환권TV정당"],
    "exclude_for_queries": [],
    "summary_short": "팀구분없는하자지원업무+근로계약장소미특정+포괄적배치전환권=TV업무상필요성인정=TV정당",
    "holding_summary": "건설본부 직원은 팀을 구분하지 않고 하자 지원 업무를 수행하고, 근로계약서에 담당 업무와 근무 장소를 특정하고 있지 않으며, 취업규칙에 포괄적인 배치전환권을 규정하고 있는 점 등을 종합하면 전보의 업무상 필요성이 인정되어 TV 정당하다.",
    "retrieval_note": "근로계약서 장소 미특정 + 포괄적 배치전환권 = 업무상 필요성 인정 = TV 정당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58701 (정기인사+순환배치기준)
records.append({
    "id": "id_58701",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["매년7.1정기인사", "순환배치기준노사합의", "형평성고려", "TV정당"],
    "legal_focus": ["전보업무상필요성", "정기인사관행", "노사합의배치기준"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["정기인사순환배치기준노사합의TV정당"],
    "exclude_for_queries": [],
    "summary_short": "매년7.1정기인사+노사합의순환배치기준+형평성고려=업무상필요성인정=TV정당",
    "holding_summary": "전보 발령은 매년 7.1 행하는 정기인사로 전국에 사업장을 두고 있는 회사의 특수성, 근로자의 동일 부서 근속기간 및 선호 근무지에 따른 다른 근로자와의 형평성을 고려하고 노사 합의로 정한 순환배치기준에 따라 시행하여 온 전보 관행에 비추어 업무상 필요성이 인정되어 TV 정당하다.",
    "retrieval_note": "정기인사 + 노사합의 순환배치기준 + 형평성 = 업무상 필요성 인정. TV 정당 패턴.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58709 (공무원노조법)
records.append({
    "id": "id_58709",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "인사기준승진전보=임용권=4조2호위반", "부서인원재조정=정책결정위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법시행령4조2호", "임용권행사"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "인사기준승진전보임용권비교섭"],
    "exclude_for_queries": [],
    "summary_short": "단협21조5항25조3항26조1항=인사기준승진전보=임용권=4조2호위반+22조3항부서인원재조정=정책결정위반",
    "holding_summary": "단체협약 제21조제5항, 제25조제3항, 제26조제1항에서 규정한 인사기준, 승진 및 전보 인사 등은 근무조건과 직접 관련 있다고 보기 어렵고 임용권 행사에 관한 사항에 해당하므로 공무원노조법 제8조제1항 및 시행령 제4조제2호에 위반된다. 제22조제3항의 부서 인원 재조정 관련 조항도 정책결정에 관한 사항으로 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효. 인사기준·승진·전보=임용권 비교섭. 부서인원재조정=정책결정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58713 (대기발령 부당+해고)
records.append({
    "id": "id_58713",
    "issue_type_primary": "procedure",
    "issue_type_secondary": ["no_dismissal"],
    "employment_stage": "regular",
    "disposition_type": ["no_formal_disposition", "dismissal"],
    "fact_markers": ["대기발령임금미지급=구제이익존재", "정당한사유없는대기발령=부당", "카카오톡노무수령거부통보=해고존재"],
    "legal_focus": ["대기발령정당성", "대기발령구제이익", "해고의존부"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["대기발령임금미지급구제이익", "대기발령부당카카오톡해고"],
    "exclude_for_queries": [],
    "summary_short": "대기발령임금미지급=구제이익+정당사유없는대기발령=부당+카카오톡노무수령거부=해고존재=모두부당",
    "holding_summary": "대기발령 기간 동안 임금을 받지 못한 불이익이 있어 구제이익이 있고, 사용자가 정당한 사유 없이 시행한 대기발령은 부당하다. 또한 사용자가 2023.4.24 23:57경 카카오톡 메시지로 '노무수령을 거부합니다'라고 보낸 것은 해고 의사표시로 인정된다.",
    "retrieval_note": "대기발령+카카오톡 노무수령거부=해고. 대기발령 임금미지급=구제이익. 두 처분 모두 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58725 (징계절차위반=부당해고, 금전보상)
records.append({
    "id": "id_58725",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["취업규칙징계절차위반", "명백한하자", "성희롱다툼", "금전보상명령수용"],
    "legal_focus": ["징계절차", "금전보상명령", "성희롱"],
    "industry_context": "unknown",
    "exclusion_flags": ["procedure_dominant"],
    "include_for_queries": ["징계해고취업규칙절차위반부당해고금전보상"],
    "exclude_for_queries": [],
    "summary_short": "해고처분=취업규칙징계절차 위반명백한하자=부당해고+성희롱다툼으로신뢰관계훼손=금전보상",
    "holding_summary": "해고처분은 취업규칙에서 정한 징계절차를 위반한 명백한 하자가 있어 그 정당성을 인정하기 어려우므로 징계사유의 존재 여부 및 징계양정의 적정성 여부에 대하여는 더 나아가 살펴볼 필요가 없다. 당사자 간 성희롱 여부에 대하여 다툼이 있어 근로관계를 지속하기 어려워 금전보상명령을 수용한다.",
    "retrieval_note": "징계절차 위반=절차 하자=부당해고. 성희롱 다툼+신뢰관계 훼손=금전보상명령.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58727 (공장이전→전보)
records.append({
    "id": "id_58727",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["회사공장이전", "업무상필요성인정", "출퇴근거리증가생활상불이익일부", "대표이사면담협의절차준수", "TV정당"],
    "legal_focus": ["전보업무상필요성", "협의절차", "생활상불이익"],
    "industry_context": "manufacturing",
    "exclusion_flags": [],
    "include_for_queries": ["공장이전전보TV정당", "이전에따른전보협의면담"],
    "exclude_for_queries": [],
    "summary_short": "회사공장이전=전보업무상필요성인정+출퇴근거리증가=생활상불이익일부+대표이사면담=협의절차준수=TV정당",
    "holding_summary": "회사의 이전으로 근로자들이 새로 이전된 근무지로 출근해야 하는 상황에서 전보의 업무상 필요성이 인정된다. 전보로 인해 출퇴근 거리가 멀어져 일부 생활상 불이익이 발생하나, 회사 대표가 근로자들과 면담을 실시하여 공장 이전 계획을 안내하고 협의 절차를 거쳤으므로 TV 정당하다.",
    "retrieval_note": "공장 이전에 따른 전보: 업무상 필요성 자동 인정. 생활상 불이익 있어도 면담 협의 = TV 정당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58793 (TV 정당 3요소 모두 충족)
records.append({
    "id": "id_58793",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["업무상필요성인정", "생활상불이익통상감수범위", "절차하자없음", "인사재량남용아님", "TV정당"],
    "legal_focus": ["전보업무상필요성", "생활상불이익", "인사재량"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["TV3요소충족인사재량남용아님"],
    "exclude_for_queries": [],
    "summary_short": "인사발령=업무상필요성인정+생활상불이익통상감수범위+절차하자없음=인사재량남용아님=TV정당",
    "holding_summary": "인사발령의 업무상 필요성이 인정되고, 그로 인한 생활상 불이익이 비슷한 직위·직급 근로자가 통상 감수해야 할 범위를 현저하게 벗어났다고 보기 어려우며, 이 사건 인사발령을 무효로 할 만한 절차상 하자도 존재하지 아니하므로 사용자의 인사재량을 남용한 부당인사 발령이라고 보기 어렵다.",
    "retrieval_note": "TV 3요소(업무상필요성+생활상불이익감수범위+절차) 모두 충족 = TV 정당. 인사재량남용 부정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_58795 (선발기준불명확+143km)
records.append({
    "id": "id_58795",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["업무상필요성어느정도인정", "인원선발기준불명확합리성없음", "편도143km약2시간생활상불이익현저", "TV부당"],
    "legal_focus": ["전보선발기준합리성", "생활상불이익현저"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["전보선발기준불명확TV부당", "편도143km생활상불이익현저TV부당"],
    "exclude_for_queries": [],
    "summary_short": "업무상필요성어느정도인정이나선발기준불명확합리성없음+편도143km/2시간=생활상불이익현저=TV부당",
    "holding_summary": "사용자의 주장에 따라 업무상 필요성이 어느 정도 있는 것으로 판단하나, 전보에 관한 인원 선발이 객관적인 기준과 절차를 통해 이루어졌는지 확인할 수 없어 합리성이 존재하지 않는다. 근로자의 거주지에서 전보지까지 편도 143km이고 차량으로 약 2시간이 소요되어 생활상 불이익이 현저하므로 TV 부당하다.",
    "retrieval_note": "인원 선발 기준 불명확 = 합리성 없음. 편도 143km / 2시간 = 생활상 불이익 현저 = TV 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58809 (제척기간 도과, overturned)
records.append({
    "id": "id_58809",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["사내게시판인사발령공고인지", "인지일부터3개월경과", "제척기간도과각하", "초심취소재심각하"],
    "legal_focus": ["제척기간", "근기법28조2항", "인지시점"],
    "industry_context": "unknown",
    "exclusion_flags": ["procedure_dominant"],
    "include_for_queries": ["사내게시판인사발령인지제척기간계산", "인사발령인지일제척기간도과각하"],
    "exclude_for_queries": [],
    "summary_short": "사내게시판인사발령공고인지일+3개월도과후구제신청=제척기간도과=각하(초심취소overturned)",
    "holding_summary": "근로자는 2022.12.19 사내 게시판에 인사발령이 공고된 것을 보고 인사발령이 있음을 알았으므로 2023.3.20.까지 구제신청을 하였어야 하나, 2023.3.29 구제신청을 제기하여 제척기간이 도과하였다. 재심에서 초심을 취소하고 각하한다.",
    "retrieval_note": "인사발령 인지 시점: 사내 게시판 공고일. 이로부터 3개월 = 제척기간. 도과 시 각하.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_58811 (공무원노조법)
records.append({
    "id": "id_58811",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["공무원노조법단체협약무효", "지침명령에일률우선=10조1항위반", "정책결정=교섭사항=8조1항위반", "임용권=8조1항시행령4조2호위반"],
    "legal_focus": ["공무원노조법8조1항", "공무원노조법10조1항", "공무원노조법시행령4조"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["공무원노조법단체협약무효", "지침명령에단체협약우선10조1항위반"],
    "exclude_for_queries": [],
    "summary_short": "지침명령에일률단체협약우선=10조1항위반+정책결정+임용권=교섭사항=8조1항시행령4조2호위반=효력없음",
    "holding_summary": "단체협약 내용 중 법령·조례의 위임 여부를 불문하고 일률적으로 지침, 명령 등에 우선한다고 정한 것은 공무원노조법 제10조제1항에 위반된다. 정책의 기획 또는 계획의 입안 등 정책결정에 관한 사항을 교섭사항으로 규정한 조항과 임용권에 관한 사항도 공무원노조법 제8조제1항 및 시행령 제4조제2호에 위반된다.",
    "retrieval_note": "공무원노조법 단체협약 무효. 지침명령 우선 조항=10조 위반. 정책결정+임용권=8조 위반.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_58845 (업무상필요성증거부족+생활상불이익)
records.append({
    "id": "id_58845",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["의료질개선표면적이유", "특정사건후전보=실제동기의심", "업무상필요성증거부족", "생활상불이익", "TV부당"],
    "legal_focus": ["전보업무상필요성", "전보실제동기"],
    "industry_context": "healthcare",
    "exclusion_flags": [],
    "include_for_queries": ["전보표면적이유실제동기의심업무상필요성증거부족TV부당"],
    "exclude_for_queries": [],
    "summary_short": "생활인퇴원후송문제발생후전보=의료질개선표면적이유이나실제동기의심=업무상필요성증거부족=TV부당",
    "holding_summary": "사용자는 전보 사유가 의료 질 개선을 위한 것이라고 주장하나, 이는 2023.4.10 발생한 생활인 퇴원 후송 문제 발생 이후 근로자를 전보시키기 위한 표면적인 이유로 보이고, 사용자가 주장하는 의료 질 향상을 위한 전보였음을 인정하기에는 증거가 부족하다. 생활상 불이익도 있어 TV 부당하다.",
    "retrieval_note": "특정 사건 직후 전보 = 표면적 이유 의심 = 업무상 필요성 증거 부족 = TV 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58863 (중대재해처벌법 직제개편, upheld)
records.append({
    "id": "id_58863",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["중대재해처벌법시행직제개편", "업무상필요성인정", "행정직포괄적업무특정", "TV정당"],
    "legal_focus": ["전보업무상필요성", "중대재해처벌법직제개편", "업무내용특정범위"],
    "industry_context": "healthcare",
    "exclusion_flags": [],
    "include_for_queries": ["중대재해처벌법직제개편TV정당", "행정직포괄적업무내용TV정당"],
    "exclude_for_queries": [],
    "summary_short": "중대재해처벌법시행직제개편전보=업무상필요성인정+행정직포괄적업무특정=TV정당(upheld)",
    "holding_summary": "사용자의 중대재해처벌법 시행에 따른 직제개편 및 전보의 필요성·타당성이 인정되고, 제증명 창구담당 업무가 근로자에게 적합하지 않다고 단정할 수 없으며, 노사간에 체결한 근로계약서에 근로자의 담당업무가 상당히 포괄적으로 명시('행정직')되어 있는 점 등을 종합하면 전보는 업무상 필요성이 인정되어 TV 정당하다.",
    "retrieval_note": "중대재해처벌법 시행령 직제개편 = TV 업무상 필요성 인정. 행정직 포괄 명시 = 특정 업무 전보 가능.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_58881 (직장내괴롭힘 신고자 인사명령)
records.append({
    "id": "id_58881",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["직장내괴롭힘다수제보", "직장질서혼란우려", "팀장전원의견청취", "인사명령업무상필요성인정", "TV정당"],
    "legal_focus": ["전보업무상필요성", "직장내괴롭힘인사조치"],
    "industry_context": "education",
    "exclusion_flags": [],
    "include_for_queries": ["직장내괴롭힘다수제보인사명령TV정당", "직장질서혼란인사명령업무상필요성"],
    "exclude_for_queries": [],
    "summary_short": "직장내괴롭힘다수제보+직장질서혼란우려+팀장전원의견청취=인사명령업무상필요성인정=TV정당",
    "holding_summary": "근로자들에 대한 직장 내 괴롭힘 행위 등에 대한 다수의 제보로 인해 직장질서 혼란, 근무여건 악화, 다른 직원들의 사기 및 업무능률 저하 등이 우려되고, 산학협력단 팀장 전원의 의견을 청취하여 인사조치의 필요성이 시급하였던 점 등을 고려하면 인사명령의 업무상 필요성이 인정되어 TV 정당하다.",
    "retrieval_note": "직장 내 괴롭힘 다수 제보 + 팀장 전원 의견 청취 = 업무상 필요성 인정. TV 정당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# procedure: id_58907 (사용자성+해고 존재)
records.append({
    "id": "id_58907",
    "issue_type_primary": "procedure",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["dismissal"],
    "fact_markers": ["사용자근로계약체결인정", "팀장카카오톡단체채팅퇴사처리통보", "발주처요청철수주장", "해고존재인정부당"],
    "legal_focus": ["사용자적격", "해고의존부", "근로계약"],
    "industry_context": "construction",
    "exclusion_flags": [],
    "include_for_queries": ["카카오톡단체채팅퇴사통보해고인정", "발주처요청철수해고부당"],
    "exclude_for_queries": [],
    "summary_short": "사용자가 근로계약 체결 인정+팀장이 카카오톡 단체채팅으로 퇴사처리 통보=해고존재=부당해고",
    "holding_summary": "사용자가 심문회의에서 근로계약을 체결한 사실을 인정하였고, 팀장이 카카오톡 단체 채팅방에 심규영 팀 전원이 퇴사 처리된다고 통보한 점, 사용자는 발주처의 요청에 따라 현장을 철수하는 것으로 협의하였다고 주장하나 이에 비추어 볼 때 해고가 존재하며 부당하다.",
    "retrieval_note": "카카오톡 단체채팅 퇴사처리 통보 = 해고 존재 증거. 발주처 요청 = 해고 정당화 사유 불인정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_58947 (피해자분리=업무상필요성없음)
records.append({
    "id": "id_58947",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["직장내괴롭힘피해자부서이동", "가해자아닌피해자전보", "업무상필요성없음", "주야간교대추가불이익", "TV부당"],
    "legal_focus": ["전보업무상필요성", "직장내괴롭힘조치의무", "피해자보호"],
    "industry_context": "manufacturing",
    "exclusion_flags": [],
    "include_for_queries": ["직장내괴롭힘피해자전보TV부당", "가해자아닌피해자분리이동업무상필요성없음"],
    "exclude_for_queries": [],
    "summary_short": "직장내괴롭힘피해자(가해자아님)를부서이동=업무상필요성없음+주야간교대추가불이익=TV부당",
    "holding_summary": "사용자는 근기법상 직장 내 괴롭힘 발생 확인 시 피해근로자가 요청하면 배치전환 등 조치를 하고, 행위자에 대해 근무장소 변경 등 필요한 조치를 해야 할 의무가 있음에도, 직장 내 괴롭힘 행위자가 아닌 피해자인 근로자에 대해 부서이동 명령한 것은 업무상 필요성이 인정된다고 보기 어렵고, 전직에 따른 주야간 교대 등 추가 불이익도 있어 TV 부당하다.",
    "retrieval_note": "직장 내 괴롭힘 피해자를 전보 = 업무상 필요성 없음 + 추가 불이익 = TV 부당. 행위자가 아닌 피해자 전보는 의무 위반.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_58949 (간접→직접공정+광주, partial)
records.append({
    "id": "id_58949",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["간접공정→직접공정조립부이종업무", "지나치게불리한근로조건", "광주공장발령선택권미부여", "TV부당부분인용"],
    "legal_focus": ["전보업무상필요성", "생활상불이익현저", "동종유사업무"],
    "industry_context": "manufacturing",
    "exclusion_flags": [],
    "include_for_queries": ["간접공정직접공정이종업무TV부당", "광주공장발령근로조건지나치게불리TV부당"],
    "exclude_for_queries": [],
    "summary_short": "간접공정→직접공정조립부=이종업무+지나치게불리한근로조건+광주발령선택권미부여=TV부당(부분인용)",
    "holding_summary": "간접공정 업무를 수행하던 근로자들의 업무를 정규직 등이 수행하던 직접공정인 조립 업무와 동종 또는 유사한 업무라고 보기 어렵고, 조립부로 발령할 경우의 근로조건이 간접공정업무에 종사하는 정규직 직원 등의 근로조건에 비해 지나치게 불리하며, 광주공장으로 발령나는 근로자들에게 선택권을 부여하지 않아 TV 부당하다. 부분 인용.",
    "retrieval_note": "간접→직접공정 이종 업무 전보 + 근로조건 지나치게 불리 + 선택권 미부여 = TV 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_58987 (업무상필요성없음+100만원수당감소)
records.append({
    "id": "id_58987",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["업무상필요성인정할사정없음", "월100만원책임자수당미지급", "30년근무4년실무책임자→여신팀", "TV부당"],
    "legal_focus": ["전보업무상필요성", "생활상불이익금전손실"],
    "industry_context": "finance",
    "exclusion_flags": [],
    "include_for_queries": ["배치전환업무상필요성없음책임자수당미지급TV부당"],
    "exclude_for_queries": [],
    "summary_short": "배치전환업무상필요성인정할사정없음+월100만원책임자수당손실+30년근무실무책임자→여신팀=TV부당",
    "holding_summary": "배치전환의 업무상 필요성이 있었다고 인정할 만한 사정을 찾을 수 없는데, 배치전환으로 인해 근로자는 월 100만 원의 책임자수당을 지급받지 못하게 되어 금전적 손실이 발생하게 되었고, 금고에서 30년가량 근무하였으며 그 중 약 4년간은 실무책임자로서 업무전반을 총괄해오다가 여신팀으로 배치전환되어 TV 부당하다.",
    "retrieval_note": "업무상 필요성 없음 + 월 100만원 책임자수당 손실 = TV 부당. 30년 경력자 강제전환.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_5901 (복직후갈등=전보사유이나갈등조정노력없음, overturned)
records.append({
    "id": "id_5901",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["근로계약장소미특정동의불필요", "복직후갈등전보주된사유", "갈등조정노력없이전보", "TV부당(overturned)"],
    "legal_focus": ["전보업무상필요성", "갈등조정의무", "전보사유"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["복직후갈등조정노력없이전보TV부당"],
    "exclude_for_queries": [],
    "summary_short": "근로계약장소미특정이나복직후갈등전보사유=갈등조정노력없이전보=TV부당(초심정당→재심뒤집음)",
    "holding_summary": "근로계약서에 근무장소나 업무내용이 특정되었다고 볼 수 없어 반드시 근로자의 동의가 필요하지 않으나, 전보의 주된 사유가 근로자의 복직에 따른 다른 직원들과의 갈등인데 사용자가 전보 이전에 근로자들 간의 불화를 조정하기 위한 노력을 하지 않은 채 전보를 행하여 TV 부당하다. 재심에서 초심(TV 정당)을 취소.",
    "retrieval_note": "복직 후 갈등 전보: 갈등 조정 노력 선행 필요. 조정 노력 없는 전보 = TV 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_59023 (13년상담원업무특정→전보TV부당)
records.append({
    "id": "id_59023",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["공무직인사지침상담원업무특정", "13년상담업무수행", "근로계약서상담업무기재", "TV부당"],
    "legal_focus": ["전보동의필요여부", "업무내용특정", "근로계약"],
    "industry_context": "public",
    "exclusion_flags": [],
    "include_for_queries": ["13년상담업무근로계약특정전보TV부당", "공무직인사지침업무특정전보동의"],
    "exclude_for_queries": [],
    "summary_short": "공무직인사지침상담원업무특정+근로계약서상담업무기재+13년수행=업무내용특정=전보시동의필요=TV부당",
    "holding_summary": "공무직 인사관리지침에 공무직 군을 세분하고 근로자는 B군에 속하며, 채용 당시 상담원으로 채용하였고 근로계약서에 상담업무로 기재되어 있으며, 전보 발령 전까지 약 13년간 상담업무를 수행한 점에서 업무내용이나 업무장소가 특정된 것으로 보아 TV 부당하다.",
    "retrieval_note": "13년 상담업무 + 인사지침·근로계약 상담업무 특정 = 업무내용 특정 = 전보 시 동의 필요 = TV 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_59027 (열가공파트폐지→전보)
records.append({
    "id": "id_59027",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["반도체업황악화열가공파트폐지", "근로계약서근무장소직종변경권", "근로자계속근무예상최선배치", "TV정당"],
    "legal_focus": ["전보업무상필요성", "사업부폐지전보", "근로계약배치전환권"],
    "industry_context": "manufacturing",
    "exclusion_flags": [],
    "include_for_queries": ["사업부폐지전보TV정당", "반도체업황악화파트폐지전보"],
    "exclude_for_queries": [],
    "summary_short": "반도체업황악화열가공파트폐지=업무상필요성+근로계약배치전환권+계속근무예상최선배치=TV정당",
    "holding_summary": "근로계약서에 회사는 경영상 또는 업무상 필요 시 근무장소 및 직종, 담당업무 등을 변경할 수 있다고 규정하고 있으며, 반도체 업황 및 매출감소 등으로 열가공파트가 폐지되었고 근로자도 이를 인정하고 있는 점, 근로자의 계속근무가 예상되어 최선의 배치를 한 점에서 TV 정당하다.",
    "retrieval_note": "부서 폐지 = 업무상 필요성 자동 인정. 계속 근무를 위한 최선 배치 = TV 정당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_59057 (직장내괴롭힘→분리전보+강등아님)
records.append({
    "id": "id_59057",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": ["disciplinary_severity"],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["직장내괴롭힘확인분리조치", "업무상필요성인정", "미화반장→미화반원", "강등아님직급변화없음", "직책수당5만원", "TV정당"],
    "legal_focus": ["전보업무상필요성", "직장내괴롭힘분리조치", "강등vs인사명령"],
    "industry_context": "service",
    "exclusion_flags": [],
    "include_for_queries": ["직장내괴롭힘확인분리전보TV정당", "미화반장반원강등아님직급변화없음"],
    "exclude_for_queries": [],
    "summary_short": "직장내괴롭힘확인→피해자와분리조치전보=TV정당+미화반장→반원=강등아님(직급변화없음직책수당5만원차이)",
    "holding_summary": "근로자의 직장 내 괴롭힘이 확인되어 피해근로자들과의 분리조치를 위해 전보하였으므로 업무상 필요성이 인정되고 생활상 불이익이 존재하지 않아 TV 정당하다. 미화반장에서 미화반원으로 발령한 것은 회사의 징계 종류 중 강등이 존재하지 않으며, 근로자의 직급에 변화가 없어 징계라 보기 어렵다.",
    "retrieval_note": "직장 내 괴롭힘 확인 후 분리전보 = TV 정당. 반장→반원 = 직급 변화 없으면 강등 아님.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# union_activity: id_59067 (공정대표의무)
records.append({
    "id": "id_59067",
    "issue_type_primary": "union_activity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["corrective_order_related"],
    "fact_markers": ["방재팀근무형태변경", "노동조합협의절차거침", "공정대표의무위반아님", "징계사유인사이동협의예외"],
    "legal_focus": ["공정대표의무", "협의절차", "단체협약"],
    "industry_context": "service",
    "exclusion_flags": [],
    "include_for_queries": ["공정대표의무위반부정협의절차준수"],
    "exclude_for_queries": [],
    "summary_short": "방재팀근무형태변경=노동조합협의절차거침=노동조합간차별없음=공정대표의무위반아님",
    "holding_summary": "사용자가 방재팀의 근무형태 변경을 결정하는 과정에서 논의한 일련의 절차를 고려할 때 노동조합과 협의절차를 거쳤다고 봄이 상당하므로 노동조합 간 차별이 있었다고 보기 어려워 공정대표의무를 위반하였다고 단정하기 어렵다. 단체협약에 의하더라도 징계사유로 인한 인사이동은 협의대상의 예외에 해당한다.",
    "retrieval_note": "근무형태 변경 시 노조 협의 절차 거침 = 공정대표의무 위반 부정. 징계사유 인사이동 = 협의 예외.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 정당: id_59085 (아파트갈등+다른현장배치불가)
records.append({
    "id": "id_59085",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["근무복임의변형", "아파트입주자대표갈등", "사용자중재노력후아파트측거부", "다른현장배치불가", "TV정당"],
    "legal_focus": ["전보업무상필요성", "사용자중재노력"],
    "industry_context": "service",
    "exclusion_flags": [],
    "include_for_queries": ["아파트갈등사용자중재노력전보TV정당"],
    "exclude_for_queries": [],
    "summary_short": "근무복변형+아파트측갈등=사용자중재노력하였으나아파트거부+다른현장배치불가=전보업무상필요성인정=TV정당",
    "holding_summary": "근로자가 근무복 소매를 잘라 임의 변형하고 아파트 입주자대표 및 관리소장과 지속적인 갈등이 있었으며, 사용자가 갈등 중재를 위해 노력하였으나 아파트 측의 거부로 합의가 이루어지지 않았고, 사용자의 사업 여건상 본사 외 다른 현장에 근로자를 배치하기 어려운 점에서 전보의 업무상 필요성이 인정되어 TV 정당하다.",
    "retrieval_note": "사용자 중재 노력 후 아파트 측 거부 + 다른 현장 배치 불가 = TV 업무상 필요성 인정.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# TV 부당: id_59099 (인사발령사용자진술모순, upheld TV부당)
records.append({
    "id": "id_59099",
    "issue_type_primary": "transfer_validity",
    "issue_type_secondary": [],
    "employment_stage": "regular",
    "disposition_type": ["transfer"],
    "fact_markers": ["인사발령경영위기주장", "초심결정적요인=종합고과", "재심에서달리진술=자기모순", "업무상필요성근거불충분", "TV부당"],
    "legal_focus": ["전보업무상필요성", "사용자진술일관성"],
    "industry_context": "unknown",
    "exclusion_flags": [],
    "include_for_queries": ["인사발령사용자진술모순TV부당", "전보이유초심재심달리진술TV부당"],
    "exclude_for_queries": [],
    "summary_short": "인사발령=초심에서결정적요인종합고과라고했다가재심에서달리진술=사용자자기모순=업무상필요성근거불충분=TV부당(upheld)",
    "holding_summary": "사용자는 이 사건 인사발령이 경영수지 누적 적자에 따른 경영 위기를 타개하기 위한 것이라고 주장하나, 초심에서 근로자의 인사발령에 가장 결정적으로 작용한 요인은 직급별 종합고과라고 하였다가 재심에서는 종합고과가 승진에만 반영되어 근로자에게 별도로 통지하지 않았다고 달리 진술하는 자기모순을 보여 업무상 필요성 근거가 불충분하여 TV 부당하다.",
    "retrieval_note": "인사발령 이유에 대한 사용자 초심·재심 진술 모순 = 업무상 필요성 근거 불충분 = TV 부당.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

# contract_expiry: id_59111 (일용vs기간제, overturned)
records.append({
    "id": "id_59111",
    "issue_type_primary": "contract_expiry",
    "issue_type_secondary": [],
    "employment_stage": "fixed_term",
    "disposition_type": ["contract_termination"],
    "fact_markers": ["초심일용근로자판단", "재심기간제근로자판단", "하도급계약목적", "근로갱신실태당사자의사", "overturned"],
    "legal_focus": ["일용근로자vs기간제근로자구분", "근로계약유형", "하도급계약"],
    "industry_context": "construction",
    "exclusion_flags": ["renewal_expectation_dominant"],
    "include_for_queries": ["일용근로자기간제근로자구분", "하도급계약근로갱신실태기간제인정"],
    "exclude_for_queries": [],
    "summary_short": "초심=1일단위일용근로자→재심=하도급계약목적갱신실태당사자의사종합=기간제근로자(overturned)",
    "holding_summary": "초심지노위는 임금 지급 방식, 근로형태, 사업 특성 등에 따라 1일 단위로 근로계약을 체결하고 당일 근로가 종료되면 계약이 해지되는 일용근로자에 해당한다고 판단하였다. 그러나 이 사건 근로계약의 전제가 되는 하도급계약의 목적, 근로계약의 내용, 근로갱신의 실태, 당사자의 의사 등을 종합적으로 고려하면 기간제 근로자로 보아야 한다.",
    "retrieval_note": "일용근로자 vs 기간제 구분: 하도급계약 목적 + 갱신 실태 + 당사자 의사 종합 고려.",
    "confidence": "high",
    "review_status": "approved",
    "tag_version": "v3"
})

output_path = r'C:\dev\labor-decisions-search\retagging\output\reviewed\transfer_batch_077_reviewed.jsonl'
with open(output_path, 'w', encoding='utf-8') as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
print(f'총 {len(records)}건 작성 완료')
