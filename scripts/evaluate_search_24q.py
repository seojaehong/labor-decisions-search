from __future__ import annotations

import argparse
import difflib
import json
import math
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


ROOT = Path(r"C:\dev\labor-decisions-search")
DEFAULT_OUTPUT_DIR = ROOT / "evaluation" / "search_quality_99"
BASELINE_REPORT_PATH = ROOT / "evaluation" / "rubric_haiku_eval_20260330.md"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_CHAT_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
NON_LABOR_CASE_TYPES = ("헌법", "특허", "형사", "군사", "행정소송법")
DB_REASON_CATEGORIES = {
    "absence",
    "sexual_harassment",
    "workplace_bullying",
    "transfer",
    "probation",
    "contract_expiry",
    "no_dismissal",
    "worker_status",
    "discrimination",
    "redundancy",
    "misconduct",
    "violence",
    "embezzlement",
    "incompetence",
    "union_activity",
}
GENERIC_QUERY_TERMS = {
    "사건",
    "반복",
    "실제",
    "핵심",
    "문제",
    "여부",
    "정당",
    "정당성",
    "정당한지",
    "과한지",
    "최종적으로는",
    "함께",
    "여러",
    "있지만",
    "같은",
    "본",
    "보고",
    "다툰",
    "다툼",
    "언급되지만",
}
CATEGORY_CORE_TERMS: dict[str, set[str]] = {
    "absence": {"무단결근", "결근", "해고"},
    "workplace_bullying": {"직장내괴롭힘", "괴롭힘"},
    "probation": {"수습", "시용", "본채용"},
    "contract_expiry": {"갱신기대권", "기간제", "계약만료", "계약기간"},
    "transfer": {"전보", "인사발령", "배치전환", "대기발령"},
    "violence": {"폭행", "폭언", "욕설"},
    "incompetence": {"업무능력", "저성과", "해고"},
    "worker_status": {"근로자성"},
}


@dataclass(frozen=True)
class EvalQuery:
    query_id: str
    text: str
    category: str


@dataclass(frozen=True)
class BaselineQueryScore:
    query_id: str
    weighted_score: int
    precision_hits: int


EVAL_QUERIES: list[EvalQuery] = [
    EvalQuery("Q01", "반복 무단결근으로 해고된 사건", "absence"),
    EvalQuery("Q02", "무단결근이 언급되지만 실제 핵심은 절차 위반인 사건", "absence"),
    EvalQuery("Q03", "택시나 버스 기사 무단결근 징계해고", "absence"),
    EvalQuery("Q04", "직장내괴롭힘이 실제로 성립하는지 다툼이 핵심인 사건", "workplace_bullying"),
    EvalQuery("Q05", "직장내괴롭힘 신고 후 불이익이나 보복이 문제 된 사건", "workplace_bullying"),
    EvalQuery("Q06", "괴롭힘은 인정되는데 징계 수위가 과한지 보는 사건", "workplace_bullying"),
    EvalQuery("Q07", "수습기간 중 본채용 거부가 정당한지", "probation"),
    EvalQuery("Q08", "수습기간 중 업무능력 부족으로 해고하거나 본채용 거부한 사건", "probation"),
    EvalQuery("Q09", "수습인데 서면통지나 절차 문제가 있는 사건", "probation"),
    EvalQuery("Q10", "정규직 저성과나 업무능력 부족으로 해고된 사건", "incompetence"),
    EvalQuery("Q11", "개선기회나 경고를 주고도 업무능력 부족으로 해고한 사건", "incompetence"),
    EvalQuery("Q12", "징계사유는 인정되지만 해고가 너무 과하다고 본 사건", ""),
    EvalQuery("Q13", "정직 처분 양정이 적정한지 본 사건", ""),
    EvalQuery("Q14", "감봉 처분이 과한지 본 사건", ""),
    EvalQuery("Q15", "기간제 근로자의 갱신기대권이 인정되는지", "contract_expiry"),
    EvalQuery("Q16", "계약기간 만료인데 사실상 해고처럼 다퉈진 사건", "contract_expiry"),
    EvalQuery("Q17", "전보나 인사발령이 정당한지 다툰 사건", "transfer"),
    EvalQuery("Q18", "대기발령이나 배치전환이 징계인지 인사권 행사인지 다툼", "transfer"),
    EvalQuery("Q19", "폭행이나 욕설 같은 비위 사실 자체가 인정되는지가 핵심", "violence"),
    EvalQuery("Q20", "폭행은 있었지만 해고까지는 과하다고 본 사건", "violence"),
    EvalQuery("Q21", "욕설이나 직장질서 문란이 반복되어 징계해고된 사건", "violence"),
    EvalQuery("Q22", "근로자성이 실제 핵심 쟁점인 사건", "worker_status"),
    EvalQuery("Q23", "괴롭힘은 인정되지 않지만 그 신고나 요구 때문에 갈등이 커진 사건", "workplace_bullying"),
    EvalQuery("Q24", "여러 비위가 함께 있었지만 최종적으로는 해고 정당성 전체를 본 사건", ""),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate 24 precedent search queries before/after hybrid upgrades.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--skip-rerank", action="store_true")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--baseline-report", default=str(BASELINE_REPORT_PATH))
    return parser.parse_args()


