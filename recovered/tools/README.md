# WarcraftLogs → WoW combat log recovery tools

Rebuild lost `WoWCombatLog-*.txt` files (TBC Anniversary, 2.5.x, `COMBAT_LOG_VERSION 9`) from reports
uploaded to fresh.warcraftlogs.com. Python 3 standard library only, nothing to install.

Run everything from `wow-tbc-logs/recovered/` as `python3 tools/<script>.py ...`.

## Setup (once)

1. Create an API client at https://fresh.warcraftlogs.com/api/clients/ (redirect URL `http://localhost`,
   "Public Client" unchecked).
2. Put the values in `wow-tbc-logs/.env`:
   ```
   WCL_CLIENT_ID=...
   WCL_CLIENT_SECRET=...
   ```
   The access token is cached in `tools/.token-cache.json` (valid ~1 year; delete it to force a new one).
   For non-Fresh classic reports set `WCL_HOST`, e.g. `WCL_HOST=https://classic.warcraftlogs.com`.

## Scripts

| Script | What it does |
|---|---|
| `recover.py` | **All-in-one.** Download (cached in `raw/`) and convert reports. `--links file.md` takes every report link in a file; `--refetch` re-downloads. |
| `fetch.py` | Download one report's metadata + every event to `raw/<code>.json`. |
| `convert.py` | Turn a `raw/<code>.json` into combat logs, **one file per zone**, e.g. `black-temple/`, `hyjal-summit/`. |
| `list_fights.py` | Report title, date, owner, boss pulls (kill / wipe %), zones, players. `--trash` includes trash. |
| `list_reports.py` | Find reports by guild (`--guild X --server thunderstrike`) or user (`--user <id>`), optional `--zone 534`. `--links` prints only URLs, ready to paste into a links file. |
| `wcl_table.py` | WarcraftLogs' own damage / healing table for a fight, for cross-checking. |
| `summary.py` | Damage / effective-healing per player for each pull in a combat log (works on real logs too). |
| `split_log.py` | Split any combat log per zone, or per boss pull with `--encounters` (`<date>_<boss>_<n>_kill|wipe|incomplete.txt`). |
| `rename_player.py` | Copy logs to a new folder with a player's name (and optionally GUID, `--guid OLD NEW`) replaced. Originals untouched. |
| `archive_character.py` | Archive every raid a character took part in, one report per raid night. Paced to the API budget and resumable. `--dry-run` previews the nights; `--keep-raw` keeps the JSON dumps. |
| `raid_time.py` | Start, end and duration of each log. `--shift MINUTES OUT_DIR` writes copies with every timestamp (and the file name) shifted; negative = earlier. Originals untouched. |
| `compare_format.py` | Compare field counts per event type between a real log and a rebuilt one. |
| `wcl.py` | Shared helper (credentials, token, GraphQL with retries); not run directly. |

## Examples

```sh
python3 tools/recover.py --links ../wow-tbc-bt-links.md          # everything in the links file
python3 tools/recover.py https://fresh.warcraftlogs.com/reports/ABC123xyz
python3 tools/list_fights.py ABC123xyz
python3 tools/archive_character.py MyCharacter --dry-run
python3 tools/list_reports.py --guild "My Guild" --server thunderstrike --zone 534 --links >> ../hyjal-links.md
python3 tools/split_log.py black-temple/WoWCombatLog-091326_203307.txt bt-pulls --encounters
python3 tools/summary.py bt-pulls/9-13-2026_the-illidari-council_4_kill.txt --top 5
python3 tools/wcl_table.py 6MGfJ2tR3mBwL1hn 38 --top 5                 # should match the line above
```

Zone IDs: 532 Karazhan, 534 Hyjal Summit, 564 Black Temple, 565 Gruul's Lair, 544 Magtheridon,
548 Serpentshrine Cavern, 550 Tempest Keep, 568 Zul'Aman, 580 Sunwell Plateau.

## How faithful the rebuilt logs are

Checked against a real Karazhan log (`../tbc-kara-example/`): almost every event type has the same field layout.
Damage and healing totals match WarcraftLogs to within ~0.1%.

Recovered exactly: timestamps (local time), sources / targets, spell IDs, names and schools, damage, healing,
overheal, overkill, absorbs, resists, blocks, crits / glancing / crushing, misses, aura applies / removes / stacks,
casts, energize / drain, deaths, interrupts, dispels, summons, boss encounter start / end, gear / gems / enchants /
talents / stats (`COMBATANT_INFO`), unit HP, power, AP / SP / armor, position, item level, raid markers.

Approximated:
- **Player GUIDs** `Player-<realm>-<hex>`. The hex part is exact. Realm IDs: Thunderstrike 6409 (from the
  real log), **Spineshatter 6408 is a guess**. Edit `REALM_IDS` in `convert.py` if you learn the real one.
- **NPC / pet GUIDs** are synthetic but consistent within a file.
- **Unit flags** are standard values (players `0x514`, pets `0x1114`, totems `0x2114`, NPCs `0xa48`).
  Friendly NPCs are marked hostile.
- **Facing** is a best-guess conversion from WarcraftLogs' rotated coordinate system.
- **Periodic vs direct energize** uses a fixed list of known periodic spells (`PERIODIC_ENERGIZE`).
- **Damage shields** (Thorns, Retribution Aura) come from a fixed spell list (`DAMAGE_SHIELD`).

Not recoverable (WarcraftLogs doesn't keep them): `SPELL_CAST_FAILED`, `EMOTE`, `ENCHANT_APPLIED/REMOVED`,
`MAP_CHANGE`, `SWING_DAMAGE_LANDED`, and anything outside the uploaded time range.

## Notes on the WarcraftLogs data (for anyone editing convert.py)

- Coordinates: world X = `y / 100`, world Y = `-x / 100`.
- The resource fields are shifted relative to the raw log: `absorb` = power type, `classResources.type` = current
  power, `.amount` = max power, `.max` = power cost. Rage is on a 0-1000 scale.
- Player `hitPoints` are percentages (the 2.5.x client logs player HP as 0-100 too). NPC HP is absolute.
- Damage `amount` excludes overkill (log amount = amount + overkill) and absorbed damage.
- Heal `amount` excludes overheal (log amount = amount + overheal).
- A player actor's `gameID` in hex is the player GUID suffix.
