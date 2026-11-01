"""Rebuild WoW TBC (2.5.x, COMBAT_LOG_VERSION 9) combat logs from a WarcraftLogs v2 events dump (see fetch.py).

usage: python3 convert.py <raw.json> [out_dir]     (default out_dir: ../)

Writes one WoWCombatLog-MMDDYY_HHMMSS.txt per zone into <out_dir>/<zone-name>/,
e.g. black-temple/ and hyjal-summit/, so mixed BT + Hyjal reports are split automatically.
"""
import json, math, re, sys, zlib
from datetime import datetime
from pathlib import Path

REALM_IDS = {"Thunderstrike": 6409, "Spineshatter": 6408}  # Spineshatter is a guess
REGION = "EU"
SHARD = 6426
NIL = "0000000000000000,nil,0x80000000,0x80000000"
ZONES = {564: "Black Temple", 534: "Hyjal Summit"}

RANGED = {75, 5019, 3018, 2764}
DAMAGE_SHIELD = {467, 782, 1075, 8914, 9756, 9910, 26992, 7294, 10298, 10299, 10300, 10301, 27150}
PERIODIC_ENERGIZE = {5677, 10491, 10493, 10494, 25569, 29166, 34919, 39609, 29131, 12964, 30824}
MISS_TYPES = {0: "MISS", 7: "DODGE", 8: "PARRY", 9: "DEFLECT", 10: "IMMUNE", 11: "MISS", 12: "REFLECT", 13: "EVADE", 14: "RESIST"}
CRIT, GLANCE, CRUSH = {2, 5, 17}, {6}, {15}

if len(sys.argv) < 2:
    sys.exit(__doc__)
src_path = Path(sys.argv[1])
out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent
d = json.load(open(src_path))
meta, events = d["meta"], d["events"]
md = meta["masterData"]
actors = {a["id"]: a for a in md["actors"]}
abilities = {a["gameID"]: (a["name"], int(a["type"] or 0)) for a in md["abilities"]}
zone_uid = zlib.crc32(src_path.stem.encode()) % 900000 + 100000
fight_zone = {f["id"]: (f.get("gameZone") or {}).get("id", 564) for f in meta["fights"]}
ZONES.update({f["gameZone"]["id"]: f["gameZone"]["name"] for f in meta["fights"] if f.get("gameZone")})


def q(s):
    return '"' + s.replace('"', "'") + '"'


def is_pet(a):
    owner = actors.get(a.get("petOwner"))
    return (owner and owner["subType"] in ("Hunter", "Warlock") and "Totem" not in a["name"]
            and a["name"] not in ("Infernal", "Doomguard"))


def guid(aid, inst=None, fight=None):
    a = actors.get(aid)
    if a is None or aid == -1:
        return "0000000000000000"
    if a["type"] == "Player":
        return "Player-%d-%08X" % (REALM_IDS.get(a["server"], 6409), a["gameID"])
    kind = "Pet" if a["type"] == "Pet" and is_pet(a) else "Creature"
    zone = fight_zone.get(fight, 564)
    spawn = 0x0000400000 + aid * 256 + (inst or 0)
    return "%s-0-%d-%d-%d-%d-%010X" % (kind, SHARD, zone, zone_uid, a["gameID"], spawn)


def flags(aid):
    a = actors.get(aid)
    if a is None:
        return "0x80000000"
    if a["type"] == "Player":
        return "0x514"
    if a.get("petOwner"):
        return "0x1114" if is_pet(a) else "0x2114"
    return "0xa48"


def raid_flags(marker):
    return "0x%x" % (0x80000000 | (1 << (marker - 1))) if marker else "0x80000000"


def name(aid):
    a = actors.get(aid)
    if a is None or aid == -1:
        return "nil"
    if a["type"] == "Player":
        return q("%s-%s-%s" % (a["name"], a["server"], REGION))
    return q(a["name"])


def unit(aid, inst, marker, fight):
    if aid is None or aid == -1 or aid not in actors:
        return NIL
    return "%s,%s,%s,%s" % (guid(aid, inst, fight), name(aid), flags(aid), raid_flags(marker))


def src(e):
    return unit(e.get("sourceID"), e.get("sourceInstance"), e.get("sourceMarker"), e["fight"])


def dst(e):
    return unit(e.get("targetID"), e.get("targetInstance"), e.get("targetMarker"), e["fight"])


def spell(sid):
    n, school = abilities.get(sid, ("Unknown", 1))
    return "%d,%s,0x%x" % (sid, q(n), school)