def load_env_file() -> None:
    for candidate in (ROOT / ".env.local", ROOT / ".env", ROOT / "supabase" / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip()
            if name not in os.environ:
                os.environ[name] = value.strip()


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def with_timeout_post(
    url: str,
    *,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout: int,
) -> requests.Response:
    return requests.post(url, headers=headers, json=payload, timeout=timeout)


def call_supabase_rpc(function_name: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    base_url = require_env("NEXT_PUBLIC_SUPABASE_URL")
    api_key = os.environ.get("SUPABASE_SERVICE_KEY") or require_env("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    response = requests.post(
        f"{base_url}/rest/v1/rpc/{function_name}",
        headers={
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else []


def fetch_table_rows(params: dict[str, str]) -> list[dict[str, Any]]:
    base_url = require_env("NEXT_PUBLIC_SUPABASE_URL")
    api_key = os.environ.get("SUPABASE_SERVICE_KEY") or require_env("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    response = requests.get(
        f"{base_url}/rest/v1/nlrc_decisions",
        headers={
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
        },
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else []


def safe_fetch_table_rows(params: dict[str, str]) -> list[dict[str, Any]]:
    try:
        return fetch_table_rows(params)
    except requests.HTTPError:
        return []


def parse_baseline_report(path: Path) -> dict[str, BaselineQueryScore]:
    if not path.exists():
        raise RuntimeError(f"Baseline report not found: {path}")

    text = path.read_text(encoding="utf-8")
    query_pattern = re.compile(
        r"^(Q\d+):.*?Precision@5:\s+(\d+)/5\s+\|\s+Weighted:\s+(\d+)/10$",
        re.MULTILINE | re.DOTALL,
    )
    results: dict[str, BaselineQueryScore] = {}
    for query_id, precision_hits, weighted_score in query_pattern.findall(text):
        results[query_id] = BaselineQueryScore(
            query_id=query_id,
            weighted_score=int(weighted_score),
            precision_hits=int(precision_hits),
        )
    if len(results) != len(EVAL_QUERIES):
        raise RuntimeError(f"Expected {len(EVAL_QUERIES)} baseline query scores, found {len(results)}")
    return results


def normalize_category(value: str | None) -> str:
    db_categories = {
        "absence",
        "sexual_harassment",
        "workplace_bullying",
        "transfer",
        "probation",
        "contract_expiry",
        "no_dismissal",
        "worker_status",
        "discrimination",
        "redundancy",
        "misconduct",
        "violence",
        "embezzlement",
        "incompetence",
        "union_activity",
    }
    # Map non-DB categories to closest DB category
    category_aliases = {
        "dismissal": "misconduct",
        "discipline": "misconduct",
        "disciplinary_severity": "",  # keep original query category
        "wage": "",
        "industrial_accident": "",
        "other": "",
    }
    normalized = (value or "").strip()
    if normalized in db_categories:
        return normalized
    if normalized in category_aliases:
        return category_aliases[normalized]
    return ""


def fallback_rewrite(query: str) -> dict[str, Any]:
    lowered = query.lower()
    category = ""
    intent = "generic"
    if any(token in lowered for token in ["무단결근", "결근", "지각", "조퇴"]):
        category = "absence"
        intent = "validity_check"
    elif any(token in lowered for token in ["괴롭힘", "직장내괴롭힘"]):
        category = "workplace_bullying"
        intent = "retaliation_check" if any(token in lowered for token in ["보복", "불이익", "신고"]) else "validity_check"
    elif any(token in lowered for token in ["성희롱", "성추행"]):
        category = "sexual_harassment"
        intent = "validity_check"
    elif any(token in lowered for token in ["폭행", "폭언", "욕설", "폭력"]):
        category = "violence"
        intent = "severity_check" if any(token in lowered for token in ["과하", "양정", "수위"]) else "validity_check"
    elif any(token in lowered for token in ["수습", "시용", "본채용"]):
        category = "probation"
        intent = "procedure_check"
    elif any(token in lowered for token in ["업무능력", "저성과", "성과 부족"]):
        category = "incompetence"
        intent = "validity_check"
    elif any(token in lowered for token in ["갱신기대권", "계약만료", "기간제", "계약직"]):
        category = "contract_expiry"
        intent = "termination_check"
    elif any(token in lowered for token in ["전보", "인사이동", "인사발령", "배치전환"]):
        category = "transfer"
        intent = "validity_check"
    elif any(token in lowered for token in ["근로자성", "도급", "파견", "원청"]):
        category = "worker_status"
        intent = "status_check"
    elif any(token in lowered for token in ["노조", "노동조합", "단체교섭", "부당노동행위", "쟁의행위", "파업"]):
        category = "union_activity"
        intent = "labor_relation_check"

    keywords = [token.strip() for token in query.split() if len(token.strip()) >= 2][:5]
    return {
        "searchQuery": query.strip(),
        "category": category,
        "intent": intent,
        "keywords": keywords,
    }


def extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if "```" in stripped:
        parts = stripped.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{") and part.endswith("}"):
                try:
                    return json.loads(part)
                except json.JSONDecodeError:
                    continue
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(stripped[start : end + 1])
    except json.JSONDecodeError:
        return None


def rewrite_query(query: str) -> dict[str, Any]:
    fallback = fallback_rewrite(query)
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if anthropic_key:
        try:
            response = with_timeout_post(
                ANTHROPIC_URL,
                headers={
                    "content-type": "application/json",
                    "x-api-key": anthropic_key,
                    "anthropic-version": "2023-06-01",
                },
                payload={
                    "model": ANTHROPIC_MODEL,
                    "max_tokens": 260,
                    "temperature": 0,
                    "system": (
                        "당신은 한국 노동위원회 판정례 검색용 쿼리 최적화 엔진입니다. 반드시 JSON 객체만 반환하세요.\n"
                        "키: searchQuery, category, intent, keywords\n\n"
                        "중요 규칙:\n"
                        "1. category는 반드시 DB에 존재하는 값만 사용: absence, workplace_bullying, probation, incompetence, contract_expiry, transfer, violence, worker_status, sexual_harassment, embezzlement, misconduct, redundancy, no_dismissal, discrimination, union_activity\n"
                        "2. 존재하지 않는 category(dismissal, discipline, disciplinary_severity, wage 등)는 절대 사용 금지. 가장 가까운 DB category로 매핑하세요.\n"
                        "3. '해고가 과하다/양정과다' 쿼리 → category는 원래 비위 유형(violence, misconduct 등) 유지. intent를 severity_check로 설정.\n"
                        "4. '~인정되지 않지만/불인정/미해당' 같은 부정 조건은 searchQuery에 '불인정', '미해당', '부인' 키워드를 명시적으로 포함.\n"
                        "5. '보복/불이익/신고 후' 쿼리 → keywords에 '보복', '불이익 취급', '불이익 조치', '신고 후 징계' 포함.\n"
                        "6. '계약만료 + 사실상 해고' → category는 contract_expiry. keywords에 '갱신거절', '갱신기대권', '사실상 해고' 포함.\n"
                        "7. searchQuery는 판정례 제목/쟁점과 매칭될 수 있는 구체적 법률 용어로 변환."
                    ),
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                f"사용자 입력: {query}\n"
                                "위 규칙에 따라 JSON을 반환하세요.\n"
                                '예시: {"searchQuery":"업무능력 부족 개선 기회 경고 시정 교육 후 해고","category":"incompetence","intent":"validity_check","keywords":["개선 기회","경고","시정","업무능력 부족","해고"]}'
                            ),
                        }
                    ],
                },
                timeout=3,
            )
            response.raise_for_status()
            payload = response.json()
            text = next((item.get("text", "") for item in payload.get("content", []) if item.get("type") == "text"), "")
            parsed = extract_json_object(text) or {}
            return {
                "searchQuery": str(parsed.get("searchQuery") or fallback["searchQuery"]).strip()[:50],
                "category": normalize_category(str(parsed.get("category") or fallback["category"])),
                "intent": str(parsed.get("intent") or fallback["intent"]).strip() or fallback["intent"],
                "keywords": [str(item).strip() for item in parsed.get("keywords", fallback["keywords"])[:5]],
            }
        except Exception:
            pass

    if openai_key:
        try:
            response = with_timeout_post(
                OPENAI_CHAT_URL,
                headers={
                    "content-type": "application/json",
                    "authorization": f"Bearer {openai_key}",
                },
                payload={
                    "model": OPENAI_CHAT_MODEL,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {
                            "role": "system",
                            "content": "당신은 한국 노동위원회 판정례 검색용 쿼리 최적화 엔진입니다. 반드시 JSON 객체만 반환하세요. 키는 searchQuery, category, intent, keywords만 사용합니다.",
                        },
                        {
                            "role": "user",
                            "content": f"사용자 입력: {query}",
                        },
                    ],
                },
                timeout=3,
            )
            response.raise_for_status()
            payload = response.json()
            text = payload["choices"][0]["message"]["content"]
            parsed = extract_json_object(text) or json.loads(text)
            return {
                "searchQuery": str(parsed.get("searchQuery") or fallback["searchQuery"]).strip()[:50],
                "category": normalize_category(str(parsed.get("category") or fallback["category"])),
                "intent": str(parsed.get("intent") or fallback["intent"]).strip() or fallback["intent"],
                "keywords": [str(item).strip() for item in parsed.get("keywords", fallback["keywords"])[:5]],
            }
        except Exception:
            pass

    return fallback


def create_embedding(text: str) -> list[float] | None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    response = with_timeout_post(
        OPENAI_EMBEDDING_URL,
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}",
        },
        payload={"model": OPENAI_EMBEDDING_MODEL, "input": text[:8000]},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data", [])
    if not data:
      return None
    embedding = data[0].get("embedding")
    return embedding if isinstance(embedding, list) else None


