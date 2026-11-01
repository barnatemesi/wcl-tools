"""Write a trash guide per zone (pack identity, kill order, positioning, what hits the raid) from raw/<code>.json dumps.

usage: python3 guides/tools/trash_guide.py recovered/raw/*.json [--out guides]

- A "pack" is a set of mob types killed together at the same spot (within PACK_RADIUS yd); the same pack pulled
  on several raid nights is merged.
- Kill order and raid markers come from death events; positions (yards) from the x/y on every event.
- Roles are guessed per player: healer if healing > damage, tank if they took >= TANK_SHARE of all mob melee hits,
  melee if most of their damage events are melee swings, otherwise ranged.
"""
import argparse, collections, json, math, re, statistics
from datetime import datetime
from pathlib import Path

PACK_RADIUS = 30
PACK_OVERLAP = 0.5  # min share of mob types two pulls must have in common to be the same pack
MIN_HP = 15000  # critters (toads, rats) are not trash
MIN_PULL_MS = 5000
AOE_COUNT = 3
AOE_WINDOW_S = 6
TANK_SHARE = 0.07
MARKERS = {1: "star", 2: "circle", 3: "diamond", 4: "triangle", 5: "moon", 6: "square", 7: "cross", 8: "skull"}
CC = {"Polymorph", "Shackle Undead", "Banish", "Freezing Trap Effect", "Sap", "Hibernate", "Seduction", "Fear",
      "Entangling Roots", "Repentance", "Scare Beast", "Mind Control", "Cyclone", "Turn Undead", "Turn Evil"}
ROLES = ("tank", "melee", "ranged", "healer")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def med(xs):
    return statistics.median(xs) if xs else None


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 100


def src_key(e):
    return e.get("sourceID"), e.get("sourceInstance", 0)


def dst_key(e):
    return e.get("targetID"), e.get("targetInstance", 0)


def roles(events, actors):
    heal, dmg, swings, hits, taken = (collections.Counter() for _ in range(5))
    for e in events:
        s, t = actors.get(e.get("sourceID")), actors.get(e.get("targetID"))
        if e["type"] == "heal" and s and s["type"] == "Player":
            heal[s["id"]] += e.get("amount", 0) + e.get("absorbed", 0)
        elif e["type"] == "damage":
            if s and s["type"] == "Player":
                dmg[s["id"]] += e.get("amount", 0)
                hits[s["id"]] += 1
                swings[s["id"]] += e["abilityGameID"] == 1
            elif s and s["type"] == "NPC" and t and t["type"] == "Player" and e["abilityGameID"] == 1:
                taken[t["id"]] += 1
    total_taken = sum(taken.values()) or 1
    out = {}
    for pid in set(heal) | set(dmg):
        if heal[pid] > dmg[pid]:
            out[pid] = "healer"
        elif taken[pid] / total_taken >= TANK_SHARE:
            out[pid] = "tank"
        elif swings[pid] > 0.3 * hits[pid]:
            out[pid] = "melee"
        else:
            out[pid] = "ranged"
    return out


