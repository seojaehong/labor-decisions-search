from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).parent.parent
OUTPUT_DIR = REPO_DIR / "evaluation" / "lawgo" / "prec"
API_URL = "https://www.law.go.kr/DRF/lawService.do"
SPACE_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n{3,}")
SECTION_RE = re.compile(r"(〖[^〗]+〗|【[^】]+】)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect Korean precedent bodies from law.go.kr prec API")
    parser.add_argument("--id", dest="ids", action="append", help="판례 일련번호. 여러 번 지정 가능")
    parser.add_argument("--id-file", help="판례 일련번호 목록 파일 (한 줄에 하나)")
    parser.add_argument("--oc", help="법제처 Open API OC 값. 미지정 시 LAWGO_OC 또는 OC 환경변수 사용")
    parser.add_argument("--type", choices=["JSON", "HTML", "XML"], default="JSON")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--output-dir", help="기존 run 디렉터리를 재사용")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            os.environ[name.strip()] = value.strip()


def require_oc(explicit: str | None) -> str:
    value = explicit or os.environ.get("LAWGO_OC") or os.environ.get("OC")
    if not value:
        raise SystemExit("Error: --oc or LAWGO_OC/OC environment variable must be set")
    return value


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    text = (
        value.replace("<br/>", "\n")
        .replace("<br />", "\n")
        .replace("<br>", "\n")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\xa0", " ")
    )
    text = re.sub(r"<[^>]+>", "", text)
    text = "\n".join(SPACE_RE.sub(" ", line).strip() for line in text.splitlines())
    text = BLANK_RE.sub("\n\n", text)
    return text.strip()


def split_sections(body_text: str) -> list[dict[str, Any]]:
    normalized = clean_text(body_text)
    if not normalized:
        return []

    parts = SECTION_RE.split(normalized)
    sections: list[dict[str, Any]] = []
    current_title = "본문"
    current_text = ""

    for part in parts:
        stripped = clean_text(part)
        if not stripped:
            continue
        if (
            stripped.startswith("〖") and stripped.endswith("〗")
        ) or (
            stripped.startswith("【") and stripped.endswith("】")
        ):
            if current_text:
                sections.append({
                    "title": current_title,
                    "text": current_text,
                    "type": infer_section_type(current_title),
                })
            current_title = stripped.strip("〖〗【】")
            current_text = ""
        else:
            current_text = clean_text(f"{current_text}\n{stripped}" if current_text else stripped)

    if current_text:
        sections.append({
            "title": current_title,
            "text": current_text,
            "type": infer_section_type(current_title),
        })

    for index, section in enumerate(sections):
        section["index"] = index
    return sections


def infer_section_type(title: str) -> str:
    normalized = clean_text(title)
    if normalized in {"전문", "피 고 인", "상 고 인", "변 호 인", "원심판결"}:
        return "fulltext"
    if normalized in {"주 문", "주문"}:
        return "order"
    if normalized in {"이 유", "이유"}:
        return "reasoning"
    if normalized in {"판시사항"}:
        return "issues"
    if normalized in {"판결요지"}:
        return "summary"
    if normalized in {"참조조문"}:
        return "reference_statutes"
    if normalized in {"참조판례"}:
        return "reference_cases"
    return "body"


def load_ids(args: argparse.Namespace) -> list[str]:
    values: list[str] = []
    if args.ids:
        values.extend(args.ids)
    if args.id_file:
        values.extend(
            line.strip()
            for line in Path(args.id_file).read_text(encoding="utf-8").splitlines()
            if line.strip()
        )

    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    if args.limit > 0:
        deduped = deduped[: args.limit]
    return deduped


def shard_ids(values: list[str], shard_index: int, shard_count: int) -> list[str]:
    if shard_count <= 1:
        return values
    return [value for idx, value in enumerate(values) if idx % shard_count == shard_index]


