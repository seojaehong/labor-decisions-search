# Load Merged Tags Report

- input: `retagging\output\merged\merged_final_v2.jsonl`
- rows read: `3923`
- mode: `dry-run`
- target table: `nlrc_decisions`
- snapshot version: `merged_final_v2`

## Primary Distribution

- `disciplinary_severity`: `1174`
- `dismissal_validity`: `763`
- `misconduct`: `432`
- `work_ability`: `313`
- `workplace_harassment`: `235`
- `procedure`: `232`
- `renewal_expectation`: `180`
- `absence_without_leave`: `175`
- `transfer_validity`: `158`
- `unfair_treatment`: `120`

## Sample Mapping

- `2017부해OOO` -> primary `misconduct`, stage `regular`
- `2022부노OOO` -> primary `unfair_treatment`, stage `regular`
- `id_10015` -> primary `misconduct`, stage `regular`

## Dry-Run Result

- no DB writes executed
- rerun safe: `yes` (same snapshot payload can be re-applied)
