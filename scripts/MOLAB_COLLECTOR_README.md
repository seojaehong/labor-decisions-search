# 고용노동부 행정해석 수집 스크립트

법제처 Open API (open.law.go.kr)를 사용하여 고용노동부 행정해석을 자동 수집하고 Supabase에 적재하는 Python 스크립트입니다.

## 개요

- **API**: http://www.law.go.kr/DRF/lawSearch.do (법제처 National Law Information 공동활용)
- **기능**:
  - 키워드 기반 행정해석 검색
  - 날짜 범위 필터링 (예: 2024~2026년)
  - JSON/JSONL 저장
  - Supabase 자동 적재 (옵션)
- **수집 대상**:
  - 고용노동부 행정해석 (회시)
  - 질의 요지 + 답변 전문
  - 관련 법령 정보

## 사전 준비

### 1. 환경 설정

```bash
# Supabase 환경변수 로드
cd /home/ubuntu/work-orchestrator/repos/labor-law-guide
export $(cat supabase/.env | xargs)

# 검증
echo $SUPABASE_URL
echo $SUPABASE_SERVICE_KEY
```

### 2. 테이블 생성

```bash
# Supabase 콘솔에서 직접 실행 또는:
# 1. 수동으로 복사/붙여넣기 (SQL Editor 사용)
# 2. CLI 사용
cat /home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_schema.sql
```

콘솔 또는 `supabase` CLI로 스키마를 로드하세요:

```bash
# 테이블이 생성되면 검증
curl -X GET https://mewqgevgdgghhatqtuos.supabase.co/rest/v1/molab_interpretations \
  -H "apikey: YOUR_SUPABASE_KEY" \
  -H "Authorization: Bearer YOUR_SUPABASE_KEY"
```

### 3. 선택사항: 법제처 API 인증값 설정

기본값은 `test` 키이며, 실무 사용 시 공식 등록 필요:

```bash
# 법제처 open.law.go.kr에서 등록 후
export MOLAB_API_KEY="your-actual-api-key"
```

> **참고**: 테스트용 `OC=test` 키는 레이트 리미트가 있을 수 있습니다.
> 공식 API 키는 02-2109-6446 (법제처 콜센터)으로 문의하세요.

## 사용 방법

### 기본 사용

```bash
cd /home/ubuntu/work-orchestrator/repos/labor-decisions-search

# 키워드 수집 (최신 2024~2026년)
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고,임금,퇴직금,근로계약,취업규칙,산재,괴롭힘,노동조합"
```

### 옵션

#### 1. 기간 제한

```bash
# 특정 연도만
python3 scripts/molab_interpretations_collector.py \
  --keywords "임금" \
  --start-year 2024

# 특정 기간 (YYYYMMDD)
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고" \
  --start-date 20240101 \
  --end-date 20241231
```

#### 2. 건수 제한 (테스트 용)

```bash
# 50건만 수집
python3 scripts/molab_interpretations_collector.py \
  --keywords "임금" \
  --limit 50

# 10건만 테스트 (DB 저장 안함)
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고" \
  --limit 10 \
  --dry-run
```

#### 3. 파일 저장만 (DB 적재 X)

```bash
# JSON/JSONL만 저장
python3 scripts/molab_interpretations_collector.py \
  --keywords "퇴직금" \
  --output-dir ./molab_data \
  --skip-db

# 저장 위치
ls -lh ./molab_data/molab_interpretations_*.json*
```

#### 4. 복합 옵션

```bash
# 2025년, 5개 키워드, 최대 200건, 파일만 저장
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고,임금,퇴직금,근로계약,취업규칙" \
  --start-year 2025 \
  --limit 200 \
  --output-dir ./molab_2025 \
  --skip-db
```

### 드라이런 (테스트)

```bash
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고" \
  --limit 5 \
  --dry-run
```

출력:
```
====================
고용노동부 행정해석 수집 스크립트
====================
API: http://www.law.go.kr/DRF/lawSearch.do
키워드: 해고
기간: 20240101 ~ 20261231
출력 디렉토리: ./molab_interpretations
수집 제한: 5건
[DRY RUN 모드]

Step 1: 행정해석 수집 중...

[키워드] 해고
  페이지 1... 100건 조회 (전체: 234)
 ...

Step 3: Supabase 적재 중...
  [DRY RUN] 5건 insert 예정 (누적: 5)

====================
수집 완료!
====================
```

## 출력 형식

### JSON 형식 (molab_interpretations_20260328_143022.json)

```json
[
  {
    "id": "ml_abc12345",
    "case_id": "12345",
    "case_number": "해석-2024-00123",
    "title": "근로기준법상 월급제 근로자의 퇴직금 산정 방법",
    "inquiry_org": "중소벤처기업부",
    "answer_org": "고용노동부",
    "decision_date": "2024-03-15",
    "inquiry_summary": "Q. 월급제로 임금을 지급받는 근로자의...",
    "answer_summary": "A. 근로기준법 제34조에 따라...",
    "full_text": "【질의요지】\n근로기준법 제34조에 따라...",
    "related_laws": ["근로기준법", "근로기준법시행령"],
    "tags": ["퇴직금", "임금"],
    "url": "http://www.law.go.kr/DRF/lawSearch.do?...",
    "source": "molab.api",
    "collected_at": "2026-03-28T14:30:22.123456"
  }
]
```

### JSONL 형식 (molab_interpretations_20260328_143022.jsonl)

