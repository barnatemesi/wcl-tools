"""Compare top vs median DPS parses per spec (from fetch_rankings.py) and list what the top players do differently.

usage: python3 guides/tools/best_rotation.py [--encounter 50607] [--out guides/best-rotations]

Writes <out>/<encounter>.md: per spec, the top players' rotation (casts/min and damage share per ability, next to
the median group), active time, debuff / cooldown / consumable uptimes, the usual opener, and an automatic list of
the biggest differences. Medians are used throughout so one odd parse doesn't skew a group.
"""
import argparse, collections, json, re, statistics
from pathlib import Path
from trash_guide import slug

GUIDES = Path(__file__).resolve().parents[1]
RAW = GUIDES.parent / "recovered" / "raw" / "rankings"
GCD_MS = 1500
AUTO = {"Melee", "Auto Shot", "Shoot"}
OPENER = 8
ALIASES = {"Seal of Blood": "Seal of Blood / the Martyr", "Seal of the Martyr": "Seal of Blood / the Martyr",
           "Judgement of Blood": "Judgement of Blood / the Martyr", "Judgement of the Martyr": "Judgement of Blood / the Martyr"}
COOLDOWN_PER_FIGHT = 2.5  # used at most this often per fight: compare uses per fight, not per minute
RACIALS = {"Blood Fury", "Berserking", "Arcane Torrent", "Stoneform", "Will of the Forsaken", "Perception",
           "Gift of the Naaru", "War Stomp", "Escape Artist", "Shadowmeld"}
# buffs the raid gives you: differences here are raid setup, not the player's rotation
EXTERNAL = re.compile(r"Bloodlust|Heroism|Drums|Power Infusion|Innervate|Blessing|Mark of the Wild|Gift of the Wild|"
                      r"Fortitude|Arcane Intellect|Arcane Brilliance|Spirit|Totem|Aura$|Inspiration|Ancestral|Earth Shield|"
                      r"Renew|Rejuvenation|Regrowth|Lifebloom|Prayer of Mending|Power Word|Unleashed Rage|Trueshot|"
                      r"Ferocious Inspiration|Leader of the Pack|Moonkin Aura|Battle Shout|Commanding Shout|Blood Pact|"
                      r"Shadow Protection|Thorns|Misery|Vampiric|Totem of Wrath|Wrath of Air|Windfury|Grace of Air|"
                      r"Strength of Earth|Mana Spring|Improved|Heroic Presence|Sanctity|Divine Spirit|Fear Ward|Shadowform")
CONSUMABLE = re.compile(r"Flask|Elixir|Well Fed|Potion|Haste|Destruction|Super |Draenic|Pipeweed|Scroll|Oil|Stone|"
                        r"Bloodthistle|Mana Rune|Dark Rune|Insane Strength|Heroic Potion")


def med(xs):
    return statistics.median(xs) if xs else 0


def union(iv):
    total, end = 0, None
    for a, b in sorted(iv):
        if end is None or a > end:
            total += b - a; end = b
        elif b > end:
            total += b - end; end = b
    return total


def parse(path):
    d = json.loads(path.read_text())
    r = d["ranking"]
    name, secs = r["name"], r["duration"] / 1000
    names, dmg, casts = {}, collections.Counter(), collections.Counter()
    for e in d["dmg"]["data"].get("entries", []):
        label = ALIASES.get(e["name"], e["name"]) if e.get("actorName") == name else "(pet / guardian)"  # pets: one entry
        dmg[label] += e["total"]
        names[e.get("guid")] = e["name"]
    me = None
    for e in d["casts"]["data"].get("entries", []):
        if e.get("actorName", name) == name:
            casts[ALIASES.get(e["name"], e["name"])] += e["total"]
            names[e.get("guid")] = ALIASES.get(e["name"], e["name"])
            me = e.get("actor", me)
    total = sum(dmg.values()) or 1
    # active time: own casts only; cast-time spells from begincast, instants one GCD
    begins, busy, order = {}, [], []
    for e in sorted(d["events"]["data"], key=lambda e: e["timestamp"]):
        if me is not None and e.get("sourceID") != me:
            continue
        n = names.get(e.get("abilityGameID"), str(e.get("abilityGameID")))
        if e["type"] == "begincast":
            begins[n] = e["timestamp"]
        elif e["type"] == "cast" and n not in AUTO:
            b = begins.pop(n, None)
            b = b if b is not None and e["timestamp"] - b < 10000 else e["timestamp"]
            busy.append((b, max(e["timestamp"], b + GCD_MS)))
            order.append(n)
    up = lambda key: {a["name"]: min(1, a["totalUptime"] / r["duration"]) for a in d[key]["data"].get("auras", [])}
    return {"name": name, "dps": r["amount"], "secs": secs, "server": r["server"]["name"],
            "cpm": {n: c / (secs / 60) for n, c in casts.items()}, "uses": dict(casts), "share": {n: v / total for n, v in dmg.items()},
            "active": union(busy) / r["duration"], "buffs": up("buffs"), "debuffs": up("debuffs"),
            "opener": order[:OPENER], "self_cast": set(casts)}


