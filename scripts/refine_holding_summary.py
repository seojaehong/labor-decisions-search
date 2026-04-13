#!/usr/bin/env python3
"""
BigCase holding_summary AI 재정제 스크립트

80.6%의 holding_summary에 판결문 원문 패턴("원고/피고", "이 사건", "을 제" 등)이
그대로 남아있어 일반 사용자에게 부적절. AI로 깔끔한 요약으로 재작성.

사용법:
  python3 refine_holding_summary.py --dry-run          # 샘플 5건만 테스트
  python3 refine_holding_summary.py --batch 100        # 100건씩 처리
  python3 refine_holding_summary.py --category absence  # 특정 카테고리만
  python3 refine_holding_summary.py --resume            # 마지막 위치부터 재개

환경변수:
  SUPABASE_URL, SUPABASE_KEY — Supabase 접속
  ANTHROPIC_API_KEY 또는 OPENAI_API_KEY — AI 모델
"""

import os
import sys
import json
import time
import argparse
import re
from datetime import datetime
from pathlib import Path

try:
    from supabase import create_client
except ImportError:
    print("pip install supabase 필요")
    sys.exit(1)

# ─── Config ───────────────────────────────────────────────────────────────────

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://mewqgevgdgghhatqtuos.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

BATCH_SIZE = 50
PROGRESS_FILE = Path(__file__).parent / ".refine_progress.json"
LOG_DIR = Path(__file__).parent / "refine_logs"

# 원문 오염 패턴 (이 패턴이 있으면 재정제 대상)
RAW_PATTERNS = [
    r"원고[는가의을]",
    r"피고[는가의을]",
    r"이 사건",
    r"[갑을] 제\s?\d+호증",
    r"변론 전체의 취지",
    r"원고와 피고",
    r"원심판결",
    r"항소이유",
]

REFINE_PROMPT = """당신은 노동법 전문가입니다. 아래 법원 판결문 요약을 일반 실무자가 이해할 수 있도록 다시 작성해주세요.

## 규칙
1. "원고"→"근로자", "피고"→"회사(사용자)" 로 치환
2. "갑 제○호증", "을 제○호증" 등 증거번호 제거
3. "이 사건 해고/징계" → "해당 해고/징계"로 자연스럽게
4. "변론 전체의 취지" 같은 소송법 용어 제거
5. 핵심 쟁점과 결론을 명확하게
6. 200~500자 분량으로 요약
7. 마크다운 사용 가능 (## 헤딩, **굵게**, - 목록)
8. 판결의 핵심 논리와 실무적 시사점 포함

## 사건 정보
- 제목: {title}
- 카테고리: {category}
- 판결결과: {result}
- 핵심쟁점: {key_issue}

## 현재 요약 (재작성 대상)
{holding_summary}

## 재작성된 요약 (위 규칙을 준수하여):"""


def is_contaminated(text: str) -> bool:
    """원문 오염 패턴이 있는지 확인"""
    if not text:
        return False
    for pattern in RAW_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def count_contamination(text: str) -> int:
    """오염 패턴 매칭 수"""
    if not text:
        return 0
    count = 0
    for pattern in RAW_PATTERNS:
        if re.search(pattern, text):
            count += 1
    return count


def refine_with_anthropic(record: dict) -> str | None:
    """Anthropic Claude로 재정제"""
    try:
        import anthropic
    except ImportError:
        print("pip install anthropic 필요")
        return None

    client = anthropic.Anthropic()
    prompt = REFINE_PROMPT.format(
        title=record.get("title", ""),
        category=", ".join(record.get("reason_category", [])),
        result=record.get("decision_result", ""),
        key_issue=record.get("key_issue", ""),
        holding_summary=record.get("holding_summary", ""),
    )

    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


def refine_with_openai(record: dict) -> str | None:
    """OpenAI GPT로 재정제"""
    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai 필요")
        return None

    client = OpenAI()
    prompt = REFINE_PROMPT.format(
        title=record.get("title", ""),
        category=", ".join(record.get("reason_category", [])),
        result=record.get("decision_result", ""),
        key_issue=record.get("key_issue", ""),
        holding_summary=record.get("holding_summary", ""),
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()


def get_refiner():
    """사용 가능한 AI 모델 선택"""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return refine_with_anthropic, "claude-haiku-4.5"
    elif os.environ.get("OPENAI_API_KEY"):
        return refine_with_openai, "gpt-4o-mini"
    else:
        print("ANTHROPIC_API_KEY 또는 OPENAI_API_KEY 환경변수 필요")
        sys.exit(1)


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"last_id": None, "processed": 0, "errors": 0, "skipped": 0}


