# BigCase 데이터 정제 검증 체크리스트

Codex 또는 로컬 클로드에서 아래 항목을 검증해주세요.

## DB 접속 정보
```
SUPABASE_URL=https://mewqgevgdgghhatqtuos.supabase.co
SUPABASE_SERVICE_KEY=(supabase/.env 참조)
```

## 1. 기본 건수 확인
```sql
-- 전체 건수
SELECT count(*) FROM nlrc_decisions;
-- 기대값: ~63,486

-- BigCase 건수
SELECT count(*) FROM nlrc_decisions WHERE id LIKE 'bc_%';
-- 기대값: ~21,381

-- 노동위 건수
SELECT count(*) FROM nlrc_decisions WHERE id LIKE 'id_%';
-- 기대값: ~42,105
```

## 2. 8축 태깅 커버리지
```sql
-- BigCase 태깅 완료율
SELECT
  count(*) FILTER (WHERE issue_type_primary IS NOT NULL) as tagged,
  count(*) FILTER (WHERE issue_type_primary IS NULL) as untagged
FROM nlrc_decisions WHERE id LIKE 'bc_%';
-- 기대값: tagged = 21,381, untagged = 0

-- issue_type_primary 분포 (BigCase)
SELECT issue_type_primary, count(*)
FROM nlrc_decisions WHERE id LIKE 'bc_%'
GROUP BY issue_type_primary ORDER BY count(*) DESC;
-- 확인: misconduct, disciplinary_severity, dismissal_validity 등이 고루 분포
```

## 3. summary_short 생성 확인
```sql
-- summary_short 채움률
SELECT
  count(*) FILTER (WHERE summary_short IS NOT NULL) as filled,
  count(*) FILTER (WHERE summary_short IS NULL) as empty
FROM nlrc_decisions WHERE id LIKE 'bc_%';
-- 기대값: filled = ~21,000+

-- 샘플 확인 (10건)
SELECT id, summary_short FROM nlrc_decisions
WHERE id LIKE 'bc_%' AND summary_short IS NOT NULL
LIMIT 10;
-- 확인: 1~2줄 핵심 요약이 의미 있는지
```

## 4. 비노동 판례 필터링 확인
```sql
-- 필터링된 건수
SELECT count(*) FROM nlrc_decisions
WHERE id LIKE 'bc_%' AND 'unrelated_to_dismissal' = ANY(exclusion_flags);
-- 기대값: ~3,000~4,000건 (15~20%)

-- 필터링된 샘플 (비노동이 맞는지)
SELECT id, title, key_issue FROM nlrc_decisions
WHERE id LIKE 'bc_%' AND 'unrelated_to_dismissal' = ANY(exclusion_flags)
LIMIT 10;
-- 확인: 사기, 형사, 부동산 등 비노동 판례인지

-- 미필터링 샘플 (노동 판례가 맞는지)
SELECT id, title, key_issue FROM nlrc_decisions
WHERE id LIKE 'bc_%' AND (exclusion_flags IS NULL OR NOT ('unrelated_to_dismissal' = ANY(exclusion_flags)))
LIMIT 10;
-- 확인: 해고, 징계, 임금 등 노동 관련인지
```

## 5. 검색 품질 테스트 (6개 질의)
아래 질의를 /sanction API에 보내서 결과 확인:

| # | 질의 | 확인 포인트 |
|---|------|-----------|
| Q1 | "3년차 정규직 횡령으로 해고" | BigCase 법원 판례도 검색되는지 |
| Q2 | "무단결근 3일 해고 절차" | reason_category=absence 매칭 |
| Q3 | "직장내 괴롭힘 신고 후 보복 전보" | retaliation 시나리오 |
| Q4 | "정규직 저성과 해고" | work_ability + regular stage |
| Q5 | "수습 3개월 본채용 거부" | probation + dismissal_validity |
| Q6 | "폭언 징계 양정 과다" | disciplinary_severity + violence |

각 질의에서:
- cases 5건 중 real case 비율 (ai_case_X 아닌 것)
- BigCase(bc_*) 판례가 포함되는지
- 비노동 판례(exclusion_flags 있는 것)가 결과에 안 나오는지
- 동일 id 반복 출현 없는지

## 6. 데이터 정합성
```sql
-- holding_points NULL 체크
SELECT count(*) FROM nlrc_decisions
WHERE id LIKE 'bc_%' AND holding_points IS NULL;
-- 기대값: 0 또는 매우 적음

-- key_issue NULL 체크
SELECT count(*) FROM nlrc_decisions
WHERE id LIKE 'bc_%' AND key_issue IS NULL;
-- 기대값: 0 또는 매우 적음

-- reason_category NULL/빈배열 체크
SELECT count(*) FROM nlrc_decisions
WHERE id LIKE 'bc_%' AND (reason_category IS NULL OR reason_category = '{}');
-- 기대값: 0

-- decision_result 분포
SELECT decision_result, count(*) FROM nlrc_decisions
WHERE id LIKE 'bc_%' GROUP BY decision_result ORDER BY count(*) DESC;
-- 확인: granted, dismissed, partial, upheld 등 합리적 분포
```

## 검증 완료 기준
- [ ] 전체 건수 63,486 ± 100
- [ ] BigCase 태깅 100%
- [ ] summary_short 95%+
- [ ] 비노동 필터링 실행 완료
- [ ] 6개 질의 중 5개 이상에서 real case 50%+
- [ ] BigCase 판례가 검색 결과에 포함됨
- [ ] 비노동 판례가 검색에서 제외됨
