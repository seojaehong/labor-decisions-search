from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = REPO_DIR / "evaluation" / "reason_category_refinement"


@dataclass(frozen=True)
class CategoryBucket:
    name: str
    patterns: tuple[str, ...]


MISCONDUCT_BUCKETS: tuple[CategoryBucket, ...] = (
    CategoryBucket("sexual_harassment", (r"성희롱|성추행|성비위|불륜|스토킹|성관계",)),
    CategoryBucket("violence", (r"폭행|상해|욕설|폭언|신체\s*접촉|위협|협박|모욕|쌍방\s*폭행",)),
    CategoryBucket("embezzlement", (r"횡령|배임|유용|법인카드|공금|금품\s*수수",)),
    CategoryBucket("workplace_bullying", (r"직장\s*내\s*괴롭힘|괴롭힘\s*행위|분리조치|괴롭힘\s*조사",)),
    CategoryBucket("transfer", (r"전보|대기발령|직위해제|보직변경",)),
    CategoryBucket("probation", (r"시용|수습|본채용\s*거부",)),
    CategoryBucket("contract_expiry", (r"갱신거절|계약갱신\s*거절|갱신기대권",)),
    CategoryBucket("incompetence", (r"업무능력\s*부족|저성과|PIP|근무성적\s*불량|역량\s*부족",)),
    CategoryBucket("no_dismissal", (r"권고사직|사직서|합의해지|해고가\s*존재하지|해고로\s*볼\s*수\s*없|당연퇴직",)),
    CategoryBucket("worker_status", (r"근로기준법상\s*근로자|사용종속관계|임금을\s*목적으로|근로자성",)),
    CategoryBucket("other_special_misconduct", (r"면허취소|음주운전|도로교통법위반|징계양정|징계절차",)),
)

PROBATION_BUCKETS: tuple[CategoryBucket, ...] = (
    CategoryBucket("contract_expiry", (r"갱신기대권|계약만료|기간만료|갱신거절|재계약\s*거절|계약갱신\s*기대권",)),
    CategoryBucket("no_dismissal", (r"권고사직|사직서|합의해지|해고가\s*존재하지|해고로\s*볼\s*수\s*없|당연퇴직|근로관계\s*종료",)),
    CategoryBucket("dismissal_procedure", (r"서면통지|해고의\s*정당성|해고의\s*절차적\s*정당성|해고사유",)),
    CategoryBucket("probation_pure", (r"시용근로자|수습근로자|본채용\s*거부|수습기간|수습\s*평가|시용\s*평가|계속\s*근로가\s*부적당",)),
    CategoryBucket("worker_status", (r"근로기준법상\s*근로자|사용종속관계|임금을\s*목적으로|근로자성",)),
    CategoryBucket("incompetence", (r"업무능력\s*부족|저성과|PIP|개선\s*기회\s*부여|업무\s*적격성",)),
    CategoryBucket("mixed_review", (r"전보|대기발령|직장\s*내\s*괴롭힘|징계사유",)),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate v6 refinement analysis artifacts from v5 payloads.")
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_OUTPUT_ROOT / "20260402_224157"),
        help="v5 산출물 폴더",
    )
    parser.add_argument("--output-dir", help="출력 폴더")
    return parser.parse_args()


def ensure_output_dir(path_arg: str | None) -> Path:
    if path_arg:
        path = Path(path_arg)
    else:
        path = DEFAULT_OUTPUT_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def text_from_row(row: dict[str, Any]) -> str:
    values = (
        str(row.get("title") or ""),
        str(row.get("evidence_snippet") or ""),
        str(row.get("decision_notes") or ""),
        " ".join(str(hit) for hit in row.get("negative_hits") or []),
        " ".join(str(hit) for hit in row.get("positive_hits") or []),
        " ".join(str(hit) for hit in row.get("positive_context_hits") or []),
    )
    return " ".join(value for value in values if value)


def count_pattern_hits(text: str, patterns: tuple[str, ...]) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))


def confidence_from_stage(stage: str, hit_count: int) -> str:
    if stage == "competitor_category":
        return "high"
    if stage == "negative_hits":
        return "medium" if hit_count >= 1 else "low"
    return "medium" if hit_count >= 2 else "low"


