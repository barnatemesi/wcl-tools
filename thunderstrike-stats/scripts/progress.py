"""Show progress of the data collection: one bar per step, what is running, and the latest log lines.

usage: python3 progress.py            (from thunderstrike-stats/scripts)
       python3 progress.py --watch    (refresh every 30 s, Ctrl-C to stop)
       python3 progress.py --api      (also show the API points budget; costs ~0 points)
"""
import json, os, re, subprocess, sys, time
from datetime import datetime, timedelta
from common import DATA, OUTPUT, read_jsonl

STEPS = ["collect_guild_reports.py", "sample_players.py", "make_chart.py"]
DISCOVERY = 9  # server list + 8 ranking encounters (see collect_guild_reports.DISCOVERY_ENCOUNTERS)


def bar(done, total, width=30):
    frac = done / total if total else 0
    fill = int(round(frac * width))
    return "[%s%s] %5.1f%%  %s/%s" % ("#" * fill, "-" * (width - fill), frac * 100, done, total)


def running():
    """Steps with a live python process (ignores shell loops that merely mention the script names)."""
    out = subprocess.run(["ps", "-axo", "command="], capture_output=True, text=True).stdout
    found = set()
    for line in out.splitlines():
        args = line.split()
        if args and "python" in os.path.basename(args[0]).lower():
            found.update(s for s in STEPS if any(a.endswith(s) for a in args[1:3]))
    return [s for s in STEPS if s in found]


def eta(path, done, total):
    """Rough time left from the file's age and how far along it is."""
    if not path.exists() or not done or done >= total:
        return ""
    started = path.stat().st_birthtime if hasattr(path.stat(), "st_birthtime") else path.stat().st_ctime
    per_item = (time.time() - started) / done
    left = per_item * (total - done)
    return "   ~%dh%02dm left" % (left // 3600, left % 3600 // 60)


def tail(path, n=2):
    if not path.exists():
        return []
    return [l for l in path.read_text().splitlines() if l.strip()][-n:]


def waiting_until(run):
    """If the running step's last log line is a budget sleep that hasn't ended yet, return the wake-up time."""
    log = DATA / ("sample.log" if "sample_players.py" in run else "collect.log")
    lines = tail(log, 1)
    m = re.match(r"\[(\d\d):(\d\d)\] .*sleeping (\d+)s", lines[0]) if lines else None
    if not m:
        return None
    now = datetime.now()
    slept_at = now.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0, microsecond=0)
    if slept_at > now:
        slept_at -= timedelta(days=1)
    wake = slept_at + timedelta(seconds=int(m.group(3)))
    return wake if wake > now else None


def show(api):
    print("Thunderstrike stats - %s" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    run = running()
    print("running now: %s" % (", ".join(run) if run else "nothing (use ./run_all.sh to start / resume)"))
    wake = waiting_until(run) if run else None
    if wake:
        print("status:      PAUSED - waiting for the hourly API budget reset, resumes by itself at ~%s"
              % wake.strftime("%H:%M"))

    partial, guilds_file = DATA / "guilds_partial.json", DATA / "guilds.json"
    if guilds_file.exists():
        guilds = json.loads(guilds_file.read_text())
        print("\n1a. find guilds        %s" % bar(DISCOVERY, DISCOVERY))
    else:
        state = json.loads(partial.read_text()) if partial.exists() else {"guilds": {}, "done": []}
        guilds = list(state["guilds"].values())
        print("\n1a. find guilds        %s   (%d guilds so far)" % (bar(len(state["done"]), DISCOVERY), len(guilds)))
    rep_file = DATA / "guild_reports.jsonl"
    reports = read_jsonl(rep_file)
    total = len(guilds) if guilds_file.exists() else 0
    print("1b. guild reports      %s%s" % (bar(len(reports), total or "?") if total else "[waiting for 1a]",
                                         eta(rep_file, len(reports), total)))

    sample_file = DATA / "sample_players.jsonl"
    sampled = read_jsonl(sample_file)
    goal = None
    for line in reversed(tail(DATA / "sample.log", 50)):
        if "sampled," in line:  # "N raid weeks, M guild-weeks total, S sampled, T to go"
            goal = int(line.split("sampled")[0].split(",")[-1])
            break
    print("2.  player sampling    %s%s" % (bar(len(sampled), goal) if goal else
                                         ("[waiting for 1b]" if not sampled else "%d guild-weeks" % len(sampled)),
                                         eta(sample_file, len(sampled), goal or 0)))
    png = OUTPUT / "thunderstrike_raiding_trend.png"
    print("3.  chart              %s" % ("done: %s (%s)" % (png, datetime.fromtimestamp(png.stat().st_mtime)
                                                              .strftime("%Y-%m-%d %H:%M")) if png.exists() else "not yet"))

    for name in ("collect.log", "sample.log"):
        lines = tail(DATA / name)
        if lines:
            print("\nlast lines of data/%s:" % name)
            for l in lines:
                print("   " + l[:160])
    if api:
        from common import wcl
        rl = wcl.query("{ rateLimitData { limitPerHour pointsSpentThisHour pointsResetIn } }")["rateLimitData"]
        print("\nAPI budget: %.0f / %d points used this hour, resets in %dm" %
              (rl["pointsSpentThisHour"], rl["limitPerHour"], rl["pointsResetIn"] // 60))
        # Searches (guild lists, guild reports, rankings) also draw on a hidden "database points" budget that
        # rateLimitData doesn't report; probe it with the smallest possible search.
        try:
            wcl.query('{ worldData { server(region:"EU", slug:"thunderstrike") { guilds(limit:1) { data { id } } } } }',
                      retries=1)
            print("database budget: available (searches work)")
        except RuntimeError as e:
            print("database budget: EMPTY - searches blocked until the hourly reset" if "database points" in str(e)
                  else "database budget: probe failed: %s" % str(e)[:100])


def main():
    api = "--api" in sys.argv
    if "--watch" not in sys.argv:
        return show(api)
    try:
        while True:
            os.system("clear")
            show(api)
            time.sleep(30)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