def analyse_pull(f, events, actors, abilities, role, report_start):
    """Everything the guide needs from one trash fight, or None if no non-boss mob died."""
    npc = lambda k: actors.get(k[0], {}).get("type") == "NPC"
    player = lambda k: k[0] in role
    summoned = {dst_key(e) for e in events if e["type"] == "summon"}
    hostile = {dst_key(e) for e in events if e["type"] == "damage" and player(src_key(e)) and npc(dst_key(e))}
    max_hp = collections.Counter()
    for e in events:
        if e.get("resourceActor") == 2 and "maxHitPoints" in e:
            max_hp[dst_key(e)] = max(max_hp[dst_key(e)], e["maxHitPoints"])
    deaths = {}
    for e in events:
        k = dst_key(e)
        if e["type"] == "death" and k in hostile and k not in summoned and k not in deaths \
                and actors[k[0]]["subType"] != "Boss" and max_hp[k] >= MIN_HP:
            deaths[k] = e["timestamp"]
    if not deaths or f["endTime"] - f["startTime"] < MIN_PULL_MS:
        return None

    marker, first_pos, last_pos, pos = collections.defaultdict(collections.Counter), {}, {}, {}
    snaps, bursts, dead = [], {}, set()
    abil = collections.defaultdict(lambda: {"hits": 0, "tank": 0, "dmg": 0, "max": 0, "casts": [], "players": set()})
    debuffs, interrupts, dispels, cc = (collections.Counter() for _ in range(4))
    tick = f["startTime"]
    for e in events:
        t = e["timestamp"]
        while t >= tick:
            snaps.append((tick, dict(pos), set(dead)))
            tick += 1000
        if e["type"] == "death" and player(dst_key(e)) and not e.get("feign"):
            dead.add(e["targetID"])
        elif e["type"] == "resurrect":
            dead.discard(e.get("targetID"))
        for k, mk in ((src_key(e), e.get("sourceMarker")), (dst_key(e), e.get("targetMarker"))):
            if mk and k in deaths:
                marker[k][mk] += 1
        if "x" in e:
            k = src_key(e) if e.get("resourceActor") == 1 else dst_key(e)
            pos[k] = (t, e["x"], e["y"])
            if k in deaths:
                first_pos.setdefault(k, (e["x"], e["y"]))
                if t <= deaths[k]:
                    last_pos[k] = (e["x"], e["y"])
        s, d = src_key(e), dst_key(e)
        sname = actors.get(s[0], {}).get("name")
        aname = abilities.get(e.get("abilityGameID"), "?")
        if e["type"] == "damage" and npc(s) and player(d) and e["abilityGameID"] != 1 and sname != "Environment":
            a = abil[(sname, aname)]
            amt = e.get("amount", 0) + e.get("absorbed", 0)
            a["hits"] += 1; a["tank"] += role[d[0]] == "tank"; a["dmg"] += amt; a["max"] = max(a["max"], amt); a["players"].add(d[0])
            b = bursts.get((s, aname))
            if b is None or t - b["t"] > 1500:
                b = bursts[(s, aname)] = {"t": t, "hit": {}, "caster": pos.get(s)}
                a["casts"].append(b)
            if "x" in e:
                b["hit"][d[0]] = (e["x"], e["y"])
        elif e["type"] == "applydebuff" and npc(s) and player(d):
            debuffs[(sname, aname)] += 1
        elif e["type"] == "interrupt" and player(s):
            interrupts[abilities.get(e.get("extraAbilityGameID"), "?")] += 1
        elif e["type"] == "dispel" and player(s) and npc(d):
            dispels[(actors[d[0]]["name"], abilities.get(e.get("extraAbilityGameID"), "?"))] += 1
        elif e["type"] == "dispel" and player(s):
            dispels[("players", abilities.get(e.get("extraAbilityGameID"), "?"))] += 1
        elif e["type"] in ("applydebuff", "applybuff") and player(s) and d in deaths and aname in CC:
            cc[(actors[d[0]]["name"], aname)] += 1

    # positioning: every second, each player's distance to the nearest living pack mob
    per_player = collections.defaultdict(list)
    healer_tank, spacing = [], []
    for t, p, dead_now in snaps:
        mobs = [(x, y) for k, (pt, x, y) in p.items() if k in deaths and t - pt < 4000 and t <= deaths[k]]
        if not mobs:
            continue
        fresh = {k[0]: (x, y) for k, (pt, x, y) in p.items() if player(k) and t - pt < 2500 and k[0] not in dead_now}
        for pid, xy in fresh.items():
            per_player[pid].append(min(dist(xy, m) for m in mobs))
        back = [xy for pid, xy in fresh.items() if role[pid] in ("ranged", "healer")]
        if len(back) >= 3:
            spacing.append(med([min(dist(a, b) for j, b in enumerate(back) if j != i) for i, a in enumerate(back)]))
        tanks = [xy for pid, xy in fresh.items() if role[pid] == "tank"]
        for pid, xy in fresh.items():
            if role[pid] == "healer" and tanks:
                healer_tank.append(min(dist(xy, tk) for tk in tanks))
    by_role = {r: [v for pid, v in per_player.items() if role[pid] == r and len(v) >= 3] for r in ROLES}
    # "farthest" = the far end of where the role usually stood, not one player running in from the graveyard
    positioning = {r: (med([med(v) for v in vs]), pct([pct(v, 0.75) for v in vs], 0.9)) for r, vs in by_role.items()}

    order = sorted(deaths, key=deaths.get)
    return {
        "when": datetime.fromtimestamp((report_start + f["startTime"]) / 1000),
        "secs": (f["endTime"] - f["startTime"]) / 1000,
        "map": next((e["mapID"] for e in events if "mapID" in e), None),
        "kills": [(actors[k[0]]["name"], MARKERS.get(marker[k].most_common(1)[0][0]) if marker[k] else None,
                   (deaths[k] - f["startTime"]) / 1000) for k in order],
        "centroid": (med([p[0] for p in first_pos.values()]), med([p[1] for p in first_pos.values()])) if first_pos else None,
        "dragged": med([dist(first_pos[k], last_pos[k]) for k in first_pos if k in last_pos]),
        "positioning": positioning, "healer_tank": med(healer_tank), "spacing": med(spacing),
        "raid": len(per_player), "abilities": abil, "debuffs": debuffs, "interrupts": interrupts,
        "dispels": dispels, "cc": cc,
    }