def classify_by_buckets(row: dict[str, Any], buckets: tuple[CategoryBucket, ...]) -> tuple[str, str, list[str], str]:
    competitor = str(row.get("competitor_category") or "")
    negative_hits = [str(hit) for hit in row.get("negative_hits") or []]
    evidence_text = text_from_row(row)

    bucket_names = {bucket.name for bucket in buckets}
    if competitor in bucket_names:
        return competitor, "competitor_category", [competitor], confidence_from_stage("competitor_category", 1)

    negative_matched: list[str] = []
    for bucket in buckets:
        for hit in negative_hits:
            if any(re.search(pattern, hit, re.IGNORECASE) for pattern in bucket.patterns):
                negative_matched.append(bucket.name)
                break
    if negative_matched:
        counts = Counter(negative_matched)
        target, count = counts.most_common(1)[0]
        return target, "negative_hits", list(counts.elements()), confidence_from_stage("negative_hits", count)

    evidence_scores: Counter[str] = Counter()
    for bucket in buckets:
        matched = count_pattern_hits(evidence_text, bucket.patterns)
        if matched:
            evidence_scores[bucket.name] += matched

    if evidence_scores:
        target, count = evidence_scores.most_common(1)[0]
        return target, "evidence", [f"{name}:{score}" for name, score in evidence_scores.items()], confidence_from_stage("evidence", count)

    fallback = "ambiguous"
    if any(bucket.name == "mixed_review" for bucket in buckets):
        fallback = "mixed_review"
    elif any(bucket.name == "other_special_misconduct" for bucket in buckets):
        fallback = "other_special_misconduct"
    return fallback, "evidence", [], "low"


def build_step1_row(row: dict[str, Any]) -> dict[str, Any]:
    target, stage, matched_signals, confidence = classify_by_buckets(row, MISCONDUCT_BUCKETS)
    subtype = str(row.get("subtype") or "")
    if subtype == "dui_termination":
        target = "other_special_misconduct"
        confidence = "high"
    elif subtype == "dui" and target == "other_special_misconduct":
        confidence = "medium"
    return {
        "id": row["id"],
        "title": row["title"],
        "case_number": row["case_number"],
        "decision_result": row["decision_result"],
        "target_bucket": target,
        "confidence": confidence,
        "match_stage": stage,
        "subtype": subtype or "general_misconduct",
        "competitor_category": row.get("competitor_category") or "",
        "negative_hits": row.get("negative_hits") or [],
        "matched_signals": matched_signals,
        "evidence_snippet": row.get("evidence_snippet") or "",
        "score_current": row.get("score_current"),
        "score_competitor": row.get("score_competitor"),
    }


def build_step2_row(row: dict[str, Any]) -> dict[str, Any]:
    target, stage, matched_signals, confidence = classify_by_buckets(row, PROBATION_BUCKETS)
    positive_score = (len(row.get("positive_hits") or []) * 5) + (len(row.get("positive_context_hits") or []) * 2)
    negative_score = len(row.get("negative_hits") or []) * 5
    if target == "probation_pure" and positive_score >= negative_score:
        confidence = "high" if positive_score >= 10 else "medium"
    elif target != "probation_pure" and negative_score > positive_score:
        confidence = "high" if negative_score >= 10 else "medium"
    return {
        "id": row["id"],
        "title": row["title"],
        "case_number": row["case_number"],
        "decision_result": row["decision_result"],
        "segment": target,
        "confidence": confidence,
        "match_stage": stage,
        "competitor_category": row.get("competitor_category") or "",
        "review_sub_bucket": row.get("review_sub_bucket") or "",
        "negative_hits": row.get("negative_hits") or [],
        "positive_hits": row.get("positive_hits") or [],
        "positive_context_hits": row.get("positive_context_hits") or [],
        "matched_signals": matched_signals,
        "evidence_snippet": row.get("evidence_snippet") or "",
        "score_current": row.get("score_current"),
        "score_competitor": row.get("score_competitor"),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines), encoding="utf-8")


