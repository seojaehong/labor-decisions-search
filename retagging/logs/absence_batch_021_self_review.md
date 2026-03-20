# absence_batch_021 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 13 |
| absence_without_leave | 9 |
| dismissal_validity | 3 |
| transfer_validity | 2 |
| procedure | 1 |
| workplace_harassment | 1 |
| worker_status | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 29 |
| medium | 1 |

## 대표 보정 사례 (2~3건)
- id_28201: absence legacy bucket -> absence_without_leave / 5일 이상 무단결근이 직접적인 징계해고 사유인 전형적 결근 사건.
- id_28241: absence legacy bucket -> dismissal_validity / 진정한 복직명령이 있었고, 복직명령 불응은 구제이익을 소멸시키는 사정일 뿐이다.
- id_28937: absence legacy bucket -> transfer_validity / 배치전환이 정당하고, 그에 대한 업무거부와 무단결근까지 결합되어 해고도 정당한 사건.

## 특이 사항
- exclusion_flags 사용 건수: 23건
- notes 기재 건수: 30건
- medium confidence: 1건
