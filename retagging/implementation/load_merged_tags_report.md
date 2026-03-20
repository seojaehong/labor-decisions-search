# Load Merged Tags Report

- input: `C:\dev\labor-decisions-search\retagging\output\merged\merged_final_v1.jsonl`
- rows read: `5`
- mode: `dry-run`
- target table: `nlrc_decisions`
- snapshot version: `merged_final_v1`

## Primary Distribution

- `disciplinary_severity`: `3`
- `unfair_treatment`: `1`
- `work_ability`: `1`

## Sample Mapping

- `id_10479` -> primary `unfair_treatment`, stage `regular`
- `id_10509` -> primary `disciplinary_severity`, stage `regular`
- `id_10561` -> primary `disciplinary_severity`, stage `regular`

## Existing ID Check

- existing check unavailable: `{'message': "Could not find the table 'public.nlrc_decisions' in the schema cache", 'code': 'PGRST205', 'hint': "Perhaps you meant the table 'public.subsidy_exclusions'", 'details': None}`

## Dry-Run Result

- no DB writes executed
- rerun safe: `yes` (same snapshot payload can be re-applied)
