"""Find reports uploaded by a guild or a WarcraftLogs user, so lost logs can be located.

usage:
  python3 list_reports.py --guild "<guild name>" --server thunderstrike [--region EU]
  python3 list_reports.py --user <warcraftlogs user id>     (number from your profile URL)
  options: --zone <zone id>  (564 = Black Temple, 534 = Hyjal, 532 = Karazhan)   --links  (print URLs only)
"""
import argparse
from datetime import datetime
import wcl

Q = """query($g:String,$s:String,$r:String,$u:Int,$z:Int,$p:Int){ reportData {
  reports(guildName:$g, guildServerSlug:$s, guildServerRegion:$r, userID:$u, zoneID:$z, limit:100, page:$p) {
    has_more_pages data { code title startTime zone { name } owner { name } } } } }"""


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("--guild"); ap.add_argument("--server"); ap.add_argument("--region", default="EU")
    ap.add_argument("--user", type=int); ap.add_argument("--zone", type=int); ap.add_argument("--links", action="store_true")
    a = ap.parse_args()
    if not a.guild and not a.user:
        ap.error("give --guild (with --server) or --user")
    v = {"g": a.guild, "s": a.server and a.server.lower().replace(" ", "-"), "r": a.region if a.guild else None,
         "u": a.user, "z": a.zone}
    page = 1
    while True:
        r = wcl.query(Q, dict(v, p=page))["reportData"]["reports"]
        for rep in r["data"]:
            url = "%s/reports/%s" % (wcl.HOST, rep["code"])
            if a.links:
                print(url)
            else:
                print("%s  %-40s %-20s %s" % (datetime.fromtimestamp(rep["startTime"] / 1000).strftime("%Y-%m-%d %H:%M"),
                                             rep["title"][:40], (rep.get("zone") or {}).get("name") or "", url))
        if not r["has_more_pages"]:
            break
        page += 1


if __name__ == "__main__":
    main()
