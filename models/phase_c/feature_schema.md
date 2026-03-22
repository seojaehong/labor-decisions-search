# Phase C Feature Schema

## 입력 피처 (505차원)

### 구조화 피처 (5차원)

| # | 이름 | 타입 | 설명 | 인코딩 |
|---|------|------|------|--------|
| 0 | issue_type_primary | categorical | 핵심 쟁점 유형 | LabelEncoder |
| 1 | employment_stage | categorical | 근로관계 단계 | LabelEncoder |
| 2 | disposition_count | integer | 처분 유형 개수 | raw count |
| 3 | exclusion_count | integer | 제외 플래그 개수 | raw count |
| 4 | secondary_count | integer | 보조 쟁점 개수 | raw count |

### 텍스트 피처 (500차원)

| # | 이름 | 타입 | 설명 |
|---|------|------|------|
| 5~504 | tfidf_char_wb | float | 판정요지 텍스트의 TF-IDF (char_wb, ngram 2~4, max 500) |

## 라벨

| 값 | 의미 | 기준 |
|----|------|------|
| 0 | 기각 (사용자 승) | 기각, 각하, 정당 판정 |
| 1 | 인용 (근로자 승) | 전부인정, 일부인정, 인용, 부당 판정 |

## 제외 대상

- issue_type_primary == 'union_activity' (노조 사건)
- 판정결과가 매핑 불가 (undecidable)

## 전처리기

- `preprocessors.pkl`: LabelEncoder(primary, stage) + TfidfVectorizer
- 시드: 42
- train/test: 80/20, stratified

## 데이터 소스

- 원본: 법제처_노동위결정문_전문.json (42,105건)
- 태깅: merged_42k_v1.jsonl (40,608건)
- 학습 사용: ~35,752건 (라벨 확정 + 노조 제외)
