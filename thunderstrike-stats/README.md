# Thunderstrike-EU raiding trend (TBC Anniversary)

Weekly statistics from the fresh.warcraftlogs.com API for the **Thunderstrike** (EU, PvE) realm:

- **Raiding guilds per week**: exact count of guilds with at least one logged TBC raid that week.
- **Raiders per week**: estimated number of players in boss pulls, from a random sample of guild raid-weeks.
- **Phase markers**: the week each phase's raids first appear in Thunderstrike logs. The chart title names the current phase.

Output:

- `output/thunderstrike_raiding_trend.png`: the chart.
- `output/weekly_stats.csv`: the numbers behind it.

## Check progress

```sh
cd thunderstrike-stats/scripts
python3 progress.py            # one snapshot
python3 progress.py --watch    # refresh every 30 s (Ctrl-C to stop)
python3 progress.py --api      # also show the API points budget for this hour
```

It shows one bar per step and which step is running right now. It also shows the last log lines, including
"sleeping … for the hourly reset" while waiting for the API budget. The ETA is a rough guess, because the
waits for the API budget make the speed uneven.

## Start, stop, restart

```sh
cd thunderstrike-stats
./run_all.sh          # run in this terminal; Ctrl-C stops it
./run_all.sh --bg     # run in the background (survives closing the terminal), log in data/run_all.log
```

- **Resume after a crash, reboot or Ctrl-C:** run `./run_all.sh` again. Every step saves as it goes and skips
  work already in `data/`.
- **Stop a background run:** `pkill -f collect_guild_reports.py; pkill -f sample_players.py; pkill -f run_all.sh`
- `run_all.sh` refuses to start if a collection step is already running, so you can't start two copies by accident.
- **Start completely fresh:** delete `data/guilds.json`, `data/guilds_partial.json`,
  `data/guild_reports.jsonl` and `data/sample_players.jsonl`, then run `./run_all.sh`.
- **Only refresh the chart** (e.g. a week later, after re-collecting): `cd scripts && ../.venv/bin/python make_chart.py`.
  Add `--partial` to label it preliminary while collection is still running.
- **Add newer weeks later:** delete `data/guild_reports.jsonl` and `data/sample_players.jsonl` (keep `guilds.json`),
  then run `./run_all.sh`.

## Steps

| Step | Script | Writes | API cost |
|---|---|---|---|
| 1a. find guilds | `collect_guild_reports.py` | `data/guilds_partial.json` → `data/guilds.json` | ~650 points |
| 1b. guild reports since 2026-01-01 | `collect_guild_reports.py` | `data/guild_reports.jsonl` (one line per guild) | ~1.7 points / guild |
| 2. player sampling (8 guild-weeks / week) | `sample_players.py --per-week 8` | `data/sample_players.jsonl` | ~2 points / report |
| 3. chart + CSV | `make_chart.py` (run with `.venv/bin/python`, it needs matplotlib) | `output/` | none |

The API has **two** hourly limits:

- **Points:** 1,000 per hour. `rateLimitData` and `progress.py --api` show how many are used.
- **Database points:** a hidden limit that every *search* draws on (realm guild lists, guild report lists,
  rankings). Ranking pages use it up fastest. The API doesn't report its size. Looking up a single report by
  its code still works while it's empty. `progress.py --api` shows whether searches currently work.

When either limit runs out, the scripts sleep until the hourly reset and carry on by themselves. If the progress
display shows "PAUSED", the collection is waiting for the reset, not stuck. A full run can take many hours.

## How the numbers are made (and their limits)

- **Guilds:** the API lists at most 1,000 of Thunderstrike's ~2,260 guilds. The scan adds every guild found in the
  per-realm kill rankings of the first bosses of each raid: Attumen, Moroes, Maulgar, Magtheridon, Hydross,
  Void Reaver, Naj'entus and Rage Winterchill. Guilds that never killed any of those are missed unless they are in the first 1,000.
- **Raid zones** (fresh.warcraftlogs.com IDs): 1047 Karazhan, 1048 Gruul / Magtheridon, 1056 SSC / TK,
  1060 BT / Hyjal. These are set in `scripts/common.py` (`RAID_ZONES`). Add Zul'Aman and Sunwell when they release.
- **Weeks** start at the EU raid reset (Wednesday 05:00 UTC). The unfinished current week is left out.
- **Raiders:** distinct players in boss pulls (`friendlyPlayers` of encounter fights), not everyone in the log,
  which would include bystanders. Estimate = mean per sampled guild-week × number of raiding guild-weeks, with a
  90% bootstrap band. Someone who raids with two guilds in the same week counts twice, so it leans slightly high.
- **Only guild-tagged logs count.** Personal uploads that aren't attached to a guild, and anyone who never logs,
  are invisible. Read the chart as a trend, not a census.
- **Phases** (official dates for comparison): Phase 2 (SSC / TK) live 14 May 2026. Phase 3 (Black Temple / Hyjal)
  scheduled for 27 Aug 2026.

## Files

```
thunderstrike-stats/
  README.md          this file
  run_all.sh         start / resume everything
  scripts/
    common.py        API access (reuses ../recovered/tools/wcl.py and the .env credentials), pacing, zones, weeks
    collect_guild_reports.py, sample_players.py, make_chart.py, progress.py
  data/              downloaded data + logs (collect.log, sample.log, run_all.log)
  output/            chart + CSV
  .venv/             local Python 3.12 environment with matplotlib 3.10.3, for make_chart.py only. Recreate with:
                     /opt/homebrew/bin/python3.12 -m venv .venv && .venv/bin/pip install matplotlib==3.10.3
                     (matplotlib 3.10 crashes with endless recursion on Python 3.15)
```