def to_vector_literal(embedding: list[float]) -> str:
    return "[" + ",".join(str(float(value)) for value in embedding) + "]"


def keyword_boost(result: dict[str, Any], keywords: list[str]) -> float:
    haystack = " ".join(
        [
            str(result.get("title") or ""),
            str(result.get("holding_summary") or ""),
            str(result.get("summary_short") or ""),
            str(result.get("key_issue") or ""),
        ]
    ).lower()
    hits = sum(1 for keyword in keywords if keyword and keyword.lower() in haystack)
    if hits >= 4:
        return 0.1
    if hits >= 2:
        return 0.05
    return 0.0


def tokenize_query(value: str) -> list[str]:
    tokens = [token.strip() for token in re.split(r"\s+", value) if len(token.strip()) >= 2]
    normalized = [token for token in tokens if token not in GENERIC_QUERY_TERMS]
    return list(dict.fromkeys(normalized or tokens))


def build_text_or_clause(term: str) -> str:
    escaped = term.replace("%", " ").replace(",", " ").replace("(", " ").replace(")", " ").strip()
    return "(" + ",".join(
        [
            f"title.ilike.*{escaped}*",
            f"holding_summary.ilike.*{escaped}*",
            f"key_issue.ilike.*{escaped}*",
            f"summary_short.ilike.*{escaped}*",
        ]
    ) + ")"