def load(path):
    d = json.load(open(path))
    meta, md = d["meta"], d["meta"]["masterData"]
    actors = {a["id"]: a for a in md["actors"]}
    abilities = {a["gameID"]: a["name"] for a in md["abilities"]}
    role = roles(d["events"], actors)
    by_fight = collections.defaultdict(list)
    for e in d["events"]:
        by_fight[e.get("fight")].append(e)
    fights = sorted(meta["fights"], key=lambda f: f["startTime"])
    pulls = []
    for f in fights:
        if f["encounterID"] or not f.get("gameZone"):
            continue
        zone = f["gameZone"]["name"]
        bosses = [b for b in fights if b["encounterID"] and (b.get("gameZone") or {}).get("name") == zone]
        prev = [b["name"] for b in bosses if b["endTime"] <= f["startTime"]]
        nxt = [b["name"] for b in bosses if b["startTime"] >= f["endTime"]]
        p = analyse_pull(f, by_fight[f["id"]], actors, abilities, role, meta["startTime"])
        if p:
            p.update(zone=zone, code=Path(path).stem, fight=f["id"], prev=prev[-1] if prev else None,
                     next=nxt[0] if nxt else None)
            pulls.append(p)
    print("%s: %d trash pulls" % (Path(path).stem, len(pulls)))
    return pulls


def group(pulls):
    """Mostly the same mob types at the same spot = same pack (WCL sometimes folds a patrol or the next pack in)."""
    names = lambda p: {n for n, _, _ in p["kills"]}
    same = lambda p, q: (q["zone"] == p["zone"] and p["centroid"] and q["centroid"]
                         and dist(p["centroid"], q["centroid"]) < PACK_RADIUS
                         and len(names(p) & names(q)) >= PACK_OVERLAP * len(names(p) | names(q)))
    packs = []
    for p in pulls:
        pk = next((pk for pk in packs if any(same(p, q) for q in pk)), None)
        if pk:
            pk.append(p)
        else:
            packs.append([p])
    return packs


def context(p):
    """Where in that night's clear the pull happened, as 'before X' / 'after X, before Y'."""
    if p["prev"] and p["next"]:
        return "between %s and %s" % (p["prev"], p["next"])
    return "before %s" % p["next"] if p["next"] else "after %s" % p["prev"] if p["prev"] else "no boss killed"


def fmt(x, unit=" yd"):
    return "–" if x is None else "%.0f%s" % (x, unit)


