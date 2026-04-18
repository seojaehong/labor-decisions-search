---
name: sanction-analysis
description: AI 징계양정 비교분석 — 유사 판정례 기반 근거 비교
version: 1.0.0
input:
  - name: messages
    type: array
    description: "대화 메시지 배열 [{role: 'user', content: '징계 상황 설명'}]"
output:
  type: stream
  description: AI 비교분석 결과 (스트리밍)
endpoint: https://www.xn--o80bk8isxeinax68f.com/api/sanction
method: POST
---

# AI 징계양정 비교분석

징계 상황을 설명하면, 유사한 노동위원회 판정례를 찾아 비교분석합니다.

## 특징
- 확률/점수/보장형 판단 제공하지 않음
- 유사 판정례 기반 근거 비교만 제공
- 실무자 검토를 전제로 한 보조 도구

## 사용 예시
```json
POST /api/sanction
{
  "messages": [
    {"role": "user", "content": "직원이 회사 물품을 횡령했습니다. 금액은 약 500만원이고 근속 5년차입니다. 해고가 정당할까요?"}
  ]
}
```

## 응답
스트리밍 텍스트: 유사 판정례 비교, 징계 수준 분석, 주의사항
