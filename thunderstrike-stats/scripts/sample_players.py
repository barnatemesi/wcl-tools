"""Step 2: for a random sample of guild raid-weeks, count the distinct players who took part in boss pulls (resumable).

usage: python3 sample_players.py [--per-week 8] [--seed 1]
reads data/guild_reports.jsonl, writes data/sample_players.jsonl (one line per sampled guild-week)

Players are taken from fights(killType: Encounters).friendlyPlayers, not the report's full actor list:
that list also contains bystanders (city, trash, other groups), e.g. 91 "players" in one 25-man log.
"""
import collections, random, sys
from common import DATA, RAID_ZONES, append_jsonl, paced_query, read_jsonl, week_start

PER_WEEK = int(sys.argv[sys.argv.index("--per-week") + 1]) if "--per-week" in sys.argv else 8
SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 1
BATCH = 8  # reports per API call


def guild_weeks():
    gw = collections.defaultdict(list)
    for g in read_jsonl(DATA / "guild_reports.jsonl"):
        for r in g["reports"]:
            if (r.get("zone") or {}).get("id") in RAID_ZONES:
                gw[(g["id"], str(week_start(r["startTime"])))].append(r["code"])
    return gw


def players_in(codes):
    """code -> set of player gameIDs that were in at least one boss pull."""
    out = {}
    for n in range(0, len(codes), BATCH):
        chunk = codes[n:n + BATCH]
        q = "{ reportData { " + " ".join(
            'r%d: report(code:"%s") { fights(killType: Encounters) { friendlyPlayers }'
            ' masterData { actors(type:"Player") { id gameID } } }' % (i, c) for i, c in enumerate(chunk)) + " } }"
        res = paced_query(q)["reportData"]
        for i, c in enumerate(chunk):
            rep = res.get("r%d" % i)
            if not rep:
                out[c] = set()
                continue
            ids = {a["id"]: a["gameID"] for a in rep["masterData"]["actors"]}
            out[c] = {ids[p] for f in rep["fights"] for p in (f.get("friendlyPlayers") or []) if p in ids}
    return out


def main():
    gw = guild_weeks()
    by_week = collections.defaultdict(list)
    for key in gw:
        by_week[key[1]].append(key)
    rng = random.Random(SEED)
    picks = []
    for week in sorted(by_week):
        keys = sorted(by_week[week])
        rng.shuffle(keys)
        picks += keys[:PER_WEEK]
    out = DATA / "sample_players.jsonl"
    done = {(r["guild"], r["week"]) for r in read_jsonl(out)}
    todo = [k for k in picks if k not in done]
    print("%d raid weeks, %d guild-weeks total, %d sampled, %d to go" % (len(by_week), len(gw), len(picks), len(todo)),
          flush=True)
    for n, (guild, week) in enumerate(todo, 1):
        sets = players_in(gw[(guild, week)])
        players = set().union(*sets.values()) if sets else set()
        append_jsonl(out, [{"guild": guild, "week": week, "reports": len(sets), "players": sorted(players)}])
        if n % 10 == 0:
            print("  %d/%d sampled guild-weeks" % (n, len(todo)), flush=True)
    print("done")


if __name__ == "__main__":
    main()
