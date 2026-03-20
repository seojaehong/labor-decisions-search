# 재태깅 배치 상태 로그

## 샘플 배치 (2026-03-20)

| 배치 | 상태 | 건수 | high | medium | low | 비고 |
|------|------|------|------|--------|-----|------|
| probation_sample | done | 20 | 19 | 1 | 0 | 갱신기대권/사직 혼입 발견 |
| incompetence_sample | done | 20 | 20 | 0 | 0 | 60% 실제 다른 쟁점 |
| absence_sample | done | 20 | 17 | 3 | 0 | 실제 결근 핵심 2건뿐 |
| violence_sample | done | 20 | 19 | 1 | 0 | 징계양정(7)·비위(5) 핵심 |
| workplace_bullying_sample | done | 20 | 20 | 0 | 0 | 6건 과잉분류 방지 |

## 핵심 발견
- 기존 단일 태그 정확도 ~40%
- exclusion_flags 활용으로 노이즈 제어 가능 확인
- 태그 사전 v1 안정적 (enum 범위 내 출력)
- 서브에이전트 방식 안정적 (100건 에러 0)