```
{"id": "ml_abc12345", "case_id": "12345", ...}
{"id": "ml_def67890", "case_id": "67890", ...}
```

## Supabase 테이블 구조

### molab_interpretations

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | TEXT PRIMARY KEY | 고유 ID (md5 해시) |
| case_id | TEXT UNIQUE | 법령해석 일련번호 (API ID) |
| case_number | TEXT | 해석 번호 (예: 해석-2024-00123) |
| title | TEXT | 해석 제목 |
| inquiry_org | TEXT | 질의 기관 |
| answer_org | TEXT | 답변 기관 (기본: 고용노동부) |
| decision_date | DATE | 해석 결정 날짜 |
| inquiry_summary | TEXT | 질의 요지 (최대 1000자) |
| answer_summary | TEXT | 답변 요약 (최대 2000자) |
| full_text | TEXT | 회시 전문 (최대 10000자) |
| related_laws | TEXT[] | 관련 법령 배열 |
| tags | TEXT[] | 키워드 태그 배열 |
| url | TEXT | 원본 API URL |
| source | TEXT | 데이터 출처 (기본: molab.api) |
| collected_at | TIMESTAMP | 수집 시간 |
| created_at | TIMESTAMP | 생성 시간 |
| updated_at | TIMESTAMP | 수정 시간 |

### 인덱스

- `idx_molab_interpretations_case_number`: case_number 빠른 조회
- `idx_molab_interpretations_decision_date`: 날짜 순 정렬 성능
- `idx_molab_interpretations_tags`: 태그 배열 필터
- `idx_molab_interpretations_inquiry_org`: 질의 기관 필터
- `idx_molab_interpretations_collected_at`: 최신순 정렬
- `idx_molab_interpretations_full_text_tsvector`: 전문 한글 전체 검색

### View: molab_latest_interpretations

최근 6개월 행정해석 (최대 500건)을 빠르게 조회할 수 있는 뷰:

```sql
SELECT * FROM molab_latest_interpretations
WHERE tags @> ARRAY['해고']  -- 태그 포함 검색
LIMIT 20;
```

## API 파라미터 설정

스크립트는 다음 파라미터를 자동으로 설정합니다:

```
target=moelCgmExpc      # 고용노동부 행정해석
type=json               # JSON 응답
OC=<api-key>           # 인증값 (환경변수 또는 --api-key)
query=<keyword>        # 검색 키워드
display=100            # 페이지당 결과 수 (최대 100)
page=<page>            # 페이지 번호
sort=date_desc         # 최신순 정렬
search=2               # 전문 검색
explYd=<start>~<end>   # 날짜 범위 필터 (YYYYMMDD~YYYYMMDD)
```

API 문서: https://open.law.go.kr/LSO/openApi/guideList.do

## 문제 해결

### "Error: SUPABASE_URL과 SUPABASE_SERVICE_KEY 필요"

```bash
# 환경변수 다시 로드
cd /home/ubuntu/work-orchestrator/repos/labor-law-guide
export $(cat supabase/.env | xargs)
printenv | grep SUPABASE
```

### API 응답 오류 (403, 429 등)

1. **403 Forbidden**: API 키 확인
   ```bash
   export MOLAB_API_KEY="your-actual-key"
   ```

2. **429 Too Many Requests**: 레이트 리미트
   - 스크립트의 `REQUEST_DELAY = 0.5` 증가
   - 또는 `--limit` 사용해 작은 단위로 수집

3. **API 응답이 없음**: 네트워크 확인
   ```bash
   curl -s "http://www.law.go.kr/DRF/lawSearch.do?target=moelCgmExpc&type=json&OC=test&query=해고&display=5&page=1"
   ```

### Supabase Insert 실패 (409 Conflict)

case_id 중복:
- `--skip-db` 사용해 기존 데이터 확인
- 또는 테이블 정리: `DELETE FROM molab_interpretations WHERE collected_at < NOW() - INTERVAL '30 days';`

## 성능 최적화

### 대량 수집 (1000건 이상)

```bash
# 분할 수집 후 병합
for year in 2024 2025 2026; do
  python3 scripts/molab_interpretations_collector.py \
    --keywords "해고,임금" \
    --start-year $year \
    --output-dir ./molab_${year} &
done
wait
```

### 선택적 전문 조회

스크립트의 `fetch_interpretation_detail()` 호출을 주석 처리하면 빠름:
```python
# detail = fetch_interpretation_detail(int(case_id)) if case_id.isdigit() else None
detail = None
```

## 정기 운영

### cron 예시

```bash
# 매주 월요일 00:00 UTC 수집
0 0 * * 1 /usr/bin/python3 /home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_collector.py --keywords "해고,임금,퇴직금,근로계약" --start-year 2026 >> /tmp/molab_cron.log 2>&1
```

### 로그 확인

```bash
tail -f /tmp/molab_cron.log
```

## 참고

- **법제처 API 문서**: https://open.law.go.kr/LSO/openApi/guideList.do
- **고용노동부 법령해석 목록 조회**: https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=cgmExpcMoelListGuide
- **고용노동부 법령해석 본문 조회**: https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=cgmExpcMoelInfoGuide
- **Supabase 콘솔**: https://app.supabase.com/project/mewqgevgdgghhatqtuos
- **공공데이터포털**: https://www.data.go.kr

## 라이선스

노란봉투법 가이드 (노란봉투법.com) 내부 도구
