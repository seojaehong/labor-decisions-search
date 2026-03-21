# sexual_harassment_batch_010_reviewed 2nd-pass self-review

- 배치: `sexual_harassment_batch_010_reviewed`
- 2차 패스 처리 건수: 50
- 실질 변경 건수: 50
- 개선 항목: notes(holding_points 기반), retrieval_note, secondary, confidence

## 변경 대표 사례
- `id_405629` [misconduct]
  - 변경: notes
  - notes: 사원1에 대한 근로자의 '신체접촉 행위’, '늦은 시간 자택 방문’, '필라테스 복장 사진 요구’, '이성 관계에 대한 발언’ 등은 징계사유로 
- `id_405751` [misconduct]
  - 변경: notes
  - notes: 사용자에게 합병에 따라 고용 승계한 근로자의 비위 행위에 대한 징계권이 인정되고, 공소시효가 완성된 행위에 대해서도 징계할 수 있으며, 징계의 
- `id_405843` [misconduct]
  - 변경: notes
  - notes: 근로자에 대한 직장 내 성희롱 발생 사실과 적절한 조치에 대한 근로자의 일부 요청이 확인되고, 사업주는 재택근무 부여 등의 조치를 하였으므로 근
- `id_405895` [disciplinary_severity]
  - 변경: notes
  - notes: 이 사건 징계는 관리 감독책임이 있는 근로자가 관리하던 점포 소속 여직원을 성희롱한 사건으로 징계사유가 존재하고, 신체 접촉을 동반한 언어적 성
- `id_406119` [misconduct]
  - 변경: notes, secondary:['procedure', 'disciplinary_severity']→['procedure', 'disciplinary_severity', 'unfair_treatment']
  - notes: 단체협약 전문 및 일부 조항은 공정대표의무를 위반하였고, 단체교섭 과정에서 잠정합의안을 제공하는 등 정보를 제공하고 의견을 수렴한 것으로 보아 

## 일관성 메모
- notes: holding_points 기반 사건별 생성 (템플릿 제거)
- confidence: genuine ambiguity 키워드 있을 때만 medium, 기본 high
- secondary: holding_points + source_text 양쪽 기반 보강