def group_stats(ps):
    keys = lambda k: set().union(*(p[k] for p in ps))
    stat = lambda k: {n: (med([p[k].get(n, 0) for p in ps]), sum(1 for p in ps if p[k].get(n, 0) > 0) / len(ps)) for n in keys(k)}
    return {"n": len(ps), "dps": med([p["dps"] for p in ps]), "secs": med([p["secs"] for p in ps]),
            "active": med([p["active"] for p in ps]), "cpm": stat("cpm"), "uses": stat("uses"), "share": stat("share"),
            "buffs": stat("buffs"), "debuffs": stat("debuffs"), "self_cast": keys("self_cast"),
            "opener": [collections.Counter(p["opener"][i] for p in ps if len(p["opener"]) > i).most_common(1)[0][0]
                       for i in range(min(OPENER, max((len(p["opener"]) for p in ps), default=0)))]}


def differences(top, mid):
    """The automatic 'what median players do wrong' list, biggest first."""
    out = []
    g = lambda s, k, n: s[k].get(n, (0, 0))
    if top["active"] - mid["active"] >= 0.04:
        out.append((top["active"] - mid["active"], "**Less time casting:** median players are active %.0f%% of the fight vs %.0f%% "
                    "for the top: gaps between casts (moving, late reactions, clipping)." % (100 * mid["active"], 100 * top["active"])))
    flagged = set()  # abilities already reported, so their buff isn't reported a second time
    for n in set(top["cpm"]) | set(mid["cpm"]):
        if n in AUTO or n in RACIALS:
            continue
        (tc, tu), (mc, mu) = g(top, "cpm", n), g(mid, "cpm", n)
        (tn, _), (mn, _) = g(top, "uses", n), g(mid, "uses", n)
        before = len(out)
        if tu >= 0.75 and mu <= 0.5:
            out.append((tc + 1, "**Missing %s:** %.0f%% of top players cast it (%.1f/min), only %.0f%% of median players do." % (
                n, 100 * tu, tc, 100 * mu)))
        elif mu >= 0.5 and tu <= 0.25:
            out.append((mc + 0.5, "**Casting %s:** %.0f%% of median players use it (%.1f/min); %.0f%% of top players don't bother." % (
                n, 100 * mu, mc, 100 - 100 * tu)))
        elif max(tn, mn) <= COOLDOWN_PER_FIGHT:  # cooldowns: fight length would distort per-minute rates
            if tu >= 0.5 and tn - mn >= 0.75:
                out.append(((tn - mn) / 2, "**Fewer %s uses:** %.1f per fight for median players vs %.1f for the top." % (n, mn, tn)))
        elif tc >= 0.5 and tu >= 0.5 and mc < 0.7 * tc:
            out.append(((tc - mc) / 2, "**Too few %s:** %.1f/min for median players vs %.1f/min for the top." % (n, mc, tc)))
        elif mc >= 0.5 and mu >= 0.5 and mc > 1.5 * tc and mc - tc >= 0.5:
            out.append(((mc - tc) / 2, "**Too many %s:** %.1f/min for median players vs %.1f/min for the top." % (n, mc, tc)))
        if len(out) > before:
            flagged.add(n)
    for n in set(top["debuffs"]) | set(mid["debuffs"]):
        (tv, tu), (mv, mu) = g(top, "debuffs", n), g(mid, "debuffs", n)
        if tu >= 0.5 and tv - mv >= 0.15:
            out.append((tv - mv + 0.5, "**Lower %s uptime on the boss:** %.0f%% vs %.0f%% for the top." % (n, 100 * mv, 100 * tv)))
    for n in set(top["buffs"]) | set(mid["buffs"]):
        if EXTERNAL.search(n) or n in RACIALS:
            continue
        (tv, tu), (mv, mu) = g(top, "buffs", n), g(mid, "buffs", n)
        if n in flagged:
            continue
        if CONSUMABLE.search(n) and tu >= 0.6 and tu - mu >= 0.3:
            out.append((tu - mu, "**Skipping %s:** used by %.0f%% of top players, %.0f%% of median players." % (n, 100 * tu, 100 * mu)))
        elif n in top["self_cast"] and tu >= 0.6 and tv - mv >= 0.08:
            out.append((tv - mv, "**%s up less:** %.0f%% of the fight vs %.0f%% for the top (cooldown used late or not at all)." % (
                n, 100 * mv, 100 * tv)))
    return [t for _, t in sorted(out, reverse=True)]


