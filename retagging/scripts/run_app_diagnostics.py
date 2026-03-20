from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from orchestrator_common import LOGS_DIR, ORCH_DIR


DOC_PATH = LOGS_DIR / "local_app_smoke_check.md"
AGENTS_DOC = ORCH_DIR / "AGENTS_TO_PM.md"
ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env.local"


def now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure local app and direct Supabase timings.")
    parser.add_argument("--base-url", default="http://localhost:3000")
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--append-agents-report", action="store_true")
    return parser.parse_args()


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def timed_request(url: str, *, timeout: float, method: str = "GET", body: bytes | None = None, headers: dict[str, str] | None = None) -> dict[str, str]:
    request = urllib.request.Request(url=url, data=body, method=method, headers=headers or {})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            return {
                "status": str(response.status),
                "elapsed_ms": str(elapsed_ms),
                "size": str(len(payload)),
                "error": "",
            }
    except urllib.error.HTTPError as exc:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "status": str(exc.code),
            "elapsed_ms": str(elapsed_ms),
            "size": "0",
            "error": f"HTTPError: {exc.reason}",
        }
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "status": "error",
            "elapsed_ms": str(elapsed_ms),
            "size": "0",
            "error": str(exc),
        }


def build_supabase_url(base: str) -> str:
    params = urllib.parse.urlencode(
        {
            "select": "id,decision_date",
            "reason_category": "cs.{absence}",
            "order": "decision_date.desc",
            "limit": "20",
        }
    )
    return f"{base}/rest/v1/nlrc_decisions?{params}"


def build_doc_markdown(results: dict[str, dict[str, str]], supabase_result: dict[str, str] | None) -> str:
    def line(name: str, result: dict[str, str]) -> str:
        if result["error"]:
            return f"- `{name}`: {result['status']} / {result['elapsed_ms']}ms / error=`{result['error']}`"
        return f"- `{name}`: {result['status']} / {result['elapsed_ms']}ms / size={result['size']}"

    lines = [
        "",
        f"## Diagnostic Snapshot ({now_label()})",
        "",
        "### Local endpoint timings",
        line("/", results["home"]),
        line("/search", results["search"]),
        line("/sanction", results["sanction"]),
        line("/api/sanction", results["api_sanction"]),
        "",
    ]
    if supabase_result is not None:
        lines.append("### Direct Supabase REST timing")
        lines.append(line("supabase reason_category absence", supabase_result))
        lines.append("")

    lines.extend(
        [
            "### Diagnosis",
            "- 홈이 빠르고 `/search`, `/sanction`, `/api/sanction`이 상대적으로 느리면 초기 데이터 조회 또는 blocking 모델 호출이 병목일 가능성이 높다.",
            "- direct Supabase REST가 빠른데 `/search`와 `/api/sanction`이 느리면 Next route/client query 조합이나 모델 호출이 우세 병목이다.",
            "- direct Supabase REST도 느리면 DB 인덱스, `count=exact`, 정렬, text search 조건 조합을 먼저 의심한다.",
            "",
            "### Fix proposals",
            "- `/search`: `count=exact`를 초기 렌더에서 분리하고, free-text가 비어 있을 때 `textSearch`를 붙이지 않도록 조정",
            "- `/search`: reason-only 조회는 더 가벼운 first page query와 별도 total count query로 분리",
            "- `/api/sanction`: retrieval 시간과 모델 호출 시간을 별도 로깅해서 병목을 분리",
            "- `/api/sanction`: retrieval 결과를 먼저 응답 가능한 구조로 바꾸거나, 모델 timeout 시 partial fallback을 반환",
            "- retrieval: retagged field를 reason-only 검색 필터와 exclusion-aware filter에 더 직접 반영할 후보를 재정리",
            "",
        ]
    )
    return "\n".join(lines)


def build_agents_markdown(results: dict[str, dict[str, str]], supabase_result: dict[str, str] | None) -> str:
    slowest = max(results.items(), key=lambda item: int(item[1]["elapsed_ms"]))
    lines = [
        "",
        "---",
        "",
        f"## Codex App Diagnostic ({now_label()})",
        "",
        f"- `/`: {results['home']['elapsed_ms']}ms",
        f"- `/search`: {results['search']['elapsed_ms']}ms",
        f"- `/sanction`: {results['sanction']['elapsed_ms']}ms",
        f"- `/api/sanction`: {results['api_sanction']['elapsed_ms']}ms",
        f"- 가장 느린 경로: `{slowest[0]}`",
    ]
    if supabase_result is not None:
        lines.append(f"- direct Supabase REST(absence): {supabase_result['elapsed_ms']}ms")
    lines.append("- 상세와 수정안은 `logs/local_app_smoke_check.md` 참조")
    lines.append("")
    return "\n".join(lines)


def append_text(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    results = {
        "home": timed_request(f"{base_url}/", timeout=args.timeout),
        "search": timed_request(f"{base_url}/search", timeout=args.timeout),
        "sanction": timed_request(f"{base_url}/sanction", timeout=args.timeout),
        "api_sanction": timed_request(
            f"{base_url}/api/sanction",
            timeout=args.timeout,
            method="POST",
            body=json.dumps({"messages": [{"role": "user", "content": "직원이 반복적으로 무단결근합니다"}]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        ),
    }

    env_values = load_env_file(ENV_PATH)
    supabase_result = None
    supabase_url = env_values.get("NEXT_PUBLIC_SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    supabase_key = env_values.get("NEXT_PUBLIC_SUPABASE_ANON_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    if supabase_url and supabase_key:
        supabase_result = timed_request(
            build_supabase_url(supabase_url),
            timeout=args.timeout,
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
            },
        )

    append_text(DOC_PATH, build_doc_markdown(results, supabase_result))
    if args.append_agents_report:
        append_text(AGENTS_DOC, build_agents_markdown(results, supabase_result))

    print(f"Updated {DOC_PATH}")
    if args.append_agents_report:
        print(f"Updated {AGENTS_DOC}")
    for key, value in results.items():
        print(f"{key}: {value['status']} {value['elapsed_ms']}ms {value['error']}")
    if supabase_result is not None:
        print(f"supabase: {supabase_result['status']} {supabase_result['elapsed_ms']}ms {supabase_result['error']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