def parse_embedding(value: Any) -> list[float]:
    if isinstance(value, list):
        return [float(item) for item in value]
    if not isinstance(value, str):
        return []
    stripped = value.strip()
    if not stripped.startswith("[") or not stripped.endswith("]"):
        return []
    body = stripped[1:-1].strip()
    if not body:
        return []
    return [float(part) for part in body.split(",")]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def trigram_like_score(query: str, row: dict[str, Any]) -> float:
    fields = [
        str(row.get("title") or ""),
        str(row.get("holding_summary") or ""),
        str(row.get("key_issue") or ""),
        str(row.get("summary_short") or ""),
    ]
    ratios = [difflib.SequenceMatcher(None, query, field).ratio() for field in fields if field]
    tokens = tokenize_query(query)
    token_hits = 0
    haystack = " ".join(fields).lower()
    for token in tokens:
        if token.lower() in haystack:
            token_hits += 1
    token_score = (token_hits / max(len(tokens), 1)) * 0.35
    return max(ratios, default=0.0) + token_score


def metadata_boost(query: str, row: dict[str, Any]) -> float:
    text = f"{row.get('title') or ''} {row.get('holding_summary') or ''}"
    key_issue = str(row.get("key_issue") or "")
    reason_category = row.get("reason_category") or []
    if not isinstance(reason_category, list):
        reason_category = []
    sanction_type = str(row.get("sanction_type") or "")
    decision_result = str(row.get("decision_result") or "")
    boost = 0.0

    # Sanction type matching
    if "감봉" in query and sanction_type == "pay_cut":
        boost += 0.15
    if "정직" in query and sanction_type == "suspension":
        boost += 0.12

    # Composite misconduct
    if re.search(r"(여러|함께|복합|복수).*(비위|사유)|비위.*(여러|함께|복합|복수)|정당성 전체", query) and len(reason_category) >= 3:
        boost += 0.10
    if re.search(r"(여러|함께|복합|복수|정당성|양정|과하|정당)", query) and "징계사유" in text and re.search(r"(양정|과하|정당)", text):
        boost += 0.08

    # Transport workers
    if re.search(r"(택시|버스|기사|운전|운수)", query) and re.search(r"(택시|버스|기사|운전|운수)", text):
        boost += 0.12

    # Improvement opportunity / low performance
    if re.search(r"(개선|시정|경고|교육|기회|주고도|부여|업무능력|저성과)", query) and re.search(r"(개선|시정|경고|교육|기회|주고도|부여)", text):
        boost += 0.10

    # Q05/Q23: Retaliation after harassment report
    if re.search(r"(보복|불이익|신고.{0,5}후)", query):
        if re.search(r"(보복|불이익|신고.{0,5}(후|이후)|불이익.{0,5}(취급|조치))", text + " " + key_issue):
            boost += 0.15
        if re.search(r"(전보|배치전환|대기발령|감봉|정직)", text) and re.search(r"신고", text):
            boost += 0.08
        if "workplace_bullying" in reason_category and re.search(r"(직위해제|전보|보직해임|대기발령)", text + " " + key_issue):
            boost += 0.12
        if "workplace_bullying" not in reason_category and "union_activity" in reason_category:
            boost -= 0.12

    # Q23: Harassment NOT recognized but conflict escalated
    if re.search(r"(인정되지 않|불인정|미해당|부인)", query):
        if re.search(r"(괴롭힘.{0,10}(인정.{0,5}않|불인정|해당.{0,5}않|부인)|불인정)", text + " " + key_issue):
            boost += 0.15
        if re.search(r"(갈등|분쟁|대립)", text + " " + key_issue):
            boost += 0.05
        if re.search(r"(신고|요구|문제제기|불이익|보복)", query) and re.search(r"(신고|요구|문제제기|불이익|보복)", text + " " + key_issue):
            boost += 0.08

    # Q20: Violence recognized but dismissal too severe (양정과다)
    if re.search(r"(과하다|과하|과중|양정과다|해고까지는)", query):
        if re.search(r"(양정.{0,5}(과하|과다|과중)|해고.{0,10}(과하|과중|과다)|징계.{0,5}(과하|과중))", text + " " + key_issue):
            boost += 0.12
        # Boost cases where dismissal was overturned (인용 = worker won)
        if "인용" in decision_result and re.search(r"(폭행|폭언)", text):
            boost += 0.08

    # Q16: Contract expiry treated as de facto dismissal
    if re.search(r"(사실상 해고|해고처럼|해고.{0,5}다퉈)", query):
        if re.search(r"(갱신거절|갱신기대권|사실상.{0,5}해고|해고.{0,5}다퉈)", text + " " + key_issue):
            boost += 0.12
        if "contract_expiry" in reason_category and "인용" in decision_result:
            boost += 0.06

    # Q10: Regular employee incompetence
    if re.search(r"(정규직|저성과|업무능력 부족)", query) and "incompetence" in reason_category:
        if re.search(r"(저성과|업무능력.{0,5}(부족|미달)|근무성적)", text + " " + key_issue):
            boost += 0.10

    # Non-labor penalty
    if any(token in str(row.get("title") or "") for token in NON_LABOR_CASE_TYPES):
        boost -= 0.25
    return boost


