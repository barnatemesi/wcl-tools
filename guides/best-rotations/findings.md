# Best rotations and common mistakes: Mother Shahraz, TBC Anniversary

Hand-written summary of [50607.md](50607.md), which `guides/tools/best_rotation.py` generates from public fresh.warcraftlogs.com
rankings (`fetch_rankings.py`). Each spec: the **8 top-ranked parses** vs **8 parses around the median rank** of the top 2000
the API exposes (so "median" players are decent, not bad). One boss, small samples: treat single-spec details as strong
hints, the patterns that repeat across specs as solid.

Names in *italics* are effects whose source I could not confirm (not standard TBC class spells; likely items or
consumables available on Anniversary). Check them in-game before acting on them.

## What separates top parses from median ones, across almost every spec

1. **Raid setup and kill speed, not the player.** Top parses come from ~90–100 s kills; median ones from 130–250 s.
   Top players had Bloodlust/Heroism for ~40% of the fight (median 0–25%), plus Drums, Ferocious Inspiration, Unleashed
   Rage, Leader of the Pack. A short kill also lets one potion + one cooldown cycle cover a bigger share of the fight.
   Part of every DPS gap below is this; the rest is what the player controls:
2. **Every throughput consumable, every pull.** Top players use, nearly 100%: Haste Potion (melee/hunters) or
   Destruction Potion (casters), Flame Cap (fire mage), Thistle Tea (rogues), Super Sapper Charge (engineers, ~75–88% of
   top melee and hunters vs 0–40% of median), their DPS racial (Blood Fury / Berserking), and *Dire Drunkard* /
   *Dark Iron Pipeweed* (one use per fight each). Median players skip one or more of these in 40–100% of parses.
3. **No dead time.** Top casters are casting 94–97% of the fight, median 83–92%. Melee shows the same 7–12 point gap.
   This is gaps between casts: late reactions, unnecessary movement, clipping, casting something useless.
4. **No wasted GCDs on utility.** Median players spend GCDs on things the top players leave to others or do before the
   pull: totems mid-fight (Elemental), Battle Shout and Demoralizing Shout (Arms), Hunter's Mark (Survival/MM when
   another hunter has it), Blink, Ice Barrier, Shadow Ward, Death Coil, healthstones.
5. **Cooldowns at the pull, and twice if possible.** Avenging Wrath, Recklessness, Icy Veins, Rapid Fire, Arcane
   Power: top players have them up longer (they pop them on pull, with lust, and reuse them on cooldown; Frost and
   Arcane mages Cold Snap for a second Icy Veins).

## Per spec: the top rotation, and the clear mistakes

**Druid — Balance.** Faerie Fire → Force of Nature → Moonfire → Starfire spam. Keep Moonfire up (top 83%, median 59%);
skip Insect Swarm. Median players are casting only 86% of the time vs 97%.

**Druid — Feral.** Shred spam (23/min), Rip kept up, and **Ferocious Bite twice as often** as median players (4.1 vs
2.1/min). Top ferals shift out and back into Cat Form far more (13 vs 9 per minute: powershifting for energy) and keep
Mangle up themselves (2.0 vs 0.8/min). Median: 81% active vs 95%, no Haste Potion / Sapper in most parses.

