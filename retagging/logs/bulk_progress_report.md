# Bulk Retagging 진행 현황

## 배치 현황

| 주제군 | 전체 | 샘플 완료 | 신규 배치 | 배치 수 | reviewed |
|--------|------|----------|----------|---------|----------|
| probation | 2,049 | 20 | 974 | 33 | 0 |
| incompetence | 342 | 20 | 322 | 11 | 0 |
| absence | 2,424 | 20 | 980 | 33 | 0 |
| violence | 2,205 | 20 | 977 | 33 | 0 |
| workplace_bullying | 1,642 | 20 | 979 | 33 | 0 |
| **합계** | **8,662** | **100** | **4,232** | **143** | **0** |

## 파이프라인 상태

- input 배치: 143개 준비 완료
- reviewed: 샘플 5개 (84건 고유)
- merged: merged_sample_v1.jsonl (84건, 충돌 0)
- 수동 판정: 5건 해소 (override 적용 완료)

## 다음 작업

웹: probation_batch_001 ~ 003부터 태깅 시작
클코: reviewed 파일 도착 시 validate → merge 실행
