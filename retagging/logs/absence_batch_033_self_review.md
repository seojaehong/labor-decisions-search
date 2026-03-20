# absence_batch_033 Self-Review

## 배치 개요
- **입력**: 20건 (absence_batch_033.jsonl)
- **출력**: 20건 (absence_batch_033_reviewed.jsonl)
- **작업일**: 2026-03-20

## 무단결근 핵심 vs 배경 분류

### 결근이 핵심 사유 (8건)
| case_id | 요약 | issue_type_primary |
|---------|------|--------------------|
| id_348203 | 인사발령 거부 후 11일 무단결근 → 해고 정당 | absence_without_leave |
| id_348207 | 약 5개월 장기 무단결근 → 해고 정당 | absence_without_leave |
| id_348211 | 8일 이상 무단결근 → 해고 정당 | absence_without_leave |
| id_348397 | 22일 무단결근 → 징계해고 정당 | absence_without_leave |
| id_348555 | 장기결근 + 폭행 → 징계해고 정당 | absence_without_leave |
| id_34885 | 무단결근 → 해고 정당 + 부당노동행위 부정 | absence_without_leave |
| id_348913 | 1회 무단결근 → 정직6월 양정 과다 | absence_without_leave |

### 결근이 복합 사유 중 하나 (5건)
| case_id | 요약 | issue_type_primary |
|---------|------|--------------------|
| id_348269 | 무단이탈+결근+지시불이행 복합 | misconduct |
| id_348547 | 근무성적부진+직무태만+무단이탈, 양정과다 | disciplinary_severity |
| id_348663 | 인사명령 거부→결근→정직, 전보가 전제 | transfer_validity |
| id_348839 | 결근+교통법규위반+공갈+발령거부 복합 | misconduct |
| id_349003 | 결근+업무불이행+거래처 분쟁 복합 | misconduct |

### 결근이 배경사실 (not_really_absence_case) (7건)
| case_id | 요약 | 실질 쟁점 |
|---------|------|-----------|
| id_348237 | 건설현장 해고부존재, 결근은 자발적 퇴사 정황 | dismissal_validity |
| id_348303 | 근무태만·사고가 해고사유, 1일 불참은 경미 | dismissal_validity |
| id_348353 | 자택대기 지시 후 40일 무출근, 해고부존재·서면통지 | dismissal_validity |
| id_348451 | 결근신고의무위반은 징계사유 불인정, 상관모독이 핵심 | disciplinary_severity |
| id_348619 | 결근 중 계약만료, 해고부존재 | dismissal_validity |
| id_348721 | 하극상·폭행이 핵심, 근태불량은 부수 | misconduct |
| id_348885 | 갱신기대권 핵심, 근무태만은 증거 부족 불인정 | renewal_expectation |
| id_349009 | 갱신기대권 핵심, 무단지각은 배경 이력 중 하나 | renewal_expectation |

## 통계
- **absence_without_leave** primary: 7건 (35%)
- **not_really_absence_case** 플래그: 8건 (40%)
- **confidence high**: 20건 (100%)
- **decision_result 분포**: dismissed 9, granted 5, upheld 5, overturned 1

## 판단 근거 메모
- **id_348203**: 인사발령 배경이 있으나, 수차례 면담·복귀 독려 후에도 11일 무출근한 것이 결정적 사유로 작동 → 결근 핵심으로 분류
- **id_348663**: 인사명령 정당성 판단이 결근 판단의 전제 → transfer_validity가 primary이나, 결근이 직접적 징계사유이므로 not_really_absence_case 미적용
- **id_348839**: 운수업종(승무지시 거부). 결근이 복합 비위 중 하나이나 공갈·인사발령거부도 중요 → misconduct primary
- **id_348913**: 1회 결근으로 정직 6월은 회사 자체 근태가이드(무급+5%)와 큰 괴리 → 양정 과다의 좋은 레퍼런스

## 검수 필요 사항
- 없음. 전건 high confidence.
