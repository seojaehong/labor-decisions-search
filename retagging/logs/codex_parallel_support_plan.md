# Codex Parallel Support Plan

- 작성시각: 2026-03-20 21:47
- 전제: Claude가 잔여 배치 생산 담당, Codex는 QA/검수/통합 분석/병목 진단 담당

## 목표

Claude가 배치를 계속 생산하는 동안, 전체 결과물이 "한 사람이 끝까지 한 것처럼" 보이도록 아래 지원 업무를 병렬 진행한다.

## 작업축

### 1. 산출물 QA 추적

- 신규 reviewed + self-review가 생길 때마다 아래를 확인
  - `worker_status`, `procedure`, `confidence=medium` 과잉 여부
  - `exclusion_flags` 사용 일관성
  - `notes` 공란/설명력 부족 여부
- 결과는 기존 QA 문서에 누적
  - `logs/codex_crosscheck_review.md`
  - `logs/claude_rear_review.md`

### 2. 충돌 예방 규칙 정교화

- 새 배치가 쌓일수록 예상 충돌 패턴을 갱신
- 우선 감시 축
  - `misconduct` vs `disciplinary_severity`
  - `dismissal_validity` vs `procedure`
  - `dismissal_validity` vs `worker_status`
  - topic legacy vs 실제 판정축
- 결과는 `logs/predicted_collision_patterns.md`에 누적

### 3. override 품질 감시

- `manual_merge_overrides_v1.json`는 직접 수정하지 않고 품질 점검만 수행
- `자동 판정`, `원본 정보 부족` 사유 항목을 우선 watchlist로 관리
- 결과는 `logs/override_quality_review.md`에 누적

### 4. 로컬 앱 / 검색 / AI 체인 진단

- 실제 서비스 문제는 retagging 외에 `모델 + Supabase + 조회 경로` 병목이 함께 얽혀 있음
- 체크 항목
  - `/search` 응답 지연 원인
  - `/api/sanction` 지연 원인
  - retrieval 단계와 모델 호출 단계 분리 진단
  - Claude 생산분이 들어왔을 때 검색 품질이 실제로 좋아지는지 재테스트

### 5. PM 보고

- 큰 변화가 생기면 `logs/orchestrator/AGENTS_TO_PM.md`에 append
- 원칙: 말보다 실제 파일 기준으로 보고

## 현재 우선순위

1. 로컬 앱 병목 메모 정리
2. Claude 신규 배치 유입분 QA 추적
3. 충돌 패턴 갱신
4. override watchlist 보강

## 하지 않는 것

- reviewed JSONL 직접 수정
- merge/override 파일 직접 수정
- 새 배치 생산
- v1 문서 본문 수정
