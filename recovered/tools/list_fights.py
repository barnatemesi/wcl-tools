"""Show a report's title, date, zones, boss pulls and players without downloading events.

usage: python3 list_fights.py <report code or URL> [--trash]
"""
import sys
from datetime import datetime
import wcl

Q = """query($c:String){ reportData { report(code:$c) {
  title startTime endTime owner { name } guild { name server { name } }
  fights { id name encounterID kill fightPercentage size startTime endTime gameZone { name } }
  masterData { actors(type: "Player") { name server subType } } } } }"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    code = wcl.report_code(sys.argv[1])
    r = wcl.query(Q, {"c": code})["reportData"]["report"]
    if r is None:
        sys.exit("report %s not found" % code)
    t0 = r["startTime"]
    print("%s  [%s]  %s  owner=%s  guild=%s" % (r["title"], code, datetime.fromtimestamp(t0 / 1000).strftime("%Y-%m-%d %H:%M"),
                                              (r.get("owner") or {}).get("name"), (r.get("guild") or {}).get("name")))
    for f in r["fights"]:
        if not f["encounterID"] and "--trash" not in sys.argv:
            continue
        when = datetime.fromtimestamp((t0 + f["startTime"]) / 1000).strftime("%H:%M")
        dur = (f["endTime"] - f["startTime"]) // 1000
        result = "trash" if not f["encounterID"] else "KILL" if f["kill"] else "wipe %s%%" % round((f.get("fightPercentage") or 0))
        print("  #%-3d %s  %-28s %-14s %3dm%02ds  %s" % (f["id"], when, f["name"], result, dur // 60, dur % 60,
                                                       (f.get("gameZone") or {}).get("name")))
    players = r["masterData"]["actors"]
    print("players (%d): %s" % (len(players), ", ".join(sorted("%s-%s" % (p["name"], p["server"]) for p in players))))


if __name__ == "__main__":
    main()
