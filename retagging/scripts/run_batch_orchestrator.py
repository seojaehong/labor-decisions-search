from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

from orchestrator_common import (
    ORCH_DIR,
    PRIORITY_CATEGORIES,
    ROOT,
    is_retryable_failure,
    load_state,
    mark_abandoned_running_batches,
    postprocess_outputs,
    record_run_event,
    refresh_status_outputs,
    save_state,
    scan_batches,
    set_batch_state,
)


def choose_next_batch(state: dict, categories: list[str], max_batch: int) -> str | None:
    scans = scan_batches(state=state, categories=categories, max_batch=max_batch)
    for category in categories:
        category_scans = [scan for scan in scans if scan.category == category]
        for scan in sorted(category_scans, key=lambda item: item.batch_number):
            if scan.queue_status == "pending":
                return scan.batch_name
    return None


def launch_worker(batch_name: str, worker_command: str, attempt: int) -> subprocess.Popen[str]:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "run_batch_worker.py"),
        "--batch-name",
        batch_name,
        "--attempt",
        str(attempt),
    ]
    if worker_command:
        command.extend(["--worker-command", worker_command])
    return subprocess.Popen(
        command,
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="retagging batch orchestrator")
    parser.add_argument("--max-parallel", type=int, default=3)
    parser.add_argument("--max-batch", type=int, default=100)
    parser.add_argument("--poll-seconds", type=int, default=3)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--worker-command", default=os.environ.get("RETAGGING_WORKER_COMMAND", ""))
    parser.add_argument("--continue-on-collision", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--status-only", action="store_true")
    args = parser.parse_args()

    ORCH_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    if mark_abandoned_running_batches(state):
        save_state(state)
    if args.status_only:
        refresh_status_outputs()
        return 0

    running: dict[str, tuple[subprocess.Popen[str], int]] = {}
    postprocess_needed = False
    launch_pass_done = False
    refresh_status_outputs()

    while True:
        state = load_state()
        scans = scan_batches(state=state, categories=PRIORITY_CATEGORIES, max_batch=args.max_batch)

        if (
            not args.continue_on_collision
            and any(scan.queue_status == "waiting_manual_review" for scan in scans)
        ):
            refresh_status_outputs()
            return 20

        while len(running) < args.max_parallel and not (args.once and launch_pass_done):
            batch_name = choose_next_batch(state, PRIORITY_CATEGORIES, args.max_batch)
            if not batch_name:
                break
            entry = state.setdefault("batches", {}).setdefault(batch_name, {})
            attempt = int(entry.get("attempts", 0) or 0) + 1
            set_batch_state(
                state,
                batch_name,
                "running",
                attempts=attempt,
                last_error="",
                last_exit_code=None,
            )
            record_run_event(
                state,
                {
                    "batch_name": batch_name,
                    "event": "launch",
                    "attempt": attempt,
                },
            )
            save_state(state)
            running[batch_name] = (launch_worker(batch_name, args.worker_command, attempt), attempt)
        if args.once:
            launch_pass_done = True

        finished: list[str] = []
        for batch_name, (proc, attempt) in list(running.items()):
            exit_code = proc.poll()
            if exit_code is None:
                continue
            finished.append(batch_name)
            state = load_state()
            entry = state.setdefault("batches", {}).setdefault(batch_name, {})
            current_status = entry.get("status", "")
            if exit_code == 0:
                record_run_event(
                    state,
                    {
                        "batch_name": batch_name,
                        "event": "completed",
                        "attempt": attempt,
                        "exit_code": exit_code,
                    },
                )
                postprocess_needed = True
            elif exit_code == 2 or current_status == "needs_operator":
                set_batch_state(
                    state,
                    batch_name,
                    "needs_operator",
                    attempts=attempt,
                    last_error=entry.get("last_error", ""),
                    last_exit_code=exit_code,
                )
                record_run_event(
                    state,
                    {
                        "batch_name": batch_name,
                        "event": "needs_operator",
                        "attempt": attempt,
                        "exit_code": exit_code,
                    },
                )
            elif exit_code == 3:
                set_batch_state(
                    state,
                    batch_name,
                    "failed",
                    attempts=attempt,
                    last_error=entry.get("last_error", "input batch file not found"),
                    last_exit_code=exit_code,
                )
            else:
                retryable = is_retryable_failure(current_status or "failed", exit_code)
                if retryable and attempt < args.max_retries:
                    set_batch_state(
                        state,
                        batch_name,
                        "pending",
                        attempts=attempt,
                        last_error=entry.get("last_error", ""),
                        last_exit_code=exit_code,
                    )
                    record_run_event(
                        state,
                        {
                            "batch_name": batch_name,
                            "event": "retry_scheduled",
                            "attempt": attempt,
                            "exit_code": exit_code,
                        },
                    )
                else:
                    record_run_event(
                        state,
                        {
                            "batch_name": batch_name,
                            "event": "failed",
                            "attempt": attempt,
                            "exit_code": exit_code,
                        },
                    )
            save_state(state)

        for batch_name in finished:
            running.pop(batch_name, None)

        if postprocess_needed:
            results = postprocess_outputs()
            state = load_state()
            if results["collision_count"] > 0 and not args.continue_on_collision:
                recent_completed = [
                    scan.batch_name
                    for scan in scan_batches(state=state, categories=PRIORITY_CATEGORIES, max_batch=args.max_batch)
                    if scan.queue_status == "completed"
                ][-args.max_parallel:]
                for batch_name in recent_completed:
                    entry = state.get("batches", {}).get(batch_name, {})
                    if entry.get("status") == "completed":
                        set_batch_state(
                            state,
                            batch_name,
                            "waiting_manual_review",
                            attempts=entry.get("attempts", 0),
                            last_error=f"merge collision count={results['collision_count']}",
                            last_exit_code=0,
                        )
                save_state(state)
                refresh_status_outputs()
                return 21
            postprocess_needed = False

        refresh_status_outputs()

        scans = scan_batches(state=load_state(), categories=PRIORITY_CATEGORIES, max_batch=args.max_batch)
        runnable_exists = any(scan.queue_status == "pending" for scan in scans)
        still_running = bool(running)

        if args.once and not still_running:
            return 0
        if not runnable_exists and not still_running:
            return 0
        time.sleep(max(1, args.poll_seconds))


if __name__ == "__main__":
    sys.exit(main())