def kill_order(pk):
    """Mob types ordered by their average normalized death position over all pulls."""
    rank = collections.defaultdict(list)
    for p in pk:
        n = len(p["kills"])
        for i, (name, _, _) in enumerate(p["kills"]):
            rank[name].append(i / max(n - 1, 1))
    counts = {name: statistics.mode([sum(1 for k in p["kills"] if k[0] == name) for p in pk]) for name in rank}
    marks = {name: collections.Counter(m for p in pk for k, m, _ in p["kills"] if k == name and m) for name in rank}
    return [(name, counts[name], [m for m, _ in marks[name].most_common(3)]) for name in sorted(rank, key=lambda n: med(rank[n]))]


def ability_notes(pk):
    merged = collections.defaultdict(lambda: {"hits": 0, "tank": 0, "dmg": 0, "max": 0, "casts": [], "players": set()})
    raid = med([p["raid"] for p in pk]) or 25
    for p in pk:
        for k, a in p["abilities"].items():
            m = merged[k]
            m["hits"] += a["hits"]; m["tank"] += a["tank"]; m["dmg"] += a["dmg"]; m["max"] = max(m["max"], a["max"])
            m["casts"] += a["casts"]; m["players"] |= a["players"]
    notes = []
    for (mob, name), a in sorted(merged.items(), key=lambda kv: -kv[1]["dmg"]):
        if a["dmg"] < 0.03 * sum(m["dmg"] for m in merged.values()) or a["hits"] < 3:
            continue
        per_cast = a["hits"] / len(a["casts"])
        line = "- **%s** (%s): %d hits in %d cast%s, ~%.0f per cast, avg %d / max %d dmg." % (
            name, mob, a["hits"], len(a["casts"]), "s" * (len(a["casts"]) > 1), per_cast, a["dmg"] / a["hits"], a["max"])
        multi = [c for c in a["casts"] if len(c["hit"]) >= 3]
        if per_cast >= 2.5 and multi:
            reach = pct([dist(c["caster"][1:], xy) for c in multi if c["caster"] for xy in c["hit"].values()], 0.9)
            share = med([len(c["hit"]) for c in multi]) / raid
            if reach is not None and reach <= 15:
                line += " Point-blank AoE: hit players stood within ~%.0f yd of the mob, so **ranged and healers stay beyond ~%.0f yd**." % (reach, reach + 5)
            elif share >= 0.6:
                line += " Hits most of the raid wherever they stand (raid-wide), so spreading doesn't help; healers pre-heal / top off."
            else:
                gap = med([med([min(dist(a_, b_) for b_ in c["hit"].values() if b_ is not a_) for a_ in c["hit"].values()]) for c in multi])
                line += (" Lands on a clump of players up to ~%s from the mob (those hit stood ~%s apart): splash / ground AoE, "
                         "so **don't stack, and move out of it**." % (fmt(reach), fmt(gap)))
        elif a["tank"] >= 0.8 * a["hits"]:
            line += " Mostly on the tanks."
        elif per_cast < 1.5:
            line += " Single-target on %d different player(s) (%.0f%% on tanks)." % (len(a["players"]), 100 * a["tank"] / a["hits"])
        notes.append(line)
    return notes


def aoe_types(pk):
    """Mob types killed together: at least AOE_COUNT of them, all dead within AOE_WINDOW_S (median over pulls)."""
    spans = collections.defaultdict(list)
    for p in pk:
        times = collections.defaultdict(list)
        for name, _, t in p["kills"]:
            times[name].append(t)
        for name, ts in times.items():
            if len(ts) >= AOE_COUNT:
                spans[name].append(max(ts) - min(ts))
    return {name for name, s in spans.items() if len(s) * 2 >= len(pk) and med(s) <= AOE_WINDOW_S}


def order_md(order, aoe=()):
    return " → ".join("%s%s%s%s" % (n, " ×%d" % c if c > 1 else "", " **AoE**" if n in aoe else "",
                                    " (%s)" % "/".join(m) if m else "") for n, c, m in order)


