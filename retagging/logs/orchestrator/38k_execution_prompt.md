# 38k 확장 태깅 실행 프롬프트 (소넷용)

## 상황

재태깅 1단계(5개 주제군 4,232건)가 완료되고 DB 반영까지 끝났다.
지금은 2단계: 나머지 38k 중 22,165건을 Tier 1 → Tier 2 순서로 태깅한다.

## 실행 명령

```
38k 확장 실행

1. 입력 배치 경로: retagging/input/batches_38k/
2. 출력 경로: retagging/output/reviewed/ (기존과 동일)
3. 자기리뷰 경로: retagging/logs/ (기존과 동일, {group}_batch_{nnn}_self_review.md)
4. 배치 크기: 50건
5. 순서: Tier 1 먼저 (transfer → contract_expiry → sexual_harassment)
6. 기존 5개 주제군 태깅 프롬프트 재사용 + tagging_hint 필드 활용

금지:
- retagging/output/merged/merged_final_v2.jsonl 직접 수정 금지
- 기존 reviewed 파일 수정 금지
- v1 관련 문서 수정 금지
```

## 배치 현황

| Tier | 그룹 | 건수 | 배치 수 |
|------|------|------|---------|
| 1 | transfer | 4,245 | 85 |
| 1 | contract_expiry | 6,297 | 126 |
| 1 | sexual_harassment | 993 | 20 |
| 2 | misconduct_remaining | 7,712 | 155 |
| 2 | union_activity | 2,185 | 44 |
| 2 | redundancy | 477 | 10 |
| 2 | discrimination | 256 | 6 |
| **합계** | | **22,165** | **446** |

## tagging_hint 필드 활용

각 배치에 `tagging_hint` 필드가 있다. 태깅 시 참조:

| 그룹 | hint |
|------|------|
| transfer | 전보/전직/대기발령 정당성 |
| contract_expiry | 갱신기대권/계약만료 |
| sexual_harassment | 성희롱 징계 |
| misconduct_remaining | 복합비위/misconduct vs disciplinary_severity |
| union_activity | 부당노동행위/노조 관련 |
| redundancy | 경영상 해고/정리해고 |
| discrimination | 차별시정 |

## merge 규칙

완료 후:
```bash
python3 scripts/merge_tagging_outputs.py \
  retagging/output/reviewed/*.jsonl \
  retagging/output/reviewed/38k_reviewed/*.jsonl \  # 신규 파일 있으면
  --output retagging/output/merged/merged_final_v3.jsonl \
  --overrides retagging/output/reviewed/manual_merge_overrides_v1.json \
  --report
```

## 진행 추적

- SHARED_STATUS.md 갱신 책임: PM
- 배치별 self_review.md: 태깅 에이전트
- 현재 기준본: merged_final_v2.jsonl (3,923건)
- 목표 기준본: merged_final_v3.jsonl (~26,088건 예상)
