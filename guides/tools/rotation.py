"""Rotation breakdown per class / spec, bosses and trash separately, from raw/<code>.json dumps.

usage: python3 guides/tools/rotation.py recovered/raw/*.json [--boss NAME] [--out guides/rotations]

Writes <out>/<zone>.md. Per spec: casts per minute and damage / healing share per ability, per-player DPS / HPS
and cast-time usage, self-buff uptimes, debuff uptimes on the boss, the usual boss opener, and what changes on trash.
--boss limits the boss half to fights whose name contains NAME (trash is always every trash pull).

- Specs come from the WarcraftLogs icon (e.g. Mage-Arcane); when WCL has no spec, the guessed role is used instead
  (see trash_guide.roles).
- Per-minute rates use the time each player was alive in the fights they took part in.
- "Active" is the share of alive time spent casting or on the global cooldown (1.5 s per instant, begincast→cast for
  cast-time spells; channels count as one GCD, so channel-heavy specs read low).
"""
import argparse, collections, json
from pathlib import Path
from trash_guide import med, roles, slug

AUTO = {1, 75}  # Melee, Auto Shot: not rotation choices
GCD_MS = 1500
MIN_TRASH_MS = 5000
OPENER = 8
PROC_RATE = 0.3
def new_stats():
    return {"fights": 0, "alive": 0, "busy": 0, "casts": collections.Counter(), "dmg": collections.Counter(),
            "heal": collections.Counter(), "buffs": collections.Counter(), "debuffs": collections.Counter(),
            "openers": [], "prepull": collections.Counter(), "info_pulls": 0}


def spec_of(actor, role):
    if "-" in (actor.get("icon") or ""):
        cls, spec = actor["icon"].split("-", 1)
        return "%s — %s" % (cls, spec)
    return "%s — %s" % (actor["subType"], role or "unknown spec")


def union(intervals):
    total, end = 0, None
    for a, b in sorted(intervals):
        if end is None or a > end:
            total += b - a
            end = b
        elif b > end:
            total += b - end
            end = b
    return total


def self_buffs(events, abilities, players, fights):
    """(player, buff name) -> intervals inside pulls, for short buffs and procs only.

    WCL only keeps events inside pulls, so what happens to a buff between pulls is invisible. Long buffs (anything
    combatantinfo lists at boss pulls: food, flasks, armors, auras) are reported from combatantinfo instead; forms and
    aspects show up as casts. Anything applied / refreshed less than PROC_RATE times per minute of pull time is treated
    as long too. A buff whose first event in a pull is a remove / refresh was up since the pull started."""
    fight_start = {f["id"]: f["startTime"] for f in fights}
    fight_end = {f["id"]: f["endTime"] for f in fights}
    long_ = {a["name"] for e in events if e["type"] == "combatantinfo" for a in e.get("auras") or []}
    open_, iv, procs = {}, collections.defaultdict(list), collections.Counter()  # open_[k] = (since, pull)
    for e in events:
        t, s, fight = e["timestamp"], e.get("sourceID"), e.get("fight")
        if s not in players or fight not in fight_start or e.get("targetID") != s or \
                e["type"] not in ("applybuff", "removebuff", "refreshbuff", "applybuffstack", "removebuffstack"):
            continue
        k = (s, abilities.get(e.get("abilityGameID"), "?"))
        if k[1] in long_ or k[1].startswith("Aspect of") or k[1].endswith(" Form"):
            continue
        if k in open_ and open_[k][1] != fight:  # still open from an earlier pull: it ended with that pull
            iv[k].append((open_[k][0], fight_end[open_.pop(k)[1]]))
        if e["type"] in ("applybuff", "refreshbuff", "applybuffstack"):
            procs[k] += 1
        if e["type"] == "applybuff":
            open_.setdefault(k, (t, fight))
        elif e["type"] == "removebuff":
            iv[k].append((open_.pop(k, (fight_start[fight], fight))[0], t))
        else:
            open_.setdefault(k, (fight_start[fight], fight))
    for k, (a, fight) in open_.items():
        iv[k].append((a, fight_end[fight]))
    pull_min = sum(f["endTime"] - f["startTime"] for f in fights) / 60000
    return {k: v for k, v in iv.items() if procs[k] / pull_min >= PROC_RATE}


