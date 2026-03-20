from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from orchestrator_common import LOGS_DIR, ORCH_DIR, REVIEWED_DIR


OVERRIDE_PATH = REVIEWED_DIR / "manual_merge_overrides_v1.json"
DOC_PATH = LOGS_DIR / "override_quality_review.md"
AGENTS_DOC = ORCH_DIR / "AGENTS_TO_PM.md"


def now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append override watchlist snapshots without mutating override data.")
    parser.add_argument("--append-agents-report", action="store_true")
    return parser.parse_args()


def load_overrides() -> list[dict[str, Any]]:
    payload = json.loads(OVERRIDE_PATH.read_text(encoding="utf-8"))
    return payload.get("overrides", [])


def append_text(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def main() -> int:
    args = parse_args()
    overrides = load_overrides()
    reason_counter = Counter()
    field_counter = Counter()
    watchlist: list[dict[str, Any]] = []
    for item in overrides:
        reason = str(item.get("reason", "")).strip()
        reason_counter[reason] += 1
        fields = item.get("fields", {})
        for key in fields:
            field_counter[key] += 1
        if "자동 판정" in reason or "원본 정보 부족" in reason:
            watchlist.append(item)

    lines = [
        "",
        f"## Override Watchlist Snapshot ({now_label()})",
        "",
        f"- override 총량: {len(overrides)}건",
        f"- watchlist(`자동 판정`/`원본 정보 부족`): {len(watchlist)}건",
        f"- 상위 수정 필드: {', '.join(f'`{k}` {v}' for k, v in field_counter.most_common(4))}",
        f"- 상위 reason: {', '.join(f'`{k}` {v}' for k, v in reason_counter.most_common(4))}",
        "",
    ]
    if watchlist:
        lines.append("### 재확인 우선 대상")
        for item in watchlist[:12]:
            fields = ", ".join(f"{k}={v}" for k, v in (item.get("fields") or {}).items())
            lines.append(f"- `{item.get('case_id', 'unknown')}`: {item.get('reason', '')} / {fields}")
        lines.append("")
    else:
        lines.append("- watchlist 대상 없음")
        lines.append("")

    append_text(DOC_PATH, "\n".join(lines))

    if args.append_agents_report:
        append_text(
            AGENTS_DOC,
            "\n".join(
                [
                    "",
                    "---",
                    "",
                    f"## Codex Override Watchlist ({now_label()})",
                    "",
                    f"- override 총량: {len(overrides)}건",
                    f"- `자동 판정`/`원본 정보 부족` watchlist: {len(watchlist)}건",
                    "- 상세는 `logs/override_quality_review.md` 참조",
                    "",
                ]
            ),
        )

    print(f"Updated {DOC_PATH}")
    if args.append_agents_report:
        print(f"Updated {AGENTS_DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