def save_progress(progress: dict):
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="BigCase holding_summary AI 재정제")
    parser.add_argument("--dry-run", action="store_true", help="샘플 5건만 테스트 (DB 미수정)")
    parser.add_argument("--batch", type=int, default=BATCH_SIZE, help="배치 크기")
    parser.add_argument("--category", type=str, help="특정 카테고리만 처리")
    parser.add_argument("--resume", action="store_true", help="마지막 위치부터 재개")
    parser.add_argument("--max-records", type=int, default=0, help="최대 처리 건수 (0=무제한)")
    args = parser.parse_args()

    if not SUPABASE_KEY:
        print("SUPABASE_KEY 환경변수 필요")
        sys.exit(1)

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    refine_fn, model_name = get_refiner()

    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"refine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

    progress = load_progress() if args.resume else {"last_id": None, "processed": 0, "errors": 0, "skipped": 0}

    print(f"[재정제 시작] 모델: {model_name}, 배치: {args.batch}, dry-run: {args.dry_run}")
    if args.category:
        print(f"  카테고리 필터: {args.category}")
    if args.resume and progress["last_id"]:
        print(f"  재개 위치: {progress['last_id']} (처리됨: {progress['processed']})")

    limit = 5 if args.dry_run else args.batch
    total_processed = progress["processed"]
    total_errors = progress["errors"]
    total_skipped = progress["skipped"]

    while True:
        # Fetch batch
        q = supabase.table("nlrc_decisions") \
            .select("id, title, holding_summary, key_issue, reason_category, decision_result") \
            .like("id", "bc_%") \
            .not_.is_("holding_summary", "null") \
            .order("id") \
            .limit(limit)

        if args.category:
            q = q.contains("reason_category", [args.category])

        if progress["last_id"]:
            q = q.gt("id", progress["last_id"])

        resp = q.execute()
        rows = resp.data or []

        if not rows:
            print(f"\n[완료] 더 이상 처리할 레코드 없음")
            break

        for row in rows:
            record_id = row["id"]
            holding = row.get("holding_summary", "") or ""

            # Skip if not contaminated
            if not is_contaminated(holding):
                total_skipped += 1
                progress["last_id"] = record_id
                progress["skipped"] = total_skipped
                continue

            contamination = count_contamination(holding)
            print(f"  [{total_processed + 1}] {record_id} (오염:{contamination}) ", end="", flush=True)

            try:
                refined = refine_fn(row)
                if not refined:
                    print("SKIP (empty)")
                    total_errors += 1
                    continue

                # Validate: refined should be cleaner
                new_contamination = count_contamination(refined)
                if new_contamination >= contamination:
                    print(f"WARN (재정제 후에도 오염 {new_contamination}개)")
                    # Log but still update if some improvement
                    with open(log_file, "a") as f:
                        json.dump({"id": record_id, "status": "warn", "before": contamination, "after": new_contamination}, f, ensure_ascii=False)
                        f.write("\n")

                if not args.dry_run:
                    supabase.table("nlrc_decisions") \
                        .update({"holding_summary": refined}) \
                        .eq("id", record_id) \
                        .execute()
                    print(f"OK ({len(refined)}자)")
                else:
                    print(f"DRY ({len(refined)}자)")
                    print(f"    원본: {holding[:80]}...")
                    print(f"    정제: {refined[:80]}...")

                # Log
                with open(log_file, "a") as f:
                    json.dump({
                        "id": record_id,
                        "status": "ok",
                        "before_len": len(holding),
                        "after_len": len(refined),
                        "before_contamination": contamination,
                        "after_contamination": new_contamination if 'new_contamination' in dir() else 0,
                    }, f, ensure_ascii=False)
                    f.write("\n")

                total_processed += 1

            except Exception as e:
                print(f"ERROR ({e})")
                total_errors += 1
                with open(log_file, "a") as f:
                    json.dump({"id": record_id, "status": "error", "error": str(e)}, f, ensure_ascii=False)
                    f.write("\n")
                time.sleep(2)  # Rate limit backoff

            progress["last_id"] = record_id
            progress["processed"] = total_processed
            progress["errors"] = total_errors
            progress["skipped"] = total_skipped
            save_progress(progress)

            # Rate limiting
            time.sleep(0.5)

        if args.dry_run:
            break

        if args.max_records and total_processed >= args.max_records:
            print(f"\n[중단] max-records ({args.max_records}) 도달")
            break

        print(f"  --- 배치 완료 (처리: {total_processed}, 스킵: {total_skipped}, 에러: {total_errors}) ---")

    # Summary
    print(f"\n{'='*50}")
    print(f"[재정제 완료]")
    print(f"  처리: {total_processed}건")
    print(f"  스킵(깨끗): {total_skipped}건")
    print(f"  에러: {total_errors}건")
    print(f"  로그: {log_file}")
    save_progress(progress)


if __name__ == "__main__":
    main()
