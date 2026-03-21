# `/search` Candidate/Compare Checklist

## URL modes

- `/search?mode=baseline`
- `/search?mode=candidate&q=<query>`
- `/search?mode=compare&q=<query>`

## What changed

- baseline: 기존 `reason_category` 검색 유지
- candidate: 8축 태그 retrieval 결과 노출
- compare: 같은 질의에 대해 baseline / candidate를 나란히 표시

## Candidate debug fields

- `case_id`
- `primary`
- `stage`
- `disposition`
- `score`
- `why surfaced`
- baseline `reason_category` badge

## Smoke queries

1. `무단결근 절차위반`
2. `직장내괴롭힘 신고 보복`
3. `정규직 저성과 해고`
4. `징계사유 인정 해고 과다`

## Visual checks

1. mode 전환 시 URL `mode=`가 바뀌는지
2. compare에서 baseline / candidate가 2열로 보이는지
3. candidate 카드에 `primary/stage/disposition/why`가 보이는지
4. Q2/Q4/Q7/Q8에서 baseline과 candidate 상위 결과 차이가 보이는지
5. baseline pagination이 그대로 유지되는지

## Notes

- candidate는 내부 검증용 top-5 중심
- baseline은 기존 페이지네이션 유지
- runtime smoke는 별도 로컬 실행 환경에서 확인 권장
