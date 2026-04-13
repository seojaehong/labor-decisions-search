# 고용노동부 행정해석 수집 — 빠른 시작 가이드

## 1단계: 환경 설정 (1분)

```bash
# Supabase 환경변수 로드
cd /home/ubuntu/work-orchestrator/repos/labor-law-guide
export $(cat supabase/.env | xargs)

# 검증
echo "Supabase URL: $SUPABASE_URL"
```

## 2단계: 테이블 생성 (2분)

Supabase 콘솔에서:
1. https://app.supabase.com/project/mewqgevgdgghhatqtuos
2. SQL Editor 클릭
3. `/home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_schema.sql` 내용 복사
4. 붙여넣고 실행

또는 파일 확인:
```bash
cat /home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_schema.sql
```

## 3단계: 테스트 실행 (2분)

```bash
cd /home/ubuntu/work-orchestrator/repos/labor-decisions-search

# 샘플 데이터로 테스트
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고,임금" \
  --limit 5 \
  --dry-run

# 출력 확인
ls -lh molab_interpretations/
cat molab_interpretations/molab_interpretations_*.json | head -50
```

## 4단계: 실제 수집 (5분~)

```bash
# 2024년 행정해석 수집 (IP 등록 필요!)
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고,임금,퇴직금,근로계약,취업규칙,산재,괴롭힘,노동조합" \
  --start-year 2024
```

### 오류: "사용자 정보 검증에 실패했습니다"

**원인**: API 키의 IP 주소가 미등록

**해결**:
1. 공식 API 키 신청: 02-2109-6446 (법제처)
2. IP 등록 요청
3. 환경변수 설정:
   ```bash
   export MOLAB_API_KEY="your-actual-api-key"
   ```

## 주요 명령어

### 키워드 기반 수집
```bash
python3 scripts/molab_interpretations_collector.py \
  --keywords "임금,휴직,연차"
```

### 특정 기간 수집
```bash
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고" \
  --start-date 20250101 \
  --end-date 20251231
```

### 파일만 저장 (DB 저장 X)
```bash
python3 scripts/molab_interpretations_collector.py \
  --keywords "산재" \
  --output-dir ./molab_2024 \
  --skip-db
```

### 드라이런 (시뮬레이션)
```bash
python3 scripts/molab_interpretations_collector.py \
  --keywords "임금" \
  --limit 10 \
  --dry-run
```

## 파일 위치

| 파일 | 설명 |
|------|------|
| `molab_interpretations_collector.py` | 메인 스크립트 |
| `molab_interpretations_schema.sql` | Supabase 테이블 생성 SQL |
| `MOLAB_COLLECTOR_README.md` | 상세 문서 |
| `MOLAB_QUICK_START.md` | 이 파일 |
| `molab_interpretations/` | 수집 결과 저장소 |

## 수집 결과 확인

### JSON 파일
```bash
cat molab_interpretations/molab_interpretations_*.json | python3 -m json.tool | head -100
```

### JSONL 파일
```bash
head -5 molab_interpretations/molab_interpretations_*.jsonl
```

### Supabase에서 조회
```sql
SELECT id, case_number, title, decision_date, tags
FROM molab_interpretations
WHERE tags @> ARRAY['해고']
ORDER BY decision_date DESC
LIMIT 10;
```

## 문제 해결

### "경고: 수집된 항목이 없습니다"

1. **API 키 확인**
   ```bash
   echo $MOLAB_API_KEY
   ```
   (비어있으면 `--api-key your-key` 사용)

2. **IP 주소 확인**
   ```bash
   curl -s https://api.ipify.org
   ```
   → 법제처에 등록된 IP와 일치하는지 확인

3. **테스트 API 호출**
   ```bash
   curl -v "http://www.law.go.kr/DRF/lawSearch.do?target=moelCgmExpc&type=json&OC=test&query=test&display=1&page=1"
   ```

### Supabase 연결 실패

```bash
# 환경변수 재로드
export $(cat /home/ubuntu/work-orchestrator/repos/labor-law-guide/supabase/.env | xargs)

# 테이블 존재 확인
curl -s -H "apikey: $SUPABASE_SERVICE_KEY" \
  https://mewqgevgdgghhatqtuos.supabase.co/rest/v1/molab_interpretations
```

## 다음 단계

- [상세 문서](./MOLAB_COLLECTOR_README.md) 읽기
- 정기 cron 작업 설정
- 수집 데이터로 검색 기능 구현
- 블로그 자동 게시와 통합

## 지원

- **법제처 API 문제**: 02-2109-6446
- **Supabase 문제**: https://app.supabase.com/project/mewqgevgdgghhatqtuos
- **스크립트 개선**: 스크립트 헤더 주석 참조
