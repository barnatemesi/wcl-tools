#!/bin/bash
# Start or resume the whole pipeline: guild scan -> player sampling -> chart.
# Every step skips work already saved in data/, so it is safe to run again after a crash, reboot or Ctrl-C.
#
#   ./run_all.sh            run in this terminal (Ctrl-C stops; run again to resume)
#   ./run_all.sh --bg       run in the background, survives closing the terminal; watch with progress.py
set -euo pipefail
SELF="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
cd "$(dirname "$SELF")/scripts"

# only real python processes count (not shells or editors that merely mention the script names)
if pgrep -f "ython[0-9.]* (collect_guild_reports|sample_players)\.py" >/dev/null; then
    echo "Already running (see: python3 scripts/progress.py). Not starting a second copy."
    exit 1
fi

if [[ "${1:-}" == "--bg" ]]; then
    # caffeinate -i keeps the Mac from idle-sleeping until the run ends (closing the lid still sleeps it)
    nohup caffeinate -i "$SELF" > ../data/run_all.log 2>&1 &
    echo "Started in the background (pid $!), Mac kept awake while it runs. Progress: python3 scripts/progress.py --watch"
    exit 0
fi

echo "== 1. guild scan";      python3 collect_guild_reports.py >> ../data/collect.log 2>&1
echo "== 2. player sampling"; python3 sample_players.py        >> ../data/sample.log 2>&1
echo "== 3. chart";           ../.venv/bin/python make_chart.py