def render_step1_markdown(rows: list[dict[str, Any]]) -> list[str]:
    counter = Counter(row["target_bucket"] for row in rows)
    confidence_counter = Counter(row["confidence"] for row in rows)
    lines = [
        "# v6 Step 1: misconduct lean_remove 자동 이관",
        "",
        f"- 대상: {len(rows):,}건",
        f"- 버킷 분포: {dict(counter)}",
        f"- confidence 분포: {dict(confidence_counter)}",
        "",
    ]
    for bucket, count in counter.most_common():
        lines.extend([f"## {bucket}", f"- 건수: {count:,}", ""])
        sample_rows = [row for row in rows if row["target_bucket"] == bucket][:10]
        for row in sample_rows:
            lines.append(
                f"- `{row['case_number']}` {row['title']} | {row['confidence']} | {row['match_stage']} | {row['subtype']} | {row['evidence_snippet']}"
            )
        lines.append("")
    return lines


def render_step2_markdown(rows: list[dict[str, Any]]) -> list[str]:
    counter = Counter(row["segment"] for row in rows)
    confidence_counter = Counter(row["confidence"] for row in rows)
    lines = [
        "# v6 Step 2: probation ambiguous 세분화",
        "",
        f"- 대상: {len(rows):,}건",
        f"- 세그먼트 분포: {dict(counter)}",
        f"- confidence 분포: {dict(confidence_counter)}",
        "",
    ]
    for segment, count in counter.most_common():
        lines.extend([f"## {segment}", f"- 건수: {count:,}", ""])
        sample_rows = [row for row in rows if row["segment"] == segment][:10]
        for row in sample_rows:
            lines.append(
                f"- `{row['case_number']}` {row['title']} | {row['confidence']} | {row['match_stage']} | {row['review_sub_bucket'] or '-'} | {row['evidence_snippet']}"
            )
        lines.append("")
    return lines


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = ensure_output_dir(args.output_dir)

    misconduct_updates = load_jsonl(input_dir / "misconduct_updates_v5.jsonl")
    probation_updates = load_jsonl(input_dir / "probation_updates_v5.jsonl")

    misconduct_target_rows = [
        row for row in misconduct_updates if row.get("outcome") == "needs_review" and row.get("review_sub_bucket") == "lean_remove"
    ]
    probation_target_rows = [
        row for row in probation_updates if row.get("outcome") == "needs_review" and row.get("review_sub_bucket") in {"ambiguous", "lean_remove"}
    ]

    step1_rows = [build_step1_row(row) for row in misconduct_target_rows]
    step2_rows = [build_step2_row(row) for row in probation_target_rows]

    step1_counter = Counter(row["target_bucket"] for row in step1_rows)
    step2_counter = Counter(row["segment"] for row in step2_rows)

    report = {
        "scope": "reason_category_refinement_v6_analysis",
        "input_dir": str(input_dir),
        "db_applied": False,
        "step1": {
            "target": "misconduct lean_remove",
            "total": len(step1_rows),
            "bucket_counts": dict(step1_counter),
            "confidence_counts": dict(Counter(row["confidence"] for row in step1_rows)),
            "match_stage_counts": dict(Counter(row["match_stage"] for row in step1_rows)),
        },
        "step2": {
            "target": "probation ambiguous + lean_remove",
            "total": len(step2_rows),
            "segment_counts": dict(step2_counter),
            "confidence_counts": dict(Counter(row["confidence"] for row in step2_rows)),
            "match_stage_counts": dict(Counter(row["match_stage"] for row in step2_rows)),
        },
    }

    summary_lines = [
        "# reason_category v6 분석 요약",
        "",
        f"- Step 1 misconduct lean_remove 대상: {len(step1_rows):,}건",
        f"- Step 1 버킷 분포: {dict(step1_counter)}",
        f"- Step 2 probation ambiguous+lean_remove 대상: {len(step2_rows):,}건",
        f"- Step 2 세그먼트 분포: {dict(step2_counter)}",
        "",
        "- 이번 산출물은 DB 반영 없이 다음 자동 이관 우선군을 드러내는 목적입니다.",
    ]

    write_json(output_dir / "report.json", report)
    write_markdown(output_dir / "summary.md", summary_lines)
    write_markdown(output_dir / "v6_step1_misconduct_lean_remove_auto_migrate.md", render_step1_markdown(step1_rows))
    write_markdown(output_dir / "v6_step2_probation_ambiguous_segmentation.md", render_step2_markdown(step2_rows))
    write_json(output_dir / "step1_misconduct_lean_remove.json", {"rows": step1_rows})
    write_json(output_dir / "step2_probation_ambiguous.json", {"rows": step2_rows})
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
