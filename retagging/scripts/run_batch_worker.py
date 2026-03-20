from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from orchestrator_common import (
    INPUT_DIR,
    RUNS_DIR,
    VALIDATE_SCRIPT,
    batch_paths,
    completion_ok,
    ensure_dirs,
    load_state,
    now_iso,
    relpath,
    run_python_script,
    save_state,
    set_batch_state,
    write_worker_prompt,
)


def build_command(template: str, batch_name: str) -> str:
    category = batch_name.rsplit("_batch_", 1)[0]
    batch_number = int(batch_name[-3:])
    paths = batch_paths(category, batch_number)
    return template.format(
        batch_name=batch_name,
        input_path=str(paths.input_path),
        reviewed_path=str(paths.reviewed_path),
        self_review_path=str(paths.self_review_path),
    )


def validate_reviewed_file(reviewed_path: Path) -> tuple[bool, int, str]:
    result = run_python_script(VALIDATE_SCRIPT, str(reviewed_path))
    ok = result.returncode == 0
    return ok, result.returncode, (result.stdout + result.stderr).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="retagging batch worker")
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--worker-command", default=os.environ.get("RETAGGING_WORKER_COMMAND", ""))
    parser.add_argument("--attempt", type=int, default=1)
    args = parser.parse_args()

    ensure_dirs()
    batch_name = args.batch_name
    category = batch_name.rsplit("_batch_", 1)[0]
    batch_number = int(batch_name[-3:])
    paths = batch_paths(category, batch_number)
    state = load_state()
    log_path = RUNS_DIR / f"{batch_name}.attempt_{args.attempt:02d}.log"

    if not paths.input_path.exists():
        set_batch_state(
            state,
            batch_name,
            "failed",
            attempts=args.attempt,
            last_error="input batch file not found",
            last_exit_code=3,
        )
        save_state(state)
        log_path.write_text("input batch file not found\n", encoding="utf-8")
        return 3

    if completion_ok(paths):
        set_batch_state(
            state,
            batch_name,
            "completed",
            attempts=args.attempt,
            last_exit_code=0,
            last_error="",
            reviewed_path=relpath(paths.reviewed_path),
            self_review_path=relpath(paths.self_review_path),
        )
        save_state(state)
        log_path.write_text("already completed\n", encoding="utf-8")
        return 0

    if not args.worker_command:
        prompt_path = write_worker_prompt(batch_name, category)
        set_batch_state(
            state,
            batch_name,
            "needs_operator",
            attempts=args.attempt,
            last_error=f"worker command not configured; prompt written to {relpath(prompt_path)}",
            last_exit_code=2,
            prompt_path=relpath(prompt_path),
        )
        save_state(state)
        log_path.write_text(
            f"[{now_iso()}] worker command not configured\nprompt: {prompt_path}\n",
            encoding="utf-8",
        )
        return 2

    command = build_command(args.worker_command, batch_name)
    with log_path.open("w", encoding="utf-8") as handle:
        handle.write(f"[{now_iso()}] command: {command}\n")
        process = subprocess.run(
            command,
            cwd=str(INPUT_DIR.parent.parent),
            shell=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=handle,
            stderr=subprocess.STDOUT,
        )

    if process.returncode != 0:
        state = load_state()
        set_batch_state(
            state,
            batch_name,
            "failed",
            attempts=args.attempt,
            last_error=f"worker command exited with {process.returncode}",
            last_exit_code=process.returncode,
            worker_log=relpath(log_path),
        )
        save_state(state)
        return process.returncode

    if not completion_ok(paths):
        state = load_state()
        set_batch_state(
            state,
            batch_name,
            "failed",
            attempts=args.attempt,
            last_error="worker finished but reviewed/self-review outputs are incomplete",
            last_exit_code=5,
            worker_log=relpath(log_path),
        )
        save_state(state)
        return 5

    valid, exit_code, details = validate_reviewed_file(paths.reviewed_path)
    state = load_state()
    if not valid:
        set_batch_state(
            state,
            batch_name,
            "failed",
            attempts=args.attempt,
            last_error=f"reviewed JSONL validation failed: {details[:400]}",
            last_exit_code=exit_code,
            worker_log=relpath(log_path),
        )
        save_state(state)
        return exit_code or 6

    set_batch_state(
        state,
        batch_name,
        "completed",
        attempts=args.attempt,
        last_error="",
        last_exit_code=0,
        reviewed_path=relpath(paths.reviewed_path),
        self_review_path=relpath(paths.self_review_path),
        worker_log=relpath(log_path),
    )
    save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
