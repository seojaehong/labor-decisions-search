from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


INPUT_DIR = Path('evaluation/bigcase_bulk')
OUTPUT_FILE = INPUT_DIR / 'court_decisions_ready.jsonl'
RESULT_MAP = {
  '원고승': 'worker_win',
  '원고패': 'employer_win',
  '원고일부승': 'partial',
  '파기환송': 'remanded',
  '파기자판': 'reversed_and_decided',
  '각하': 'rejected',
  '화해': 'settled',
  '취하': 'withdrawn',
  '항소기각': 'appeal_dismissed',
  '상고기각': 'appeal_dismissed',
}


def normalize_case_number(case_number: str) -> str:
  return re.sub(r'\s+', '', case_number.strip())


def map_decision_result(result: str | None) -> str:
  normalized = (result or '').strip()
  if not normalized:
    return 'unknown'
  return RESULT_MAP.get(normalized, 'unmapped')


def clean_summary(summary: object) -> str:
  if isinstance(summary, str):
    text = summary
  else:
    text = json.dumps(summary, ensure_ascii=False)

  lines = []
  for raw_line in text.splitlines():
    line = re.sub(r'^#+\s*', '', raw_line).strip()
    if line:
      lines.append(line)

  cleaned = '\n'.join(lines)
  return cleaned[:2000]


def measure_full_text_length(full_text: object) -> int:
  if isinstance(full_text, str):
    return len(full_text)
  return len(json.dumps(full_text, ensure_ascii=False))


def iter_input_files() -> list[Path]:
  return sorted(INPUT_DIR.glob('*_details.jsonl'))


def main() -> None:
  input_files = iter_input_files()
  total = 0
  encoding_error_count = 0
  category_counts: Counter[str] = Counter()
  result_counts: Counter[str] = Counter()
  case_number_counts: Counter[str] = Counter()
  unmapped_value_counts: Counter[str] = Counter()

  OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

  with OUTPUT_FILE.open('w', encoding='utf-8') as output_handle:
    for input_file in input_files:
      with input_file.open('r', encoding='utf-8', errors='replace') as input_handle:
        for raw_line in input_handle:
          if not raw_line.strip():
            continue

          if '\ufffd' in raw_line:
            encoding_error_count += 1

          record = json.loads(raw_line)
          case_number = str(record.get('case_number', '')).strip()
          normalized_case_number = normalize_case_number(case_number)
          decision_result = map_decision_result(record.get('result'))
          category = str(record.get('category', '')).strip() or 'unknown'
          raw_result = str(record.get('result', '') or '').strip()

          transformed = {
            'id': f'court_{normalized_case_number}',
            'source': 'bigcase',
            'court': record.get('court'),
            'case_number': case_number,
            'title': record.get('title'),
            'date': record.get('date'),
            'case_type': record.get('case_type'),
            'decision_result': decision_result,
            'summary': clean_summary(record.get('summary')),
            'full_text_length': measure_full_text_length(record.get('full_text')),
            'keywords': record.get('keywords') if isinstance(record.get('keywords'), list) else [],
            'url': record.get('url'),
            'category': category,
          }

          output_handle.write(json.dumps(transformed, ensure_ascii=False) + '\n')

          total += 1
          category_counts[category] += 1
          result_counts[decision_result] += 1
          case_number_counts[case_number] += 1
          if decision_result == 'unmapped':
            unmapped_value_counts[raw_result or '<empty>'] += 1

  duplicate_case_numbers = sum(1 for count in case_number_counts.values() if count > 1)

  print(f'TOTAL {total}')
  print('CATEGORY_COUNTS')
  for category, count in sorted(category_counts.items()):
    print(f'  {category}: {count}')
  print('DECISION_RESULT_COUNTS')
  for result, count in sorted(result_counts.items()):
    print(f'  {result}: {count}')
  print('UNMAPPED_RESULT_COUNTS')
  if unmapped_value_counts:
    for result, count in sorted(unmapped_value_counts.items()):
      print(f'  {result}: {count}')
  else:
    print('  <none>: 0')
  print(f'ENCODING_ERRORS {encoding_error_count}')
  print(f'DUPLICATE_CASE_NUMBERS {duplicate_case_numbers}')
  print(f'OUTPUT {OUTPUT_FILE}')


if __name__ == '__main__':
  main()
