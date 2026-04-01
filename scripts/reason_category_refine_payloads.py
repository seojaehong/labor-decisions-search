from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = REPO_DIR / "evaluation" / "reason_category_refinement"
DEFAULT_BATCH_SIZE = 100
DEFAULT_TIMEOUT = 20
PAGE_SIZE = 1000

DEFAULT_TARGET_CATEGORIES: tuple[str, ...] = (
    "worker_status",
    "no_dismissal",
    "incompetence",
    "contract_expiry",
    "probation",
    "transfer",
    "misconduct",
    "violence",
    "embezzlement",
    "workplace_bullying",
    "sexual_harassment",
    "union_activity",
    "discrimination",
    "redundancy",
)

LABOR_POSITIVE_PATTERNS: tuple[str, ...] = (
    "부당해고",
    "부당징계",
    "구제신청",
    "지방노동위원회",
    "중앙노동위원회",
    "노동위원회",
    "노동조합",
    "부당노동행위",
    "차별시정",
    "갱신기대권",
    "본채용",
    "수습",
    "시용",
    "전보",
    "대기발령",
    "근로자",
    "근로관계",
    "징계",
    "해고",
)

NON_LABOR_NEGATIVE_PATTERNS: tuple[str, ...] = (
    "고단",
    "도단",
    "형사",
    "피고인",
    "공소사실",
    "도로교통법",
    "음주운전",
    "교통사고",
    "절도",
    "사기",
    "마약",
    "살인",
    "상해죄",
    "폭행치사",
    "공갈",
    "강도",
    "주거침입",
)


def make_patterns(values: tuple[str, ...]) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(value, re.IGNORECASE) for value in values)


@dataclass(frozen=True)
class CategoryRule:
    positive: tuple[str, ...]
    negative: tuple[str, ...]
    review: tuple[str, ...] = ()