**Hunter — Beast Mastery / Survival / Marksmanship.** All three top groups **melee-weave**: Raptor Strike 6–8/min,
melee 6–13% of their damage (median MM hunters don't weave at all). Kill Command on cooldown (7–8/min), Steady Shot as
the filler, Arcane Shot 4–6/min, Multi-Shot on cooldown, Misdirection on the tank at the pull. Mistakes: no weaving,
too few Kill Commands (MM median 4.5 vs 7.0/min), wasting GCDs on Serpent Sting and Hunter's Mark, no Sapper.

**Mage — Arcane.** Arcane Blast spam (46/min with haste); Icy Veins → Cold Snap → second Icy Veins, Arcane Power,
Presence of Mind and the racial at the pull. Mistakes: Frostbolt filler and Evocation in a fight short enough not to
need them, Icy Veins up less (30% vs 41%).

**Mage — Fire.** Scorch ×5 to stack Fire Vulnerability, then Fireball spam (20/min), Scorch only to refresh. Mistakes:
no Flame Cap (12% of median vs 75%), no Destruction Potion (12% vs 88%), casting mana gems / Blink instead of
Fireballs, Ignite uptime 44% vs 64%, active 83% vs 94%.

**Mage — Frost.** Water Elemental at the pull (**100% of top, 38% of median**), Frostbolt spam, Icy Veins + Cold Snap
for two of each. Mistakes: no Water Elemental, no Cold Snap, no Destruction Potion (0% of median), Ice Barrier and Ice
Lance taking GCDs.

**Paladin — Retribution.** **Seal twisting**: Seal of Command and Seal of Blood / the Martyr ~9 times each per minute
(median ~6), Crusader Strike on cooldown, Judgement ~4.6/min, Avenging Wrath at the pull. Mistakes: less twisting,
too many Exorcisms (2.3 vs 1.5/min), Avenging Wrath up less (14% vs 23%), no Sapper, active 62% vs 74%.

**Priest — Shadow.** Vampiric Touch → Shadow Word: Pain → Mind Blast → Shadow Word: Death → Mind Flay; then Mind Blast
and SW:Death on cooldown, Mind Flay filler (16.5 vs 12.7/min), Shadowfiend. DoTs ~96%/90% up. Main gap: active 82% vs
73% — median priests leave dead time between Mind Flays.

**Rogue — Combat.** Sinister Strike, Slice and Dice ~93% up, Expose Armor if no one else has it, Blade Flurry +
Adrenaline Rush + Haste Potion together. Rotations are nearly identical between groups; the gap is Thistle Tea (88% of
top vs 50%), Sapper (88% vs 12%), 9 points of active time, and raid group placement (Leader of the Pack and Ferocious
Inspiration were up 90–98% for top rogues, 0% for median ones).

**Rogue — Assassination / Subtlety** (small populations: 204 and 226 parses). Top rogues keep **Expose Armor up
themselves (~85%; median 0%)**, use Thistle Tea and Haste Potion; top Subtlety open from stealth with Garrote and use
Vanish + Preparation.

**Shaman — Elemental.** Lightning Bolt spam, **Chain Lightning on every cooldown** (7.1 vs 4.9/min), totems and Water
Shield placed before the pull. Mistakes: re-dropping Mana Spring / Tremor / Totem of Wrath / Wrath of Air mid-fight,
Water Shield mid-fight, no Destruction Potion (38% skip it).

**Shaman — Enhancement.** Stormstrike on cooldown, **Earth Shock rather than Flame Shock** (3.7 ES vs 2.6 FS per minute
for the top; median the other way round), Windfury / Grace of Air totem twisting (4.5/min each), Lightning Shield up,
Shamanistic Rage. Mistakes: Searing Totem (88% of median, 75% of top don't), Fire Nova, no Lightning Shield.

**Warlock — Destruction / Affliction / Demonology.** All three top groups are Shadow Bolt spam (80–94% of damage).
Curse of Doom first (Destruction, Demonology) or Curse of the Elements + Corruption (Affliction), Shadowburn as an
extra instant. Mistakes: **too many Life Taps** (median 2.0–2.8/min vs 1.3–1.9), Siphon Life on Affliction (median
1.7/min, top 0.6), Shadow Ward / Death Coil / Incinerate taking cast time, no Destruction Potion (25% of median
Affliction, 12% of median Demonology), no Curse of Doom on Demonology (0% uptime vs 63%).

**Warrior — Fury / Arms.** **Heroic Strike on every swing** as the rage dump (Arms top 26/min vs median 9/min!),
**Hamstring weaving** in the GCDs between Bloodthirst/Mortal Strike and Whirlwind (Fury 7.5 vs 3.3/min, Arms 6.4 vs 0),
Recklessness and *Bloodbath* on the pull. Mistakes: Arms median players cast Slam, Battle Shout, Demoralizing Shout
and Intercept instead; both specs use Recklessness/*Bloodbath* less and skip Sapper.

## How to use this for your raid

- Run `python3 guides/tools/rotation.py recovered/raw/*.json --boss shahraz --names --out <somewhere local>` (from the repo root) and compare your players' casts/min,
  active time and buff list against the tables in [50607.md](50607.md).
- More bosses: `python3 guides/tools/fetch_rankings.py --encounter <id>` (≈1.5 h of API budget for all specs at 8 + 8), then
  `python3 guides/tools/best_rotation.py --encounter <id>`. Encounter ids are in the fetch script's docstring.
