"""Step 3: weekly statistics + chart.

usage: ../.venv/bin/python make_chart.py [--partial]
reads data/guild_reports.jsonl (+ data/sample_players.jsonl if present)
writes output/weekly_stats.csv and output/thunderstrike_raiding_trend.png

- raiding guilds / week: exact count of guilds with >= 1 report in a TBC raid zone that raid week
- raiders / week: (mean distinct boss-pull players per sampled guild-week) x (raiding guild-weeks),
  with a 90% bootstrap interval. Players in two guilds' raids the same week count twice (pugs, alts).
- phase lines: the first week a phase's raid shows up in Thunderstrike logs (Phase 1 = first Karazhan week)
"""
import collections, csv, random, sys
from datetime import date, timedelta
from common import DATA, OUTPUT, RAID_ZONES, read_jsonl, week_start

PHASES = [("Phase 1", "Karazhan, Gruul, Magtheridon", {1047, 1048}),
          ("Phase 2", "SSC, Tempest Keep", {1056}),
          ("Phase 3", "Black Temple, Hyjal", {1060})]
# A phase starts in the first week that >= 25% of raiding guilds log its raid. A plain "first report" rule
# fires a week early on a handful of stray reports (11 SSC/TK guilds on 29 Apr, 13 BT/Hyjal guilds on 12 Aug).
PHASE_SHARE = 0.25

# reference palette (dataviz skill), light mode
SURFACE, INK, INK2, MUTED, GRID, AXIS, BLUE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#2a78d6"


def load():
    guilds_by_week = collections.defaultdict(set)
    zone_guilds = collections.defaultdict(lambda: collections.defaultdict(set))
    n_guilds = 0
    for g in read_jsonl(DATA / "guild_reports.jsonl"):
        n_guilds += 1
        for r in g["reports"]:
            z = (r.get("zone") or {}).get("id")
            if z in RAID_ZONES:
                w = week_start(r["startTime"])
                guilds_by_week[w].add(g["id"])
                zone_guilds[z][w].add(g["id"])
    return n_guilds, guilds_by_week, zone_guilds


def phase_starts(zone_guilds, guilds_by_week):
    out = []
    for name, raids, zones in PHASES:
        weeks = sorted(w for w in guilds_by_week
                       if len(set().union(*(zone_guilds[z].get(w, set()) for z in zones)))
                       >= PHASE_SHARE * len(guilds_by_week[w]))
        if weeks:
            out.append((name, raids, weeks[0]))
    return out


def estimate(guilds_by_week):
    samples = collections.defaultdict(list)
    for s in read_jsonl(DATA / "sample_players.jsonl"):
        samples[date.fromisoformat(s["week"])].append(len(s["players"]))
    rng, est = random.Random(7), {}
    for w, xs in samples.items():
        n = len(guilds_by_week.get(w, ()))
        if not xs or not n:
            continue
        boot = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) * n for _ in range(2000))
        est[w] = (sum(xs) / len(xs) * n, boot[100], boot[1899], len(xs))
    return est


