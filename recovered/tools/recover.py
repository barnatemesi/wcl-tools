"""One-shot recovery: download (if not cached) and convert reports into zone-split WoWCombatLog files.

usage:
  python3 recover.py <code or URL> [<code or URL> ...]
  python3 recover.py --links ../../wow-tbc-bt-links.md      (every report link in a file)
  options: --refetch   ignore cached raw/<code>.json and download again
           --out DIR   where the zone folders go (default: recovered/)
"""
import argparse, subprocess, sys
from pathlib import Path
import wcl, fetch

TOOLS = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("reports", nargs="*")
    ap.add_argument("--links"); ap.add_argument("--refetch", action="store_true")
    ap.add_argument("--out", default=str(TOOLS.parent))
    a = ap.parse_args()
    codes = [wcl.report_code(r) for r in a.reports] + (wcl.codes_from_file(a.links) if a.links else [])
    if not codes:
        ap.error("no reports given")
    for code in codes:
        raw = TOOLS.parent / "raw" / (code + ".json")
        if a.refetch or not raw.exists():
            fetch.fetch(code, raw)
        else:
            print("%s: using cached %s" % (code, raw))
        subprocess.run([sys.executable, "-I", str(TOOLS / "convert.py"), str(raw), a.out], check=True)


if __name__ == "__main__":
    main()