def add_unique_terms(base: str, extra_terms: list[str]) -> str:
    existing = {token.strip() for token in base.split() if token.strip()}
    additions = [term for term in extra_terms if term and term not in existing]
    return " ".join([base, *additions]).strip()


def build_intent_aware_query(query_text: str, rewrite: dict[str, Any]) -> str:
    intent = str(rewrite.get("intent") or "generic")
    category = str(rewrite.get("category") or "")
    lowered = query_text.lower()
    extra_terms: list[str] = []

    if intent == "retaliation_check":
        extra_terms.extend(["불이익", "보복", "신고"])

    if category == "workplace_bullying" and re.search(r"(불인정|미인정|미해당|부인)", lowered):
        extra_terms.extend(["괴롭힘 불인정", "괴롭힘 미해당"])

    if category == "workplace_bullying" and re.search(r"(갈등|불이익|보복|신고|요구|문제제기)", lowered):
        extra_terms.extend(["신고 후", "갈등", "불이익 취급", "직위해제", "전보", "보직해임", "대기발령"])

    if category == "contract_expiry" and re.search(r"(사실상 해고|해고처럼|실질적 해고|갱신거절)", lowered):
        extra_terms.extend(["사실상 해고", "실질적 해고", "갱신거절"])

    if intent == "severity_check":
        extra_terms.extend(["양정과다", "과중"])

    if category == "violence" and intent == "severity_check":
        extra_terms.extend(["징계 과도", "해고 과중"])

    if category == "incompetence" and re.search(r"(개선|경고|시정|교육|기회|주고도|부여)", lowered):
        extra_terms.extend(["개선 기회", "경고", "시정", "교육"])

    return add_unique_terms(query_text, extra_terms) if extra_terms else query_text


def build_debug_payload(query: EvalQuery, upgraded: dict[str, Any], evaluation: dict[str, Any]) -> dict[str, Any]:
    return {
        "query_id": query.query_id,
        "query": query.text,
        "category": query.category,
        "rewrite": upgraded["rewrite"],
        "reranked": upgraded["reranked"],
        "top5": sanitize_results(upgraded["results"]),
        "ai_rerank": upgraded["ai_rerank"],
        "evaluation": evaluation,
    }


