"""Copy combat logs into a new folder with one player's name (and optionally GUID) replaced.

usage: python3 rename_player.py <out_dir> <old name> <new name> [--guid OLD_GUID NEW_GUID] <log.txt> [<log.txt> ...]

Names are the full log form, e.g. "Sarazein-Thunderstrike-EU". GUIDs look like Player-6409-04AF0032.
The originals are never modified; out_dir must not be the folder the logs are in.
"""
import sys
from pathlib import Path


def main():
    args = sys.argv[1:]
    guid = None
    if "--guid" in args:
        i = args.index("--guid")
        guid = (args[i + 1], args[i + 2])
        del args[i:i + 3]
    if len(args) < 4:
        sys.exit(__doc__)
    out_dir, old, new, logs = Path(args[0]), args[1], args[2], [Path(p) for p in args[3:]]
    out_dir.mkdir(parents=True, exist_ok=True)
    reps = [('"%s"' % old, '"%s"' % new)] + ([guid] if guid else [])
    for log in logs:
        dest = out_dir / log.name
        if dest.resolve() == log.resolve():
            sys.exit("refusing to overwrite the original: %s" % log)
        counts = [0] * len(reps)
        with open(log, encoding="utf-8") as src, open(dest, "w", encoding="utf-8", newline="\n") as out:
            for line in src:
                for i, (a, b) in enumerate(reps):
                    if a in line:
                        counts[i] += line.count(a)
                        line = line.replace(a, b)
                out.write(line)
        print("%s: %s" % (dest, ", ".join("%s -> %s x%d" % (a, b, n) for (a, b), n in zip(reps, counts))))


if __name__ == "__main__":
    main()
