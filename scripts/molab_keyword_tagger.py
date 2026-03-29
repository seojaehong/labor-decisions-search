#!/usr/bin/env python3
"""
molab_interpretations 테이블에 keywords_matched를 태깅하는 스크립트
Supabase REST API를 사용하여 배치 업데이트
"""

from __future__ import annotations

import json
import os
import re
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


REPO_DIR = Path(__file__).parent.parent

TAG_RULES: list[tuple[str, list[str]]] = [
    ("단체협약", [r"단체협약"]),
    ("노동조합", [r"노동조합", r"\b노조\b"]),
    ("도급", [r"도급", r"용역계약", r"하도급"]),
    ("노동위원회", [r"노동위원회", r"중앙노동위원회", r"지방노동위원회"]),
    ("조합원", [r"조합원"]),
    ("손해배상", [r"손해배상", r"위자료", r"구상금"]),
    ("부당노동행위", [r"부당노동행위"]),
    ("파견", [r"파견", r"파견근로", r"불법파견"]),
    ("단체교섭", [r"단체교섭", r"교섭창구", r"교섭대표"]),
    ("파업", [r"파업", r"동맹파업"]),
    ("쟁의행위", [r"쟁의행위", r"쟁의조정", r"쟁의"]),
    ("조합활동", [r"조합활동", r"노조활동"]),
    ("부당해고", [r"부당해고", r"해고무효", r"해고무효확인", r"해고취소"]),
    ("임금체불", [r"임금체불", r"체불임금", r"미지급임금"]),
    ("산재", [r"산재", r"산업재해", r"업무상 재해", r"산재보험"]),
    ("성희롱", [r"성희롱", r"직장 내 성희롱"]),
    ("폭언/폭행", [r"폭언", r"폭행", r"폭행·폭언", r"폭언·폭행"]),
    ("횡령/배임", [r"횡령", r"배임"]),
    ("비위행위", [r"비위행위", r"비위", r"징계사유", r"품위손상"]),
    ("경영상해고", [r"경영상 해고", r"정리해고", r"경영상 이유"]),
    ("전보/인사이동", [r"전보", r"인사이동", r"인사발령", r"전직", r"배치전환"]),
    ("갱신기대권", [r"갱신기대권", r"계약갱신", r"갱신거절"]),
    ("해고부존재", [r"해고부존재", r"사직의사 없는", r"의원면직 취소"]),
    ("근로자성", [r"근로자성", r"근로자에 해당", r"사용종속관계"]),
    ("취업규칙", [r"취업규칙"]),
    ("퇴직금", [r"퇴직금", r"퇴직급여", r"퇴직급여보장"]),
    ("통상임금", [r"통상임금", r"평균임금"]),
    ("최저임금", [r"최저임금"]),
    ("연장근로", [r"연장근로", r"초과근로", r"시간외근로"]),
    ("휴게시간", [r"휴게시간"]),
    ("휴일근로", [r"휴일근로", r"주휴", r"휴일수당"]),
    ("연차휴가", [r"연차휴가", r"연차수당", r"유급휴가"]),
    ("기간제", [r"기간제", r"기간의 정함이 있는", r"무기계약직", r"계약직"]),
    ("수습", [r"수습", r"시용"]),
    ("본채용거부", [r"본채용거부", r"본채용 거부", r"채용거부"]),
    ("직장내괴롭힘", [r"직장내괴롭힘", r"직장 내 괴롭힘", r"괴롭힘"]),
]


def load_env_file() -> None:
    """환경변수 로드"""
    for candidate in (REPO_DIR / ".env.local", REPO_DIR / ".env"):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip())


def require_env(name: str) -> str:
    """환경변수 필수 체크"""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} must be set")
    return value


def build_headers() -> dict[str, str]:
    """Supabase 요청 헤더 구성"""
    service_key = require_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }


def build_tag_patterns() -> list[tuple[str, list[re.Pattern[str]]]]:
    """정규식 패턴 컴파일"""
    return [
        (tag, [re.compile(pattern, re.IGNORECASE) for pattern in patterns])
        for tag, patterns in TAG_RULES
    ]


def match_keywords(text: str, compiled_rules: list[tuple[str, list[re.Pattern[str]]]]) -> list[str]:
    """텍스트에서 키워드 매칭"""
    matched: list[str] = []
    for tag, patterns in compiled_rules:
        if any(pattern.search(text) for pattern in patterns):
            matched.append(tag)
    return matched


