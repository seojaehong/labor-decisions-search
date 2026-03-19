"""
42k 노동위판정례 → Supabase nlrc_decisions 업로드
Bulk upsert (1000건 단위) + 태그 필터링

사용법:
  python3 scripts/upload_to_supabase.py              # 전체
  python3 scripts/upload_to_supabase.py --dry-run    # 미리보기
  python3 scripts/upload_to_supabase.py --batch 100  # 100건만
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json, re, argparse
from pathlib import Path
from datetime import datetime

# pip install supabase
from supabase import create_client

SUPABASE_URL = "https://mewqgevgdgghhatqtuos.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ld3FnZXZnZGdnaGhhdHF0dW9zIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjcxNTUxMCwiZXhwIjoyMDg4MjkxNTEwfQ.cfDNqZoMmoUTzSWJtt4y90R0gPMr2yRVA-OAj_ZSl-Y"

MD_DIR = Path("C:/Users/iceam/OneDrive/5.산업안전/문서/Obsidian Vault/노동위판정례")

# 허용된 태그 목록 (TAG_CATEGORIES와 동기화)
ALLOWED_TAGS = {
    '부당해고', '부당노동행위', '부당징계', '부당전보', '차별시정', '조정', '중재',
    '손해배상', '긴급조정', '휴업', '상병', '재해', '의결', '노사협의회', '교섭단위', '공정대표의무',
    '해고사유', '절차위반', '징계양정', '통상임금', '퇴직금', '연차휴가', '근로시간',
    '최저임금', '임금체불', '직장내괴롭힘', '성희롱', '비정규직', '파견근로', '원청책임',
    '도급', '취업규칙', '단체협약', '쟁의행위', '필수유지업무', '노조설립', '복수노조',
    '지배개입', '불이익취급', '단체교섭거부', '사직', '권고사직', '징계해고', '면직',
    '수습', '전보', '감봉', '정직', '산재', '4대보험', '당사자적격', '근로자성',
    '구제이익', '징계시효', '고용승계', '갱신기대권', '제척기간', '해고부존재', '소명기회', '폐업',
    '인용', '기각', '각하', '화해', '취하', '초심유지', '초심취소', '조정성립', '중재재정',
    '근로자', '사용자', '노동조합', '공무원', '교원',
    '제조업', '건설업', '운수업', '의료', '교육', '공공기관', '금융', 'IT', '서비스업',
    '임금협약', '단체교섭', '촉탁직', '비교대상근로자', '임금피크제',
}

# decisionResult → DB decision_result 매핑
RESULT_MAP = {
    '인용': 'granted', '기각': 'dismissed', '각하': 'rejected',
    '초심유지': 'upheld', '초심취소': 'overturned', '화해': 'settled', '취하': 'settled',
    '조정성립': 'settled', '일부인용': 'partial', '일부인정': 'partial',
}


def parse_md(md_path: Path) -> dict | None:
    text = md_path.read_text(encoding='utf-8')
    fm_match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not fm_match:
        return None

    fm = {}
    for line in fm_match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()

    # tags 파싱
    tags_match = re.search(r'^tags:\s*\[(.*?)\]', fm_match.group(1), re.MULTILINE)
    tags = []
    if tags_match:
        raw_tags = [t.strip() for t in tags_match.group(1).split(',') if t.strip()]
        tags = [t for t in raw_tags if t in ALLOWED_TAGS]  # 필터링

    # 본문 파싱
    body = text[fm_match.end():]
    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_path.stem

    # 섹션 추출
    holding_points = ''
    holding_summary = ''
    hp_match = re.search(r'## 판정사항\n(.*?)(?=\n## |\n---|\Z)', body, re.DOTALL)
    if hp_match:
        holding_points = hp_match.group(1).strip()[:2000]
    hs_match = re.search(r'## 판정요지\n(.*?)(?=\n## |\n---|\Z)', body, re.DOTALL)
    if hs_match:
        holding_summary = hs_match.group(1).strip()[:5000]

    # URL
    url_match = re.search(r'\[원문 링크\]\((.*?)\)', body)
    url = url_match.group(1) if url_match else ''

    # ID
    case_no = fm.get('caseNo', md_path.stem)
    file_id = case_no if case_no else md_path.stem

    # decision_result 매핑
    raw_result = fm.get('decisionResult', '')
    decision_result = 'other'
    for kr, en in RESULT_MAP.items():
        if kr in raw_result:
            decision_result = en
            break

    return {
        'id': file_id,
        'title': title[:500],
        'case_number': case_no,
        'department': fm.get('department', ''),
        'decision_date': fm.get('date', None),
        'case_type': fm.get('caseType', ''),
        'decision_result': decision_result,
        'holding_points': holding_points,
        'holding_summary': holding_summary,
        'url': url,
        'tags': tags,
        'source': fm.get('source', 'law.go.kr'),
    }


def run(args):
    files = sorted([f for f in MD_DIR.glob('*.md') if not f.name.startswith('_')])
    if args.batch:
        files = files[:args.batch]

    total = len(files)
    print(f"대상: {total}개 파일")

    rows = []
    skipped = 0
    for f in files:
        data = parse_md(f)
        if data:
            rows.append(data)
        else:
            skipped += 1

    print(f"파싱: {len(rows)}건 성공, {skipped}건 스킵")

    if args.dry_run:
        for r in rows[:5]:
            print(f"  {r['id']:20s} | tags={len(r['tags'])} | {r['title'][:40]}")
        return

    # Supabase 연결 + Bulk upsert
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    BATCH_SIZE = 1000
    uploaded = 0

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        try:
            supabase.table('nlrc_decisions').upsert(batch).execute()
            uploaded += len(batch)
            print(f"  [{uploaded}/{len(rows)}] 업로드 완료")
        except Exception as e:
            print(f"  [{i}~] 에러: {str(e)[:100]}")

    print(f"\n완료: {uploaded}/{len(rows)} 업로드")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--batch', type=int)
    run(parser.parse_args())