def advanced(e):
    if "resourceActor" not in e:
        return None
    if e["resourceActor"] == 1:
        aid, inst = e.get("sourceID"), e.get("sourceInstance")
    else:
        aid, inst = e.get("targetID"), e.get("targetInstance")
    a = actors.get(aid, {})
    owner = a.get("petOwner")
    # some uploads carry no resource data for NPCs / pets: log them as "no power" like the client does
    r = e["classResources"][0] if e["classResources"] else {"type": 0, "amount": 0, "max": 0}
    power_type = e["absorb"] if e["classResources"] else -1
    facing = (e["facing"] / 100 - math.pi / 2) % (2 * math.pi)
    return ",".join(str(v) for v in [
        guid(aid, inst, e["fight"]), guid(owner) if owner else "0000000000000000",
        e["hitPoints"], e["maxHitPoints"], e["attackPower"], e["spellPower"], e["armor"],
        e.get("versatility", 0), e.get("avoidance", 0), power_type, r["type"], r["amount"], r["max"],
        "%.2f" % (e["y"] / 100), "%.2f" % (-e["x"] / 100), e["mapID"], "%.4f" % facing, e["itemLevel"]])


def nil_adv():
    return "0000000000000000,0000000000000000,0,0,0,0,0,0,0,-1,0,0,0,0.00,0.00,0,0.0000,0"


def with_adv(*parts, e):
    adv = advanced(e) or nil_adv()
    return ",".join(list(parts[:-1]) + [adv, parts[-1]]) if parts[-1] is not None else ",".join(list(parts[:-1]) + [adv])


def aura_type(e):
    return "DEBUFF" if "debuff" in e["type"] else "BUFF"


def b(x):
    return "1" if x else "nil"


def damage(e):
    sid, ht = e["abilityGameID"], e["hitType"]
    amount, absorbed, blocked = e["amount"], e.get("absorbed", 0), e.get("blocked", 0)
    if sid == 1:
        prefix, sp = "SWING", None
    elif sid in RANGED:
        prefix, sp = "RANGE", spell(sid)
    elif e.get("tick"):
        prefix, sp = "SPELL_PERIODIC", spell(sid)
    elif sid in DAMAGE_SHIELD:
        prefix, sp = "DAMAGE_SHIELD", spell(sid)
    else:
        prefix, sp = "SPELL", spell(sid)
    aoe = "AOE" if e.get("isAoE") else "ST"
    head = [src(e), dst(e)] + ([sp] if sp else [])
    miss = None
    if amount == 0:
        if ht in MISS_TYPES:
            miss = [MISS_TYPES[ht], "nil"] + (["0"] if ht == 14 else [])
        elif absorbed:
            miss = ["ABSORB", "nil", str(absorbed), str(e.get("unmitigatedAmount", absorbed))]
        elif ht in (4, 5):
            miss = ["BLOCK", "nil", str(blocked)]
    if miss is not None:
        event = "DAMAGE_SHIELD_MISSED" if prefix == "DAMAGE_SHIELD" else prefix + "_MISSED"
        return [event + "," + ",".join(head + miss + ([] if sid == 1 else [aoe]))]
    overkill = e.get("overkill", 0)
    school = 1 if sid == 1 else abilities.get(sid, ("", 1))[1]
    suffix = [str(amount + overkill), str(e.get("unmitigatedAmount", amount)), str(overkill or -1), str(school),
              str(e.get("resisted", 0)), str(blocked), str(absorbed), b(ht in CRIT), b(ht in GLANCE), b(ht in CRUSH)]
    if sid != 1:
        suffix.append(aoe)
    adv = advanced(e) or nil_adv()
    event = "DAMAGE_SHIELD" if prefix == "DAMAGE_SHIELD" else prefix + "_DAMAGE"
    return ["%s,%s" % (event, ",".join(head + [adv] + suffix))]


def heal(e):
    prefix = "SPELL_PERIODIC_HEAL" if e.get("tick") else "SPELL_HEAL"
    total = e["amount"] + e.get("overheal", 0) + e.get("absorbed", 0)
    adv = advanced(e) or nil_adv()
    return ["%s,%s,%s,%s,%s,%d,%d,%d,%d,%s" % (prefix, src(e), dst(e), spell(e["abilityGameID"]), adv, total, total,
                                              e.get("overheal", 0), e.get("absorbed", 0), b(e["hitType"] == 2))]