def fetch_candidate_rows_for_query(query_text: str, category: str, keyword_hints: list[str]) -> list[dict[str, Any]]:
    select = (
        "id,title,decision_result,holding_summary,summary_short,key_issue,reason_category,"
        "sanction_type,decision_date,url"
    )
    rows_by_id: dict[str, dict[str, Any]] = {}

    def merge(rows: list[dict[str, Any]]) -> None:
        for row in rows:
            row_id = str(row.get("id") or "")
            if row_id and row_id not in rows_by_id:
                rows_by_id[row_id] = row

    category_filter = category if category in DB_REASON_CATEGORIES else ""

    if category_filter:
        merge(
            safe_fetch_table_rows(
                {
                    "select": select,
                    "reason_category": f"cs.{{{category_filter}}}",
                    "limit": "250",
                    "order": "decision_date.desc",
                }
            )
        )

    if "감봉" in query_text:
        merge(safe_fetch_table_rows({"select": select, "sanction_type": "eq.pay_cut", "limit": "120", "order": "decision_date.desc"}))
    if "정직" in query_text:
        merge(safe_fetch_table_rows({"select": select, "sanction_type": "eq.suspension", "limit": "120", "order": "decision_date.desc"}))

    core_terms = CATEGORY_CORE_TERMS.get(category_filter, set())
    terms = [
        term for term in tokenize_query(query_text)
        if len(term) >= 3 and " " not in term and term not in core_terms
    ][:4]
    if keyword_hints:
        for keyword in keyword_hints[:3]:
            for subterm in tokenize_query(keyword):
                if (
                    subterm not in terms
                    and len(subterm) >= 3
                    and " " not in subterm
                    and subterm not in GENERIC_QUERY_TERMS
                    and subterm not in core_terms
                ):
                    terms.append(subterm)

    if category_filter:
        text_fetch_terms = terms[:2]
    else:
        text_fetch_terms = terms[:6]

    for term in text_fetch_terms:
            merge(
                safe_fetch_table_rows(
                    {
                        "select": select,
                        "or": build_text_or_clause(term),
                        "limit": "40",
                        "order": "decision_date.desc",
                    }
                )
            )

    candidate_rows = list(rows_by_id.values())
    if not candidate_rows:
        return candidate_rows

    id_chunks: list[list[str]] = []
    ids = [str(row["id"]) for row in candidate_rows if row.get("id")]
    chunk_size = 100
    for idx in range(0, len(ids), chunk_size):
        id_chunks.append(ids[idx : idx + chunk_size])

    embeddings_by_id: dict[str, Any] = {}
    for chunk in id_chunks:
        id_filter = "(" + ",".join(chunk) + ")"
        embedding_rows = safe_fetch_table_rows(
            {
                "select": "id,embedding",
                "id": f"in.{id_filter}",
                "limit": str(len(chunk)),
            }
        )
        for row in embedding_rows:
            row_id = str(row.get("id") or "")
            if row_id:
                embeddings_by_id[row_id] = row.get("embedding")

    for row in candidate_rows:
        row["embedding"] = embeddings_by_id.get(str(row.get("id") or ""), [])

    return candidate_rows


def extract_json_array(text: str) -> list[dict[str, Any]]:
    stripped = text.strip()
    if "```" in stripped:
        parts = stripped.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("[") and part.endswith("]"):
                try:
                    return json.loads(part)
                except json.JSONDecodeError:
                    continue
    start = stripped.find("[")
    end = stripped.rfind("]")
    if start == -1 or end == -1 or end <= start:
        return []
    try:
        return json.loads(stripped[start : end + 1])
    except json.JSONDecodeError:
        return []


def sanitize_rerank_items(items: list[Any], top_k: int) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            sanitized.append(item)
        if len(sanitized) >= top_k:
            break
    return sanitized


def rerank_results(user_query: str, results: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not anthropic_key and not openai_key:
        return []

    rendered_results = "\n\n".join(
        f"{idx + 1}. [{result.get('id')}] {result.get('title')}\n"
        f"쟁점: {str(result.get('key_issue') or result.get('holding_summary') or result.get('summary_short') or '')[:320]}\n"
        f"결과: {result.get('decision_result') or '미상'}"
        for idx, result in enumerate(results)
    )

    if anthropic_key:
        try:
            response = with_timeout_post(
                ANTHROPIC_URL,
                headers={
                    "content-type": "application/json",
                    "x-api-key": anthropic_key,
                    "anthropic-version": "2023-06-01",
                },
                payload={
                    "model": ANTHROPIC_MODEL,
                    "max_tokens": 800,
                    "temperature": 0,
                    "system": "당신은 노동법 판정례 검색 결과를 평가하는 전문가입니다. 반드시 JSON 배열만 반환하세요. 각 원소는 id, score, reason만 포함합니다.",
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                f'사용자 검색 쿼리: "{user_query}"\n\n'
                                "평가 기준:\n"
                                "- 10점: 쿼리가 정확히 묻는 법적 쟁점을 다루는 사건\n"
                                "- 8-9점: 동일 쟁점이나 세부 맥락이 약간 다른 사건\n"
                                "- 5-7점: 관련 주제이나 핵심 쟁점이 다른 사건\n"
                                "- 3-4점: 일부 키워드만 겹치는 사건\n"
                                "- 0-2점: 쿼리와 무관한 사건\n"
                                "- 형사사건, 군사법 사건, 종중/교회 내부 분쟁은 0점\n\n"
                                "쿼리 의도별 추가 기준:\n"
                                "- '보복/불이익/신고 후' → 신고와 불이익 사이의 인과관계가 핵심. 단순 징계 사건은 낮은 점수\n"
                                "- '인정되지 않/불인정' → 해당 사유가 부인·불인정된 사건이 높은 점수. 인정된 사건은 낮은 점수\n"
                                "- '과하다/양정/수위' → 비위는 인정되나 징계가 과중하다고 본 사건이 높은 점수\n"
                                "- '사실상 해고/해고처럼' → 계약만료이나 실질적으로 해고 다툼인 사건이 높은 점수\n"
                                "- '정규직 저성과/업무능력' → 기간제가 아닌 정규직의 능력 부족 해고가 높은 점수\n\n"
                                f"검색 결과:\n{rendered_results}"
                            ),
                        }
                    ],
                },
                timeout=5,
            )
            response.raise_for_status()
            payload = response.json()
            text = next((item.get("text", "") for item in payload.get("content", []) if item.get("type") == "text"), "")
            parsed = extract_json_array(text)
            if parsed:
                return sanitize_rerank_items(parsed, top_k)
        except Exception:
            pass

    if openai_key:
        try:
            response = with_timeout_post(
                OPENAI_CHAT_URL,
                headers={
                    "content-type": "application/json",
                    "authorization": f"Bearer {openai_key}",
                },
                payload={
                    "model": OPENAI_CHAT_MODEL,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {
                            "role": "system",
                            "content": '당신은 노동법 판정례 검색 결과를 평가하는 전문가입니다. 반드시 {"results":[...]} 형태의 JSON만 반환하세요.',
                        },
                        {"role": "user", "content": f'사용자 검색 쿼리: "{user_query}"\n\n검색 결과:\n{rendered_results}'},
                    ],
                },
                timeout=5,
            )
            response.raise_for_status()
            payload = response.json()
            text = payload["choices"][0]["message"]["content"]
            parsed = json.loads(text)
            return sanitize_rerank_items(list(parsed.get("results", [])), top_k)
        except Exception:
            pass

    return []