def main():
    partial = "--partial" in sys.argv
    n_guilds, guilds_by_week, zone_guilds = load()
    phases = phase_starts(zone_guilds, guilds_by_week)
    est = estimate(guilds_by_week)
    first = phases[0][2] if phases else min(guilds_by_week)
    # drop weeks that hadn't ended when the guild scan started: their later raids weren't uploaded yet
    scan_started = (DATA / "guild_reports.jsonl").stat()
    scan_started = getattr(scan_started, "st_birthtime", scan_started.st_mtime) * 1000
    last_full = week_start(scan_started)
    weeks = [w for w in sorted(guilds_by_week) if first <= w < last_full]

    OUTPUT.mkdir(exist_ok=True)
    with open(OUTPUT / "weekly_stats.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["week_start (Wed reset)", "raiding_guilds", "raiders_estimate", "raiders_low_90", "raiders_high_90",
                     "sampled_guild_weeks", "phase"])
        for w in weeks:
            ph = [p[0] for p in phases if p[2] <= w][-1:] or [""]
            e = est.get(w)
            wr.writerow([w, len(guilds_by_week[w])] + ([round(e[0]), round(e[1]), round(e[2]), e[3]] if e else ["", "", "", 0]) + ph)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    plt.rcParams.update({"font.family": ["Helvetica Neue", "Arial", "sans-serif"], "font.size": 10,
                         "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED})
    fig, axes = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True, facecolor=SURFACE,
                             gridspec_kw={"height_ratios": [1, 1], "hspace": 0.28})
    ew = [w for w in weeks if w in est]
    panels = [
        (axes[0], "Raiders per week (estimate)",
         "Distinct players in boss pulls of Thunderstrike guild raids; shaded = 90% range of the sample estimate",
         ew, [est[w][0] for w in ew], ([est[w][1] for w in ew], [est[w][2] for w in ew])),
        (axes[1], "Raiding guilds per week",
         "Thunderstrike guilds with at least one logged TBC raid that week",
         weeks, [len(guilds_by_week[w]) for w in weeks], None),
    ]
    for ax, title, sub, xs, ys, band in panels:
        ax.set_facecolor(SURFACE)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(AXIS)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(length=0)
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=INK, pad=22)
        ax.text(0, 1.03, sub, transform=ax.transAxes, fontsize=9.5, color=INK2)
        if not xs:
            ax.text(0.5, 0.5, "no sampled weeks yet", transform=ax.transAxes, ha="center", color=MUTED)
            continue
        if band:
            ax.fill_between(xs, band[0], band[1], color=BLUE, alpha=0.14, linewidth=0)
        ax.plot(xs, ys, color=BLUE, linewidth=2, solid_capstyle="round")
        ax.plot(xs[-1], ys[-1], "o", color=BLUE, markersize=6, markeredgecolor=SURFACE, markeredgewidth=2)
        ax.annotate("{:,.0f}".format(ys[-1]), (xs[-1], ys[-1]), xytext=(8, 0), textcoords="offset points",
                    va="center", fontsize=10, color=INK, fontweight="bold")
        peak = max(range(len(ys)), key=ys.__getitem__)
        if peak != len(ys) - 1:
            ax.annotate("peak {:,.0f}".format(ys[peak]), (xs[peak], ys[peak]), xytext=(0, 8), textcoords="offset points",
                        ha="center", fontsize=9, color=INK2)
        ax.set_ylim(0, max(band[1] if band else ys) * 1.18)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,.0f}".format(v)))
        for name, raids, start in phases:
            ax.axvline(start, color=AXIS, linewidth=1, zorder=0)
            if ax is axes[0]:
                ax.text(start + timedelta(days=2), ax.get_ylim()[1] * 0.97, "%s\n%s" % (name, raids),
                        va="top", fontsize=8.5, color=INK2, linespacing=1.3)
    axes[1].xaxis.set_major_locator(mdates.MonthLocator())
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    if phases:
        cur = phases[-1]
        fig.suptitle("Thunderstrike-EU raiding activity, TBC Anniversary  ·  current: %s (%s, since %s)"
                     % (cur[0], cur[1], cur[2].strftime("%-d %b %Y")), x=0.07, ha="left", fontsize=11, color=INK2, y=0.995)
    note = ("Source: fresh.warcraftlogs.com API, %d Thunderstrike guilds scanned. Weeks start at the Wednesday reset;\n"
            "weeks not finished when the scan started are left out. Only guild-tagged logs count.") % n_guilds
    if partial:
        note = "PRELIMINARY: player sampling still running, raider line incomplete.\n" + note
    fig.text(0.07, 0.008, note, fontsize=8, color=MUTED, linespacing=1.4)
    fig.subplots_adjust(left=0.07, right=0.95, top=0.9, bottom=0.11)
    path = OUTPUT / "thunderstrike_raiding_trend.png"
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    print(path, "|", len(weeks), "weeks |", len(ew), "weeks with player estimate |", n_guilds, "guilds |", phases)


if __name__ == "__main__":
    main()
