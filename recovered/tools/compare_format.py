"""Compare the field count of every event type between a real combat log and a rebuilt one.

usage: python3 compare_format.py <real WoWCombatLog.txt> <rebuilt WoWCombatLog.txt> [--all]

Flags event types whose rebuilt field counts are not all seen in the real log. Some differences are
legitimate (e.g. miss variants the real log happens not to contain), so read the flagged ones by hand.
"""
import collections, csv, sys


def shape(path):
    out = collections.defaultdict(collections.Counter)
    for line in open(path, encoding="utf-8"):
        body = line.rstrip("\n").split("  ", 1)[-1]
        row = next(csv.reader([body]))
        if row[0] != "COMBATANT_INFO":  # contains nested () / [] lists, field count is meaningless
            out[row[0]][len(row)] += 1
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    real, rebuilt = shape(sys.argv[1]), shape(sys.argv[2])
    for k in sorted(set(real) | set(rebuilt)):
        ka, kb = set(real.get(k, {})), set(rebuilt.get(k, {}))
        mismatch = ka and kb and not kb <= ka
        if mismatch or "--all" in sys.argv:
            print("%-28s real=%s rebuilt=%s%s" % (k, sorted(ka), sorted(kb), "   <-- CHECK" if mismatch else ""))
    only_real = sorted(set(real) - set(rebuilt))
    if only_real:
        print("event types only in the real log (not recoverable from WCL):", ", ".join(only_real))


if __name__ == "__main__":
    main()