def evaluate_results_with_ai(query: EvalQuery, results: list[dict[str, Any]]) -> dict[str, Any]:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    rendered_results = "\n\n".join(
        f"{idx + 1}. [{result.get('id')}] {result.get('title')}\n"
        f"요지: {str(result.get('holding_summary') or result.get('summary_short') or result.get('key_issue') or '')[:400]}\n"
        f"결과: {result.get('decision_result') or '미상'}"
        for idx, result in enumerate(results[:5])
    )

    instruction = (
        f'사용자 검색 쿼리: "{query.text}"\n'
        f'카테고리: "{query.category or "없음"}"\n\n'
        "아래 상위 5개 결과를 독립적으로 평가하세요.\n"
        "반드시 JSON 배열만 반환하세요. 각 원소는 rank, id, score, reason만 포함합니다.\n"
        "score는 0, 1, 2만 허용됩니다.\n"
        "- 2점: 쿼리가 묻는 핵심 법적 쟁점을 정확히 다룬다\n"
        "- 1점: 관련은 있으나 핵심 쟁점/맥락이 다르다\n"
        "- 0점: 쿼리와 무관하거나 형사/군사/종중/교회 내부 사건이다\n\n"
        f"검색 결과:\n{rendered_results}"
    )

    if anthropic_key:
        try:
            response = with_timeout_post(
                ANTHROPIC_URL,
                headers={
                    "content-type": "application/json",
                    "x-api-key": anthropic_key,
                    "anthropic-version": "2023-06-01",
                },
                payload={
                    "model": ANTHROPIC_MODEL,
                    "max_tokens": 900,
                    "temperature": 0,
                    "system": "당신은 노동법 판정례 검색 품질을 평가하는 독립 심사자입니다. 반드시 JSON 배열만 반환하세요.",
                    "messages": [{"role": "user", "content": instruction}],
                },
                timeout=8,
            )
            response.raise_for_status()
            payload = response.json()
            text = next((item.get("text", "") for item in payload.get("content", []) if item.get("type") == "text"), "")
            parsed = extract_json_array(text)
            if parsed:
                break_result = parsed[:5]
                weighted_score = sum(int(item.get("score") or 0) for item in break_result)
                precision_hits = sum(1 for item in break_result if int(item.get("score") or 0) > 0)
                return {
                    "per_result": break_result,
                    "weighted_score": weighted_score,
                    "precision_hits": precision_hits,
                }
        except Exception:
            pass

    if openai_key:
        try:
            response = with_timeout_post(
                OPENAI_CHAT_URL,
                headers={
                    "content-type": "application/json",
                    "authorization": f"Bearer {openai_key}",
                },
                payload={
                    "model": OPENAI_CHAT_MODEL,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {
                            "role": "system",
                            "content": '당신은 노동법 판정례 검색 품질을 평가하는 독립 심사자입니다. 반드시 {"results":[...]} 형태의 JSON만 반환하세요.',
                        },
                        {"role": "user", "content": instruction},
                    ],
                },
                timeout=8,
            )
            response.raise_for_status()
            payload = response.json()
            parsed = json.loads(payload["choices"][0]["message"]["content"])
            break_result = list(parsed.get("results", []))[:5]
            weighted_score = sum(int(item.get("score") or 0) for item in break_result)
            precision_hits = sum(1 for item in break_result if int(item.get("score") or 0) > 0)
            return {
                "per_result": break_result,
                "weighted_score": weighted_score,
                "precision_hits": precision_hits,
            }
        except Exception:
            pass

    fallback_rows: list[dict[str, Any]] = []
    weighted_score = 0
    precision_hits = 0
    for idx, result in enumerate(results[:5], start=1):
        haystack = " ".join(
            [
                str(result.get("title") or ""),
                str(result.get("holding_summary") or ""),
                str(result.get("summary_short") or ""),
                str(result.get("key_issue") or ""),
            ]
        )
        score = 2 if any(token in haystack for token in query.text.split()) else 0
        if score > 0:
            precision_hits += 1
        weighted_score += score
        fallback_rows.append(
            {
                "rank": idx,
                "id": result.get("id"),
                "score": score,
                "reason": "fallback heuristic",
            }
        )
    return {
        "per_result": fallback_rows,
        "weighted_score": weighted_score,
        "precision_hits": precision_hits,
    }