def analyse_fight(f, events, actors, abilities, players, stats, kind, buff_iv):
    start, end = f["startTime"], f["endTime"]
    name = lambda e: abilities.get(e.get("abilityGameID"), "?")
    present = {e["sourceID"] for e in events if e.get("sourceID") in players}
    pets = {a["id"]: a["petOwner"] for a in actors.values() if a.get("petOwner") in players}
    bosses = {a["id"] for a in actors.values() if a.get("subType") == "Boss"}
    died, casts, begins = {}, collections.defaultdict(list), {}
    deb_open, deb_iv = {}, collections.defaultdict(list)
    for e in events:
        t, s, d = e["timestamp"], e.get("sourceID"), e.get("targetID")
        typ = e["type"]
        owner = pets.get(s, s)
        st = stats[owner] if owner in present else None
        if typ == "death" and d in present and not e.get("feign"):
            died.setdefault(d, []).append([t, end])
        elif typ == "resurrect" and d in died and died[d][-1][1] == end:
            died[d][-1][1] = t
        if st is None:
            continue
        if typ == "begincast" and s in present:
            begins[(s, e["abilityGameID"])] = t
        elif typ == "cast" and s in present and e["abilityGameID"] not in AUTO:
            b = begins.pop((s, e["abilityGameID"]), None)
            b = b if b is not None and t - b < 10000 else t
            casts[s].append((b, max(t, b + GCD_MS), name(e)))
        elif typ == "damage" and (s in present or s in pets) and actors.get(d, {}).get("type") == "NPC":
            st["dmg"][("(pet) " if s in pets else "") + name(e)] += e.get("amount", 0) + e.get("absorbed", 0)
        elif typ == "heal" and s in present:
            st["heal"][name(e)] += e.get("amount", 0) + e.get("absorbed", 0)
        elif typ == "combatantinfo" and s in present:
            st["info_pulls"] += 1
            st["prepull"].update({a["name"] for a in e.get("auras") or [] if a.get("source") == s})
        elif typ in ("applydebuff", "removedebuff") and s in present and d in bosses:
            k = (s, name(e), d, e.get("targetInstance", 0))
            if typ == "applydebuff":
                deb_open.setdefault(k, t)
            else:
                deb_iv[k].append((deb_open.pop(k, start), t))
    for k, t in deb_open.items():
        deb_iv[k].append((t, end))

    for pid in present:
        st = stats[pid]
        alive = (end - start) - sum(b - a for a, b in died.get(pid, []))
        if alive <= 0:
            continue
        st["fights"] += 1
        st["alive"] += alive
        cs = casts[pid]
        st["busy"] += union([(a, b) for a, b, _ in cs])
        st["casts"].update(n for _, _, n in cs)
        if kind == "boss":
            st["openers"].append([n for _, _, n in cs[:OPENER]])
    for (pid, buff), iv in buff_iv.items():
        if pid in present:
            ms = union([(max(a, start), min(b, end)) for a, b in iv if b > start and a < end])
            if ms:
                stats[pid]["buffs"][buff] += ms
    per_name = collections.defaultdict(int)
    for (pid, deb, _, _), iv in deb_iv.items():
        per_name[(pid, deb)] = max(per_name[(pid, deb)], union(iv))  # best-covered boss target
    for (pid, deb), ms in per_name.items():
        stats[pid]["debuffs"][deb] += ms


