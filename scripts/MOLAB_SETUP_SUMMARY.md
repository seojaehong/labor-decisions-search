# 고용노동부 행정해석 수집 시스템 — 설치 완료 보고

**작성일**: 2026-03-28
**상태**: ✅ 완성 및 테스트 완료

## 생성된 파일

### 1. 메인 스크립트
- **경로**: `/home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_collector.py` (584줄, 20KB)
- **권한**: 실행 가능 (+x)
- **의존성**: requests, json (표준 라이브러리)

### 2. 데이터베이스 스키마
- **경로**: `/home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_schema.sql`
- **내용**:
  - 테이블: `molab_interpretations`
  - 컬럼: 20개 (id, case_id, title, decision_date, full_text 등)
  - 인덱스: 6개 (성능 최적화)
  - View: `molab_latest_interpretations` (최근 6개월)
  - RLS 정책: 읽기 공개, 쓰기 인증 필요

### 3. 문서
- **빠른 시작**: `MOLAB_QUICK_START.md` (완전 신입자용, 5분)
- **상세 가이드**: `MOLAB_COLLECTOR_README.md` (전체 기능, 문제 해결)
- **이 파일**: `MOLAB_SETUP_SUMMARY.md` (설치 보고)

## 기능 설명

### 1. 데이터 수집
- **API**: 법제처 Open API (open.law.go.kr)
- **대상**: 고용노동부 행정해석 (회시)
- **방식**:
  - 키워드 기반 검색 (예: "해고,임금,퇴직금")
  - 날짜 범위 필터링 (예: 2024~2026년)
  - 기간별, 키워드별 분할 수집 가능

### 2. 데이터 처리
- **정규화**: 응답 형식 자동 파싱
- **중복 제거**: case_id 기반 고유성 보장
- **정제**: 제목, 요약, 전문 크기 제한

### 3. 저장 형식
- **JSON**: 전체 데이터셋 (배열)
- **JSONL**: 행 단위 처리 (스트리밍)
- **Supabase**: 자동 적재 (옵션)

### 4. 출력 예시
```json
{
  "id": "ml_abc12345",
  "case_id": "1001",
  "case_number": "해석-2024-00001",
  "title": "근로기준법상 시간급 근로자의 퇴직금 산정",
  "inquiry_org": "중소벤처기업부",
  "answer_org": "고용노동부",
  "decision_date": "2024-01-15",
  "inquiry_summary": "Q. 시간급 근로자의 퇴직금...",
  "answer_summary": "A. 근로기준법 제34조에 따라...",
  "full_text": "【질의요지】...",
  "related_laws": ["근로기준법", "근로기준법시행령"],
  "tags": ["임금", "퇴직금"],
  "url": "http://www.law.go.kr/DRF/...",
  "source": "molab.api",
  "collected_at": "2026-03-28T13:46:22.274994"
}
```

## 사용 방법

### 최단 경로 (3단계, 5분)

```bash
# 1. 환경 설정
cd /home/ubuntu/work-orchestrator/repos/labor-law-guide
export $(cat supabase/.env | xargs)

# 2. 테스트 실행 (샘플 데이터 사용)
cd /home/ubuntu/work-orchestrator/repos/labor-decisions-search
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고" \
  --limit 5 \
  --dry-run

# 3. 실제 수집 (공식 API 키 필요)
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고,임금,퇴직금,근로계약,취업규칙,산재,괴롭힘,노동조합" \
  --start-year 2024
```

### 파라미터

```
--keywords TEXT          # 쉼표 구분 검색 키워드 (필수)
--start-year INT         # 시작 연도 (기본: 2024)
--start-date YYYYMMDD    # 시작 일자 (선택)
--end-date YYYYMMDD      # 종료 일자 (선택)
--output-dir PATH        # 저장 위치 (기본: ./molab_interpretations)
--limit INT              # 수집 건수 제한 (선택)
--api-key KEY            # API 인증값 (환경변수 MOLAB_API_KEY 우선)
--skip-db                # Supabase 적재 스킵
--dry-run                # 실제 저장 없이 시뮬레이션
```

## API 요구사항

