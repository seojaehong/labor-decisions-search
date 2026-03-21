# Case Number Restore Summary

- Run date: 2026-03-21
- Source: `법제처_노동위결정문_전문.json`
- Script: `scripts/restore-case-numbers-from-source-json.js`

## Result

- Total rows scanned: 42,105
- Processed `id_*` case_number rows: 8,168
- Remaining `id_*` case_number rows: 0
- `holding_points < 100` rows after run: 1,225

## Notes

- This pass updated only `case_number`.
- `holding_points` was not modified.
- Failure log is empty for this run.
- Remaining short `holding_points` rows are still source-quality-limited exceptions from the earlier holding restore pass.