def load(path, boss_filter, data):
    d = json.load(open(path))
    meta, md = d["meta"], d["meta"]["masterData"]
    actors = {a["id"]: a for a in md["actors"]}
    abilities = {a["gameID"]: a["name"] for a in md["abilities"]}
    role = roles(d["events"], actors)
    players = {pid for pid in role if actors[pid]["subType"] != "Unknown"}
    by_fight = collections.defaultdict(list)
    for e in d["events"]:
        by_fight[e.get("fight")].append(e)
    buff_iv = self_buffs(d["events"], abilities, players, meta["fights"])
    n = collections.Counter()
    for f in meta["fights"]:
        if not f.get("gameZone"):
            continue
        kind = "boss" if f["encounterID"] else "trash"
        if kind == "boss" and boss_filter and boss_filter.lower() not in f["name"].lower():
            continue
        if kind == "trash" and f["endTime"] - f["startTime"] < MIN_TRASH_MS:
            continue
        zone = f["gameZone"]["name"]
        stats = {pid: data[zone][kind][(spec_of(actors[pid], role[pid]), actors[pid]["name"])] for pid in players}
        analyse_fight(f, by_fight[f["id"]], actors, abilities, players, stats, kind, buff_iv)
        data[zone]["fights"][kind].add((Path(path).stem, f["id"]))
        n[kind] += 1
    print("%s: %d boss pulls, %d trash pulls" % (Path(path).stem, n["boss"], n["trash"]))


def total(sts, key):
    c = collections.Counter()
    for st in sts:
        c.update(st[key])
    return c


