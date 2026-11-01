# Guide tools

Build the guides in `guides/` from data the recovery tools (`recovered/tools/`) cached. Python 3 standard library only; run from the repo root.

| Script              | What it does |
|---------------------|---|
| `trash_guide.py`    | Trash guide per zone into `guides/`: pack identity, kill order + markers, where each role stood, what hits the raid. `python3 guides/tools/trash_guide.py recovered/raw/*.json`. |
| `rotation.py`       | Rotation per class / spec, bosses and trash separately, into `guides/rotations/`: casts/min, damage / healing share, active time, proc and debuff uptimes, consumables at the pull, opener. `python3 guides/tools/rotation.py recovered/raw/*.json`, `--boss NAME` for one boss. |
| `fetch_rankings.py` | Download top and median DPS parses per class / spec for one boss from the public rankings into `recovered/raw/rankings/` (≈6 API points per parse, resumable, waits for the hourly reset). `--encounter 50607` (Mother Shahraz) by default. Uses `wcl.py` and `archive_character.py` from `recovered/tools/`. |
| `best_rotation.py`  | Compare those top vs median parses per spec into `guides/best-rotations/<encounter>.md`: rotation table, active time, uptimes, opener, and an automatic list of what median players do differently. |

`trash_guide.py` and `rotation.py` read `recovered/raw/<code>.json`; get those with `recovered/tools/fetch.py` or `recover.py`.
