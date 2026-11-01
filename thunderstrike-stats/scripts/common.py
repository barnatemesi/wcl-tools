"""Shared bits: WCL API access (reuses recovered/tools/wcl.py), rate-limit pacing, raid zones and weeks."""
import json, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUTPUT = HERE.parent / "output"
sys.path.insert(0, str(HERE.parents[1] / "recovered" / "tools"))
import wcl  # noqa: E402

REGION, SERVER = "EU", "thunderstrike"
SINCE = datetime(2026, 1, 1, tzinfo=timezone.utc)
# fresh.warcraftlogs.com zone ids for the TBC Anniversary raids (main list endpoint shows the old Classic ids)
RAID_ZONES = {1047: "Karazhan", 1048: "Gruul / Magtheridon", 1056: "SSC / TK", 1060: "BT / Hyjal"}
POINTS_SAFETY = 960  # pause before the 1000 points/hour limit


def _sleep_until_reset(reason):
    rl = wcl.query("{ rateLimitData { pointsSpentThisHour pointsResetIn } }")["rateLimitData"]
    wait = rl["pointsResetIn"] + 15
    print("[%s] %s (%.0f points spent), sleeping %ds for the hourly reset" %
          (datetime.now().strftime("%H:%M"), reason, rl["pointsSpentThisHour"], wait), file=sys.stderr, flush=True)
    # short naps against the wall clock: on macOS time.sleep() stops counting while the Mac is asleep,
    # so one long sleep can overrun the reset by however long the lid was closed
    deadline = time.time() + wait
    while time.time() < deadline:
        time.sleep(min(30, max(0, deadline - time.time())))


def paced_query(gql, variables=None):
    """Run a query, sleeping until the hourly reset when the points budget is (nearly) spent."""
    rl = wcl.query("{ rateLimitData { limitPerHour pointsSpentThisHour } }")["rateLimitData"]
    if rl["pointsSpentThisHour"] > min(POINTS_SAFETY, rl["limitPerHour"] - 40):
        _sleep_until_reset("budget nearly spent")
    for _ in range(4):
        try:
            return wcl.query(gql, variables, retries=2)
        except RuntimeError as e:
            if "points" not in str(e):
                raise
            _sleep_until_reset("API says no points remaining")
    return wcl.query(gql, variables)


def week_start(ms):
    """Start of the EU raid week (Wednesday 05:00 UTC reset) containing the epoch-ms timestamp."""
    t = datetime.fromtimestamp(ms / 1000, timezone.utc) - timedelta(hours=5)
    return (t - timedelta(days=(t.weekday() - 2) % 7)).date()


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def append_jsonl(path, rows):
    with open(path, "a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
