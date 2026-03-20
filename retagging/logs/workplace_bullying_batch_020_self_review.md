# workplace_bullying_batch_020 self review

## 처리 결과
- 입력: 30건
- 출력: 30건

## 분류 통계
| issue_type_primary | count |
|---|---:|
| disciplinary_severity | 14 |
| transfer_validity | 4 |
| misconduct | 4 |
| unfair_treatment | 2 |
| work_ability | 2 |
| dismissal_validity | 1 |
| procedure | 1 |
| workplace_harassment | 1 |
| renewal_expectation | 1 |

### confidence 분포
| confidence | count |
|---|---:|
| high | 26 |
| medium | 4 |

## 대표 보정 사례 (2~3건)
- id_406385: retaliation 드래프트 -> unfair_treatment / 인사평가결과 비공개는 징벌성이 없고 노조 관련 불이익 취급이 중심이다.
- id_406397: retaliation 드래프트 -> work_ability / 시용근로자 본채용 거부의 합리성 판단이 핵심이다.
- id_407233: disciplinary_severity 드래프트 -> workplace_harassment / 진술만으로는 괴롭힘 성립이 부족하다는 판단이 중심이다.

## 특이 사항
- `workplace_harassment` 관련 재검토가 많은 배치였고, `not_really_harassment_case`는 12건에 적용했다.
- secondary `retaliation`은 2건으로 남겼지만, 실제로는 전보·본채용 거부·계약해지 같은 다른 프레임이 핵심인 사건이 섞여 있었다.
- `4064xx~4072xx` 구간은 전보, 정직, 견책, 계약해지, 비위행위와 결합되어 있어 `disciplinary_severity`와 `transfer_validity`의 경계가 중요했다.