def summary_md(packs):
    """One row per distinct pack type (same mob types), with the usual kill order and how often the raid followed it."""
    kinds = {}  # mob-type set -> [pack numbers, pulls, sections], in clear order
    for i, (_, ctx, pk) in enumerate(packs, 1):
        k = kinds.setdefault(frozenset(n for p in pk for n, _, _ in p["kills"]), [[], [], []])
        k[0].append(i); k[1] += pk
        if ctx not in k[2]:
            k[2].append(ctx)
    out = ["## Summary: kill order per pack type", "",
           "**AoE** = several of that mob died within %d s of each other: cleaved / AoE'd down together, not single-target "
           "kills. *Same order* = pulls where the single-target mob types died in this order (by first death of each type; "
           "AoE'd types ignored). A low count means the raid had no fixed order for that pack." % AOE_WINDOW_S, "",
           "| Kill order (usual markers) | Packs | Where | Same order |", "|---|---|---|---|"]
    for nums, pulls, ctxs in kinds.values():
        order, aoe = kill_order(pulls), aoe_types(pulls)
        want = [n for n, _, _ in order if n not in aoe]
        same = sum(1 for p in pulls if [n for n in dict.fromkeys(n for n, _, _ in p["kills"]) if n not in aoe] == want)
        out.append("| %s | %s | %s | %s |" % (order_md(order, aoe), ", ".join("#%d" % n for n in nums), "; ".join(ctxs),
                                              "%d of %d" % (same, len(pulls)) if len(want) > 1 else "–"))
    return out + [""]


