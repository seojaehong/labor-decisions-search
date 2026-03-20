"""
판정례 재태깅 JSONL 병합 스크립트 (v2)

여러 draft/reviewed JSONL 파일을 case_id 기준으로 스마트 병합.
- 배열 필드: union merge
- 핵심 필드 충돌: 수동 검토용 collision report 분리
- reviewed > draft 우선

사용법:
    python3 scripts/merge_tagging_outputs.py retagging/output/draft/*.jsonl -o retagging/output/merged/merged_v1.jsonl --report
    python3 scripts/merge_tagging_outputs.py retagging/output/draft/*.jsonl retagging/output/reviewed/*.jsonl -o merged.jsonl
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

# ── 필드 분류 ──

# 핵심 필드 — 충돌 시 자동 병합 금지, collision report로 분리
CRITICAL_FIELDS = {
    "issue_type_primary",
    "employment_stage",
    "disposition_type",
    "industry_context",
}

# union merge 가능한 배열 필드
UNION_MERGE_FIELDS = {
    "issue_type_secondary",
    "fact_markers",
    "legal_focus",
    "exclusion_flags",
    "include_for_queries",
    "exclude_for_queries",
}

# 우선순위 병합 필드 (높은 쪽 우선)
CONFIDENCE_PRIORITY = {"high": 3, "medium": 2, "low": 1}

# review_status 우선순위
STATUS_PRIORITY = {
    "final": 5,
    "approved": 4,
    "reviewed": 3,
    "pending": 2,
    "needs_revision": 1,
}

# notes 권장 조건 체크용
def should_have_notes(record):
    """notes가 있어야 하는 조건 판단."""
    reasons = []
    if record.get("confidence") != "high":
        reasons.append(f"confidence={record.get('confidence')}")
    if record.get("exclusion_flags") and len(record["exclusion_flags"]) >= 2:
        reasons.append(f"exclusion_flags {len(record['exclusion_flags'])}개")
    return reasons


def load_jsonl(file_path):
    """JSONL 파일에서 레코드 로드."""
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


def detect_critical_conflicts(a, b):
    """두 레코드 간 핵심 필드 충돌 감지. 충돌 필드 목록 반환."""
    conflicts = []
    for field in CRITICAL_FIELDS:
        val_a = a.get(field)
        val_b = b.get(field)
        if val_a is None or val_b is None:
            continue
        # 배열 필드는 set 비교, 문자열은 직접 비교
        if isinstance(val_a, list) and isinstance(val_b, list):
            if set(val_a) != set(val_b):
                conflicts.append({
                    "field": field,
                    "value_a": val_a,
                    "value_b": val_b,
                })
        elif val_a != val_b:
            conflicts.append({
                "field": field,
                "value_a": val_a,
                "value_b": val_b,
            })
    return conflicts


def union_merge_record(base, incoming):
    """배열 필드를 union merge하고, 텍스트 필드는 더 긴 쪽 유지."""
    result = dict(base)

    # 배열 필드 union merge
    for field in UNION_MERGE_FIELDS:
        base_vals = set(base.get(field) or [])
        incoming_vals = set(incoming.get(field) or [])
        merged = sorted(base_vals | incoming_vals)
        result[field] = merged

    # confidence: 높은 쪽 유지
    base_conf = CONFIDENCE_PRIORITY.get(base.get("confidence", "low"), 0)
    inc_conf = CONFIDENCE_PRIORITY.get(incoming.get("confidence", "low"), 0)
    if inc_conf > base_conf:
        result["confidence"] = incoming["confidence"]

    # review_status: 높은 쪽 유지
    base_status = STATUS_PRIORITY.get(base.get("review_status", "pending"), 0)
    inc_status = STATUS_PRIORITY.get(incoming.get("review_status", "pending"), 0)
    if inc_status > base_status:
        result["review_status"] = incoming["review_status"]

    # 텍스트 필드: 더 긴 쪽 유지
    for field in ["summary_short", "holding_summary", "retrieval_note", "notes"]:
        base_val = base.get(field) or ""
        inc_val = incoming.get(field) or ""
        if len(inc_val) > len(base_val):
            result[field] = inc_val

    # 소스 추적
    base_sources = base.get("_merge_sources", [base.get("_source_file", "?")])
    result["_merge_sources"] = base_sources + [incoming.get("_source_file", "?")]

    return result


def merge_records(all_records):
    """case_id 기준 스마트 병합."""
    merged = {}
    auto_merged = []      # 자동 병합 성공
    collisions = []       # 핵심 필드 충돌 → 수동 검토
    status_upgrades = []  # review_status 우선순위로 교체

    for record in all_records:
        case_id = record.get("case_id")
        if not case_id:
            collisions.append({
                "case_id": "UNKNOWN",
                "reason": "case_id 없음",
                "source": record.get("_source_file", "?"),
            })
            continue

        if case_id not in merged:
            merged[case_id] = record
            continue

        existing = merged[case_id]

        # review_status 우선순위 차이 → 높은 쪽으로 교체
        new_priority = STATUS_PRIORITY.get(record.get("review_status", "pending"), 0)
        old_priority = STATUS_PRIORITY.get(existing.get("review_status", "pending"), 0)

        if new_priority > old_priority:
            status_upgrades.append({
                "case_id": case_id,
                "old_status": existing.get("review_status"),
                "new_status": record.get("review_status"),
                "old_source": existing.get("_source_file"),
                "new_source": record.get("_source_file"),
            })
            merged[case_id] = record
            continue

        # 동일 우선순위 → 핵심 필드 충돌 검사
        critical = detect_critical_conflicts(existing, record)

        if critical:
            # 핵심 충돌 → collision report로 분리
            collisions.append({
                "case_id": case_id,
                "conflicts": critical,
                "source_a": existing.get("_source_file"),
                "source_b": record.get("_source_file"),
                "record_a": {k: v for k, v in existing.items() if not k.startswith("_")},
                "record_b": {k: v for k, v in record.items() if not k.startswith("_")},
            })
            # 충돌 시 기존 유지 (수동 검토 대상으로만 표시)
        else:
            # 핵심 필드 동일 → 배열 필드 union merge
            merged[case_id] = union_merge_record(existing, record)
            auto_merged.append({
                "case_id": case_id,
                "sources": [existing.get("_source_file"), record.get("_source_file")],
            })

    return merged, auto_merged, collisions, status_upgrades


def write_collision_report(collisions, report_path):
    """충돌 리포트 MD 파일 생성."""
    lines = [
        "# 재태깅 병합 충돌 리포트\n\n",
        f"날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"충돌 건수: {len(collisions)}건\n\n",
        "이 파일의 사건들은 핵심 필드(issue_type_primary, employment_stage, disposition_type, industry_context)에서 ",
        "서로 다른 값이 발견되어 자동 병합되지 않았습니다.\n",
        "수동 검토 후 reviewed 폴더에 확정본을 넣어주세요.\n\n",
        "---\n\n",
    ]

    for i, c in enumerate(collisions, 1):
        case_id = c.get("case_id", "?")
        lines.append(f"## {i}. {case_id}\n\n")
        lines.append(f"소스 A: {c.get('source_a', '?')}\n")
        lines.append(f"소스 B: {c.get('source_b', '?')}\n\n")

        for conflict in c.get("conflicts", []):
            field = conflict["field"]
            val_a = conflict["value_a"]
            val_b = conflict["value_b"]
            lines.append(f"충돌 필드: {field}\n")
            lines.append(f"  A: {json.dumps(val_a, ensure_ascii=False)}\n")
            lines.append(f"  B: {json.dumps(val_b, ensure_ascii=False)}\n\n")

        lines.append("---\n\n")

    report_path.write_text("".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="판정례 재태깅 JSONL 스마트 병합 (v2)")
    parser.add_argument("files", nargs="+", help="병합할 JSONL 파일 경로")
    parser.add_argument("-o", "--output", default="retagging/output/merged/merged_v1.jsonl",
                        help="출력 파일 경로")
    parser.add_argument("--report", action="store_true", help="리포트 파일 저장")
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

    # 스마트 병합
    merged, auto_merged, collisions, status_upgrades = merge_records(all_records)

    # notes 경고 수집
    notes_warnings = []
    for case_id, record in merged.items():
        reasons = should_have_notes(record)
        notes_val = record.get("notes") or ""
        if reasons and notes_val.strip() == "":
            notes_warnings.append({"case_id": case_id, "reasons": reasons})

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

    # ── 콘솔 리포트 ──
    print("=" * 60)
    print("  판정례 재태깅 JSONL 스마트 병합 리포트 (v2)")
    print("=" * 60)

    print(f"\n입력 파일: {len(args.files)}개")
    for name, count in file_counts.items():
        print(f"  {name}: {count}건")

    print(f"\n입력 합계: {len(all_records)}건")
    print(f"병합 결과: {len(merged)}건 (고유 case_id)")
    print(f"  자동 병합 (union merge): {len(auto_merged)}건")
    print(f"  핵심 필드 충돌 (수동 검토 필요): {len(collisions)}건")
    print(f"  status 우선순위 교체: {len(status_upgrades)}건")
    print(f"  notes 권장인데 비어있음: {len(notes_warnings)}건")

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

    if auto_merged:
        print(f"\n{'─' * 60}")
        print(f"자동 병합 상세 ({len(auto_merged)}건):")
        for m in auto_merged[:10]:
            print(f"  {m['case_id']}: {' + '.join(m['sources'])}")
        if len(auto_merged) > 10:
            print(f"  ... 외 {len(auto_merged) - 10}건")

    if collisions:
        print(f"\n{'─' * 60}")
        print(f"핵심 필드 충돌 ({len(collisions)}건) — 수동 검토 필요:")
        for c in collisions:
            fields = [x["field"] for x in c.get("conflicts", [])]
            print(f"  {c['case_id']}: {', '.join(fields)} ({c.get('source_a')} vs {c.get('source_b')})")

    if notes_warnings:
        print(f"\n{'─' * 60}")
        print(f"notes 권장 경고 ({len(notes_warnings)}건):")
        for w in notes_warnings[:10]:
            print(f"  {w['case_id']}: {', '.join(w['reasons'])}")

    # ── 리포트 파일 저장 ──
    if args.report:
        report_dir = Path("retagging/logs")
        report_dir.mkdir(parents=True, exist_ok=True)

        # 메인 리포트
        report_path = report_dir / "merge_report.md"
        lines = [
            f"# 재태깅 JSONL 스마트 병합 리포트 (v2)\n\n",
            f"날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
            f"## 요약\n\n",
            f"| 항목 | 건수 |\n",
            f"|------|------|\n",
            f"| 입력 | {len(all_records)}건 ({len(args.files)}개 파일) |\n",
            f"| 병합 결과 | {len(merged)}건 |\n",
            f"| 자동 병합 (union) | {len(auto_merged)}건 |\n",
            f"| 핵심 충돌 (수동 검토) | {len(collisions)}건 |\n",
            f"| status 교체 | {len(status_upgrades)}건 |\n",
            f"| notes 권장 경고 | {len(notes_warnings)}건 |\n",
            f"| 출력 | {output_path} |\n\n",
        ]
        for title, dist in [("review_status", status_dist), ("confidence", confidence_dist), ("issue_type_primary", primary_dist)]:
            lines.append(f"## {title} 분포\n\n")
            for k, v in dist.most_common():
                lines.append(f"- {k}: {v}\n")
            lines.append("\n")
        report_path.write_text("".join(lines), encoding="utf-8")
        print(f"\n리포트 저장: {report_path}")

        # 충돌 리포트 (별도)
        if collisions:
            collision_path = report_dir / "merge_collisions_report.md"
            write_collision_report(collisions, collision_path)
            print(f"충돌 리포트 저장: {collision_path}")


if __name__ == "__main__":
    main()