def fetch_all_records(batch_size: int = 1000) -> list[dict[str, Any]]:
    """Supabase에서 모든 레코드 가져오기 (Range 헤더 사용)"""
    supabase_url = require_env("SUPABASE_URL")
    headers = build_headers()

    all_records = []
    start_idx = 0

    while True:
        end_idx = start_idx + batch_size - 1
        headers_with_range = dict(headers)
        headers_with_range["Range"] = f"{start_idx}-{end_idx}"
        headers_with_range["Range-Unit"] = "items"

        print(f"  Fetching records {start_idx}-{end_idx}...")

        response = requests.get(
            f"{supabase_url}/rest/v1/molab_interpretations?select=id,title,inquiry_summary,answer_summary",
            headers=headers_with_range,
            timeout=120,
        )

        if response.status_code >= 400:
            print(f"  Error: {response.status_code} {response.text[:500]}")
            break

        records = response.json()
        if not records:
            break

        all_records.extend(records)
        print(f"  Got {len(records)} records (total: {len(all_records)})")

        if len(records) < batch_size:
            break

        start_idx = end_idx + 1

    return all_records


def patch_batch(updates: list[dict[str, Any]]) -> int:
    """배치 업데이트 실행 (PATCH)"""
    supabase_url = require_env("SUPABASE_URL")
    headers = dict(build_headers())
    headers["Prefer"] = "return=minimal"

    updated_count = 0
    for update in updates:
        record_id = update["id"]
        keywords = update.get("keywords_matched", [])

        response = requests.patch(
            f"{supabase_url}/rest/v1/molab_interpretations?id=eq.{record_id}",
            headers=headers,
            json={"keywords_matched": keywords},
            timeout=120,
        )

        if response.status_code >= 400:
            print(f"  Error updating {record_id}: {response.status_code} {response.text[:500]}")
        else:
            updated_count += 1

    return updated_count


def main() -> None:
    """메인 로직"""
    print("=" * 80)
    print("molab_interpretations 키워드 태깅 시작")
    print("=" * 80)

    # 환경변수 로드
    load_env_file()

    # 패턴 컴파일
    compiled_rules = build_tag_patterns()
    print(f"\n총 {len(compiled_rules)}개 태그 규칙 준비 완료")

    # 1단계: 전체 레코드 가져오기
    print("\n[1단계] Supabase에서 모든 레코드 가져오기...")
    all_records = fetch_all_records()
    print(f"총 {len(all_records)}건 로드됨")

    if not all_records:
        print("로드된 레코드가 없습니다.")
        return

    # 2단계: 키워드 매칭
    print("\n[2단계] 키워드 매칭 중...")
    tagged_records = []
    tag_counter = Counter()

    for idx, record in enumerate(all_records):
        if (idx + 1) % 100 == 0:
            print(f"  {idx + 1}/{len(all_records)} 처리 중...")

        combined_text = " ".join(
            str(record.get(field) or "")
            for field in ("title", "inquiry_summary", "answer_summary")
        )

        keywords_matched = match_keywords(combined_text, compiled_rules)

        if keywords_matched:
            tagged_records.append({
                "id": record["id"],
                "keywords_matched": keywords_matched,
            })
            tag_counter.update(keywords_matched)

    print(f"\n키워드 매칭 완료:")
    print(f"  - 총 {len(all_records)}건 중 {len(tagged_records)}건이 키워드 포함")
    print(f"  - 총 {len(tag_counter)}개 고유 키워드 발견")

    # 3단계: 배치 업데이트
    print("\n[3단계] Supabase에 배치 업데이트 중...")
    batch_size = 50
    total_updated = 0

    for batch_idx in range(0, len(tagged_records), batch_size):
        batch = tagged_records[batch_idx : batch_idx + batch_size]
        batch_num = batch_idx // batch_size + 1
        total_batches = (len(tagged_records) + batch_size - 1) // batch_size

        print(f"  배치 {batch_num}/{total_batches} ({len(batch)}건)...")
        updated = patch_batch(batch)
        total_updated += updated

        if batch_idx + batch_size < len(tagged_records):
            time.sleep(1.0)  # 배치 간 1초 딜레이

    print(f"\n업데이트 완료: {total_updated}건 업데이트됨")

    # 결과 보고
    print("\n" + "=" * 80)
    print("최종 결과 보고")
    print("=" * 80)
    print(f"총 처리 레코드: {len(all_records)}")
    print(f"키워드 포함 레코드: {len(tagged_records)}")
    print(f"성공적으로 업데이트된 레코드: {total_updated}")

    print("\n\n[상위 키워드 분포 (상위 30개)]")
    for keyword, count in tag_counter.most_common(30):
        print(f"  {keyword}: {count}건")

    print("\n" + "=" * 80)
    print("완료!")
    print("=" * 80)


if __name__ == "__main__":
    main()