def spec_md(spec, top, mid, summary):
    out = ["## %s" % spec.replace("-", " — "), "",
           "Top %d: median %.0f DPS, fight %.0f s. Median group (%d players around rank %d of the top %d listed): %.0f DPS, "
           "fight %.0f s." % (top["n"], top["dps"], top["secs"], mid["n"], summary["median_rank"], summary["total"], mid["dps"],
                             mid["secs"]), ""]
    diffs = differences(top, mid)
    if diffs:
        out += ["**What the median players do differently:**", ""] + ["- " + d for d in diffs[:8]] + [""]
    out += ["| Ability | Top casts/min | Median casts/min | Top % dmg | Median % dmg |", "|---|---|---|---|---|"]
    names = sorted(set(top["cpm"]) | set(top["share"]),
                   key=lambda n: -(top["share"].get(n, (0,))[0] * 10 + top["cpm"].get(n, (0,))[0]))
    for n in names[:14]:
        tc, mc = top["cpm"].get(n, (0, 0))[0], mid["cpm"].get(n, (0, 0))[0]
        ts, ms = top["share"].get(n, (0, 0))[0], mid["share"].get(n, (0, 0))[0]
        if tc < 0.05 and ts < 0.005:
            continue
        f = lambda x, fmt: fmt % x if x else "–"
        out.append("| %s | %s | %s | %s | %s |" % (n + (" (racial)" if n in RACIALS else ""), f(tc, "%.1f"), f(mc, "%.1f"), f(100 * ts, "%.0f%%"), f(100 * ms, "%.0f%%")))
    out += ["", "- **Active time:** top %.0f%%, median %.0f%%." % (100 * top["active"], 100 * mid["active"]),
            "- **Usual opener (top):** " + " → ".join(top["opener"])]
    debs = [(n, v, mid["debuffs"].get(n, (0, 0))[0]) for n, (v, u) in top["debuffs"].items() if u >= 0.5 and v >= 0.1]
    if debs:
        out.append("- **Debuffs on the boss** (top / median): " + ", ".join(
            "%s %.0f%% / %.0f%%" % (n, 100 * v, 100 * m) for n, v, m in sorted(debs, key=lambda x: -x[1])))
    own = [(n, v, u, mid["buffs"].get(n, (0, 0))) for n, (v, u) in top["buffs"].items()
           if not EXTERNAL.search(n) and u >= 0.5 and (n in top["self_cast"] or CONSUMABLE.search(n))]
    if own:
        out.append("- **Own cooldowns / consumables** (uptime top / median, share of players using it top / median): " + ", ".join(
            "%s %.0f%% / %.0f%% (%.0f%% / %.0f%%)" % (n, 100 * v, 100 * m[0], 100 * u, 100 * m[1])
            for n, v, u, m in sorted(own, key=lambda x: -x[1])[:10]))
    ext = [(n, v, mid["buffs"].get(n, (0, 0))[0]) for n, (v, u) in top["buffs"].items() if EXTERNAL.search(n) and v >= 0.2]
    if ext:
        out.append("- **Raid buffs they had** (uptime top / median, not under the player's control): " + ", ".join(
            "%s %.0f%% / %.0f%%" % (n, 100 * v, 100 * m) for n, v, m in sorted(ext, key=lambda x: -x[1])[:8]))
    return out + [""]


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("--encounter", type=int, default=50607)
    ap.add_argument("--out", default=str(GUIDES / "best-rotations"))
    a = ap.parse_args()
    base = RAW / str(a.encounter)
    body, toc = [], []
    boss = None
    for spec_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        groups = {g: [parse(f) for f in sorted((spec_dir / g).glob("*.json"))] for g in ("top", "mid")}
        if not groups["top"] or not groups["mid"]:
            continue
        boss = boss or json.loads(next((spec_dir / "top").glob("*.json")).read_text())["ranking"].get("encounterName")
        summary = json.loads((spec_dir / "summary.json").read_text())
        body += spec_md(spec_dir.name, group_stats(groups["top"]), group_stats(groups["mid"]), summary)
        toc.append("[%s](#%s)" % (spec_dir.name.replace("-", " — "), slug(spec_dir.name.replace("-", " — "))))
    head = ["# Best rotations: encounter %d" % a.encounter, "",
            "Built by `guides/tools/best_rotation.py` from fresh.warcraftlogs.com DPS rankings (TBC Anniversary), via "
            "`fetch_rankings.py`. *Top* = the best-ranked players for the spec; *median* = players around the middle of the "
            "ranking list the API exposes (its top 2000 parses), so they are decent players, not the bottom. Casts/min use the "
            "fight length; *active* is the share of the fight spent casting or on the GCD (channels count as one GCD). The "
            "difference list is automatic: read it as where to look, not as a verdict.", "", "Specs: " + ", ".join(toc), ""]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    path = out / ("%d.md" % a.encounter)
    path.write_text("\n".join(head + body), encoding="utf-8")
    print("%s: %d specs" % (path, len(toc)))


if __name__ == "__main__":
    main()
