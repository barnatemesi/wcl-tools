"""Print WarcraftLogs' own damage-done / healing table for one fight, to cross-check summary.py output.

usage: python3 wcl_table.py <report code or URL> <fight id> [--top N]
"""
import sys
import wcl

Q = """query($c:String,$f:[Int],$t:TableDataType){ reportData { report(code:$c) {
  fights(fightIDs:$f) { name kill startTime endTime }
  table(fightIDs:$f, dataType:$t) } } }"""


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    code, fight = wcl.report_code(sys.argv[1]), int(sys.argv[2])
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 10
    for label, kind in (("damage", "DamageDone"), ("effective healing", "Healing")):
        r = wcl.query(Q, {"c": code, "f": [fight], "t": kind})["reportData"]["report"]
        f = r["fights"][0]
        secs = (f["endTime"] - f["startTime"]) / 1000
        if label == "damage":
            print("== %s  %s  (%dm%02ds)" % (f["name"], "KILL" if f["kill"] else "wipe", secs // 60, secs % 60))
        print("  %s:" % label)
        rows = sorted(r["table"]["data"]["entries"], key=lambda e: -e["total"])[:top]
        for e in rows:
            print("    %-30s %10d  %7.0f/s" % (e["name"], e["total"], e["total"] / secs))


if __name__ == "__main__":
    main()
