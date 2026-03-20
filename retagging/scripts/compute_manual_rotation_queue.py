from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from orchestrator_common import INPUT_DIR, LOGS_DIR, ORCH_DIR, REVIEWED_DIR, basic_jsonl_ok

TOPICS = ["absence", "violence", "workplace_bullying"]
DEFAULT_START = 19
DEFAULT_END = 30
DEFAULT_SKIP = {("absence", 18), ("violence", 18), ("workplace_bullying", 18)}

QUEUE_JSON = ORCH_DIR / "manual_rotation_queue.json"
QUEUE_MD = ORCH_DIR / "manual_rotation_queue.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute next manual batch rotation queue from filesystem state.")
    parser.add_argument("--start", type=int, default=DEFAULT_START)
    parser.add_argument("--end", type=int, default=DEFAULT_END)
    parser.add_argument("--skip", nargs="*", default=[f"{topic}:018" for topic in TOPICS])
    parser.add_argument("--active", nargs="*", default=[])
    return parser.parse_args()


def parse_skip(values: list[str]) -> set[tuple[str, int]]:
    out: set[tuple[str, int]] = set()
    for value in values:
        try:
            topic, raw_num = value.split(":", 1)
            out.add((topic, int(raw_num)))
        except ValueError:
            continue
    return out


def parse_active(values: list[str]) -> set[str]:
    return {value.strip() for value in values if value.strip()}


def batch_name(topic: str, num: int) -> str:
    return f"{topic}_batch_{num:03d}"


def paths_for(topic: str, num: int) -> tuple[Path, Path, Path]:
    base = batch_name(topic, num)
    return (
        INPUT_DIR / f"{base}.jsonl",
        REVIEWED_DIR / f"{base}_reviewed.jsonl",
        LOGS_DIR / f"{base}_self_review.md",
    )


def completed(topic: str, num: int) -> bool:
    _input, reviewed, note = paths_for(topic, num)
    return reviewed.exists() and note.exists() and basic_jsonl_ok(reviewed)


def scan_topic(topic: str, start: int, end: int, skip: set[tuple[str, int]], active: set[str]) -> dict[str, object]:
    done: list[str] = []
    pending: list[str] = []
    blocked: list[str] = []
    active_here: list[str] = []

    for num in range(start, end + 1):
        name = batch_name(topic, num)
        input_path, reviewed, note = paths_for(topic, num)
        if (topic, num) in skip:
            blocked.append(name)
            continue
        if not input_path.exists():
            continue
        if name in active:
            active_here.append(name)
            continue
        if completed(topic, num):
            done.append(name)
        else:
            pending.append(name)

    next_candidate = pending[0] if pending else None
    return {
        "topic": topic,
        "completed": done,
        "active": active_here,
        "blocked": blocked,
        "pending": pending,
        "next_candidate": next_candidate,
    }


def build_markdown(data: dict[str, object], start: int, end: int) -> str:
    lines = [
        "# Manual Rotation Queue",
        "",
        f"- updated_at: {data['updated_at']}",
        f"- range: batch_{start:03d}~batch_{end:03d}",
        "",
    ]
    for topic_data in data["topics"]:
        topic = topic_data["topic"]
        lines.append(f"## {topic}")
        lines.append("")
        lines.append(f"- active: {', '.join(topic_data['active']) or 'none'}")
        lines.append(f"- next_candidate: {topic_data['next_candidate'] or 'none'}")
        lines.append(f"- blocked: {', '.join(topic_data['blocked']) or 'none'}")
        lines.append(f"- completed_count: {len(topic_data['completed'])}")
        lines.append(f"- pending_count: {len(topic_data['pending'])}")
        if topic_data["pending"]:
            lines.append(f"- pending_head: {', '.join(topic_data['pending'][:5])}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    skip = parse_skip(args.skip) or set(DEFAULT_SKIP)
    active = parse_active(args.active)

    ORCH_DIR.mkdir(parents=True, exist_ok=True)

    topics = [scan_topic(topic, args.start, args.end, skip, active) for topic in TOPICS]
    payload = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "range": {"start": args.start, "end": args.end},
        "active": sorted(active),
        "skip": sorted(f"{topic}:{num:03d}" for topic, num in skip),
        "topics": topics,
    }

    QUEUE_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QUEUE_MD.write_text(build_markdown(payload, args.start, args.end), encoding="utf-8")
    print(f"Wrote {QUEUE_JSON}")
    print(f"Wrote {QUEUE_MD}")


if __name__ == "__main__":
    main()
