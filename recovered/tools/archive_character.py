"""Archive every raid a character took part in as WoWCombatLog files, one report per raid night (resumable).

usage: python3 archive_character.py <name> [--server thunderstrike] [--region EU] [--out DIR]
                                          [--zones 1047,1048,1056,1060] [--keep-raw] [--dry-run]

- Lists the character's reports (the "Recent Reports" on its warcraftlogs page) in the given raid zones.
- Reports whose time ranges overlap are the same raid uploaded by several people: one is kept per group,
  the longest one, or the character's own upload (owner name starts with the first 5 letters of the character)
  if that is at least 90% as long.
- Each kept report is downloaded to raw/, converted into <out>/<zone>/WoWCombatLog-*.txt, and the raw dump is
  deleted again (unless --keep-raw, or it was already in raw/ before). Finished codes are recorded in
  <out>/archived.json, so running the same command again continues where it stopped.
- Waits for the hourly reset when the API points budget (1000/hour) is nearly spent.
"""
import argparse, json, subprocess, sys, time
from datetime import datetime
from pathlib import Path
import wcl, fetch

TOOLS = Path(__file__).resolve().parent
RAW = TOOLS.parent / "raw"
RAID_ZONES = "1047,1048,1056,1060"  # fresh.warcraftlogs.com: Karazhan, Gruul/Mag, SSC/TK, BT/Hyjal
POINTS_SAFETY = 950

_query, _calls = wcl.query, [0]


def _wait_for_reset(reason):
    rl = _query("{ rateLimitData { pointsSpentThisHour pointsResetIn } }")["rateLimitData"]
    wait = rl["pointsResetIn"] + 15
    print("[%s] %s (%.0f points spent), waiting %ds for the hourly reset" % (
        datetime.now().strftime("%H:%M"), reason, rl["pointsSpentThisHour"], wait), flush=True)
    deadline = time.time() + wait  # wall clock: time.sleep() stops counting while a Mac sleeps
    while time.time() < deadline:
        time.sleep(min(30, max(0, deadline - time.time())))


def paced_query(gql, variables=None, retries=5):
    """wcl.query that checks the points budget every 10 calls and waits for the reset when it runs out."""
    _calls[0] += 1
    if _calls[0] % 10 == 1:
        spent = _query("{ rateLimitData { pointsSpentThisHour } }")["rateLimitData"]["pointsSpentThisHour"]
        if spent > POINTS_SAFETY:
            _wait_for_reset("budget nearly spent")
    for _ in range(3):
        try:
            return _query(gql, variables, retries)
        except Exception as e:
            if "429" not in str(e) and "points" not in str(e).lower():
                raise
            _wait_for_reset("API rate limit hit")
    return _query(gql, variables, retries)


wcl.query = paced_query  # fetch.py calls wcl.query


def list_reports(name, server, region):
    q = '''query($p:Int){ characterData { character(name:"%s", serverSlug:"%s", serverRegion:"%s") {
      recentReports(limit:100, page:$p) { last_page data { code title startTime endTime zone { id name } owner { name } } }
    } } }''' % (name, server, region)
    reports, page = [], 1
    while True:
        c = wcl.query(q, {"p": page})["characterData"]["character"]
        if c is None:
            sys.exit("character %s-%s (%s) not found" % (name, server, region))
        rr = c["recentReports"]
        reports += rr["data"]
        if page >= (rr["last_page"] or 1):
            return reports
        page += 1


def pick_per_night(reports, name):
    """Group overlapping reports (same raid, several uploaders) and keep one per group."""
    groups = []
    for r in sorted(reports, key=lambda r: r["startTime"]):
        if groups and r["startTime"] < max(x["endTime"] for x in groups[-1]):
            groups[-1].append(r)
        else:
            groups.append([r])
    own = name[:5].lower()
    dur = lambda r: r["endTime"] - r["startTime"]
    picks = []
    for g in groups:
        # the most complete upload; the character's own one if it is at least 90% as long
        full = [r for r in g if dur(r) >= 0.9 * max(map(dur, g))]
        best = max(full, key=lambda r: (r["owner"]["name"].lower().startswith(own), dur(r)))
        span = max(r["endTime"] for r in g) - min(r["startTime"] for r in g)
        picks.append((best, len(g), (best["endTime"] - best["startTime"]) / span))
    return picks


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("name"); ap.add_argument("--server", default="thunderstrike"); ap.add_argument("--region", default="EU")
    ap.add_argument("--out"); ap.add_argument("--zones", default=RAID_ZONES)
    ap.add_argument("--keep-raw", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    out = Path(a.out) if a.out else TOOLS.parent / a.name.lower()
    zones = {int(z) for z in a.zones.split(",")}

    reports = [r for r in list_reports(a.name, a.server, a.region) if (r["zone"] or {}).get("id") in zones]
    picks = pick_per_night(reports, a.name)
    state_path = out / "archived.json"
    done = json.loads(state_path.read_text()) if state_path.exists() else {}
    print("%s: %d raid reports -> %d raid nights, %d already archived" % (a.name, len(reports), len(picks), len(done)))
    for n, (r, group, cover) in enumerate(picks, 1):
        print("%3d. %s %-21s %-18s %4.1fh  %s%s%s" % (
            n, datetime.fromtimestamp(r["startTime"] / 1000).strftime("%Y-%m-%d %H:%M"), r["zone"]["name"],
            r["owner"]["name"], (r["endTime"] - r["startTime"]) / 3.6e6, r["code"],
            "  (%d uploads)" % group if group > 1 else "",
            "  covers %.0f%% of the night" % (100 * cover) if cover < 0.9 else ""))
    if a.dry_run:
        return

    out.mkdir(parents=True, exist_ok=True)
    for n, (r, _, _) in enumerate(picks, 1):
        code = r["code"]
        if code in done:
            continue
        raw = RAW / (code + ".json")
        cached = raw.exists()
        print("\n[%s] %d/%d %s %s" % (datetime.now().strftime("%H:%M"), n, len(picks), code, r["title"]), flush=True)
        if not cached:
            fetch.fetch(code, raw)
        res = subprocess.run([sys.executable, str(TOOLS / "convert.py"), str(raw), str(out)],
                             check=True, capture_output=True, text=True)
        files = [l.split(": ", 1)[0] for l in res.stdout.splitlines() if "WoWCombatLog-" in l]
        print(res.stdout.strip(), flush=True)
        if not cached and not a.keep_raw:
            raw.unlink()
        done[code] = {"title": r["title"], "start": r["startTime"], "owner": r["owner"]["name"], "output": files}
        state_path.write_text(json.dumps(done, indent=1))
    print("\nall %d raid nights archived in %s" % (len(picks), out))


if __name__ == "__main__":
    main()