def run_upgraded(query: EvalQuery, limit: int, top_k: int, skip_rerank: bool) -> dict[str, Any]:
    rewrite = rewrite_query(query.text)
    effective_query = build_intent_aware_query(rewrite["searchQuery"] or query.text, rewrite)
    effective_category = query.category or rewrite["category"]
    embedding = create_embedding(effective_query)
    rows: list[dict[str, Any]] = []

    if embedding:
        try:
            rows = call_supabase_rpc(
                "search_similar_cases_hybrid",
                {
                    "query_text": effective_query,
                    "query_embedding": to_vector_literal(embedding),
                    "category": effective_category,
                    "match_count": limit,
                    "semantic_weight": 0.6,
                },
            )
        except requests.HTTPError:
            rows = []

    if not rows:
        rows = fetch_candidate_rows_for_query(effective_query, effective_category, rewrite["keywords"])

    rescored_rows = []
    for row in rows:
        trigram_score = trigram_like_score(effective_query, row)
        semantic_score = cosine_similarity(embedding or [], parse_embedding(row.get("embedding")))
        category_boost = 0.08 if effective_category and effective_category in (row.get("reason_category") or []) else 0.0
        meta_boost = metadata_boost(effective_query, row)
        relevance = (0.4 * trigram_score) + (0.6 * semantic_score) + category_boost + meta_boost
        rescored_rows.append(
            {
                **row,
                "_trigram_score": trigram_score,
                "_semantic_score": semantic_score,
                "_metadata_boost": meta_boost,
                "_keyword_boost": keyword_boost(row, rewrite["keywords"]),
                "_effective_relevance": relevance + keyword_boost(row, rewrite["keywords"]),
            }
        )

    rescored_rows.sort(
        key=lambda row: (
            float(row.get("_effective_relevance") or 0),
            str(row.get("decision_date") or ""),
        ),
        reverse=True,
    )

    ai_reranked = [] if skip_rerank else rerank_results(query.text, rescored_rows[:limit], top_k)
    if ai_reranked:
        rank_by_id = {str(item.get("id")): item for item in ai_reranked}
        rescored_rows.sort(
            key=lambda row: (
                float(rank_by_id.get(str(row.get("id")), {}).get("score", -1)),
                float(row.get("_effective_relevance") or 0),
                str(row.get("decision_date") or ""),
            ),
            reverse=True,
        )

    return {
        "rewrite": rewrite,
        "results": rescored_rows[:top_k],
        "reranked": bool(ai_reranked),
        "ai_rerank": ai_reranked,
    }


def sanitize_results(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for row in rows:
        cleaned = dict(row)
        cleaned.pop("embedding", None)
        sanitized.append(cleaned)
    return sanitized


def main() -> None:
    load_env_file()
    args = parse_args()
    baseline_scores = parse_baseline_report(Path(args.baseline_report))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    debug_dir = output_dir / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)

    started_at = time.time()
    result_bundle: list[dict[str, Any]] = []
    total_before = 0
    total_after = 0

    for query in EVAL_QUERIES:
        upgraded = run_upgraded(query, args.limit, args.top_k, args.skip_rerank)
        evaluation = evaluate_results_with_ai(query, upgraded["results"])
        baseline = baseline_scores[query.query_id]
        total_before += baseline.weighted_score
        total_after += int(evaluation["weighted_score"])
        result_bundle.append(
            {
                "query_id": query.query_id,
                "query": query.text,
                "category": query.category,
                "baseline_weighted_score": baseline.weighted_score,
                "baseline_precision_hits": baseline.precision_hits,
                "upgraded_top5": sanitize_results(upgraded["results"]),
                "rewrite": upgraded["rewrite"],
                "reranked": upgraded["reranked"],
                "ai_rerank": upgraded["ai_rerank"],
                "evaluation": evaluation,
            }
        )
        if query.query_id in {"Q05", "Q10", "Q16", "Q20", "Q23"}:
            debug_path = debug_dir / f"{query.query_id}.json"
            debug_path.write_text(
                json.dumps(build_debug_payload(query, upgraded, evaluation), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    duration_seconds = round(time.time() - started_at, 2)
    results_path = output_dir / "results.json"
    report_path = output_dir / "report.json"

    results_path.write_text(json.dumps(result_bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(
        json.dumps(
            {
                "queries": len(EVAL_QUERIES),
                "limit": args.limit,
                "top_k": args.top_k,
                "skip_rerank": args.skip_rerank,
                "duration_seconds": duration_seconds,
                "baseline_report_path": str(Path(args.baseline_report)),
                "baseline_total_score": total_before,
                "upgraded_total_score": total_after,
                "score_delta": total_after - total_before,
                "results_path": str(results_path),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
