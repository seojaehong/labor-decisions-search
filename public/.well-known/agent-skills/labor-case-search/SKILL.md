---
name: labor-case-search
description: 노동위원회 판정례 검색 — 29,622건 키워드·카테고리·사유·결과 기반
version: 1.0.0
input:
  - name: query
    type: string
    description: 검색 키워드 (예: "무단결근 해고")
  - name: category
    type: string
    description: "카테고리 필터 (unfair-dismissal, unfair-discipline, sexual-harassment 등)"
  - name: result
    type: string
    description: "결과 필터 (인용, 기각, 화해 등)"
output:
  type: json
  description: 판정례 목록 (제목, 사건번호, 카테고리, 결과, 요약)
endpoint: https://www.xn--o80bk8isxeinax68f.com/api/search
method: GET
---

# 노동위원회 판정례 검색

대한민국 노동위원회(중앙·지방) 판정례 29,622건을 검색합니다.

## 카테고리 (16개)
- 부당해고, 부당징계, 성희롱, 폭언/폭행
- 횡령/배임, 비위행위, 경영상해고, 전보/인사이동
- 갱신기대권, 해고부존재, 임금분쟁, 직장내괴롭힘
- 수습/시용, 퇴직, 산업재해, 차별

## 사용 예시
```
GET /api/search?q=무단결근&category=unfair-dismissal&result=인용
```

## 응답
판정례 목록 (JSON): 제목, 사건번호, 카테고리, 결과, AI 분류, 핵심 요약
