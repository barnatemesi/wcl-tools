"""Step 1: list every Thunderstrike-EU guild and all of its reports since SINCE (resumable).

usage: python3 collect_guild_reports.py [--batch 20]
writes data/guilds.json and data/guild_reports.jsonl (one line per guild: id, name, reports[])
"""
import json, sys
from common import DATA, REGION, SERVER, SINCE, append_jsonl, paced_query, read_jsonl

BATCH = int(sys.argv[sys.argv.index("--batch") + 1]) if "--batch" in sys.argv else 20
T0 = int(SINCE.timestamp() * 1000)
FIELDS = "code startTime endTime zone { id }"


# First bosses of each TBC raid: almost every raiding guild kills at least one of these.
DISCOVERY_ENCOUNTERS = {50652: "Attumen the Huntsman", 50653: "Moroes", 50649: "High King Maulgar",
                        50651: "Magtheridon", 100623: "Hydross the Unstable", 100731: "Void Reaver",
                        50601: "High Warlord Naj'entus", 50618: "Rage Winterchill"}


def all_guilds():
    """The server guild list stops at 10 pages (1000 guilds), so also collect every guild that appears in the
    per-server kill rankings (one entry per guild) of the first boss of each raid."""
    path, partial = DATA / "guilds.json", DATA / "guilds_partial.json"
    if path.exists():
        return json.loads(path.read_text())
    state = json.loads(partial.read_text()) if partial.exists() else {"guilds": {}, "done": []}
    guilds = {int(k): v for k, v in state["guilds"].items()}
    if "server list" not in state["done"]:
        for page in range(1, 11):
            g = paced_query('query($p:Int){ worldData { server(region:"%s", slug:"%s") { guilds(limit:100, page:$p) {'
                            ' last_page data { id name } } } } }' % (REGION, SERVER), {"p": page})["worldData"]["server"]["guilds"]
            for x in g["data"]:
                guilds[x["id"]] = {"id": x["id"], "name": x["name"], "source": "server list"}
            if page >= g["last_page"]:
                break
        state["done"].append("server list")
        partial.write_text(json.dumps({"guilds": guilds, "done": state["done"]}))
        print("server list: %d guilds" % len(guilds), flush=True)
    for enc, boss in DISCOVERY_ENCOUNTERS.items():
        if boss in state["done"]:
            continue
        page, found = 1, 0
        while True:
            fr = paced_query('query($e:Int,$p:Int){ worldData { encounter(id:$e) { fightRankings(serverRegion:"%s",'
                             ' serverSlug:"%s", page:$p) } } }' % (REGION, SERVER), {"e": enc, "p": page}
                             )["worldData"]["encounter"]["fightRankings"]
            for r in fr.get("rankings", []):
                gd = r.get("guild")
                if gd and gd["id"] not in guilds:
                    guilds[gd["id"]] = {"id": gd["id"], "name": gd["name"], "source": "rankings: " + boss}
                    found += 1
            if not fr.get("hasMorePages"):
                break
            page += 1
        state["done"].append(boss)
        partial.write_text(json.dumps({"guilds": guilds, "done": state["done"]}))
        print("%s: %d pages, %d new guilds (total %d)" % (boss, page, found, len(guilds)), flush=True)
    path.write_text(json.dumps(list(guilds.values())))
    return list(guilds.values())


def reports_for(ids, page=1):
    q = "{ reportData { " + " ".join(
        'g%d: reports(guildID:%d, startTime:%d, limit:100, page:%d) { last_page data { %s } }' % (i, i, T0, page, FIELDS)
        for i in ids) + " } }"
    return {int(k[1:]): v for k, v in paced_query(q)["reportData"].items()}


def main():
    guilds = all_guilds()
    out = DATA / "guild_reports.jsonl"
    done = {r["id"] for r in read_jsonl(out)}
    # guilds seen in TBC kill rankings first: they certainly raid, so a partial scan already shows the trend
    todo = sorted((g for g in guilds if g["id"] not in done), key=lambda g: g.get("source") == "server list")
    print("%d guilds, %d already done, %d to go" % (len(guilds), len(done), len(todo)), flush=True)
    for n in range(0, len(todo), BATCH):
        chunk = todo[n:n + BATCH]
        res = reports_for([g["id"] for g in chunk])
        rows = []
        for g in chunk:
            r = res[g["id"]]
            reports = list(r["data"])
            for page in range(2, (r["last_page"] or 1) + 1):  # rare: guilds with >100 reports this year
                reports += reports_for([g["id"]], page)[g["id"]]["data"]
            rows.append({"id": g["id"], "name": g["name"], "reports": reports})
        append_jsonl(out, rows)
        print("  %d/%d guilds" % (len(done) + n + len(chunk), len(guilds)), flush=True)
    print("done")


if __name__ == "__main__":
    main()
