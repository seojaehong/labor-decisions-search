"""
판정례 재태깅 JSONL 병합 스크립트

여러 draft/reviewed JSONL 파일을 case_id 기준으로 병합.
reviewed > draft 우선. 동일 case_id 충돌 시 review_status 우선순위 적용.

사용법:
    python3 scripts/merge_tagging_outputs.py retagging/output/draft/*.jsonl -o retagging/output/merged/merged_v1.jsonl
    python3 scripts/merge_tagging_outputs.py retagging/output/draft/*.jsonl retagging/output/reviewed/*.jsonl -o merged.jsonl
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

# review_status 우선순위 (높을수록 우선)
STATUS_PRIORITY = {
    "final": 5,
    "approved": 4,
    "reviewed": 3,
    "pending": 2,
    "needs_revision": 1,
}


def load_jsonl(file_path):
    """JSONL 파일에서 레코드 로드. (records, errors) 반환."""
    records = []
    errors = []
    path = Path(file_path)

    if not path.exists():
        errors.append(f"파일 없음: {file_path}")
        return records, errors

    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if isinstance(record, dict):
                    record["_source_file"] = path.name
                    record["_source_line"] = line_num
                    records.append(record)
                else:
                    errors.append(f"{path.name}:{line_num} — dict가 아님")
            except json.JSONDecodeError as e:
                errors.append(f"{path.name}:{line_num} — JSON 파싱 실패: {e}")

    return records, errors


def get_priority(record):
    """레코드의 review_status 기반 우선순위."""
    status = record.get("review_status", "pending")
    return STATUS_PRIORITY.get(status, 0)


def merge_records(all_records):
    """case_id 기준 병합. 우선순위 높은 레코드 유지."""
    merged = {}
    overwritten = []
    conflicts = []

    for record in all_records:
        case_id = record.get("case_id")
        if not case_id:
            conflicts.append({"reason": "case_id 없음", "source": record.get("_source_file", "?")})
            continue

        if case_id not in merged:
            merged[case_id] = record
        else:
            existing = merged[case_id]
            new_priority = get_priority(record)
            old_priority = get_priority(existing)

            if new_priority > old_priority:
                overwritten.append({
                    "case_id": case_id,
                    "old_status": existing.get("review_status"),
                    "new_status": record.get("review_status"),
                    "old_source": existing.get("_source_file"),
                    "new_source": record.get("_source_file"),
                })
                merged[case_id] = record
            elif new_priority == old_priority:
                conflicts.append({
                    "case_id": case_id,
                    "reason": f"동일 우선순위 ({record.get('review_status')})",
                    "sources": [existing.get("_source_file"), record.get("_source_file")],
                })
                # 나중 파일 우선 (덮어쓰기)
                merged[case_id] = record
            # else: 기존 유지

    return merged, overwritten, conflicts


def main():
    parser = argparse.ArgumentParser(description="판정례 재태깅 JSONL 병합")
    parser.add_argument("files", nargs="+", help="병합할 JSONL 파일 경로")
    parser.add_argument("-o", "--output", default="retagging/output/merged/merged_v1.jsonl",
                        help="출력 파일 경로")
    parser.add_argument("--report", action="store_true", help="logs/merge_report.md 저장")
    args = parser.parse_args()

    # 로드
    all_records = []
    load_errors = []
    file_counts = {}

    for file_path in args.files:
        records, errors = load_jsonl(file_path)
        all_records.extend(records)
        load_errors.extend(errors)
        file_counts[Path(file_path).name] = len(records)

    if load_errors:
        print(f"로드 에러 {len(load_errors)}건:")
        for e in load_errors:
            print(f"  {e}")

    # 병합
    merged, overwritten, conflicts = merge_records(all_records)

    # 내부 메타 필드 제거 후 저장
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for case_id in sorted(merged.keys()):
            record = merged[case_id]
            clean = {k: v for k, v in record.items() if not k.startswith("_")}
            f.write(json.dumps(clean, ensure_ascii=False) + "\n")

    # 통계
    status_dist = Counter(r.get("review_status", "?") for r in merged.values())
    confidence_dist = Counter(r.get("confidence", "?") for r in merged.values())
    primary_dist = Counter(r.get("issue_type_primary", "?") for r in merged.values())

    # ── 리포트 출력 ──
    print("=" * 60)
    print("  판정례 재태깅 JSONL 병합 리포트")
    print("=" * 60)

    print(f"\n입력 파일: {len(args.files)}개")
    for name, count in file_counts.items():
        print(f"  {name}: {count}건")

    print(f"\n입력 합계: {len(all_records)}건")
    print(f"병합 결과: {len(merged)}건 (고유 case_id)")
    print(f"덮어쓴 건: {len(overwritten)}건")
    print(f"충돌 건:   {len(conflicts)}건")
    print(f"로드 에러: {len(load_errors)}건")

    print(f"\n출력 파일: {output_path}")

    print(f"\n[review_status 분포]")
    for k, v in status_dist.most_common():
        print(f"  {k}: {v}")

    print(f"\n[confidence 분포]")
    for k, v in confidence_dist.most_common():
        print(f"  {k}: {v}")

    print(f"\n[issue_type_primary 분포]")
    for k, v in primary_dist.most_common():
        print(f"  {k}: {v}")

    if overwritten:
        print(f"\n{'─' * 60}")
        print(f"덮어쓴 건 상세:")
        for o in overwritten:
            print(f"  {o['case_id']}: {o['old_status']}({o['old_source']}) → {o['new_status']}({o['new_source']})")

    if conflicts:
        print(f"\n{'─' * 60}")
        print(f"충돌 건 상세:")
        for c in conflicts[:20]:
            print(f"  {c}")

    # ── 리포트 파일 저장 ──
    if args.report:
        report_dir = Path("retagging/logs")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "merge_report.md"

        lines = [
            f"# 재태깅 JSONL 병합 리포트\n",
            f"날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
            f"## 요약\n",
            f"- 입력: {len(all_records)}건 ({len(args.files)}개 파일)\n",
            f"- 병합: {len(merged)}건\n",
            f"- 덮어쓰기: {len(overwritten)}건\n",
            f"- 충돌: {len(conflicts)}건\n",
            f"- 출력: {output_path}\n\n",
            f"## review_status 분포\n",
        ]
        for k, v in status_dist.most_common():
            lines.append(f"- {k}: {v}\n")
        lines.append(f"\n## confidence 분포\n")
        for k, v in confidence_dist.most_common():
            lines.append(f"- {k}: {v}\n")
        lines.append(f"\n## issue_type_primary 분포\n")
        for k, v in primary_dist.most_common():
            lines.append(f"- {k}: {v}\n")

        report_path.write_text("".join(lines), encoding="utf-8")
        print(f"\n리포트 저장: {report_path}")


if __name__ == "__main__":
    main()