CATEGORY_RULES: dict[str, CategoryRule] = {
    "worker_status": CategoryRule(
        positive=(
            r"근로자성",
            r"근로자에\s*해당",
            r"근로기준법상\s*근로자",
            r"당사자적격",
            r"종속적\s*관계",
            r"종속관계",
            r"사용종속관계",
            r"계약의\s*형식",
            r"도급계약인지",
            r"고용계약인지",
            r"실질에\s*있어",
            r"임금을\s*목적으로",
            r"지휘\s*감독",
            r"출퇴근",
            r"사업소득세",
            r"4대보험",
            r"독자적\s*사업",
            r"업무수행\s*과정",
        ),
        negative=(
            r"양정이\s*(과도|과중|과하여)",
            r"감봉",
            r"정직",
            r"대기발령",
            r"전보",
            r"인사발령",
            r"직장\s*내\s*괴롭힘",
            r"성희롱",
        ),
        review=(
            r"상시근로자\s*수",
            r"5인\s*미만",
            r"사용자에\s*해당",
        ),
    ),
    "no_dismissal": CategoryRule(
        positive=(
            r"해고가\s*존재하지",
            r"해고부존재",
            r"권고사직",
            r"사직서",
            r"자발적\s*사직",
            r"합의\s*퇴직",
            r"합의해지",
            r"해고로\s*볼\s*수\s*없",
            r"당연퇴직",
            r"사직의\s*의사",
            r"근로관계\s*종료",
        ),
        negative=(
            r"부당해고에\s*해당",
            r"실질적인\s*해고",
            r"해고의\s*절차적\s*정당성",
            r"해고의\s*정당성",
            r"본채용\s*거부",
            r"갱신거절",
        ),
        review=(
            r"권고사직임을\s*입증",
            r"카카오톡\s*메시지",
            r"사직서를\s*작성",
        ),
    ),
    "incompetence": CategoryRule(
        positive=(
            r"업무능력\s*부족",
            r"저성과",
            r"근무성적\s*불량",
            r"부적격",
            r"실적\s*최하위",
            r"개선\s*기회",
            r"개선기회",
            r"경고",
            r"시정",
            r"교육",
            r"본채용\s*거부",
            r"능력\s*부족",
            r"업무수행\s*능력",
        ),
        negative=(
            r"음주운전",
            r"절도",
            r"폭행",
            r"횡령",
            r"배임",
            r"직장\s*내\s*괴롭힘",
            r"성희롱",
        ),
        review=(
            r"건강상\s*이유",
            r"적격성",
            r"배치전환",
        ),
    ),
    "contract_expiry": CategoryRule(
        positive=(
            r"갱신기대권",
            r"계약만료",
            r"기간제",
            r"계약\s*갱신",
            r"재계약",
            r"근로계약\s*기간",
            r"갱신거절",
        ),
        negative=(
            r"권고사직",
            r"합의해지",
            r"해고가\s*존재하지",
            r"양정이\s*(과도|과중|과하여)",
        ),
        review=(r"무기계약직\s*전환",),
    ),
    "probation": CategoryRule(
        positive=(
            r"수습",
            r"시용",
            r"본채용\s*거부",
            r"수습기간",
            r"수습\s*평가",
            r"시용근로자",
        ),
        negative=(
            r"갱신기대권",
            r"계약만료",
            r"전보",
            r"직장\s*내\s*괴롭힘",
        ),
    ),
    "transfer": CategoryRule(
        positive=(
            r"전보",
            r"인사발령",
            r"배치전환",
            r"대기발령",
            r"전직명령",
            r"보직\s*변경",
        ),
        negative=(
            r"근로자성",
            r"근로기준법상\s*근로자",
            r"업무능력\s*부족",
            r"갱신기대권",
        ),
    ),
    "misconduct": CategoryRule(
        positive=(
            r"비위행위",
            r"복무규정\s*위반",
            r"복종의무\s*위반",
            r"업무\s*지시\s*불이행",
            r"허위\s*보고",
            r"겸직",
            r"징계사유",
        ),
        negative=(
            r"음주운전",
            r"절도",
            r"사기",
            r"폭행",
            r"성희롱",
        ),
    ),
    "violence": CategoryRule(
        positive=(
            r"폭행",
            r"폭언",
            r"욕설",
            r"협박",
            r"모욕",
            r"가혹행위",
        ),
        negative=(r"직장\s*내\s*괴롭힘", r"성희롱"),
    ),
    "embezzlement": CategoryRule(
        positive=(
            r"횡령",
            r"배임",
            r"공금\s*유용",
            r"착복",
            r"부정\s*수령",
            r"금전\s*비위",
        ),
        negative=(r"음주운전", r"폭행"),
    ),
    "workplace_bullying": CategoryRule(
        positive=(
            r"직장\s*내\s*괴롭힘",
            r"괴롭힘",
            r"괴롭힘\s*행위",
            r"따돌림",
            r"신고\s*후",
            r"분리조치",
            r"접촉금지",
        ),
        negative=(r"성희롱",),
        review=(r"괴롭힘\s*불인정", r"괴롭힘\s*미해당"),
    ),
    "sexual_harassment": CategoryRule(
        positive=(r"성희롱", r"성추행", r"성적\s*언동", r"성폭력"),
        negative=(r"직장\s*내\s*괴롭힘",),
    ),
    "union_activity": CategoryRule(
        positive=(
            r"부당노동행위",
            r"노동조합",
            r"지배개입",
            r"불이익취급",
            r"조합활동",
            r"단체교섭",
            r"단체협약",
        ),
        negative=(r"근로자성",),
    ),
    "discrimination": CategoryRule(
        positive=(r"차별시정", r"차별적\s*처우", r"비교\s*대상\s*근로자", r"동일가치노동", r"남녀고용평등"),
        negative=(r"부당노동행위",),
    ),
    "redundancy": CategoryRule(
        positive=(r"경영상\s*해고", r"정리해고", r"구조조정", r"경영\s*악화", r"인원\s*감축", r"사업\s*폐지"),
        negative=(r"근로자성", r"직장\s*내\s*괴롭힘"),
    ),
}