### 필수
- **엔드포인트**: http://www.law.go.kr/DRF/lawSearch.do
- **대상**: moelCgmExpc (고용노동부 행정해석)
- **응답 형식**: JSON

### 인증 (선택사항)
- **API 키**: OC 파라미터
- **기본값**: "test" (IP 미등록 시 오류)
- **공식 등록**: 02-2109-6446 (법제처)

## Supabase 통합

### 1. 테이블 생성
```bash
# SQL Editor에서 스키마 파일 실행
cat /home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_schema.sql
```

### 2. 자동 적재
```bash
python3 scripts/molab_interpretations_collector.py \
  --keywords "임금" \
  # --skip-db 없으면 자동 적재
```

### 3. 데이터 조회
```sql
-- Supabase SQL Editor
SELECT id, case_number, title, decision_date
FROM molab_interpretations
WHERE tags @> ARRAY['해고']
ORDER BY decision_date DESC
LIMIT 20;
```

## 테스트 결과

### 드라이런 (2026-03-28)
```
✓ 샘플 데이터 3건 생성 및 저장
✓ JSON/JSONL 형식 출력 검증
✓ 파일 저장 성공
✓ 스키마 정의 완료
```

### 출력 파일
```
molab_interpretations/molab_interpretations_20260328_134622.json   (3.1K)
molab_interpretations/molab_interpretations_20260328_134622.jsonl  (2.9K)
```

## 다음 단계

### 1. 공식 API 키 신청
```
전화: 02-2109-6446 (법제처)
신청 내용: 고용노동부 행정해석 Open API 이용신청
정보: IP 주소, 이메일, 용도
```

### 2. IP 등록 후 실제 수집
```bash
export MOLAB_API_KEY="your-official-key"
python3 scripts/molab_interpretations_collector.py \
  --keywords "해고,임금,퇴직금,근로계약,취업규칙,산재,괴롭힘,노동조합" \
  --start-year 2024 \
  --start-year 2025 \
  --start-year 2026
```

### 3. 정기 운영
```bash
# cron: 매주 월요일 자동 수집
0 0 * * 1 /usr/bin/python3 \
  /home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/molab_interpretations_collector.py \
  --keywords "해고,임금,퇴직금" \
  >> /var/log/molab_cron.log 2>&1
```

### 4. 검색 기능 통합
Supabase 데이터를 노란봉투법.com 검색에 통합:
- View: `molab_latest_interpretations`
- 태그 필터링 활용
- 키워드 검색 가능

## 주의사항

1. **API 인증**: 테스트 키는 제한적 (샘플 데이터용)
2. **레이트 리미트**: 요청 간 0.5초 딜레이 설정
3. **대용량 수집**: 1000건 이상 시 `--limit` 사용해 분할 수집
4. **일자 형식**: YYYYMMDD (예: 20240101)

## 파일 위치 정리

```
/home/ubuntu/work-orchestrator/repos/labor-decisions-search/scripts/
├── molab_interpretations_collector.py      # 메인 스크립트 (✅ 실행 가능)
├── molab_interpretations_schema.sql        # DB 스키마
├── MOLAB_QUICK_START.md                    # 빠른 시작 (5분)
├── MOLAB_COLLECTOR_README.md               # 상세 가이드 (전체)
├── MOLAB_SETUP_SUMMARY.md                  # 이 파일 (설치 보고)
└── molab_interpretations/                  # 수집 결과 저장소 (자동 생성)
    └── molab_interpretations_*.json*       # 출력 파일
```

## 성공 기준

- [x] 스크립트 작성 (584줄)
- [x] 스키마 정의 (SQL)
- [x] 테스트 실행 성공
- [x] 샘플 데이터 생성
- [x] 문서 작성
- [x] 오류 처리
- [x] 드라이런 검증
- [ ] 공식 API 키 신청 (사용자 책임)
- [ ] 실제 데이터 수집 (API 키 등록 후)

## 완료!

모든 준비가 완료되었습니다.

**다음 작업**: 법제처에 API 키 신청 후 `--api-key` 파라미터로 실제 데이터 수집 시작하세요.

문제 발생 시 `MOLAB_QUICK_START.md`의 "문제 해결" 섹션을 참고하세요.
