from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

ROOT = Path('/mnt/c/dev/labor-decisions-search/retagging')
REVIEWED = ROOT / 'output' / 'reviewed'
MERGED = ROOT / 'output' / 'merged'
LOGS = ROOT / 'logs'
OVERRIDES = REVIEWED / 'manual_merge_overrides_v1.json'
STATUS_MD = LOGS / 'current_status.md'
HTML = ROOT / 'status_dashboard.html'
JSON_OUT = LOGS / 'status_dashboard_data.json'


def count_jsonl_records(path: Path) -> int:
    n = 0
    if not path.exists():
        return 0
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            n += 1
    return n


def latest_files(dir_path: Path, limit: int = 12):
    files = sorted(dir_path.glob('*.jsonl'), key=lambda p: p.stat().st_mtime, reverse=True)
    return [p.name for p in files[:limit]]


def parse_status(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith('상태:'):
            return line.split(':', 1)[1].strip()
    return '작업중'


def main():
    reviewed_files = sorted(REVIEWED.glob('*.jsonl'))
    merged_files = sorted(MERGED.glob('*.jsonl'))
    self_review_files = sorted(LOGS.glob('*_self_review.md'))

    reviewed_count = len(reviewed_files)
    reviewed_records = sum(count_jsonl_records(p) for p in reviewed_files)
    merged_count = len(merged_files)
    merged_records = sum(count_jsonl_records(p) for p in merged_files)
    override_count = 0
    if OVERRIDES.exists():
        override_count = len(json.loads(OVERRIDES.read_text(encoding='utf-8')).get('overrides', []))

    status_md = STATUS_MD.read_text(encoding='utf-8') if STATUS_MD.exists() else '상태: 작업중\n'
    status = parse_status(status_md)

    data = {
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': status,
        'reviewed_file_count': reviewed_count,
        'reviewed_record_count': reviewed_records,
        'merged_file_count': merged_count,
        'merged_record_count': merged_records,
        'override_count': override_count,
        'self_review_count': len(self_review_files),
        'recent_reviewed_files': latest_files(REVIEWED, 14),
        'root': str(ROOT),
    }
    JSON_OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    pills = ''.join(f'<span class="pill">{x}</span>' for x in [
        'output/reviewed/*.jsonl', 'logs/*_self_review.md', 'logs/merge_collisions_report.md',
        'output/reviewed/manual_merge_overrides_v1.json', 'output/merged/*.jsonl',
        'logs/merge_report.md', 'logs/validation_report.md'
    ])
    recent_rows = ''.join(f'<li>{name}</li>' for name in data['recent_reviewed_files']) or '<li>없음</li>'

    html = f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Retagging Status Dashboard</title>
  <style>
    :root {{ --bg:#0b1020; --panel:#121a2f; --panel2:#18223d; --text:#e8ecf6; --muted:#9aa6c1; --green:#3ddc97; --border:#243252; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,system-ui,sans-serif; background:linear-gradient(180deg,var(--bg),#0f1730 55%,#111a35); color:var(--text); padding:24px; }}
    .wrap {{ max-width:1200px; margin:0 auto; }}
    h1 {{ margin:0 0 8px; font-size:32px; }} .sub {{ color:var(--muted); margin-bottom:24px; }}
    .grid {{ display:grid; grid-template-columns:repeat(12,1fr); gap:16px; }}
    .card {{ background:rgba(18,26,47,.92); border:1px solid var(--border); border-radius:16px; padding:18px; box-shadow:0 8px 30px rgba(0,0,0,.22); }}
    .span-3 {{ grid-column:span 3; }} .span-4 {{ grid-column:span 4; }} .span-6 {{ grid-column:span 6; }} .span-8 {{ grid-column:span 8; }} .span-12 {{ grid-column:span 12; }}
    .label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }}
    .value {{ font-size:30px; font-weight:700; margin-top:8px; }}
    .status {{ display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px; background:rgba(61,220,151,.12); color:var(--green); border:1px solid rgba(61,220,151,.35); font-weight:700; }}
    .dot {{ width:10px; height:10px; border-radius:50%; background:currentColor; }}
    .pill {{ display:inline-block; padding:4px 8px; border-radius:999px; background:var(--panel2); border:1px solid var(--border); margin-right:6px; margin-bottom:6px; }}
    ul {{ margin:10px 0 0 18px; padding:0; }} li {{ margin:6px 0; }}
    code {{ background:var(--panel2); padding:2px 6px; border-radius:6px; color:#cfe0ff; }}
    .muted {{ color:var(--muted); }} .small {{ font-size:13px; color:var(--muted); margin-top:8px; }}
    @media (max-width:900px) {{ .span-3,.span-4,.span-6,.span-8,.span-12 {{ grid-column:span 12; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Retagging Status Dashboard</h1>
    <div class="sub">{data['root']} 기준 작업 상태창</div>
    <div class="grid">
      <div class="card span-3"><div class="label">현재 상태</div><div style="margin-top:10px" class="status"><span class="dot"></span>{data['status']}</div><div class="small">업데이트: {data['updated_at']}</div></div>
      <div class="card span-3"><div class="label">Reviewed 파일</div><div class="value">{data['reviewed_file_count']}</div><div class="small">records: {data['reviewed_record_count']}</div></div>
      <div class="card span-3"><div class="label">Merged 파일</div><div class="value">{data['merged_file_count']}</div><div class="small">records: {data['merged_record_count']}</div></div>
      <div class="card span-3"><div class="label">Override</div><div class="value">{data['override_count']}</div><div class="small">self-review: {data['self_review_count']}</div></div>

      <div class="card span-6">
        <div class="label">이 대시보드가 하는 일</div>
        <ul>
          <li>현재 작업 상태를 한 줄로 보여줌</li>
          <li>reviewed / merged / override 숫자를 파일 기준으로 계산</li>
          <li>최근 생성된 reviewed 파일 목록 표시</li>
          <li>내가 실제로 일하고 있는지, 멈췄는지 눈으로 확인 가능</li>
        </ul>
      </div>

      <div class="card span-6">
        <div class="label">자동 팔로우 대상</div>
        <div style="margin-top:10px">{pills}</div>
      </div>

      <div class="card span-6">
        <div class="label">최근 reviewed 파일</div>
        <ul>{recent_rows}</ul>
      </div>

      <div class="card span-6">
        <div class="label">상태 해석</div>
        <ul>
          <li><b>작업중</b>: 내가 같은 범위 안에서 다음 수를 계속 두는 중</li>
          <li><b>대기</b>: 새 input 또는 방향 지정이 필요함</li>
          <li><b>판정필요</b>: 충돌/예외에 대한 수동 판단이 필요함</li>
          <li><b>외부입력필요</b>: 네가 넘겨줘야 다음 단계로 갈 수 있음</li>
        </ul>
      </div>

      <div class="card span-12">
        <div class="label">반자동 갱신 방법</div>
        <div class="muted" style="margin-top:10px">
          이 페이지는 정적 HTML이지만, 아래 스크립트를 다시 실행하면 숫자를 파일 기준으로 재생성함.<br/><br/>
          <code>python3 /mnt/c/dev/labor-decisions-search/retagging/scripts/update_status_dashboard.py</code>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
'''
    HTML.write_text(html, encoding='utf-8')
    print('updated dashboard')

if __name__ == '__main__':
    main()