def fetch_prec_json(oc_value: str, prec_id: str, output_type: str, timeout: int) -> str:
    response = requests.get(
        API_URL,
        params={
            "OC": oc_value,
            "target": "prec",
            "ID": prec_id,
            "type": output_type,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def normalize_json_payload(payload: dict[str, Any], prec_id: str) -> dict[str, Any]:
    if payload.get("Law"):
        raise ValueError(clean_text(str(payload.get("Law"))))
    data = payload.get("PrecService", {})
    body_text = clean_text(data.get("판례내용"))
    title = clean_text(data.get("사건명"))
    if not title and not body_text:
        raise ValueError("판례 본문 또는 메타가 비어 있습니다")
    sections = split_sections(body_text)
    return {
        "source_provider": "lawgo",
        "source_kind": "case",
        "source_id": str(data.get("판례정보일련번호") or prec_id),
        "title": title,
        "reference_number": clean_text(data.get("사건번호")),
        "decision_date": clean_text(str(data.get("선고일자") or "")),
        "decision_date_display": clean_text(data.get("선고")),
        "court": clean_text(data.get("법원명")),
        "court_type_code": clean_text(str(data.get("법원종류코드") or "")),
        "case_type_name": clean_text(data.get("사건종류명")),
        "case_type_code": clean_text(str(data.get("사건종류코드") or "")),
        "judgment_type": clean_text(data.get("판결유형")),
        "issue_text": clean_text(data.get("판시사항")),
        "summary_text": clean_text(data.get("판결요지")),
        "reference_statutes": clean_text(data.get("참조조문")),
        "reference_cases": clean_text(data.get("참조판례")),
        "body_text": body_text,
        "body_sections": sections,
        "body_length": len(body_text),
        "api_id": prec_id,
    }


def main() -> None:
    load_env_file()
    args = parse_args()
    oc_value = require_oc(args.oc)
    ids = shard_ids(load_ids(args), args.shard_index, args.shard_count)
    if not ids:
        raise SystemExit("Error: provide --id or --id-file")

    if args.shard_index < 0 or args.shard_index >= args.shard_count:
        raise SystemExit("--shard-index must be in range 0..shard-count-1")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(args.output_dir) if args.output_dir else (OUTPUT_DIR / timestamp)
    run_dir.mkdir(parents=True, exist_ok=True)
    results_path = run_dir / f"results_shard_{args.shard_index}.jsonl"
    ready_path = run_dir / f"lawgo_cases_ready_shard_{args.shard_index}.jsonl"

    rows: list[dict[str, Any]] = []
    success_count = 0
    error_count = 0
    body_length_sum = 0
    body_length_count = 0

    with results_path.open("w", encoding="utf-8") as results_handle, (
        ready_path.open("w", encoding="utf-8") if not args.dry_run else open(os.devnull, "w", encoding="utf-8")
    ) as ready_handle:
        for index, prec_id in enumerate(ids, start=1):
            try:
                raw_text = fetch_prec_json(oc_value, prec_id, args.type, args.timeout)
                if args.type == "JSON":
                    payload = json.loads(raw_text)
                    row = normalize_json_payload(payload, prec_id)
                else:
                    row = {
                        "source_provider": "lawgo",
                        "source_kind": "case",
                        "source_id": prec_id,
                        "api_id": prec_id,
                        "raw_text": raw_text,
                    }
                success_count += 1
                if row.get("body_length"):
                    body_length_sum += int(row["body_length"])
                    body_length_count += 1
            except Exception as exc:  # noqa: BLE001
                row = {
                    "source_provider": "lawgo",
                    "source_kind": "case",
                    "source_id": prec_id,
                    "api_id": prec_id,
                    "error": str(exc)[:500],
                }
                error_count += 1

            rows.append(row)
            results_handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            if not args.dry_run and not row.get("error"):
                ready_handle.write(json.dumps(row, ensure_ascii=False) + "\n")

            if index % 100 == 0 or index == len(ids):
                print(f"shard {args.shard_index}: {index}/{len(ids)} done")
            if args.delay > 0:
                import time
                time.sleep(args.delay)

    report = {
        "count": len(rows),
        "success": success_count,
        "errors": error_count,
        "avg_body_length": round(
            body_length_sum / max(1, body_length_count),
            2,
        ),
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "results_path": str(results_path),
        "ready_path": str(ready_path),
    }

    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "report_path": str(report_path),
        "jsonl_path": str(results_path),
        "success": report["success"],
        "errors": report["errors"],
        "avg_body_length": report["avg_body_length"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