@dataclass(frozen=True)
class DecisionRow:
    id: str
    title: str
    case_number: str
    department: str
    decision_date: str
    decision_result: str
    key_issue: str
    holding_summary: str
    holding_points: str
    reason_category: list[str]


@dataclass(frozen=True)
class EvaluationResult:
    outcome: str
    removal_basis: str
    domain_bucket: str
    review_priority: str
    positive_hits: list[str]
    negative_hits: list[str]
    domain_hits: list[str]
    evidence_snippet: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate v2 reviewable payloads for reason_category refinement without mutating DB by default"
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=list(DEFAULT_TARGET_CATEGORIES),
        help="대상 reason_category 목록",
    )
    parser.add_argument("--apply-db", action="store_true", help="생성된 keep/remove payload를 실제 DB에 반영")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--output-dir")
    parser.add_argument("--limit-per-reason", type=int, default=0)
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() not in os.environ:
                os.environ[name.strip()] = value.strip()


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} must be set")
    return value


def build_headers() -> dict[str, str]:
    service_key = require_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }


def ensure_output_dir(path_arg: str | None) -> Path:
    if path_arg:
        output_dir = Path(path_arg)
    else:
        output_dir = DEFAULT_OUTPUT_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def fetch_reason_rows(reason: str, timeout: int, limit_per_reason: int) -> list[DecisionRow]:
    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    rows: list[DecisionRow] = []
    offset = 0

    while True:
        current_limit = PAGE_SIZE
        if limit_per_reason > 0:
            current_limit = min(PAGE_SIZE, max(limit_per_reason - len(rows), 0))
        if current_limit <= 0:
            break

        params = {
            "select": "id,title,case_number,department,decision_date,decision_result,key_issue,holding_summary,holding_points,reason_category",
            "reason_category": f"cs.{{{reason}}}",
            "order": "decision_date.desc.nullslast,id.asc",
            "limit": str(current_limit),
            "offset": str(offset),
        }
        response = requests.get(
            f"{supabase_url}/rest/v1/nlrc_decisions",
            headers=headers,
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        chunk = response.json()
        if not chunk:
            break

        for row in chunk:
            rows.append(
                DecisionRow(
                    id=str(row.get("id") or ""),
                    title=str(row.get("title") or ""),
                    case_number=str(row.get("case_number") or ""),
                    department=str(row.get("department") or ""),
                    decision_date=str(row.get("decision_date") or ""),
                    decision_result=str(row.get("decision_result") or ""),
                    key_issue=str(row.get("key_issue") or ""),
                    holding_summary=str(row.get("holding_summary") or ""),
                    holding_points=str(row.get("holding_points") or ""),
                    reason_category=list(row.get("reason_category") or []),
                )
            )

        if len(chunk) < current_limit or (limit_per_reason > 0 and len(rows) >= limit_per_reason):
            break
        offset += len(chunk)

    return rows


def build_text(row: DecisionRow) -> str:
    return " ".join(
        value for value in (row.title, row.key_issue, row.holding_summary, row.holding_points, row.case_number, row.department) if value
    )


def find_hits(text: str, patterns: tuple[str, ...]) -> list[str]:
    hits: list[str] = []
    for pattern in make_patterns(patterns):
        if pattern.search(text):
            hits.append(pattern.pattern)
    return hits


def infer_domain_bucket(text: str, positive_hits: list[str]) -> tuple[str, list[str]]:
    domain_hits = find_hits(text, LABOR_POSITIVE_PATTERNS)
    non_labor_hits = find_hits(text, NON_LABOR_NEGATIVE_PATTERNS)
    if non_labor_hits and not domain_hits and not positive_hits:
        return "non_labor_case", non_labor_hits
    if domain_hits or positive_hits:
        return "labor_case", domain_hits
    return "needs_review", non_labor_hits


def build_evidence_snippet(row: DecisionRow, matched_tokens: list[str]) -> str:
    source = row.holding_summary or row.key_issue or row.holding_points or row.title
    if not source:
        return ""
    snippet = source.replace("\n", " ").strip()
    if not matched_tokens:
        return snippet[:240]
    lowered = snippet.lower()
    positions = [lowered.find(token.lower().replace("\\s*", " ")) for token in matched_tokens]
    positions = [position for position in positions if position >= 0]
    if not positions:
        return snippet[:240]
    start = max(min(positions) - 40, 0)
    end = min(start + 240, len(snippet))
    return snippet[start:end].strip()


def next_reason_category(row: DecisionRow, removed_reason: str) -> list[str]:
    remaining = [reason for reason in row.reason_category if reason != removed_reason]
    return remaining or ["other"]


def evaluate_row(row: DecisionRow, reason: str) -> EvaluationResult:
    rule = CATEGORY_RULES[reason]
    text = build_text(row)
    positive_hits = find_hits(text, rule.positive)
    negative_hits = find_hits(text, rule.negative)
    review_hits = find_hits(text, rule.review)
    domain_bucket, domain_hits = infer_domain_bucket(text, positive_hits)

    if domain_bucket == "non_labor_case":
        return EvaluationResult(
            outcome="remove",
            removal_basis="non_labor_domain",
            domain_bucket=domain_bucket,
            review_priority="high",
            positive_hits=positive_hits,
            negative_hits=negative_hits,
            domain_hits=domain_hits,
            evidence_snippet=build_evidence_snippet(row, positive_hits or negative_hits or domain_hits),
        )

    if positive_hits and not negative_hits:
        return EvaluationResult(
            outcome="keep",
            removal_basis="",
            domain_bucket=domain_bucket,
            review_priority="low",
            positive_hits=positive_hits,
            negative_hits=negative_hits,
            domain_hits=domain_hits,
            evidence_snippet=build_evidence_snippet(row, positive_hits),
        )

    if positive_hits and negative_hits:
        return EvaluationResult(
            outcome="needs_review",
            removal_basis="needs_review",
            domain_bucket="needs_review",
            review_priority="high",
            positive_hits=positive_hits,
            negative_hits=negative_hits,
            domain_hits=domain_hits,
            evidence_snippet=build_evidence_snippet(row, positive_hits + negative_hits),
        )

    if review_hits:
        return EvaluationResult(
            outcome="needs_review",
            removal_basis="needs_review",
            domain_bucket="needs_review",
            review_priority="medium",
            positive_hits=positive_hits,
            negative_hits=review_hits,
            domain_hits=domain_hits,
            evidence_snippet=build_evidence_snippet(row, review_hits),
        )

    if not positive_hits and negative_hits:
        return EvaluationResult(
            outcome="remove",
            removal_basis="label_mismatch",
            domain_bucket=domain_bucket,
            review_priority="medium",
            positive_hits=positive_hits,
            negative_hits=negative_hits,
            domain_hits=domain_hits,
            evidence_snippet=build_evidence_snippet(row, negative_hits),
        )

    if not positive_hits:
        priority = "medium" if domain_bucket == "labor_case" else "high"
        basis = "guard_miss" if domain_bucket == "labor_case" else "needs_review"
        outcome = "remove" if domain_bucket == "labor_case" else "needs_review"
        return EvaluationResult(
            outcome=outcome,
            removal_basis=basis,
            domain_bucket=domain_bucket,
            review_priority=priority,
            positive_hits=[],
            negative_hits=[],
            domain_hits=domain_hits,
            evidence_snippet=build_evidence_snippet(row, domain_hits),
        )

    return EvaluationResult(
        outcome="needs_review",
        removal_basis="needs_review",
        domain_bucket="needs_review",
        review_priority="medium",
        positive_hits=positive_hits,
        negative_hits=negative_hits,
        domain_hits=domain_hits,
        evidence_snippet=build_evidence_snippet(row, positive_hits),
    )


def summarize_row(row: DecisionRow, evaluation: EvaluationResult, reason: str) -> dict[str, Any]:
    return {
        "id": row.id,
        "title": row.title,
        "case_number": row.case_number,
        "department": row.department,
        "decision_date": row.decision_date,
        "decision_result": row.decision_result,
        "current_reason_category": row.reason_category,
        "target_reason": reason,
        "outcome": evaluation.outcome,
        "removal_basis": evaluation.removal_basis,
        "domain_bucket": evaluation.domain_bucket,
        "review_priority": evaluation.review_priority,
        "positive_hits": evaluation.positive_hits,
        "negative_hits": evaluation.negative_hits,
        "domain_hits": evaluation.domain_hits,
        "evidence_snippet": evaluation.evidence_snippet,
    }


def build_update_payload(row: DecisionRow, reason: str, evaluation: EvaluationResult) -> dict[str, Any]:
    proposed = next_reason_category(row, reason) if evaluation.outcome == "remove" else row.reason_category
    return {
        "id": row.id,
        "current_reason_category": row.reason_category,
        "proposed_reason_category": proposed,
        "removed_reason": reason if evaluation.outcome == "remove" else "",
        "outcome": evaluation.outcome,
        "removal_basis": evaluation.removal_basis,
        "domain_bucket": evaluation.domain_bucket,
        "review_priority": evaluation.review_priority,
        "positive_hits": evaluation.positive_hits,
        "negative_hits": evaluation.negative_hits,
        "domain_hits": evaluation.domain_hits,
        "evidence_snippet": evaluation.evidence_snippet,
        "title": row.title,
        "case_number": row.case_number,
        "department": row.department,
        "decision_date": row.decision_date,
        "decision_result": row.decision_result,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def apply_updates(updates: list[dict[str, Any]], timeout: int, batch_size: int) -> int:
    actionable = [row for row in updates if row["outcome"] == "remove"]
    if not actionable:
        return 0

    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()
    updated = 0

    for start in range(0, len(actionable), batch_size):
        batch = actionable[start:start + batch_size]
        for update in batch:
            response = requests.patch(
                f"{supabase_url}/rest/v1/nlrc_decisions?id=eq.{update['id']}",
                headers=headers,
                json={"reason_category": update["proposed_reason_category"]},
                timeout=timeout,
            )
            if response.status_code not in (200, 204):
                raise RuntimeError(
                    f"update failed for {update['id']}: {response.status_code} {response.text[:400]}"
                )
            updated += 1
        time.sleep(0.1)

    return updated


def write_samples_markdown(path: Path, reason: str, kept: list[dict[str, Any]], removed: list[dict[str, Any]], review: list[dict[str, Any]]) -> None:
    lines = [f"# {reason} 샘플", ""]
    sections = (
        ("유지", kept[:50]),
        ("제거", removed[:50]),
        ("검토필요", review[:20]),
    )
    for title, rows in sections:
        lines.extend([f"## {title}", ""])
        for row in rows:
            lines.append(
                f"- `{row['case_number']}` {row['title']} | {row['decision_result']} | "
                f"{row['removal_basis'] or 'keep'} | {row['domain_bucket']} | {row['evidence_snippet']}"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    load_env_file()
    args = parse_args()
    output_dir = ensure_output_dir(args.output_dir)

    markdown_lines = [
        "# reason_category 정교화 payload v2",
        "",
        "이번 산출물은 `positive + negative + domain gate` 기준으로 생성한 검토용 payload v2입니다.",
        "",
    ]

    overall_counter: Counter[str] = Counter()
    report_rows: list[dict[str, Any]] = []
    all_updates: list[dict[str, Any]] = []

    for reason in args.categories:
        if reason not in CATEGORY_RULES:
            raise RuntimeError(f"unsupported category: {reason}")

        rows = fetch_reason_rows(reason=reason, timeout=args.timeout, limit_per_reason=args.limit_per_reason)
        kept: list[dict[str, Any]] = []
        removed: list[dict[str, Any]] = []
        review: list[dict[str, Any]] = []
        updates: list[dict[str, Any]] = []
        removal_basis_counter: Counter[str] = Counter()
        negative_signal_counter: Counter[str] = Counter()

        granted_before = sum(1 for row in rows if row.decision_result == "granted")
        granted_after = 0

        for row in rows:
            evaluation = evaluate_row(row, reason)
            payload = build_update_payload(row, reason, evaluation)
            updates.append(payload)
            all_updates.append(payload)
            if evaluation.outcome == "keep":
                kept.append(summarize_row(row, evaluation, reason))
                if row.decision_result == "granted":
                    granted_after += 1
            elif evaluation.outcome == "remove":
                removed.append(summarize_row(row, evaluation, reason))
                removal_basis_counter[evaluation.removal_basis] += 1
            else:
                review.append(summarize_row(row, evaluation, reason))
                removal_basis_counter[evaluation.removal_basis] += 1
            for hit in evaluation.negative_hits:
                negative_signal_counter[hit] += 1

        overall_counter["total"] += len(rows)
        overall_counter["kept"] += len(kept)
        overall_counter["removed"] += len(removed)
        overall_counter["needs_review"] += len(review)
        overall_counter["granted_before"] += granted_before
        overall_counter["granted_after"] += granted_after

        detail = {
            "reason": reason,
            "definition": {
                "positive": list(CATEGORY_RULES[reason].positive),
                "negative": list(CATEGORY_RULES[reason].negative),
                "review": list(CATEGORY_RULES[reason].review),
            },
            "total": len(rows),
            "kept": len(kept),
            "removed": len(removed),
            "needs_review": len(review),
            "kept_ratio": round((len(kept) / len(rows)) if rows else 0.0, 4),
            "granted_before": granted_before,
            "granted_after": granted_after,
            "removal_basis_counts": dict(removal_basis_counter),
            "negative_signal_counts": dict(negative_signal_counter.most_common(20)),
            "kept_examples": kept[:15],
            "removed_examples": removed[:15],
            "review_examples": review[:15],
        }
        (output_dir / f"{reason}_detail_v2.json").write_text(
            json.dumps(detail, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        write_jsonl(output_dir / f"{reason}_updates_v2.jsonl", updates)
        write_samples_markdown(output_dir / f"{reason}_samples.md", reason, kept, removed, review)

        report_rows.append(
            {
                "reason": reason,
                "total": len(rows),
                "kept": len(kept),
                "removed": len(removed),
                "needs_review": len(review),
                "kept_ratio": round((len(kept) / len(rows)) if rows else 0.0, 4),
                "granted_before": granted_before,
                "granted_after": granted_after,
                "remove_candidates": len(removed),
                "review_candidates": len(review),
                "removal_basis_counts": dict(removal_basis_counter),
            }
        )

        markdown_lines.extend(
            [
                f"## {reason}",
                f"- 전체: {len(rows):,}",
                f"- 유지: {len(kept):,}",
                f"- 제거 후보: {len(removed):,}",
                f"- 검토 필요: {len(review):,}",
                f"- 인정(구제) 전/후: {granted_before:,} -> {granted_after:,}",
                f"- payload: `{reason}_updates_v2.jsonl`",
                f"- samples: `{reason}_samples.md`",
                "",
            ]
        )

    write_jsonl(output_dir / "all_updates_v2.jsonl", all_updates)

    applied_count = 0
    if args.apply_db:
        applied_count = apply_updates(all_updates, timeout=args.timeout, batch_size=args.batch_size)

    report = {
        "scope": "reason_category_refinement_payloads_v2",
        "categories": args.categories,
        "total_rows": overall_counter["total"],
        "kept_rows": overall_counter["kept"],
        "removed_rows": overall_counter["removed"],
        "needs_review_rows": overall_counter["needs_review"],
        "granted_before": overall_counter["granted_before"],
        "granted_after": overall_counter["granted_after"],
        "update_candidates": overall_counter["removed"],
        "review_candidates": overall_counter["needs_review"],
        "db_applied": bool(args.apply_db),
        "db_applied_count": applied_count,
        "rows": report_rows,
    }

    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "summary.md").write_text("\n".join(markdown_lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
