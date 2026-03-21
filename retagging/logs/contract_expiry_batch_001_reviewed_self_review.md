# contract_expiry_batch_001_reviewed 2nd-pass self-review

- 배치: `contract_expiry_batch_001_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `2000부노OOO` [unfair_treatment]
  - 변경: notes, secondary:[]→['renewal_expectation']
  - notes: 근로계약기간 종료에 따라 근로관계가 당연 종료된다고 판단한 사례 — 부당노동행위(불이익취급·지배개입) 여부가 핵심
- `2016차별OOO` [discrimination]
  - 변경: notes
  - notes: 공무원인 시간제기간제교원도「기간제 및 단시간근로자 보호 등에 관한 법률」적용을 받고, 정교사에 비해 호봉 및 급여 등에 있어 불리한 처우를 한 
- `2017차별OOO` [discrimination]
  - 변경: notes
  - notes: 기간제근로자에 대해 사택수당 및 휴일보전수당을 미지급한 것과, 파견근로자에 대해 가족수당, 휴일보전수당 및 하계휴가비를 미지급하거나 적게 지급한
- `2018부해OOO` [renewal_expectation]
  - 변경: notes
  - notes: 당사자 간의 근로관계는 계약기간 만료로 종료되었고, 근로자에게 근로계약에 대한 갱신기대권이 형성되었다고 볼 수 없다고 판정한 사례 — 갱신기대권
- `2019차별OOO` [discrimination]
  - 변경: notes
  - notes: 비교대상근로자가 존재하지 않는다고 판정한 사례 — discrimination 판단이 핵심

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