def section(kind, sts, other):
    """Markdown for one spec on bosses or trash; `other` is the same spec's stats for the other kind."""
    sts = {p: st for p, st in sts.items() if st["fights"]}
    if not sts:
        return []
    users = lambda k: " (%d of %d)" % (k, len(sts)) if k < len(sts) else ""
    alive_min = sum(st["alive"] for st in sts.values()) / 60000
    casts, dmg, heal = (total(sts.values(), k) for k in ("casts", "dmg", "heal"))
    healer = sum(heal.values()) > sum(dmg.values())
    out_name, out = ("healing", heal) if healer else ("damage", dmg)
    out_total = sum(out.values()) or 1
    rows = ["#### %s (%d player%s, %.0f player-minutes)" % ("Bosses" if kind == "boss" else "Trash", len(sts),
                                                            "s" * (len(sts) > 1), alive_min), "",
            "| Ability | Casts/min | %% of casts | %% of %s |" % out_name, "|---|---|---|---|"]
    names = sorted(set(casts) | set(out), key=lambda n: -(out[n] / out_total + casts[n] / max(sum(casts.values()), 1)))
    for n in names[:12]:
        if casts[n] / alive_min < 0.05 and out[n] / out_total < 0.01:
            continue
        rows.append("| %s | %s | %s | %s |" % (
            n, "%.1f" % (casts[n] / alive_min) if casts[n] else "–",
            "%.0f%%" % (100 * casts[n] / max(sum(casts.values()), 1)) if casts[n] else "–",
            "%.0f%%" % (100 * out[n] / out_total) if out[n] else "–"))

    rows += ["", "| Player | Pulls | %s | Active | Most cast |" % ("HPS" if healer else "DPS"), "|---|---|---|---|---|"]
    for p, st in sorted(sts.items(), key=lambda kv: -sum(kv[1]["heal" if healer else "dmg"].values()) / kv[1]["alive"]):
        per_sec = sum(st["heal" if healer else "dmg"].values()) / (st["alive"] / 1000)
        top = ", ".join("%s %.1f" % (n, c / (st["alive"] / 60000)) for n, c in st["casts"].most_common(3))
        rows.append("| %s | %d | %.0f | %.0f%% | %s |" % (p, st["fights"], per_sec, 100 * st["busy"] / st["alive"], top or "–"))

    def uptimes(key, floor):
        """Uptime per aura over the alive time of the players who used it at all."""
        up = collections.Counter()
        for n in total(sts.values(), key):
            users = [st for st in sts.values() if st[key][n]]
            up[n] = sum(st[key][n] for st in users) / sum(st["alive"] for st in users)
        return [(n, u, sum(1 for st in sts.values() if st[key][n])) for n, u in up.most_common(8) if u >= floor]

    top_buffs = uptimes("buffs", 0.1)
    if top_buffs:
        rows += ["", "**Short buff / proc uptime:** " + ", ".join("%s %.0f%%%s" % (n, 100 * min(u, 1), users(k)) for n, u, k in top_buffs)]
    if kind == "boss":
        n_info = sum(st["info_pulls"] for st in sts.values())
        pre = total(sts.values(), "prepull")
        if n_info:
            rows.append("**Self-buffs up at the pull** (%% of %d boss pulls): " % n_info + ", ".join(
                "%s %.0f%%" % (n, 100 * c / n_info) for n, c in pre.most_common(10) if c / n_info >= 0.15))
        top_debs = uptimes("debuffs", 0.05)
        if top_debs:
            rows.append("**Debuff uptime on the boss:** " + ", ".join(
                "%s %.0f%%%s" % (n, 100 * min(u, 1), users(k)) for n, u, k in top_debs))
        openers = [o for st in sts.values() for o in st["openers"] if o]
        if openers:
            typical = [collections.Counter(o[i] for o in openers if len(o) > i).most_common(1)[0][0]
                       for i in range(min(OPENER, max(map(len, openers))))]
            rows.append("**Usual opener** (most common cast at each step over %d pulls): %s" % (len(openers), " → ".join(typical)))
    if kind == "trash" and other:
        o_alive = sum(st["alive"] for st in other.values() if st["fights"]) / 60000
        if o_alive:
            o_casts = total(other.values(), "casts")
            diff = sorted(((casts[n] / alive_min - o_casts[n] / o_alive, n) for n in set(casts) | set(o_casts)), reverse=True)
            more = ["%s +%.1f" % (n, v) for v, n in diff[:3] if v >= 0.3]
            less = ["%s %.1f" % (n, v) for v, n in diff[::-1][:3] if v <= -0.3]
            if more or less:
                rows.append("**Compared with bosses** (casts/min): " + "; ".join(
                    x for x in ("more " + ", ".join(more) if more else "", "less " + ", ".join(less) if less else "") if x))
    return rows + [""]


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("raw", nargs="+"); ap.add_argument("--boss")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "rotations"))
    a = ap.parse_args()
    data = collections.defaultdict(lambda: {"boss": collections.defaultdict(new_stats), "trash": collections.defaultdict(new_stats),
                                            "fights": {"boss": set(), "trash": set()}})
    for path in a.raw:
        load(path, a.boss, data)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for zone, z in sorted(data.items()):
        if not z["fights"]["boss"]:
            continue  # e.g. a few minutes logged outside the raid after it ended
        specs = sorted({spec for kind in ("boss", "trash") for spec, _ in z[kind] if z[kind][(spec, _)]["fights"]})
        body = ["# %s rotations" % zone, "",
                "Built by `guides/tools/rotation.py` from %d boss pulls%s and %d trash pulls. Per spec, bosses and trash "
                "separately. Casts/min is per minute alive; *Active* is the share of alive time spent casting or on the GCD "
                "(channels count as one GCD; energy and rage classes are resource-capped, so they read lower). Damage and healing include absorbed amounts; pet damage is listed as (pet)." % (
                    len(z["fights"]["boss"]), " matching '%s'" % a.boss if a.boss else "", len(z["fights"]["trash"])), ""]
        body += ["Specs: " + ", ".join("[%s](#%s)" % (s, slug(s)) for s in specs), ""]
        for spec in specs:
            by_kind = {kind: {p: st for (sp, p), st in z[kind].items() if sp == spec} for kind in ("boss", "trash")}
            body += ["## %s" % spec, ""]
            body += section("boss", by_kind["boss"], by_kind["trash"])
            body += section("trash", by_kind["trash"], by_kind["boss"])
        path = out / (slug(zone) + (("-" + slug(a.boss)) if a.boss else "") + ".md")
        path.write_text("\n".join(body), encoding="utf-8")
        print("%s: %d specs" % (path, len(specs)))


if __name__ == "__main__":
    main()
