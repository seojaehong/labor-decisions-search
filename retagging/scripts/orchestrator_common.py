from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROOT_ALIAS = "/mnt/c/dev/labor-decisions-search/retagging"
INPUT_DIR = ROOT / "input" / "batches"
REVIEWED_DIR = ROOT / "output" / "reviewed"
MERGED_DIR = ROOT / "output" / "merged"
LOGS_DIR = ROOT / "logs"
ORCH_DIR = LOGS_DIR / "orchestrator"
RUNS_DIR = ORCH_DIR / "runs"
PROMPTS_DIR = ORCH_DIR / "prompts"
STATE_PATH = ORCH_DIR / "state.json"
STATUS_JSON_PATH = ORCH_DIR / "status.json"

VALIDATE_SCRIPT = ROOT.parent / "scripts" / "validate_tagging_jsonl.py"
MERGE_SCRIPT = ROOT.parent / "scripts" / "merge_tagging_outputs.py"

PRIORITY_CATEGORIES = [
    "probation",
    "incompetence",
    "absence",
    "violence",
    "workplace_bullying",
]


def ensure_dirs() -> None:
    for path in [REVIEWED_DIR, MERGED_DIR, LOGS_DIR, ORCH_DIR, RUNS_DIR, PROMPTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def relpath(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def run_command(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd or ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def run_python_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run_command([sys.executable, str(script), *args], cwd=ROOT.parent)


def count_jsonl_records(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1
    return count


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_state() -> dict[str, Any]:
    ensure_dirs()
    state = load_json(STATE_PATH, {})
    if not isinstance(state, dict):
        state = {}
    state.setdefault("batches", {})
    state.setdefault("runs", [])
    state.setdefault("updated_at", now_iso())
    return state


def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    save_json(STATE_PATH, state)


def record_run_event(state: dict[str, Any], event: dict[str, Any]) -> None:
    state.setdefault("runs", []).append(event)
    state["runs"] = state["runs"][-400:]


@dataclass
class BatchPaths:
    batch_name: str
    category: str
    batch_number: int
    input_path: Path
    reviewed_path: Path
    self_review_path: Path


@dataclass
class BatchScan:
    batch_name: str
    category: str
    batch_number: int
    input_exists: bool
    reviewed_exists: bool
    self_review_exists: bool
    completed: bool
    state_status: str
    state_attempts: int
    state_last_error: str
    state_last_exit_code: int | None
    state_updated_at: str
    queue_status: str


def batch_paths(category: str, batch_number: int) -> BatchPaths:
    batch_name = f"{category}_batch_{batch_number:03d}"
    return BatchPaths(
        batch_name=batch_name,
        category=category,
        batch_number=batch_number,
        input_path=INPUT_DIR / f"{batch_name}.jsonl",
        reviewed_path=REVIEWED_DIR / f"{batch_name}_reviewed.jsonl",
        self_review_path=LOGS_DIR / f"{batch_name}_self_review.md",
    )


def basic_jsonl_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                if not isinstance(data, dict):
                    return False
        return True
    except Exception:
        return False


def completion_ok(paths: BatchPaths) -> bool:
    return (
        paths.reviewed_path.exists()
        and paths.self_review_path.exists()
        and basic_jsonl_ok(paths.reviewed_path)
    )


def queue_status_for(paths: BatchPaths, batch_state: dict[str, Any]) -> str:
    if completion_ok(paths):
        return "completed"
    raw = batch_state.get("status", "")
    if not paths.input_path.exists():
        return "missing_input"
    if raw in {"running", "queued"}:
        return "in_progress"
    if raw == "needs_operator":
        return "needs_operator"
    if raw == "waiting_manual_review":
        return "waiting_manual_review"
    if raw == "failed":
        return "failed"
    return "pending"


def scan_batches(
    state: dict[str, Any] | None = None,
    categories: list[str] | None = None,
    max_batch: int = 100,
) -> list[BatchScan]:
    state = state or load_state()
    categories = categories or PRIORITY_CATEGORIES
    results: list[BatchScan] = []
    for category in categories:
        for batch_number in range(1, max_batch + 1):
            paths = batch_paths(category, batch_number)
            batch_state = state.get("batches", {}).get(paths.batch_name, {})
            results.append(
                BatchScan(
                    batch_name=paths.batch_name,
                    category=category,
                    batch_number=batch_number,
                    input_exists=paths.input_path.exists(),
                    reviewed_exists=paths.reviewed_path.exists(),
                    self_review_exists=paths.self_review_path.exists(),
                    completed=completion_ok(paths),
                    state_status=batch_state.get("status", ""),
                    state_attempts=int(batch_state.get("attempts", 0) or 0),
                    state_last_error=batch_state.get("last_error", ""),
                    state_last_exit_code=batch_state.get("last_exit_code"),
                    state_updated_at=batch_state.get("updated_at", ""),
                    queue_status=queue_status_for(paths, batch_state),
                )
            )
    return results


def summarize_batches(scans: list[BatchScan], categories: list[str]) -> dict[str, Any]:
    category_stats: dict[str, dict[str, int]] = {}
    overall = {
        "total_slots": 0,
        "with_input": 0,
        "completed": 0,
        "in_progress": 0,
        "pending": 0,
        "missing_input": 0,
        "failed": 0,
        "needs_operator": 0,
        "waiting_manual_review": 0,
    }
    for category in categories:
        category_stats[category] = {
            "total_slots": 0,
            "with_input": 0,
            "completed": 0,
            "in_progress": 0,
            "pending": 0,
            "missing_input": 0,
            "failed": 0,
            "needs_operator": 0,
            "waiting_manual_review": 0,
        }
    for scan in scans:
        stats = category_stats[scan.category]
        stats["total_slots"] += 1
        overall["total_slots"] += 1
        if scan.input_exists:
            stats["with_input"] += 1
            overall["with_input"] += 1
        stats[scan.queue_status] += 1
        overall[scan.queue_status] += 1
    return {"overall": overall, "categories": category_stats}


def set_batch_state(
    state: dict[str, Any],
    batch_name: str,
    status: str,
    **extra: Any,
) -> None:
    entry = state.setdefault("batches", {}).setdefault(batch_name, {})
    entry["status"] = status
    entry["updated_at"] = now_iso()
    for key, value in extra.items():
        entry[key] = value


def read_collision_count() -> int:
    report_path = LOGS_DIR / "merge_collisions_report.md"
    if not report_path.exists():
        return 0
    text = report_path.read_text(encoding="utf-8")
    match = re.search(r"충돌 건수:\s*(\d+)건", text)
    return int(match.group(1)) if match else 0


def build_current_status_text(scans: list[BatchScan], summary: dict[str, Any]) -> str:
    overall = summary["overall"]
    if overall["waiting_manual_review"] or overall["needs_operator"]:
        status = "판정필요"
    elif overall["in_progress"]:
        status = "작업중"
    elif overall["pending"]:
        status = "대기"
    elif overall["missing_input"] == overall["total_slots"]:
        status = "외부입력필요"
    else:
        status = "대기"

    lines = [
        "# current_status",
        "",
        f"상태: {status}",
        "",
        "## 지금 내가 하고 있는 것",
        f"- 작업 루트 `{ROOT_ALIAS}` 기준으로 batch 오케스트레이션 상태를 추적 중",
        "- 완료 기준은 reviewed JSONL + self-review 메모 동시 존재",
        "- merge / override / progress report는 기존 v1 산출물을 존중하는 증분 방식으로 갱신",
        "",
        "## 현재 단계",
        f"- 누적 reviewed 완료: {overall['completed']}개 batch",
        f"- 실행 중: {overall['in_progress']}개 batch",
        f"- 대기 중: {overall['pending']}개 batch",
        f"- 입력 미도착: {overall['missing_input']}개 slot",
        f"- 수동 개입 필요: {overall['needs_operator'] + overall['waiting_manual_review']}개 batch",
        "",
        "## 주제군별 진행",
    ]
    for category, stats in summary["categories"].items():
        denominator = stats["with_input"] or 0
        ratio = (stats["completed"] / denominator * 100) if denominator else 0.0
        lines.append(
            f"- {category}: 완료 {stats['completed']} / 입력존재 {stats['with_input']} / 실행중 {stats['in_progress']} / 진행률 {ratio:.1f}%"
        )
    lines.extend(
        [
            "",
            "## 내가 자동으로 보는 것",
            "- `input/batches/*.jsonl`",
            "- `output/reviewed/*_reviewed.jsonl`",
            "- `logs/*_self_review.md`",
            "- `logs/merge_collisions_report.md`",
            "- `output/reviewed/manual_merge_overrides_v1.json`",
            "- `logs/bulk_progress_report.md`",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def build_progress_report_text(scans: list[BatchScan], summary: dict[str, Any]) -> str:
    overall = summary["overall"]
    lines = [
        "# Bulk Retagging 진행 현황",
        "",
        f"최종 갱신: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 전체 요약",
        "",
        "| 항목 | 값 |",
        "|------|-----|",
        f"| batch slot(001~100 x 5) | {overall['total_slots']} |",
        f"| 입력 존재 batch | {overall['with_input']} |",
        f"| 완료 batch | {overall['completed']} |",
        f"| 실행 중 batch | {overall['in_progress']} |",
        f"| 대기 batch | {overall['pending']} |",
        f"| 입력 미도착 slot | {overall['missing_input']} |",
        f"| 수동 개입 필요 | {overall['needs_operator'] + overall['waiting_manual_review']} |",
        f"| 실패 batch | {overall['failed']} |",
        f"| merge collision | {read_collision_count()} |",
        "",
        "## 주제군별 진행",
        "",
        "| 주제군 | 입력 존재 | 완료 | 실행중 | 대기 | 수동개입 | 진행률 |",
        "|--------|-----------|------|--------|------|----------|--------|",
    ]
    for category, stats in summary["categories"].items():
        denominator = stats["with_input"] or 0
        ratio = (stats["completed"] / denominator * 100) if denominator else 0.0
        lines.append(
            f"| {category} | {stats['with_input']} | {stats['completed']} | {stats['in_progress']} | {stats['pending']} | {stats['needs_operator'] + stats['waiting_manual_review']} | {ratio:.1f}% |"
        )
    return "\n".join(lines) + "\n"


def build_dashboard_payload(scans: list[BatchScan], summary: dict[str, Any]) -> dict[str, Any]:
    overall = summary["overall"]
    recent_completed = sorted(
        [scan.batch_name for scan in scans if scan.completed],
        reverse=True,
    )[:14]
    return {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "판정필요"
        if overall["waiting_manual_review"] or overall["needs_operator"]
        else ("작업중" if overall["in_progress"] else "대기"),
        "root": ROOT_ALIAS,
        "completed_batches": overall["completed"],
        "running_batches": overall["in_progress"],
        "pending_batches": overall["pending"],
        "missing_input_batches": overall["missing_input"],
        "failed_batches": overall["failed"],
        "manual_attention_batches": overall["needs_operator"] + overall["waiting_manual_review"],
        "collision_count": read_collision_count(),
        "recent_completed_batches": recent_completed,
        "categories": summary["categories"],
    }


def build_dashboard_html(payload: dict[str, Any]) -> str:
    pills = "".join(
        f'<span class="pill">{name}</span>' for name in payload["recent_completed_batches"]
    ) or '<span class="pill">없음</span>'
    rows = []
    for category, stats in payload["categories"].items():
        denominator = stats["with_input"] or 0
        ratio = (stats["completed"] / denominator * 100) if denominator else 0.0
        rows.append(
            f"<tr><td>{category}</td><td>{stats['with_input']}</td><td>{stats['completed']}</td><td>{stats['in_progress']}</td><td>{stats['pending']}</td><td>{ratio:.1f}%</td></tr>"
        )
    rows_html = "".join(rows)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Retagging Status Dashboard</title>
  <style>
    :root {{ --bg:#0b1020; --panel:#121a2f; --panel2:#18223d; --text:#e8ecf6; --muted:#9aa6c1; --green:#3ddc97; --border:#243252; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:system-ui,sans-serif; background:linear-gradient(180deg,var(--bg),#0f1730 55%,#111a35); color:var(--text); padding:24px; }}
    .wrap {{ max-width:1200px; margin:0 auto; }}
    .grid {{ display:grid; grid-template-columns:repeat(12,1fr); gap:16px; }}
    .card {{ background:rgba(18,26,47,.92); border:1px solid var(--border); border-radius:16px; padding:18px; }}
    .span-3 {{ grid-column:span 3; }} .span-4 {{ grid-column:span 4; }} .span-12 {{ grid-column:span 12; }}
    .label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }}
    .value {{ font-size:30px; font-weight:700; margin-top:8px; }}
    .status {{ display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px; background:rgba(61,220,151,.12); color:var(--green); border:1px solid rgba(61,220,151,.35); font-weight:700; }}
    .dot {{ width:10px; height:10px; border-radius:50%; background:currentColor; }}
    .pill {{ display:inline-block; padding:4px 8px; border-radius:999px; background:var(--panel2); border:1px solid var(--border); margin-right:6px; margin-bottom:6px; }}
    table {{ width:100%; border-collapse:collapse; margin-top:12px; }}
    th, td {{ text-align:left; padding:10px; border-bottom:1px solid var(--border); }}
    .small {{ font-size:13px; color:var(--muted); margin-top:8px; }}
    @media (max-width:900px) {{ .span-3,.span-4,.span-12 {{ grid-column:span 12; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Retagging Status Dashboard</h1>
    <div class="small">{payload['root']} 기준 자동 오케스트레이션 상태</div>
    <div class="grid" style="margin-top:20px">
      <div class="card span-3"><div class="label">상태</div><div style="margin-top:10px" class="status"><span class="dot"></span>{payload['status']}</div><div class="small">업데이트: {payload['updated_at']}</div></div>
      <div class="card span-3"><div class="label">완료 batch</div><div class="value">{payload['completed_batches']}</div></div>
      <div class="card span-3"><div class="label">실행 중</div><div class="value">{payload['running_batches']}</div></div>
      <div class="card span-3"><div class="label">대기 batch</div><div class="value">{payload['pending_batches']}</div></div>
      <div class="card span-4"><div class="label">입력 미도착</div><div class="value">{payload['missing_input_batches']}</div></div>
      <div class="card span-4"><div class="label">수동 개입 필요</div><div class="value">{payload['manual_attention_batches']}</div></div>
      <div class="card span-4"><div class="label">merge collision</div><div class="value">{payload['collision_count']}</div></div>
      <div class="card span-12"><div class="label">최근 완료 batch</div><div style="margin-top:10px">{pills}</div></div>
      <div class="card span-12"><div class="label">주제군별 진행</div><table><thead><tr><th>주제군</th><th>입력 존재</th><th>완료</th><th>실행중</th><th>대기</th><th>진행률</th></tr></thead><tbody>{rows_html}</tbody></table></div>
    </div>
  </div>
</body>
</html>
"""


def refresh_status_outputs() -> dict[str, Any]:
    ensure_dirs()
    state = load_state()
    scans = scan_batches(state=state)
    summary = summarize_batches(scans, PRIORITY_CATEGORIES)

    (LOGS_DIR / "current_status.md").write_text(
        build_current_status_text(scans, summary),
        encoding="utf-8",
    )
    (LOGS_DIR / "bulk_progress_report.md").write_text(
        build_progress_report_text(scans, summary),
        encoding="utf-8",
    )

    payload = build_dashboard_payload(scans, summary)
    save_json(LOGS_DIR / "status_dashboard_data.json", payload)
    (ROOT / "status_dashboard.html").write_text(build_dashboard_html(payload), encoding="utf-8")
    save_json(
        STATUS_JSON_PATH,
        {
            "updated_at": now_iso(),
            "summary": summary,
            "batches": [asdict(scan) for scan in scans],
        },
    )
    return payload


def worker_prompt_text(batch_name: str, category: str) -> str:
    emphasis = {
        "probation": [
            "- rejection_of_regular_employment vs probation_termination 구분",
            "- 비수습이면 unrelated_to_probation 점검",
            "- 수습기간 도과 후 일반해고 여부 확인",
        ],
        "absence": [
            "- 무단결근이 핵심인지 배경인지 분리",
            "- 배경이면 not_really_absence_case 점검",
            "- no_formal_disposition / transfer / unfair_treatment 혼입 확인",
        ],
        "violence": [
            "- misconduct vs disciplinary_severity 구분",
            "- 비해고 처분이면 unrelated_to_dismissal 점검",
            "- 부당노동행위 문구 병기 시 과대분류 주의",
        ],
        "workplace_bullying": [
            "- 괴롭힘 성립 vs 양정 vs 보복 구분",
            "- 배경이면 not_really_harassment_case 점검",
            "- transfer_validity / unfair_treatment / no_formal_disposition 경계 확인",
        ],
        "incompetence": [
            "- work_ability vs dismissal_validity 경계 점검",
            "- 평가점수 존재 시에도 실제 중심 판단구조 우선",
            "- 개선기회, 교육, 절차 하자를 notes에 명시",
        ],
    }
    points = "\n".join(emphasis.get(category, ["- 실제 중심 판단구조를 primary에 반영"]))
    reviewed = f"C:/dev/labor-decisions-search/retagging/output/reviewed/{batch_name}_reviewed.jsonl"
    memo = f"C:/dev/labor-decisions-search/retagging/logs/{batch_name}_self_review.md"
    return f"""너는 /mnt/c/dev/labor-decisions-search/retagging 작업의 배치 워커다.

입력:
C:/dev/labor-decisions-search/retagging/input/batches/{batch_name}.jsonl

태그 사전:
C:/dev/labor-decisions-search/docs/tagging-schema-v1.json

출력:
{reviewed}

요약:
{memo}

공통 원칙:
- 표면 키워드보다 위원회의 실제 중심 판단구조를 우선
- 기존 v1 문서 본문은 수정하지 말 것
- 규칙 보강 필요 사항은 logs/rule_change_notes_v1.md에만 제안
- 결과는 reviewed JSONL과 self-review 메모 둘 다 생성
- 애매하거나 충돌 가능성이 큰 사건은 notes에 남길 것
- 기존 reviewed/self-review 포맷을 유지할 것

{category} 중점:
{points}
"""


def write_worker_prompt(batch_name: str, category: str) -> Path:
    ensure_dirs()
    prompt_path = PROMPTS_DIR / f"{batch_name}.md"
    prompt_path.write_text(worker_prompt_text(batch_name, category), encoding="utf-8")
    return prompt_path


def postprocess_outputs() -> dict[str, Any]:
    reviewed_files = sorted(REVIEWED_DIR.glob("*_reviewed.jsonl"))
    validate_result = None
    if reviewed_files and VALIDATE_SCRIPT.exists():
        validate_result = run_python_script(
            VALIDATE_SCRIPT,
            *[str(path) for path in reviewed_files],
            "--report",
        )

    merge_result = None
    if reviewed_files and MERGE_SCRIPT.exists():
        merge_result = run_python_script(
            MERGE_SCRIPT,
            *[str(path) for path in reviewed_files],
            "--overrides",
            str(REVIEWED_DIR / "manual_merge_overrides_v1.json"),
            "-o",
            str(MERGED_DIR / "merged_v1.jsonl"),
            "--report",
        )

    report = refresh_status_outputs()
    return {
        "validate_exit_code": None if validate_result is None else validate_result.returncode,
        "merge_exit_code": None if merge_result is None else merge_result.returncode,
        "collision_count": read_collision_count(),
        "status_report": report,
        "validate_stdout": "" if validate_result is None else validate_result.stdout,
        "validate_stderr": "" if validate_result is None else validate_result.stderr,
        "merge_stdout": "" if merge_result is None else merge_result.stdout,
        "merge_stderr": "" if merge_result is None else merge_result.stderr,
    }


def is_retryable_failure(reason: str, exit_code: int | None) -> bool:
    if reason in {"missing_input", "needs_operator", "waiting_manual_review"}:
        return False
    if exit_code == 0:
        return False
    return True


def mark_abandoned_running_batches(state: dict[str, Any]) -> bool:
    changed = False
    for _, entry in state.get("batches", {}).items():
        if entry.get("status") == "running":
            entry["status"] = "failed"
            entry["last_error"] = "orchestrator restart detected while batch marked running"
            entry["updated_at"] = now_iso()
            changed = True
    return changed
