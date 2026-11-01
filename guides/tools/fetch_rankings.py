"""Download top and median DPS parses per class / spec for a boss, for best_rotation.py (resumable, API-budget paced).

usage: python3 guides/tools/fetch_rankings.py [--encounter 50607] [--top 10] [--mid 10] [--specs Warlock-Destruction,Mage-Fire]

- "top" = the first N players on the encounter's DPS rankings; "mid" = N players around the median rank
  (the ranking's last page is found by doubling then bisecting; ~2 points per page).
- Per parse, one query (~6 points) fetches the player's damage by ability (pets included), casts by ability,
  buffs on them, their debuffs on enemies and their cast timeline, into
  recovered/raw/rankings/<encounter>/<Class>-<Spec>/<top|mid>/<report>-<fight>-<name>.json. Existing files are skipped.
- Shares the 1000 points/hour pacing of archive_character.py (importing it installs the paced wcl.query).
Encounter ids (fresh, BT/Hyjal 1060): 50601 Naj'entus, 50602 Supremus, 50605 Bloodboil, 50607 Mother Shahraz.
"""
import argparse, json, math, re, sys
from pathlib import Path
RECOVERED = Path(__file__).resolve().parents[2] / "recovered"
sys.path.insert(0, str(RECOVERED / "tools"))  # wcl.py and archive_character.py live with the recovery tools
import wcl
import archive_character  # noqa: F401  (paces wcl.query to the hourly points budget)

OUT = RECOVERED / "raw" / "rankings"
SPECS = ["Druid-Balance", "Druid-Feral", "Hunter-BeastMastery", "Hunter-Marksmanship", "Hunter-Survival",
         "Mage-Arcane", "Mage-Fire", "Mage-Frost", "Paladin-Retribution", "Priest-Shadow", "Rogue-Assassination",
         "Rogue-Combat", "Rogue-Subtlety", "Shaman-Elemental", "Shaman-Enhancement", "Warlock-Affliction",
         "Warlock-Demonology", "Warlock-Destruction", "Warrior-Arms", "Warrior-Fury"]

RANKINGS = """query($e:Int,$c:String,$s:String,$p:Int){ worldData { encounter(id:$e) {
  characterRankings(className:$c, specName:$s, metric:dps, page:$p) } } }"""

PARSE = """query($c:String,$a:Float,$b:Float,$s:String,$t:String){ reportData { report(code:$c) {
  dmg: table(dataType: DamageDone, viewBy: Ability, startTime:$a, endTime:$b, filterExpression:$s)
  casts: table(dataType: Casts, viewBy: Ability, startTime:$a, endTime:$b, filterExpression:$s)
  buffs: table(dataType: Buffs, startTime:$a, endTime:$b, filterExpression:$t)
  debuffs: table(dataType: Debuffs, hostilityType: Enemies, startTime:$a, endTime:$b, filterExpression:$s)
  events(dataType: Casts, startTime:$a, endTime:$b, filterExpression:$s, limit: 10000) { data nextPageTimestamp }
} } }"""


def rankings_page(enc, spec, page, cache):
    path = cache / ("page-%d.json" % page)
    if path.exists():
        return json.loads(path.read_text())
    cls, sp = spec.split("-")
    r = wcl.query(RANKINGS, {"e": enc, "c": cls, "s": sp, "p": page})["worldData"]["encounter"]["characterRankings"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(r))
    return r


def last_page(enc, spec, cache):
    """Doubling then bisection on hasMorePages."""
    lo, hi = 1, 1
    while rankings_page(enc, spec, hi, cache).get("hasMorePages"):
        lo, hi = hi, hi * 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        r = rankings_page(enc, spec, mid, cache)
        if r.get("rankings"):
            lo = mid
        else:
            hi = mid - 1
    return lo


def quote(name):
    return '"%s"' % name.replace('"', '\\"')


def fetch_parse(r, path):
    rep = r["report"]
    a = r["startTime"] - rep["startTime"]
    n = quote(r["name"])
    d = wcl.query(PARSE, {"c": rep["code"], "a": a, "b": a + r["duration"],
                          "s": "source.name = %s or source.owner.name = %s" % (n, n),
                          "t": "target.name = %s" % n})["reportData"]["report"]
    d["ranking"] = r
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(d))


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("--encounter", type=int, default=50607)
    ap.add_argument("--top", type=int, default=10); ap.add_argument("--mid", type=int, default=10)
    ap.add_argument("--specs", default=",".join(SPECS))
    a = ap.parse_args()
    for spec in a.specs.split(","):
        base = OUT / str(a.encounter) / spec
        top = rankings_page(a.encounter, spec, 1, base / "pages")["rankings"]
        if len(top) < a.top + a.mid:
            print("%s: only %d ranked parses, skipped" % (spec, len(top)))
            continue
        last = last_page(a.encounter, spec, base / "pages")
        total = (last - 1) * 100 + len(rankings_page(a.encounter, spec, last, base / "pages")["rankings"])
        mid_rank = total // 2
        at = lambda rank: rankings_page(a.encounter, spec, math.ceil(rank / 100), base / "pages")["rankings"][(rank - 1) % 100]
        # walk outward from the median until a.mid distinct parses (API pages overlap at their edges)
        mid, seen, step = [], set(), 0
        while len(mid) < a.mid and step < 4 * a.mid:
            for rank in (mid_rank + step, mid_rank - step - 1):
                r = at(rank)
                key = (r["name"], r["report"]["code"], r["report"]["fightID"])
                if key not in seen and len(mid) < a.mid:
                    seen.add(key)
                    mid.append(r)
            step += 1
        (base / "summary.json").write_text(json.dumps({"total": total, "median_rank": mid_rank}))
        print("%s: %d ranked, median rank %d (%.0f dps), top %.0f dps" % (spec, total, mid_rank, at(mid_rank)["amount"],
                                                                          top[0]["amount"]), flush=True)
        for group, picks in (("top", top[:a.top]), ("mid", mid)):
            wanted = set()
            for r in picks:
                path = base / group / ("%s-%d-%s.json" % (r["report"]["code"], r["report"]["fightID"], re.sub(r"\W", "_", r["name"])))
                wanted.add(path.name)
                if not path.exists():
                    fetch_parse(r, path)
            for stale in (base / group).glob("*.json"):  # from an earlier, different selection
                if stale.name not in wanted:
                    stale.unlink()
        print("  done", flush=True)


if __name__ == "__main__":
    main()
