"""Print the start, end and duration of combat logs, or copy them with every timestamp shifted.

usage: python3 raid_time.py [--shift MINUTES OUT_DIR] <log.txt> [<log.txt> ...]

Without --shift, prints the first and last timestamp of each log and the time between them.
With --shift, writes a copy of each log into OUT_DIR with every timestamp moved by MINUTES (negative moves
it earlier, fractions allowed). A WoWCombatLog-MMDDYY_HHMMSS.txt file name is shifted too.
The originals are never modified; OUT_DIR must not be the folder the logs are in.
"""
import re, sys
from datetime import datetime, timedelta
from pathlib import Path

TS = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2}):(\d{2}):(\d{2})\.(\d+)")
NAME = re.compile(r"^WoWCombatLog-(\d{6}_\d{6})\.txt$")


def parse(line):
    m = TS.match(line)
    if not m:
        return None, None
    mo, d, y, h, mi, s, frac = m.groups()
    dt = datetime(int(y), int(mo), int(d), int(h), int(mi), int(s), int(frac[:6].ljust(6, "0")))
    return dt, m


def fmt(dt, digits):
    return "%d/%d/%d %s.%s" % (dt.month, dt.day, dt.year, dt.strftime("%H:%M:%S"), ("%06d" % dt.microsecond)[:digits].ljust(digits, "0"))


def span(log):
    first = last = None
    with open(log, encoding="utf-8") as f:
        for line in f:
            dt, _ = parse(line)
            if dt:
                first = first or dt
                last = dt
    return first, last


def duration(td):
    secs = int(td.total_seconds())
    return "%d:%02d:%02d" % (secs // 3600, secs // 60 % 60, secs % 60)


def shift(log, out_dir, delta):
    m = NAME.match(log.name)
    name = (datetime.strptime(m.group(1), "%m%d%y_%H%M%S") + delta).strftime("WoWCombatLog-%m%d%y_%H%M%S.txt") if m else log.name
    dest = out_dir / name
    if dest.resolve() == log.resolve() or out_dir.resolve() == log.parent.resolve():
        sys.exit("refusing to write into the original's folder: %s" % log)
    n = 0
    with open(log, encoding="utf-8") as src, open(dest, "w", encoding="utf-8", newline="\n") as out:
        for line in src:
            dt, ts = parse(line)
            if dt:
                line = fmt(dt + delta, len(ts.group(7))) + line[ts.end():]
                n += 1
            out.write(line)
    return dest, n


def main():
    args = sys.argv[1:]
    delta = out_dir = None
    if "--shift" in args:
        i = args.index("--shift")
        try:
            delta, out_dir = timedelta(minutes=float(args[i + 1])), Path(args[i + 2])
        except (IndexError, ValueError):
            sys.exit(__doc__)
        del args[i:i + 3]
    if not args:
        sys.exit(__doc__)
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
    for log in map(Path, args):
        if out_dir:
            dest, n = shift(log, out_dir, delta)
            log = dest
            print("%s: %d timestamps shifted by %+g min" % (dest, n, delta.total_seconds() / 60))
        first, last = span(log)
        if not first:
            print("%s: no timestamps found" % log)
            continue
        print("%s\n  start    %s\n  end      %s\n  duration %s" % (log, first.strftime("%Y-%m-%d %H:%M:%S"),
                                                                 last.strftime("%Y-%m-%d %H:%M:%S"), duration(last - first)))


if __name__ == "__main__":
    main()
