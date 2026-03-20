# incompetence_batch_011_reviewed.jsonl 1차 self-review 메모

## 배치 개요
- 총 22건, incompetence 마지막 배치 (batch_011, 이후 입력 파일 없음)
- 핵심 판별 기준: work_ability vs dismissal_validity 구별, 갱신기대권 혼입 감지
- 입력 배치 총 11개 (batch_001~011), 출력 누락: batch_004, batch_005

## 유형별 분류

### 시용/수습 본채용 거부 — 정당 (8건)
- id_60739: 관리자·파트장 평가 객관적, 절차 적법
- id_60845: 재무팀장 회계오류(8억)+지각+외부갈등 (제조업)
- id_61113: CSI 50점 이하 27회, 경위서 3회, 정량평가 활용 (서비스업)
- id_6757: 직무평가 합리적+절차하자 치유+자진사직 병합 (금융업)
- id_741: 보육교사 11개소 중 7개소 항의, 소명기회 부여 (재심 초심유지, 교육업)
- id_9831: 단체급식 위생관리 소홀, 복수 평가자 정량평가 (서비스업)
- id_9855: 업무지시 거부+민원+인수인계 미준수, 문자메시지 통지 적법 (서비스업/펜션)
- 공통: issue_type_primary=dismissal_validity, disposition_type=rejection_of_regular_employment

### 시용/수습 본채용 거부 — 부당 (3건)
- id_8539: 평가 객관성 미확보(평가규정 없음, 사전고지 없음). 전자우편 통지는 적법
- id_8211: 구두통보 서면통지 위반 (재심 초심유지). procedure_dominant
- id_9007: 이메일 해고통지 부적법+금전보상명령. procedure_dominant

### 수습기간 중 해고/사직 분쟁 (3건)
- id_703: 사직 권고 vs 해고 판단 — 근로자 동의 부정, 서면통지 위반. resignation_dispute
- id_6699: 카카오톡 해고통보, 비위행위 불충분+서면통지 위반 (재심 초심취소). procedure_dominant
- id_9465: 시용근로자 부정(해약권 규정 없음)+소명기회 미부여. procedure_dominant

### 갱신기대권 혼입 사건 (4건) — exclusion 처리
- id_7009: 공공기관 연구직, 3년 최하위+괴롭힘 논란 → 거절 합리적. renewal_expectation_dominant
- id_7089: 운수업 선장, 입증 부족 → 거절 부당. renewal_expectation_dominant
- id_8505: 비등기임원, 영업실적 57.1%+대규모 손실 → 거절 합리적. renewal_expectation_dominant
- id_9735: 공공기관, 업무능력+책무성+괴롭힘 3개 사유 모두 불인정 → 거절 부당 (재심 초심취소). renewal_expectation_dominant
- 변경 이유: batch_010과 동일 — 업무능력 부족이 갱신거절의 합리적 사유로만 기능. work_ability 검색 시 상위 노출 부적절.

### 기간제 해고 (1건)
- id_61421: 3개월 기간제 계약 중 해고. 해고사유 입증 실패+서면통지 추상적. 임금상당액 지급명령

### 정규직 업무능력 부족 해고 (2건)
- id_6443: 사용자 스스로 "근거 없이 해고" 인정+서면통지 위반. 극단적 사례
- id_7195: 1차 구제이익 소멸(각하)+2차 업무능력·근태 입증 부족(인용). decision_result=rejected

### 징계 사건 (1건) — not_really_performance_case
- id_8265: 정직 2개월. 무단결근+인사명령거부+괴롭힘+업무능력 부족 복합. 업무능력은 4개 사유 중 하나일 뿐. disciplinary_severity가 primary

### 전보+계약무효 병합 (1건)
- id_9091: 전보 정당+수정계약 무효(민법 제103·104조). 시용기간 재설정 불공정 법률행위. decision_result=partial

## work_ability vs dismissal_validity 판별 기준 (batch_010 계승)
- **dismissal_validity를 primary로 선택한 이유**: 업무능력 부족은 해고/본채용거부의 *사유*이지 *쟁점* 자체가 아님. 쟁점은 "그 사유로 한 처분이 정당한가"
- **work_ability는 secondary**: 업무능력 부족이 해고 사유로 주장된 경우에만
- **갱신기대권 사건은 renewal_expectation이 primary**
- **징계 사건은 disciplinary_severity가 primary** (id_8265)

## 해고통지 방식별 적법성 비교 (배치 내 cross-reference)
| case_id | 통지 방식 | 적법 여부 | 비고 |
|---------|----------|----------|------|
| id_9855 | 문자메시지 이미지파일 | 적법 | 사유·시기 인지 가능 |
| id_8539 | 전자우편 | 적법 | 사유·시기 인지 가능 |
| id_9007 | 이메일 | 부적법 | 근기법 제27조 서면통지 불충족 |
| id_6699 | 카카오톡 | 부적법 | 해고사유 미명시 |
| id_8211 | 구두통보 | 부적법 | 서면통지 미이행 |

→ 전자적 수단의 적법성은 "사유·시기 인지 가능" 여부에 따라 갈림. 같은 이메일이라도 결론 다름(id_8539 적법 vs id_9007 부적법).

## 주의 사항
- id_9465: 시용근로자 해당 여부 판단 기준 — 해약권 유보 규정 없으면 시용 아닌 정규직. employment_stage=regular
- id_9091: 민법 제103·104조 적용 사례. 근로계약 수정 자체의 유효성이 쟁점. 특이 사례
- id_7195: decision_result=rejected — 일부각하+일부인용의 복합 결정
- id_7009 vs id_9735: 유사 사유(공공기관 갱신기대권+업무능력+괴롭힘)이나 결론 반대. 입증 정도의 차이

## 잔여 건수 확인
- 입력 배치: batch_001~011 (11개 파일)
- 출력 완료: batch_001~003, 006~011 (9개 파일)
- **미처리: batch_004, batch_005** (출력 디렉토리에 없음)
- batch_011이 마지막 입력이므로, incompetence 태깅은 batch_004·005 처리 후 완료
