from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from orchestrator_common import LOGS_DIR, ORCH_DIR, REVIEWED_DIR


CLAUDE_TOPICS = {"absence", "violence", "workplace_bullying"}
CLAUDE_DOC = LOGS_DIR / "claude_rear_review.md"
CODEX_DOC = LOGS_DIR / "codex_crosscheck_review.md"
COLLISION_DOC = LOGS_DIR / "predicted_collision_patterns.md"
AGENTS_DOC = ORCH_DIR / "AGENTS_TO_PM.md"


def now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append QA snapshot reports for completed reviewed batches.")
    parser.add_argument("--topics", nargs="+", required=True)
    parser.add_argument("--batch-from", type=int, required=True)
    parser.add_argument("--batch-to", type=int, required=True)
    parser.add_argument("--append-agents-report", action="store_true")
    return parser.parse_args()


def batch_name(topic: str, num: int) -> str:
    return f"{topic}_batch_{num:03d}"


def load_rows(topic: str, num: int) -> list[dict[str, Any]]:
    path = REVIEWED_DIR / f"{batch_name(topic, num)}_reviewed.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            obj["_batch"] = num
            obj["_topic"] = topic
            rows.append(obj)
    return rows


def counter_pct(count: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{count / total * 100:.1f}%"


def top_counter(counter: Counter[str], limit: int = 5) -> list[str]:
    return [f"`{key}` {value}" for key, value in counter.most_common(limit)]


def analyze_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    primary = Counter()
    exclusion = Counter()
    blanks: list[str] = []
    worker_status_cases: list[str] = []
    procedure_cases: list[str] = []
    medium_cases: list[str] = []
    collision_counts = Counter()
    collision_examples: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        case_id = row.get("case_id", "unknown")
        primary_name = row.get("issue_type_primary", "unknown")
        primary[primary_name] += 1

        notes = str(row.get("notes") or "").strip()
        if not notes:
            blanks.append(case_id)

        if row.get("confidence") == "medium":
            medium_cases.append(case_id)

        secondaries = row.get("issue_type_secondary") or []
        if isinstance(secondaries, str):
            secondaries = [secondaries]

        flags = row.get("exclusion_flags") or []
        if isinstance(flags, str):
            flags = [flags]
        exclusion.update(flags)

        disposition = row.get("disposition_type") or []
        if isinstance(disposition, str):
            disposition = [disposition]

        if primary_name == "worker_status":
            worker_status_cases.append(case_id)
            if "dismissal_validity" in secondaries or any(
                item in disposition
                for item in ["dismissal", "disciplinary_dismissal", "rejection_of_regular_employment", "probation_termination"]
            ):
                collision_counts["dismissal_validity_vs_worker_status"] += 1
                if len(collision_examples["dismissal_validity_vs_worker_status"]) < 5:
                    collision_examples["dismissal_validity_vs_worker_status"].append(case_id)

        if primary_name == "procedure":
            procedure_cases.append(case_id)
            if any(item in secondaries for item in ["dismissal_validity", "work_ability"]):
                collision_counts["dismissal_validity_vs_procedure"] += 1
                if len(collision_examples["dismissal_validity_vs_procedure"]) < 5:
                    collision_examples["dismissal_validity_vs_procedure"].append(case_id)

        if primary_name == "dismissal_validity" and "procedure" in secondaries:
            collision_counts["dismissal_validity_vs_procedure"] += 1
            if len(collision_examples["dismissal_validity_vs_procedure"]) < 5:
                collision_examples["dismissal_validity_vs_procedure"].append(case_id)

        if primary_name == "misconduct" and "disciplinary_severity" in secondaries:
            collision_counts["misconduct_vs_disciplinary_severity"] += 1
            if len(collision_examples["misconduct_vs_disciplinary_severity"]) < 5:
                collision_examples["misconduct_vs_disciplinary_severity"].append(case_id)

        if primary_name == "disciplinary_severity" and "misconduct" in secondaries:
            collision_counts["misconduct_vs_disciplinary_severity"] += 1
            if len(collision_examples["misconduct_vs_disciplinary_severity"]) < 5:
                collision_examples["misconduct_vs_disciplinary_severity"].append(case_id)

        mismatch_flags = {
            "not_really_absence_case",
            "not_really_harassment_case",
            "unrelated_to_dismissal",
            "unrelated_to_harassment",
        }
        if any(flag in mismatch_flags for flag in flags):
            collision_counts["topic_legacy_vs_actual_issue"] += 1
            if len(collision_examples["topic_legacy_vs_actual_issue"]) < 5:
                collision_examples["topic_legacy_vs_actual_issue"].append(case_id)

    total = len(rows)
    return {
        "total": total,
        "primary": primary,
        "exclusion": exclusion,
        "blank_notes": blanks,
        "worker_status_cases": worker_status_cases,
        "procedure_cases": procedure_cases,
        "medium_cases": medium_cases,
        "collision_counts": collision_counts,
        "collision_examples": collision_examples,
    }


def classify_doc(topics: list[str]) -> Path:
    if all(topic in CLAUDE_TOPICS for topic in topics):
        return CLAUDE_DOC
    return CODEX_DOC


def build_snapshot_markdown(topics: list[str], batch_from: int, batch_to: int, per_topic: dict[str, dict[str, Any]]) -> str:
    lines = [
        "",
        f"## Incremental QA Snapshot ({now_label()})",
        "",
        f"- 범위: `{', '.join(topics)}` / `batch_{batch_from:03d}~{batch_to:03d}`",
        "- 원칙: 직접 수정 없이 `case_id + 수정 제안 + 근거`만 누적",
        "",
    ]
    for topic in topics:
        data = per_topic.get(topic, {})
        if not data:
            continue
        lines.extend(
            [
                f"### {topic}",
                "",
                f"- 완료 레코드: {data['total']}건",
                f"- `worker_status`: {len(data['worker_status_cases'])}건",
                f"- `procedure`: {len(data['procedure_cases'])}건",
                f"- `confidence=medium`: {len(data['medium_cases'])}건 ({counter_pct(len(data['medium_cases']), data['total'])})",
                f"- `notes` 공란: {len(data['blank_notes'])}건",
                f"- 상위 primary: {', '.join(top_counter(data['primary'])) or '없음'}",
                f"- 상위 exclusion_flags: {', '.join(top_counter(data['exclusion'])) or '없음'}",
                "",
            ]
        )
        findings: list[str] = []
        if data["blank_notes"]:
            sample = ", ".join(f"`{case}`" for case in data["blank_notes"][:5])
            findings.append(f"- `notes` 공란 후보: {sample}")
        if data["worker_status_cases"]:
            sample = ", ".join(f"`{case}`" for case in data["worker_status_cases"][:5])
            findings.append(f"- `worker_status` 재검토 후보: {sample}")
        if data["procedure_cases"]:
            sample = ", ".join(f"`{case}`" for case in data["procedure_cases"][:5])
            findings.append(f"- `procedure` 재검토 후보: {sample}")
        if data["medium_cases"]:
            sample = ", ".join(f"`{case}`" for case in data["medium_cases"][:5])
            findings.append(f"- `medium` 재검토 후보: {sample}")
        if not findings:
            findings.append("- 눈에 띄는 구조 이상 없음")
        lines.extend(findings)
        lines.append("")
    return "\n".join(lines)


def build_collision_markdown(topics: list[str], batch_from: int, batch_to: int, per_topic: dict[str, dict[str, Any]]) -> str:
    totals = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    for data in per_topic.values():
        totals.update(data["collision_counts"])
        for key, values in data["collision_examples"].items():
            for case_id in values:
                if len(examples[key]) < 8 and case_id not in examples[key]:
                    examples[key].append(case_id)

    lines = [
        "",
        f"## Observed QA Snapshot ({now_label()})",
        "",
        f"- 범위: `{', '.join(topics)}` / `batch_{batch_from:03d}~{batch_to:03d}`",
        "",
    ]
    if not totals:
        lines.append("- 관찰된 고빈도 충돌 패턴 없음")
        lines.append("")
        return "\n".join(lines)

    mapping = {
        "misconduct_vs_disciplinary_severity": "`misconduct` vs `disciplinary_severity`",
        "dismissal_validity_vs_procedure": "`dismissal_validity` vs `procedure`",
        "dismissal_validity_vs_worker_status": "`dismissal_validity` vs `worker_status`",
        "topic_legacy_vs_actual_issue": "topic legacy vs 실제 판정축",
    }
    for key in [
        "misconduct_vs_disciplinary_severity",
        "dismissal_validity_vs_procedure",
        "dismissal_validity_vs_worker_status",
        "topic_legacy_vs_actual_issue",
    ]:
        count = totals.get(key, 0)
        if not count:
            continue
        case_sample = ", ".join(f"`{case}`" for case in examples.get(key, []))
        lines.append(f"- {mapping[key]}: {count}건")
        if case_sample:
            lines.append(f"  사례: {case_sample}")
    lines.append("")
    return "\n".join(lines)


def build_agents_markdown(topics: list[str], batch_from: int, batch_to: int, per_topic: dict[str, dict[str, Any]]) -> str:
    total_records = sum(item["total"] for item in per_topic.values())
    total_blank = sum(len(item["blank_notes"]) for item in per_topic.values())
    total_medium = sum(len(item["medium_cases"]) for item in per_topic.values())
    total_worker = sum(len(item["worker_status_cases"]) for item in per_topic.values())
    total_procedure = sum(len(item["procedure_cases"]) for item in per_topic.values())
    return "\n".join(
        [
            "",
            "---",
            "",
            f"## Codex QA Snapshot ({now_label()})",
            "",
            f"- 범위: `{', '.join(topics)}` / `batch_{batch_from:03d}~{batch_to:03d}`",
            f"- reviewed 레코드: {total_records}건",
            f"- `notes` 공란: {total_blank}건",
            f"- `medium`: {total_medium}건",
            f"- `worker_status`: {total_worker}건",
            f"- `procedure`: {total_procedure}건",
            "- 상세는 `logs/claude_rear_review.md` 또는 `logs/codex_crosscheck_review.md`, `logs/predicted_collision_patterns.md` 참조",
            "",
        ]
    )


def append_text(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def main() -> int:
    args = parse_args()
    topics = args.topics
    per_topic: dict[str, dict[str, Any]] = {}
    for topic in topics:
        rows: list[dict[str, Any]] = []
        for batch_num in range(args.batch_from, args.batch_to + 1):
            rows.extend(load_rows(topic, batch_num))
        if rows:
            per_topic[topic] = analyze_rows(rows)

    if not per_topic:
        print("No completed reviewed rows found for the requested range.")
        return 0

    target_doc = classify_doc(topics)
    append_text(target_doc, build_snapshot_markdown(topics, args.batch_from, args.batch_to, per_topic))
    append_text(COLLISION_DOC, build_collision_markdown(topics, args.batch_from, args.batch_to, per_topic))
    if args.append_agents_report:
        append_text(AGENTS_DOC, build_agents_markdown(topics, args.batch_from, args.batch_to, per_topic))

    print(f"Updated {target_doc}")
    print(f"Updated {COLLISION_DOC}")
    if args.append_agents_report:
        print(f"Updated {AGENTS_DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
