"""Quick sanity summary of a combat log: boss pulls, and damage / healing per player for each pull.

usage: python3 summary.py <WoWCombatLog.txt> [--top N]

Use it to compare a rebuilt log against the WarcraftLogs page (numbers should be within a few %).
Pet damage is credited to the owner when the owner GUID is in the advanced-log block.
"""
import collections, csv, sys

DAMAGE = {"SWING_DAMAGE": 0, "RANGE_DAMAGE": 3, "SPELL_DAMAGE": 3, "SPELL_PERIODIC_DAMAGE": 3, "DAMAGE_SHIELD": 3}
HEAL = {"SPELL_HEAL", "SPELL_PERIODIC_HEAL"}
ADV = 18  # number of advanced-log fields after the spell prefix


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 10
    names, owners = {}, {}
    pull, dmg, heal = None, collections.Counter(), collections.Counter()

    def report():
        if pull is None:
            return
        secs = max(pull[2], 1)
        print("\n== %s  %s  (%dm%02ds)" % (pull[0], pull[1], secs // 60, secs % 60))
        for label, c in (("damage", dmg), ("effective healing", heal)):
            print("  %s:" % label)
            for guid, v in c.most_common(top):
                print("    %-30s %10d  %7.0f/s" % (names.get(guid, guid), v, v / secs))

    for line in open(sys.argv[1], encoding="utf-8"):
        stamp, body = line.rstrip("\n").split("  ", 1)
        row = next(csv.reader([body]))
        ev = row[0]
        if ev == "ENCOUNTER_START":
            pull = [row[2], "", 0]
            dmg, heal = collections.Counter(), collections.Counter()
            t0 = stamp
            continue
        if ev == "ENCOUNTER_END" and pull:
            h0, m0, s0 = map(float, t0.split(" ")[1].split(":"))
            h1, m1, s1 = map(float, stamp.split(" ")[1].split(":"))
            pull[1] = "KILL" if row[-1] == "1" else "wipe"
            pull[2] = int(((h1 - h0) * 3600 + (m1 - m0) * 60 + (s1 - s0)) % 86400)
            report()
            pull = None
            continue
        if len(row) < 9 or not pull:
            continue
        names[row[1]] = row[2]
        base = 9 + DAMAGE.get(ev, 3)
        if ev in DAMAGE or ev in HEAL:
            if row[base + 1] not in ("0000000000000000", ""):
                owners[row[base]] = row[base + 1]
            src = owners.get(row[1], row[1])
            amounts = row[base + ADV:]
            if ev in DAMAGE and row[5].startswith("Creature"):
                dmg[src] += int(amounts[0]) - max(int(amounts[2]), 0)
            elif ev in HEAL:
                heal[src] += int(amounts[0]) - int(amounts[2])


if __name__ == "__main__":
    main()