def pack_md(i, pk):
    order = kill_order(pk)
    title = ", ".join("%s%s" % (n, " ×%d" % c if c > 1 else "") for n, c, _ in order)
    nights = {}
    for p in pk:
        nights.setdefault(p["when"].strftime("%-m/%-d"), context(p))
    out = ["### %d. %s" % (i, title), "",
           "*%s.* Pulled %d×, median fight %.0f s." % ("; ".join("%s %s" % kv for kv in nights.items()),
                                                       len(pk), med([p["secs"] for p in pk])), ""]

    out.append("**Kill order:** " + order_md(order, aoe_types(pk)))
    out.append("")
    for p in pk:
        out.append("- %s: %s" % (p["when"].strftime("%-m/%-d"), " → ".join(
            "%s%s %ds" % (n, " [%s]" % m if m else "", t) for n, m, t in p["kills"])))
    cc = collections.Counter()
    for p in pk:
        cc.update(p["cc"])
    if cc:
        out += ["", "**CC used:** " + ", ".join("%s on %s (%d)" % (s, m, n) for (m, s), n in cc.most_common())]

    pos = {r: (med([p["positioning"][r][0] for p in pk if p["positioning"][r][0] is not None]),
               max([p["positioning"][r][1] for p in pk if p["positioning"][r][1] is not None], default=None)) for r in ROLES}
    spacing, healer_tank = med([p["spacing"] for p in pk if p["spacing"]]), med([p["healer_tank"] for p in pk if p["healer_tank"]])
    dragged = med([p["dragged"] for p in pk if p["dragged"] is not None])
    style = "stacked" if spacing is not None and spacing < 3 else "loosely grouped" if spacing is not None and spacing < 7 else "spread"
    out += ["", "**Positioning** (distance to the nearest living mob):", "",
            "| Role | Typical | Farthest |", "|---|---|---|"]
    out += ["| %s | %s | %s |" % (r.capitalize(), fmt(pos[r][0]), fmt(pos[r][1])) for r in ROLES if pos[r][0] is not None]
    out += ["", "- Ranged + healers: ~%s between neighbours → **%s**." % (fmt(spacing), style) if spacing is not None else "- Not enough position data for spacing.",
            "- Healers ~%s from the nearest tank." % fmt(healer_tank)]
    if dragged is not None and dragged > 10:
        out.append("- Mobs were pulled ~%s away from where they stood (pulled back / LoS'd to a tank spot)." % fmt(dragged))

    notes = ability_notes(pk)
    if notes:
        out += ["", "**What hits the raid:**", ""] + notes
    extra = []
    ints = collections.Counter(); deb = collections.Counter(); dis = collections.Counter()
    for p in pk:
        ints.update(p["interrupts"]); deb.update(p["debuffs"]); dis.update(p["dispels"])
    if ints:
        extra.append("- **Interrupted:** " + ", ".join("%s (%d)" % kv for kv in ints.most_common(6)))
    if deb:
        extra.append("- **Debuffs on players:** " + ", ".join("%s from %s (%d)" % (s, m, n) for (m, s), n in deb.most_common(6)))
    if dis:
        extra.append("- **Dispelled:** " + ", ".join("%s on %s (%d)" % (s, m, n) for (m, s), n in dis.most_common(6)))
    if extra:
        out += [""] + extra
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("raw", nargs="+"); ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    a = ap.parse_args()
    pulls = [p for path in a.raw for p in load(path)]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for zone in sorted({p["zone"] for p in pulls}):
        zp = sorted((p for p in pulls if p["zone"] == zone), key=lambda p: p["when"])
        # route order comes from the night with the most pulls (the fullest clear); packs it skipped use their own night
        nights = collections.Counter(p["code"] for p in zp)
        ref = nights.most_common(1)[0][0]
        for code in nights:
            night = [p for p in zp if p["code"] == code]
            for i, p in enumerate(night):
                p["route"] = i / max(len(night) - 1, 1)
        groups = group(zp)
        pack_of = {id(p): n for n, pk in enumerate(groups) for p in pk}
        place = {}  # pack index -> (route position, section) on the reference night
        for n, pk in enumerate(groups):
            r = [p for p in pk if p["code"] == ref]
            if r:
                place[n] = (r[0]["route"], context(r[0]))
        on_ref = set(place)
        for n, pk in enumerate(groups):
            if n in place:
                continue
            # not pulled on the reference night: slot it in after the most similar pack that was (same mob types, then nearest)
            names = {k[0] for k in pk[0]["kills"]}

            def score(m):
                other = {k[0] for k in groups[m][0]["kills"]}
                c1, c2 = pk[0]["centroid"], groups[m][0]["centroid"]
                return len(names & other) / len(names | other), -dist(c1, c2) if c1 and c2 else 0

            anchor = max(on_ref, key=score, default=None)
            place[n] = (place[anchor][0] + 1e-3, place[anchor][1]) if anchor is not None and score(anchor)[0] > 0 \
                else (pk[0]["route"], context(pk[0]))
        packs = [(place[n][0], place[n][1], pk) for n, pk in enumerate(groups)]
        dates = sorted({p["when"].strftime("%Y-%m-%d") for p in zp})
        ref_date = next(p["when"] for p in zp if p["code"] == ref).strftime("%-m/%-d")
        body = ["# %s trash guide" % zone, "",
                "Built by `guides/tools/trash_guide.py` from %d trash pulls over %d raid night(s) (%s). "
                "Packs are in the order of the %s clear; sections say which bosses they sit between on that night%s. Kill order and raid markers are what the raid actually did. Distances "
                "are measured from the log in yards and show where people stood, which is not necessarily optimal. "
                "Roles are guessed from what each player did." % (len(zp), len(dates), ", ".join(dates), ref_date,
                    " (the boss order differed on other nights)" if len(nights) > 1 else ""), ""]
        packs.sort(key=lambda x: x[0])
        body += summary_md(packs)
        section = None
        for i, (_, ctx, pk) in enumerate(packs, 1):
            if ctx != section:
                body += ["## %s" % (ctx[0].upper() + ctx[1:]), ""]
                section = ctx
            body.append(pack_md(i, pk) + "\n")
        path = out / (slug(zone) + ".md")
        path.write_text("\n".join(body), encoding="utf-8")
        print("%s: %d packs" % (path, len(packs)))


if __name__ == "__main__":
    main()
