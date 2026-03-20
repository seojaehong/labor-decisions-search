from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
import subprocess

ROOT = Path('/mnt/c/dev/labor-decisions-search/retagging')
LOGS = ROOT / 'logs'
ORCH = LOGS / 'orchestrator'
STATE = ORCH / 'SHARED_STATUS.md'
AGENTS = ORCH / 'AGENTS_TO_PM.md'
COLLISIONS = LOGS / 'merge_collisions_report.md'
CURRENT = LOGS / 'current_status.md'
DATA = LOGS / 'status_dashboard_data.json'
PM_NOTE = ORCH / 'PM_WATCHDOG.md'


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''


def latest_mtime(paths):
    mts = []
    for p in paths:
        if p.exists():
            mts.append(p.stat().st_mtime)
    return max(mts) if mts else 0


def extract_collision_count(text: str) -> str:
    for line in text.splitlines():
        if '충돌 건수:' in line:
            return line.split(':', 1)[1].strip()
    return 'unknown'


def extract_shared_metrics(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('- merged:'):
            out['merged'] = s.split(':', 1)[1].strip()
        elif s.startswith('- 충돌:'):
            out['collisions'] = s.split(':', 1)[1].strip()
        elif s.startswith('- override:'):
            out['override'] = s.split(':', 1)[1].strip()
        elif s.startswith('- 진행률:'):
            out['progress'] = s.split(':', 1)[1].strip()
    return out


def main():
    # always refresh dashboard first
    subprocess.run(['python3', str(ROOT / 'scripts' / 'update_status_dashboard.py')], check=False)

    state_text = read_text(STATE)
    agents_text = read_text(AGENTS)
    coll_text = read_text(COLLISIONS)
    data = {}
    if DATA.exists():
        try:
            data = json.loads(DATA.read_text(encoding='utf-8'))
        except Exception:
            data = {}

    note = []
    note.append('# PM_WATCHDOG')
    note.append('')
    note.append(f'- updated_at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    note.append(f'- shared_status_seen: {STATE.exists()}')
    note.append(f'- agents_to_pm_seen: {AGENTS.exists()}')
    note.append(f'- merge_collisions_seen: {COLLISIONS.exists()}')
    note.append(f'- collision_count: {extract_collision_count(coll_text)}')
    metrics = extract_shared_metrics(state_text)
    for k in ['merged', 'override', 'progress', 'collisions']:
        if k in metrics:
            note.append(f'- {k}: {metrics[k]}')
    if data:
        note.append(f"- dashboard_reviewed_records: {data.get('reviewed_record_count')}")
        note.append(f"- dashboard_merged_records: {data.get('merged_record_count')}")
        note.append(f"- dashboard_override_count: {data.get('override_count')}")
    # light signals only
    if 'PM Check Needed' in state_text:
        note.append('- signal: PM Check Needed section present in SHARED_STATUS.md')
    if '### Waiting / Blocked' in agents_text or 'needs_from_pm' in agents_text:
        note.append('- signal: AGENTS_TO_PM contains blocked/waiting entries')
    note.append('')
    note.append('## Rule')
    note.append('- PM watchdog refreshes dashboard/state visibility only. Collision adjudication and override edits remain explicit PM actions.')
    PM_NOTE.write_text('\n'.join(note) + '\n', encoding='utf-8')

    # refresh current_status timestamp-ish note without destroying manual content
    current = read_text(CURRENT)
    marker = '## Watchdog\n'
    extra = f"## Watchdog\n- last_watchdog_refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    if marker in current:
        current = current.split(marker, 1)[0].rstrip() + '\n\n' + extra
    else:
        current = current.rstrip() + '\n\n' + extra
    CURRENT.write_text(current + ('\n' if not current.endswith('\n') else ''), encoding='utf-8')

if __name__ == '__main__':
    main()
