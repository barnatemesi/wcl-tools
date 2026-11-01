"""Split any combat log (real or rebuilt) by zone or by boss encounter.

usage:
  python3 split_log.py <WoWCombatLog.txt> [out_dir]              one file per zone (ZONE_CHANGE)
  python3 split_log.py <WoWCombatLog.txt> [out_dir] --encounters one file per ENCOUNTER_START..END pull

Encounter files are named <date>_<boss>_<n>_<kill|wipe>.txt; the header line is copied into every file.
"""
import re, sys
from pathlib import Path


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fields(line):
    return line.split("  ", 1)[1].rstrip("\n").split(",")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    src = Path(args[0])
    out = Path(args[1]) if len(args) > 1 else src.parent / (src.stem + "-split")
    out.mkdir(parents=True, exist_ok=True)
    header, current, written = None, None, []
    pulls = {}

    def flush_pull(suffix):
        path = current[0].with_name(current[0].name + suffix)
        path.write_text("".join(current[1]), encoding="utf-8")
        written.append(path)

    with open(src, encoding="utf-8") as f:
        for line in f:
            event = line.split("  ", 1)[1].split(",", 1)[0] if "  " in line else ""
            if event == "COMBAT_LOG_VERSION":
                header = line
                continue
            if "--encounters" in sys.argv:
                if event == "ENCOUNTER_START":
                    if current:  # previous pull never got an ENCOUNTER_END
                        flush_pull("_incomplete.txt")
                    boss = fields(line)[2].strip('"')
                    pulls[boss] = pulls.get(boss, 0) + 1
                    date = line.split(" ", 1)[0].replace("/", "-")
                    current = [out / ("%s_%s_%d" % (date, slug(boss), pulls[boss])), [header] if header else []]
                if current:
                    current[1].append(line)
                if event == "ENCOUNTER_END" and current:
                    flush_pull("_kill.txt" if fields(line)[-1] == "1" else "_wipe.txt")
                    current = None
            else:
                if event == "ZONE_CHANGE":
                    zone = slug(fields(line)[2].strip('"'))
                    if current:
                        current.close()
                    path = out / ("%s_%s.txt" % (src.stem, zone))
                    first_visit = path not in written
                    current = open(path, "w" if first_visit else "a", encoding="utf-8")
                    if first_visit:
                        written.append(path)
                        if header:
                            current.write(header)
                if current:
                    current.write(line)
    if isinstance(current, list):
        flush_pull("_incomplete.txt")
    elif current:
        current.close()
    for p in written:
        print(p)


if __name__ == "__main__":
    main()