def energize(e):
    prefix = "SPELL_PERIODIC_ENERGIZE" if e.get("tick") or e["abilityGameID"] in PERIODIC_ENERGIZE else "SPELL_ENERGIZE"
    adv = advanced(e) or nil_adv()
    return ["%s,%s,%s,%s,%s,%.4f,%.4f,%d,%d" % (prefix, src(e), dst(e), spell(e["abilityGameID"]), adv,
                                               e["resourceChange"], e.get("waste", 0), e["resourceChangeType"],
                                               e["maxResourceAmount"])]


def drain(e):
    leech = e.get("otherResourceChange", 0) > 0
    prefix = ("SPELL_PERIODIC_" if e.get("tick") else "SPELL_") + ("LEECH" if leech else "DRAIN")
    adv = advanced(e) or nil_adv()
    return ["%s,%s,%s,%s,%s,%d,%d,%d,%d" % (prefix, src(e), dst(e), spell(e["abilityGameID"]), adv,
                                           abs(e["resourceChange"]), e["resourceChangeType"],
                                           e.get("otherResourceChange", 0), e["maxResourceAmount"])]


def absorbed(e):
    attacker = unit(e.get("attackerID"), e.get("attackerInstance"), e.get("attackerMarker"), e["fight"])
    parts = [attacker, dst(e)]
    if e.get("extraAbilityGameID", 1) != 1:
        parts.append(spell(e["extraAbilityGameID"]))
    parts += [src(e), spell(e["abilityGameID"]), str(e["amount"]), str(e["amount"])]
    return ["SPELL_ABSORBED," + ",".join(parts)]


def death(e):
    if e.get("fake"):
        return []
    out = []
    killer = e.get("killerID")
    if killer in actors and actors[killer]["type"] == "Player" and actors.get(e["targetID"], {}).get("type") != "Player":
        out.append("PARTY_KILL,%s,%s,0" % (unit(killer, e.get("killerInstance"), None, e["fight"]), dst(e)))
    out.append("UNIT_DIED,%s,%s,0" % (NIL, dst(e)))
    return out


def gear_item(g):
    if not g.get("id"):
        return "(0,0,(),(),())"
    ench = g.get("permanentEnchant", 0), g.get("temporaryEnchant", 0)
    ench_s = "(%d,%d,0)" % ench if any(ench) else "()"
    gems = ",".join("%d,%d" % (gm["id"], gm.get("itemLevel", 0)) for gm in g.get("gems", []))
    return "(%d,%d,%s,(),(%s))" % (g["id"], g.get("itemLevel", 0), ench_s, gems)


def combatantinfo(e):
    stats = [e.get(k, 0) for k in ("faction", "strength", "agility", "stamina", "intellect", "spirit", "dodge", "parry",
                                   "block", "critMelee", "critRanged", "critSpell", "hasteMelee", "hasteRanged",
                                   "hasteSpell", "hitMelee", "hitRanged", "hitSpell", "expertise",
                                   "resilienceCritTaken", "resilienceDamageTaken", "armor")]
    talents = "(" + ",".join(str(t["id"]) for t in e.get("talents", [])) + ")"
    gear = "[" + ",".join(gear_item(g) for g in e.get("gear", [])) + "]"
    auras = "[" + ",".join("%s,%d,%d" % (guid(a["source"]), a["ability"], a.get("stacks", 1)) for a in e.get("auras", [])) + "]"
    return ["COMBATANT_INFO,%s,%s,-1,%s,(),%s,%s,0,0,()" % (guid(e["sourceID"]), ",".join(map(str, stats)), talents, gear, auras)]


