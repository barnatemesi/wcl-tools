"""Download a full WarcraftLogs report (metadata + every event) to a JSON file.

usage: python3 fetch.py <report code or URL> [out.json]     (default: ../raw/<code>.json)
"""
import json, sys
from pathlib import Path
import wcl

META = """query($c:String){ reportData { report(code:$c) {
  code title startTime endTime zone { id name }
  fights { id name encounterID kill difficulty size startTime endTime gameZone { id name } }
  masterData(translate: true) {
    logVersion gameVersion
    actors { id gameID name type subType server petOwner icon }
    abilities { gameID name type icon }
  } } } }"""

EVENTS = """query($c:String,$s:Float,$e:Float){ reportData { report(code:$c) {
  events(startTime:$s, endTime:$e, limit:10000, includeResources:true, useAbilityIDs:true, translate:true) {
    data nextPageTimestamp } } } }"""


def fetch(code, out):
    meta = wcl.query(META, {"c": code})["reportData"]["report"]
    if meta is None:
        sys.exit("report %s not found (private, or wrong site? set WCL_HOST)" % code)
    events, start, end = [], 0, meta["endTime"] - meta["startTime"]
    while start is not None:
        r = wcl.query(EVENTS, {"c": code, "s": start, "e": end})["reportData"]["report"]["events"]
        events += r["data"]
        start = r["nextPageTimestamp"]
        print("%s: %d events" % (code, len(events)), file=sys.stderr)
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump({"meta": meta, "events": events}, open(out, "w"))
    print("%s -> %s (%d events)" % (code, out, len(events)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    code = wcl.report_code(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "raw" / (code + ".json")
    fetch(code, out)