def convert(e):
    t = e["type"]
    if t == "damage":
        return damage(e)
    if t == "heal":
        return heal(e)
    if t == "resourcechange":
        return energize(e)
    if t == "drain":
        return drain(e)
    if t == "absorbed":
        return absorbed(e)
    if t == "cast":
        return ["SPELL_CAST_SUCCESS,%s,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]), advanced(e) or nil_adv())]
    if t == "begincast":
        return ["SPELL_CAST_START,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]))]
    aura = {"applybuff": "SPELL_AURA_APPLIED", "applydebuff": "SPELL_AURA_APPLIED",
            "removebuff": "SPELL_AURA_REMOVED", "removedebuff": "SPELL_AURA_REMOVED",
            "refreshbuff": "SPELL_AURA_REFRESH", "refreshdebuff": "SPELL_AURA_REFRESH"}
    if t in aura:
        return ["%s,%s,%s,%s,%s" % (aura[t], src(e), dst(e), spell(e["abilityGameID"]), aura_type(e))]
    dose = {"applybuffstack": "SPELL_AURA_APPLIED_DOSE", "applydebuffstack": "SPELL_AURA_APPLIED_DOSE",
            "removebuffstack": "SPELL_AURA_REMOVED_DOSE", "removedebuffstack": "SPELL_AURA_REMOVED_DOSE"}
    if t in dose:
        return ["%s,%s,%s,%s,%s,%d" % (dose[t], src(e), dst(e), spell(e["abilityGameID"]), aura_type(e), e["stack"])]
    if t == "summon":
        return ["SPELL_SUMMON,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]))]
    if t == "create":
        return ["SPELL_CREATE,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]))]
    if t == "death":
        return death(e)
    if t == "interrupt":
        return ["SPELL_INTERRUPT,%s,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]), spell(e["extraAbilityGameID"]).replace(",0x", ",0x"))]
    if t in ("dispel", "spellsteal"):
        ev = "SPELL_DISPEL" if t == "dispel" else "SPELL_STOLEN"
        return ["%s,%s,%s,%s,%s,%s" % (ev, src(e), dst(e), spell(e["abilityGameID"]), spell(e["extraAbilityGameID"]),
                                       "BUFF" if e.get("isBuff") else "DEBUFF")]
    if t == "aurabroken":
        kind = "BUFF" if e.get("isBuff") else "DEBUFF"
        if e.get("extraAbilityGameID"):
            return ["SPELL_AURA_BROKEN_SPELL,%s,%s,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]),
                                                                 spell(e["extraAbilityGameID"]), kind)]
        return ["SPELL_AURA_BROKEN,%s,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]), kind)]
    if t == "extraattacks":
        return ["SPELL_EXTRA_ATTACKS,%s,%s,%s,%d" % (src(e), dst(e), spell(e["abilityGameID"]), e["extraAttacks"])]
    if t == "resurrect":
        return ["SPELL_RESURRECT,%s,%s,%s" % (src(e), dst(e), spell(e["abilityGameID"]))]
    if t == "instakill":
        return ["SPELL_INSTAKILL,%s,%s,%s,0" % (src(e), dst(e), spell(e["abilityGameID"]))]
    if t == "encounterstart":
        return ['ENCOUNTER_START,%d,%s,%d,%d,%d,5' % (e["encounterID"], q(e["name"]), e["difficulty"], e["size"], fight_zone[e["fight"]])]
    if t == "encounterend":
        return ['ENCOUNTER_END,%d,%s,%d,%d,%d' % (e["encounterID"], q(e["name"]), e["difficulty"], e["size"], 1 if e.get("kill") else 0)]
    if t == "combatantinfo":
        return combatantinfo(e)
    if t == "destroy":
        return ["UNIT_DESTROYED,%s,%s,0" % (NIL, dst(e))]
    if t not in skipped:
        print("warning: skipping unhandled WCL event type %r" % t, file=sys.stderr)
    skipped[t] = skipped.get(t, 0) + 1
    return []


skipped = {}


def stamp(ms):
    dt = datetime.fromtimestamp((meta["startTime"] + ms) / 1000)
    return "%d/%d/%d %s.%03d0" % (dt.month, dt.day, dt.year, dt.strftime("%H:%M:%S"), dt.microsecond // 1000)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def file_name(ms):
    dt = datetime.fromtimestamp((meta["startTime"] + ms) / 1000)
    return dt.strftime("WoWCombatLog-%m%d%y_%H%M%S.txt")


per_zone = {}  # zone id -> (lines, counts)
for e in events:
    z = fight_zone.get(e["fight"], 0)
    if z not in per_zone:
        hdr = "COMBAT_LOG_VERSION,9,ADVANCED_LOG_ENABLED,1,BUILD_VERSION,2.5.6,PROJECT_ID,5"
        per_zone[z] = ([e["timestamp"]], ["%s  %s" % (stamp(e["timestamp"]), hdr),
                                          '%s  ZONE_CHANGE,%d,%s,3' % (stamp(e["timestamp"]), z, q(ZONES.get(z, "Unknown")))], {})
    _, lines, counts = per_zone[z]
    for line in convert(e):
        lines.append("%s  %s" % (stamp(e["timestamp"]), line))
        counts[line.split(",", 1)[0]] = counts.get(line.split(",", 1)[0], 0) + 1

for z, (first, lines, counts) in per_zone.items():
    path = out_dir / slug(ZONES.get(z, "zone-%d" % z)) / file_name(first[0])
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("%s: %d lines (%s)" % (path, len(lines), ", ".join("%s %d" % kv for kv in
                                                             sorted(counts.items(), key=lambda kv: -kv[1])[:5])))
