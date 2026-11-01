# The Eye rotations

Built by `guides/tools/rotation.py` from 5 boss pulls and 22 trash pulls. Per spec, bosses and trash separately. Casts/min is per minute alive; *Active* is the share of alive time spent casting or on the GCD (channels count as one GCD; energy and rage classes are resource-capped, so they read lower). Damage and healing include absorbed amounts; pet damage is listed as (pet).

Specs: [Druid — Balance](#druid-balance), [Druid — Restoration](#druid-restoration), [Druid — tank](#druid-tank), [Hunter — BeastMastery](#hunter-beastmastery), [Hunter — ranged](#hunter-ranged), [Mage — Arcane](#mage-arcane), [Paladin — Holy](#paladin-holy), [Paladin — Justicar](#paladin-justicar), [Paladin — Retribution](#paladin-retribution), [Paladin — tank](#paladin-tank), [Priest — Holy](#priest-holy), [Priest — Shadow](#priest-shadow), [Rogue — melee](#rogue-melee), [Shaman — Elemental](#shaman-elemental), [Shaman — Enhancement](#shaman-enhancement), [Shaman — Restoration](#shaman-restoration), [Warlock — Destruction](#warlock-destruction), [Warlock — ranged](#warlock-ranged), [Warrior — Fury](#warrior-fury)

## Druid — Balance

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Starfire | 10.0 | 55% | 75% |
| Moonfire | 5.0 | 28% | 20% |
| Faerie Fire | 1.0 | 5% | – |
| Mental Protection Field | 0.9 | 5% | – |
| Hurricane | 0.1 | 1% | 4% |
| Dark Iron Pipeweed | 0.2 | 1% | – |
| Innervate | 0.2 | 1% | – |
| (pet) Melee | – | – | 1% |
| Force of Nature | 0.2 | 1% | – |
| Cat Form | 0.1 | 1% | – |
| Moonkin Form | 0.1 | 1% | – |
| Rebirth | 0.1 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 850 | 61% | Starfire 10.0, Moonfire 5.0, Faerie Fire 1.0 |

**Short buff / proc uptime:** Nature's Grace 34%, Unstable Currents 13%
**Self-buffs up at the pull** (% of 4 boss pulls): Flask of Blinding Light 100%, Moonkin Aura 100%, Well Fed 100%
**Debuff uptime on the boss:** Moonfire 57%, Faerie Fire 49%
**Usual opener** (most common cast at each step over 5 pulls): Moonfire → Faerie Fire → Starfire → Starfire → Moonfire → Starfire → Starfire → Starfire

#### Trash (1 player, 16 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Starfire | 10.3 | 52% | 71% |
| Moonfire | 7.7 | 39% | 21% |
| Hurricane | 0.2 | 1% | 7% |
| Cyclone | 0.7 | 4% | – |
| Faerie Fire | 0.6 | 3% | – |
| Insect Swarm | 0.1 | 0% | – |
| Dash | 0.1 | 0% | – |
| Dark Iron Pipeweed | 0.1 | 0% | – |
| Thorns | 0.1 | 0% | – |
| Cat Form | 0.1 | 0% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 917 | 68% | Starfire 10.3, Moonfire 7.7, Cyclone 0.7 |

**Short buff / proc uptime:** Nature's Grace 37%, Unstable Currents 18%
**Compared with bosses** (casts/min): more Moonfire +2.6, Cyclone +0.7; less Mental Protection Field -0.9, Faerie Fire -0.4

## Druid — Restoration

#### Bosses (1 player, 20 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Regrowth | 8.8 | 26% | 51% |
| Lifebloom | 11.6 | 34% | 26% |
| Rejuvenation | 8.5 | 25% | 14% |
| Swiftmend | 1.8 | 5% | 7% |
| Tranquility | 0.2 | 0% | 2% |
| Hopped Up | 0.5 | 2% | – |
| Essence of the Martyr | 0.5 | 1% | – |
| Nature's Swiftness | 0.4 | 1% | – |
| Restore Mana | 0.4 | 1% | – |
| Dark Rune | 0.4 | 1% | – |
| Barkskin | 0.3 | 1% | – |
| Incarnation: Tree of Life | 0.2 | 1% | – |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 5 | 1025 | 83% | Lifebloom 11.6, Regrowth 8.8, Rejuvenation 8.5 |

**Short buff / proc uptime:** Band of the Eternal Restorer 14%
**Self-buffs up at the pull** (% of 4 boss pulls): Versatility 100%, Healing Power 100%, Well Fed 100%, Elixir of Draenic Wisdom 100%
**Usual opener** (most common cast at each step over 5 pulls): Lifebloom → Lifebloom → Rejuvenation → Swiftmend → Lifebloom → Lifebloom → Lifebloom → Nature's Swiftness

#### Trash (1 player, 16 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Lifebloom | 14.7 | 46% | 38% |
| Regrowth | 6.0 | 19% | 32% |
| Rejuvenation | 7.9 | 25% | 15% |
| Swiftmend | 1.7 | 5% | 12% |
| Tranquility | 0.2 | 1% | 4% |
| Essence of the Martyr | 0.5 | 2% | – |
| Hopped Up | 0.4 | 1% | – |
| Nature's Swiftness | 0.4 | 1% | – |
| Incarnation: Tree of Life | 0.2 | 1% | – |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 22 | 834 | 81% | Lifebloom 14.7, Rejuvenation 7.9, Regrowth 6.0 |

**Short buff / proc uptime:** Band of the Eternal Restorer 18%
**Compared with bosses** (casts/min): more Lifebloom +3.0; less Regrowth -2.8, Rejuvenation -0.6, Dark Rune -0.4

## Druid — tank

#### Bosses (1 player, 17 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Maul | 9.1 | 26% | 27% |
| Lacerate | 7.0 | 20% | 12% |
| Mangle (Bear) | 4.1 | 12% | 12% |
| Melee | – | – | 22% |
| Swipe (Bear) | 4.7 | 13% | 7% |
| Mangle (Cat) | 2.8 | 8% | 12% |
| Rip | 0.4 | 1% | 5% |
| Mental Protection Field | 1.8 | 5% | – |
| Cat Form | 1.1 | 3% | – |
| Dire Bear Form | 0.9 | 2% | – |
| Ferocious Bite | 0.2 | 0% | 1% |
| Enrage | 0.6 | 2% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 672 | 61% | Maul 9.1, Lacerate 7.0, Swipe (Bear) 4.7 |

**Short buff / proc uptime:** Mark of the White Stag 73%, Mental Protection Field 25%, Track Humanoids 20%, Band of the Eternal Champion 11%
**Self-buffs up at the pull** (% of 4 boss pulls): Agility 100%, Strength 100%, Mighty Agility 100%, Well Fed 100%, Leader of the Pack 100%, Gift of Arthas 75%, Dire Bear Form 50%, Elixir of Ironskin 25%
**Debuff uptime on the boss:** Lacerate 52%, Mangle (Bear) 38%, Gift of Arthas 32%, Mangle (Cat) 15%, Rip 8%
**Usual opener** (most common cast at each step over 5 pulls): Rejuvenation → Mangle (Bear) → Maul → Lacerate → Lacerate → Maul → Dire Drunkard → Mangle (Bear)

#### Trash (1 player, 17 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Maul | 10.4 | 26% | 30% |
| Swipe (Bear) | 9.4 | 24% | 18% |
| Mangle (Bear) | 5.4 | 14% | 16% |
| Lacerate | 7.4 | 19% | 6% |
| Melee | – | – | 21% |
| Mangle (Cat) | 1.8 | 5% | 6% |
| Growl | 1.5 | 4% | – |
| Ferocious Bite | 0.2 | 1% | 1% |
| Wild Charge | 0.6 | 2% | – |
| Enrage | 0.6 | 1% | – |
| Cat Form | 0.5 | 1% | – |
| (pet) Bitter Brew | – | – | 1% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 641 | 71% | Maul 10.4, Swipe (Bear) 9.4, Lacerate 7.4 |

**Short buff / proc uptime:** Mark of the White Stag 65%, Band of the Eternal Champion 17%, Track Humanoids 11%
**Compared with bosses** (casts/min): more Swipe (Bear) +4.7, Maul +1.3, Mangle (Bear) +1.3; less Mental Protection Field -1.8, Mangle (Cat) -1.0, Dire Bear Form -0.8

## Hunter — BeastMastery

#### Bosses (2 players, 39 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Steady Shot | 15.6 | 47% | 27% |
| Auto Shot | – | – | 34% |
| Arcane Shot | 3.8 | 12% | 7% |
| Multi-Shot | 3.5 | 10% | 7% |
| (pet) Melee | – | – | 17% |
| Kill Command | 5.5 | 17% | – |
| (pet) Kill Command | – | – | 4% |
| Serpent Sting | 1.0 | 3% | 1% |
| (pet) Gore | – | – | 2% |
| Dire Drunkard | 0.5 | 2% | – |
| Bestial Wrath | 0.5 | 2% | – |
| Hunter's Mark | 0.4 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1347 | 71% | Steady Shot 15.7, Kill Command 5.4, Arcane Shot 5.2 |
| 5 | 1225 | 67% | Steady Shot 15.6, Kill Command 5.6, Multi-Shot 2.6 |

**Short buff / proc uptime:** Quick Shots 26%, Dragonspine Flurry 22% (1 of 2), Dire Drunkard 17% (1 of 2), The Beast Within 14% (1 of 2), Lust for Battle 12% (1 of 2)
**Self-buffs up at the pull** (% of 8 boss pulls): Mighty Agility 100%, Well Fed 100%, Greater Versatility 62%
**Debuff uptime on the boss:** Hunter's Mark 47% (1 of 2), Serpent Sting 26% (1 of 2)
**Usual opener** (most common cast at each step over 10 pulls): Hunter's Mark → Rapid Fire → Dire Drunkard → Arcane Shot → Multi-Shot → Steady Shot → Steady Shot → Steady Shot

#### Trash (2 players, 34 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Steady Shot | 14.9 | 45% | 23% |
| Auto Shot | – | – | 29% |
| Arcane Shot | 4.3 | 13% | 7% |
| Multi-Shot | 3.1 | 9% | 9% |
| (pet) Melee | – | – | 18% |
| Kill Command | 5.4 | 16% | – |
| (pet) Kill Command | – | – | 5% |
| Raptor Strike | 0.8 | 2% | 1% |
| Hunter's Mark | 1.2 | 4% | – |
| (pet) Gore | – | – | 3% |
| Explosive Trap Effect | – | – | 2% |
| Serpent Sting | 0.4 | 1% | 0% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 1150 | 71% | Steady Shot 17.0, Kill Command 5.8, Arcane Shot 3.2 |
| 22 | 1079 | 65% | Steady Shot 12.8, Arcane Shot 5.3, Kill Command 5.1 |

**Short buff / proc uptime:** Quick Shots 23%, Dragonspine Flurry 19% (1 of 2), Dire Drunkard 11% (1 of 2)
**Compared with bosses** (casts/min): more Hunter's Mark +0.8, Raptor Strike +0.7, Arcane Shot +0.4; less Steady Shot -0.8, Serpent Sting -0.6, Multi-Shot -0.4

## Hunter — ranged

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Steady Shot | 16.7 | 68% | 40% |
| Auto Shot | – | – | 40% |
| Multi-Shot | 1.7 | 7% | 4% |
| Kill Command | 2.7 | 11% | – |
| Arcane Shot | 1.4 | 6% | 4% |
| (pet) Melee | – | – | 8% |
| Hunter's Mark | 0.6 | 3% | – |
| (pet) Kill Command | – | – | 2% |
| (pet) Gore | – | – | 2% |
| Dire Drunkard | 0.4 | 1% | – |
| Lust for Battle | 0.3 | 1% | – |
| Misdirection | 0.2 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 758 | 57% | Steady Shot 16.7, Kill Command 2.7, Multi-Shot 1.7 |

**Short buff / proc uptime:** Exploited Weakness 49%, Quick Shots 20%, Dire Drunkard 12%
**Self-buffs up at the pull** (% of 4 boss pulls): Mighty Agility 100%, Well Fed 100%
**Debuff uptime on the boss:** Expose Weakness 47%, Hunter's Mark 32%, Armor Disruption 12%
**Usual opener** (most common cast at each step over 5 pulls): Steady Shot → Steady Shot → Steady Shot → Dire Drunkard → Steady Shot → Steady Shot → Steady Shot → Steady Shot

#### Trash (1 player, 17 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Steady Shot | 17.4 | 63% | 35% |
| Auto Shot | – | – | 36% |
| Multi-Shot | 2.5 | 9% | 11% |
| Kill Command | 3.5 | 13% | – |
| Arcane Shot | 1.8 | 7% | 5% |
| (pet) Melee | – | – | 8% |
| Hunter's Mark | 1.7 | 6% | – |
| (pet) Kill Command | – | – | 3% |
| (pet) Gore | – | – | 2% |
| Dire Drunkard | 0.2 | 1% | – |
| Lust for Battle | 0.1 | 0% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 673 | 64% | Steady Shot 17.4, Kill Command 3.5, Multi-Shot 2.5 |

**Short buff / proc uptime:** Exploited Weakness 46%, Quick Shots 31%
**Compared with bosses** (casts/min): more Hunter's Mark +1.1, Multi-Shot +0.8, Kill Command +0.8

## Mage — Arcane

#### Bosses (2 players, 39 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Arcane Blast | 22.0 | 78% | 85% |
| Arcane Explosion | 1.7 | 6% | 10% |
| Frostbolt | 0.9 | 3% | 4% |
| Restore Mana | 0.4 | 2% | – |
| Replenish Mana | 0.4 | 2% | – |
| Icy Veins | 0.4 | 1% | – |
| Blessing of the Silver Crescent | 0.4 | 1% | – |
| Fireball | 0.1 | 0% | 1% |
| Arcane Power | 0.3 | 1% | – |
| Blink | 0.3 | 1% | – |
| Dark Iron Pipeweed | 0.2 | 1% | – |
| Ice Lance | 0.1 | 0% | 0% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1542 | 64% | Arcane Blast 22.3, Arcane Explosion 1.7, Frostbolt 0.6 |
| 5 | 1189 | 66% | Arcane Blast 21.6, Arcane Explosion 1.8, Frostbolt 1.1 |

**Short buff / proc uptime:** Arcane Madness 58% (1 of 2), Blessing of the Silver Crescent 15% (1 of 2), Icy Veins 14%, Band of the Eternal Sage 11% (1 of 2)
**Self-buffs up at the pull** (% of 8 boss pulls): Well Fed 100%, Mage Armor 100%, Elixir of Draenic Wisdom 100%, Spellpower Elixir 50%
**Usual opener** (most common cast at each step over 10 pulls): Arcane Blast → Arcane Blast → Arcane Blast → Arcane Blast → Arcane Blast → Arcane Blast → Arcane Blast → Arcane Blast

#### Trash (2 players, 33 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Arcane Blast | 14.6 | 50% | 67% |
| Arcane Explosion | 4.5 | 15% | 28% |
| Polymorph | 6.9 | 23% | – |
| Frostbolt | 0.8 | 3% | 4% |
| Fire Blast | 0.3 | 1% | 1% |
| Ice Lance | 0.5 | 2% | 0% |
| Blessing of the Silver Crescent | 0.3 | 1% | – |
| Arcane Power | 0.2 | 1% | – |
| Icy Veins | 0.2 | 1% | – |
| Blink | 0.2 | 1% | – |
| Flamestrike | 0.1 | 0% | 0% |
| Counterspell | 0.1 | 0% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 1157 | 77% | Arcane Blast 17.6, Arcane Explosion 5.7, Polymorph 3.1 |
| 22 | 931 | 73% | Arcane Blast 11.5, Polymorph 10.9, Arcane Explosion 3.2 |

**Short buff / proc uptime:** Arcane Madness 37% (1 of 2), Band of the Eternal Sage 18% (1 of 2), Blessing of the Silver Crescent 12% (1 of 2), Fungal Frenzy 10% (1 of 2)
**Compared with bosses** (casts/min): more Polymorph +6.9, Arcane Explosion +2.8, Ice Lance +0.3; less Arcane Blast -7.3, Restore Mana -0.4, Replenish Mana -0.4

## Paladin — Holy

#### Bosses (1 player, 20 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Flash of Light | 16.8 | 64% | 47% |
| Holy Light | 7.3 | 28% | 51% |
| Holy Shock | 0.3 | 1% | 1% |
| Divine Favor | 0.5 | 2% | – |
| Restore Mana | 0.4 | 1% | – |
| Hopped Up | 0.4 | 1% | – |
| Regeneration | – | – | 1% |
| Divine Shield | 0.3 | 1% | – |
| Blessing of Might | 0.2 | 1% | – |
| Hand of Salvation | 0.1 | 0% | – |
| Consecration | 0.1 | 0% | – |
| Fire Resistance Aura | 0.1 | 0% | – |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 5 | 619 | 69% | Flash of Light 16.8, Holy Light 7.3, Divine Favor 0.5 |

**Short buff / proc uptime:** Light's Grace 74%, Hopped Up 10%
**Self-buffs up at the pull** (% of 4 boss pulls): Righteous Fury 100%, Greater Blessing of Wisdom 100%, Elixir of Draenic Wisdom 100%, Healing Power 100%, Well Fed 75%
**Usual opener** (most common cast at each step over 5 pulls): Flash of Light → Flash of Light → Flash of Light → Flash of Light → Flash of Light → Holy Light → Flash of Light → Flash of Light

#### Trash (1 player, 16 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Holy Light | 11.5 | 42% | 70% |
| Flash of Light | 13.1 | 48% | 26% |
| Holy Shock | 0.7 | 2% | 4% |
| Cleanse | 0.6 | 2% | – |
| Hopped Up | 0.6 | 2% | – |
| Divine Favor | 0.4 | 1% | – |
| Restore Mana | 0.2 | 1% | – |
| Blessing of Wisdom | 0.2 | 1% | – |
| Divine Shield | 0.1 | 0% | – |
| Blessing of Might | 0.1 | 0% | – |
| Greater Blessing of Wisdom | 0.1 | 0% | – |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 22 | 630 | 76% | Flash of Light 13.1, Holy Light 11.5, Holy Shock 0.7 |

**Short buff / proc uptime:** Light's Grace 86%, Hopped Up 19%
**Compared with bosses** (casts/min): more Holy Light +4.2, Cleanse +0.6, Holy Shock +0.4; less Flash of Light -3.7

## Paladin — Justicar

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Consecration | 3.5 | 22% | 41% |
| Seal of Righteousness | 4.8 | 29% | 16% |
| Judgment | 3.3 | 20% | – |
| Melee | – | – | 19% |
| Holy Shield | 1.4 | 9% | 5% |
| Judgement of Righteousness | – | – | 7% |
| Seal of Truth | 1.0 | 6% | 0% |
| Censure | – | – | 5% |
| Judgment of Truth | – | – | 5% |
| Seal of Wisdom | 0.7 | 4% | – |
| Righteous Defense | 0.5 | 3% | – |
| Blessing of the Silver Crescent | 0.2 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 324 | 32% | Seal of Righteousness 4.8, Consecration 3.5, Judgment 3.3 |

**Short buff / proc uptime:** Seal of Righteousness 59%, Holy Shield 23%, Redoubt 10%
**Self-buffs up at the pull** (% of 4 boss pulls): Righteous Fury 100%, Sanctity Aura 100%, Gift of Arthas 100%, Greater Arcane Elixir 100%, Well Fed 75%
**Debuff uptime on the boss:** Judgement of Wisdom 40%, Censure 23%, Consecration 21%
**Usual opener** (most common cast at each step over 5 pulls): Judgment → Seal of Righteousness → Seal of Righteousness → Seal of Righteousness → Seal of Righteousness → Blessing of the Silver Crescent → Judgment → Seal of Righteousness

#### Trash (1 player, 17 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Consecration | 3.8 | 18% | 41% |
| Seal of Righteousness | 7.0 | 34% | 18% |
| Judgment | 4.8 | 24% | – |
| Judgement of Righteousness | – | – | 19% |
| Melee | – | – | 17% |
| Holy Shield | 2.5 | 12% | 3% |
| Righteous Defense | 1.1 | 5% | – |
| Exorcism | 0.3 | 2% | 1% |
| Hammer of Justice | 0.3 | 2% | – |
| Avenging Wrath | 0.2 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 384 | 40% | Seal of Righteousness 7.0, Judgment 4.8, Consecration 3.8 |

**Short buff / proc uptime:** Seal of Righteousness 74%, Holy Shield 40%
**Compared with bosses** (casts/min): more Seal of Righteousness +2.2, Judgment +1.6, Holy Shield +1.1; less Seal of Truth -1.0, Seal of Wisdom -0.6

## Paladin — Retribution

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Melee | – | – | 48% |
| Seal of the Martyr | 5.3 | 20% | 19% |
| Crusader Strike | 5.6 | 21% | 17% |
| Seals of Command | 3.5 | 13% | 11% |
| Seal of Command | 6.2 | 23% | – |
| Judgment | 3.5 | 13% | – |
| Seal of the Crusader | 1.1 | 4% | – |
| Judgement of the Martyr | – | – | 3% |
| Dire Drunkard | 0.4 | 1% | – |
| Consecration | 0.2 | 1% | 1% |
| Avenging Wrath | 0.3 | 1% | – |
| Abacus of Violent Odds | 0.3 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1109 | 52% | Seal of Command 6.2, Crusader Strike 5.6, Seal of the Martyr 5.3 |

**Short buff / proc uptime:** Vengeance 84%, Seal of Command 45%, Seal of the Martyr 35%, Lightning Speed 21%, Justice 19%, Speed Infusion 13%, Seal of the Crusader 12%
**Self-buffs up at the pull** (% of 4 boss pulls): Agility 100%, Flask of Relentless Assault 100%, Greater Blessing of Kings 100%, Sanctity Aura 100%, Strength 100%, Well Fed 100%
**Debuff uptime on the boss:** Judgement of the Crusader 69%
**Usual opener** (most common cast at each step over 5 pulls): Seal of the Crusader → Judgment → Crusader Strike → Seal of the Martyr → Avenging Wrath → Seal of Command → Seal of Command → Crusader Strike

#### Trash (1 player, 16 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Melee | – | – | 43% |
| Crusader Strike | 6.5 | 19% | 18% |
| Seal of the Martyr | 6.1 | 18% | 18% |
| Seals of Command | 4.6 | 14% | 15% |
| Seal of Command | 7.4 | 22% | – |
| Judgment | 4.7 | 14% | – |
| Seal of the Crusader | 2.5 | 8% | – |
| Consecration | 0.9 | 3% | 4% |
| Judgement of the Martyr | – | – | 3% |
| Hammer of Justice | 0.3 | 1% | – |
| Greater Blessing of Kings | 0.2 | 1% | – |
| Exorcism | 0.1 | 0% | 0% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 908 | 66% | Seal of Command 7.4, Crusader Strike 6.5, Seal of the Martyr 6.1 |

**Short buff / proc uptime:** Vengeance 88%, Seal of Command 52%, Seal of the Martyr 29%, Lightning Speed 24%, Justice 15%, Seal of the Crusader 14%
**Compared with bosses** (casts/min): more Seal of the Crusader +1.4, Seal of Command +1.2, Judgment +1.2

## Paladin — tank

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Consecration | 3.0 | 16% | 32% |
| Seal of Righteousness | 5.4 | 29% | 19% |
| Judgement of Righteousness | – | – | 25% |
| Judgment | 4.5 | 25% | – |
| Holy Shield | 2.7 | 14% | 5% |
| Melee | – | – | 12% |
| Avenger's Shield | 0.4 | 2% | 2% |
| Hammer of Wrath | 0.3 | 1% | 1% |
| Seal of Wisdom | 0.4 | 2% | – |
| Righteous Defense | 0.4 | 2% | – |
| Dark Iron Pipeweed | 0.3 | 2% | – |
| Seal of Light | 0.3 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 329 | 40% | Seal of Righteousness 5.4, Judgment 4.5, Consecration 3.0 |

**Short buff / proc uptime:** Seal of Righteousness 59%, Holy Shield 44%, Blessing of Righteousness 24%
**Self-buffs up at the pull** (% of 4 boss pulls): Blinding Light of Shattrath 100%, Righteous Fury 100%, Well Fed 100%, Blessing of Light 100%
**Debuff uptime on the boss:** Consecration 29%, Judgement of Light 22%, Judgement of Wisdom 13%
**Usual opener** (most common cast at each step over 5 pulls): Seal of Righteousness → Judgment → Holy Shield → Consecration → Seal of Righteousness → Consecration → Judgment → Seal of Righteousness

#### Trash (1 player, 15 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Consecration | 3.8 | 16% | 41% |
| Seal of Righteousness | 7.2 | 30% | 12% |
| Judgment | 6.0 | 25% | – |
| Holy Shield | 3.6 | 15% | 7% |
| Judgement of Righteousness | – | – | 18% |
| Melee | – | – | 8% |
| Avenger's Shield | 0.5 | 2% | 4% |
| Hammer of Wrath | 0.6 | 2% | 2% |
| Righteous Defense | 0.9 | 4% | – |
| Thorns | – | – | 3% |
| Retribution Aura | – | – | 3% |
| Exorcism | 0.4 | 2% | 1% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 623 | 54% | Seal of Righteousness 7.2, Judgment 6.0, Consecration 3.8 |

**Short buff / proc uptime:** Seal of Righteousness 67%, Holy Shield 54%, Blessing of Righteousness 35%, Redoubt 23%, Reckoning 15%
**Compared with bosses** (casts/min): more Seal of Righteousness +1.8, Judgment +1.5, Holy Shield +0.9

## Priest — Holy

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Circle of Healing | 6.7 | 31% | 43% |
| Flash Heal | 8.6 | 39% | 34% |
| Prayer of Mending | 2.1 | 10% | 15% |
| Renew | 1.8 | 8% | 7% |
| Power Word: Shield | 0.8 | 4% | – |
| Shoot | 0.3 | 1% | – |
| Desperate Prayer | 0.1 | 0% | 1% |
| Shadowfiend | 0.2 | 1% | – |
| Power Word: Fortitude | 0.2 | 1% | – |
| Fade | 0.2 | 1% | – |
| Binding Heal | 0.1 | 0% | 0% |
| Master Healthstone | 0.1 | 0% | 0% |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 5 | 912 | 53% | Flash Heal 8.6, Circle of Healing 6.7, Prayer of Mending 2.1 |

**Short buff / proc uptime:** Power Word: Shield 12%, Band of the Eternal Restorer 11%
**Self-buffs up at the pull** (% of 4 boss pulls): Healing Power 100%, Well Fed 100%
**Usual opener** (most common cast at each step over 5 pulls): Renew → Flash Heal → Flash Heal → Flash Heal → Flash Heal → Renew → Flash Heal → Prayer of Mending

#### Trash (1 player, 17 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Flash Heal | 10.7 | 43% | 41% |
| Circle of Healing | 7.6 | 31% | 37% |
| Prayer of Mending | 2.2 | 9% | 16% |
| Renew | 2.0 | 8% | 5% |
| Dispel Magic | 1.4 | 6% | – |
| Desperate Prayer | 0.1 | 0% | 1% |
| Power Word: Shield | 0.2 | 1% | – |
| Fade | 0.1 | 0% | – |
| Inner Fire | 0.1 | 0% | – |
| Mass Dispel | 0.1 | 0% | – |
| Mana Burn | 0.1 | 0% | – |
| Hopped Up | 0.1 | 0% | – |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 22 | 979 | 62% | Flash Heal 10.7, Circle of Healing 7.6, Prayer of Mending 2.2 |

**Short buff / proc uptime:** Band of the Eternal Restorer 14%
**Compared with bosses** (casts/min): more Flash Heal +2.1, Dispel Magic +1.3, Circle of Healing +0.8; less Power Word: Shield -0.6, Shoot -0.3

## Priest — Shadow

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Mind Flay | 7.9 | 33% | 24% |
| Mind Blast | 5.0 | 21% | 25% |
| Shadow Word: Pain | 2.5 | 11% | 22% |
| Vampiric Touch | 3.0 | 13% | 16% |
| Shadow Word: Death | 2.8 | 12% | 13% |
| Vampiric Embrace | 0.9 | 4% | – |
| Dark Iron Pipeweed | 0.5 | 2% | – |
| Chakra | 0.3 | 1% | – |
| Power Word: Shield | 0.2 | 1% | – |
| Blessing of the Silver Crescent | 0.2 | 1% | – |
| Shadowfiend | 0.1 | 0% | – |
| Restore Mana | 0.1 | 0% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 945 | 56% | Mind Flay 7.9, Mind Blast 5.0, Vampiric Touch 3.0 |
**Self-buffs up at the pull** (% of 4 boss pulls): Well Fed 75%, Major Shadow Power 75%
**Debuff uptime on the boss:** Misery 70%, Shadow Weaving 68%, Shadow Word: Pain 68%, Vampiric Embrace 66%, Vampiric Touch 57%, Mind Flay 27%
**Usual opener** (most common cast at each step over 5 pulls): Shadow Word: Pain → Vampiric Touch → Vampiric Embrace → Chakra → Dark Iron Pipeweed → Mind Blast → Shadow Word: Death → Mind Flay

#### Trash (1 player, 16 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Mind Flay | 7.0 | 26% | 21% |
| Mind Blast | 4.8 | 18% | 28% |
| Shadow Word: Pain | 5.4 | 20% | 23% |
| Vampiric Touch | 4.1 | 15% | 15% |
| Shadow Word: Death | 2.5 | 9% | 12% |
| Shoot | 0.6 | 2% | 0% |
| Chakra | 0.5 | 2% | – |
| Vampiric Embrace | 0.5 | 2% | – |
| Dark Iron Pipeweed | 0.4 | 2% | – |
| Power Word: Shield | 0.4 | 1% | – |
| Blessing of the Silver Crescent | 0.3 | 1% | – |
| Shadowform | 0.2 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 777 | 64% | Mind Flay 7.0, Shadow Word: Pain 5.4, Mind Blast 4.8 |
**Compared with bosses** (casts/min): more Shadow Word: Pain +2.9, Vampiric Touch +1.1, Shoot +0.6; less Mind Flay -0.8, Vampiric Embrace -0.4

## Rogue — melee

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Sinister Strike | 14.5 | 66% | 26% |
| Melee | – | – | 68% |
| Slice and Dice | 2.1 | 10% | – |
| Rupture | 1.2 | 5% | 2% |
| Expose Armor | 1.0 | 5% | – |
| Blade Flurry | 0.5 | 2% | 1% |
| Deadly Poison VII | – | – | 3% |
| Abacus of Violent Odds | 0.4 | 2% | – |
| Haste | 0.4 | 2% | – |
| Cloak of Shadows | 0.4 | 2% | – |
| Dire Drunkard | 0.4 | 2% | – |
| Adrenaline Rush | 0.3 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1068 | 45% | Sinister Strike 14.5, Slice and Dice 2.1, Rupture 1.2 |

**Short buff / proc uptime:** Slice and Dice 67%, Lightning Speed 52%, Band of the Eternal Champion 11%, Dire Drunkard 11%, Blade Flurry 11%
**Self-buffs up at the pull** (% of 4 boss pulls): Relentless Assault of Shattrath 100%, Well Fed 100%
**Debuff uptime on the boss:** Expose Armor 50%, Deadly Poison VII 36%, Rupture 21%, Magic Disruption 12%
**Usual opener** (most common cast at each step over 5 pulls): Sinister Strike → Sinister Strike → Slice and Dice → Adrenaline Rush → Blade Flurry → Abacus of Violent Odds → Sinister Strike → Sinister Strike

#### Trash (1 player, 13 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Sinister Strike | 16.6 | 63% | 23% |
| Melee | – | – | 59% |
| Blade Flurry | 0.8 | 3% | 14% |
| Slice and Dice | 3.9 | 15% | – |
| Rupture | 2.0 | 7% | 1% |
| Eviscerate | 0.8 | 3% | 1% |
| Abacus of Violent Odds | 0.5 | 2% | – |
| Dire Drunkard | 0.4 | 1% | – |
| Evasion | 0.3 | 1% | – |
| Garrote | 0.2 | 1% | 0% |
| Cloak of Shadows | 0.2 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 20 | 1140 | 57% | Sinister Strike 16.6, Slice and Dice 3.9, Rupture 2.0 |

**Short buff / proc uptime:** Slice and Dice 82%, Lightning Speed 50%, Blade Flurry 18%, Band of the Eternal Champion 12%, Dire Drunkard 10%
**Compared with bosses** (casts/min): more Sinister Strike +2.1, Slice and Dice +1.8, Rupture +0.8; less Expose Armor -1.0, Haste -0.3

## Shaman — Elemental

#### Bosses (2 players, 39 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Lightning Bolt | 17.7 | 73% | 86% |
| Chain Lightning | 2.3 | 10% | 13% |
| Wrath of Air Totem | 0.7 | 3% | – |
| Totem of Wrath | 0.7 | 3% | – |
| Mana Spring Totem | 0.7 | 3% | – |
| Earth Shock | 0.3 | 1% | 1% |
| Stoneskin Totem | 0.4 | 1% | – |
| Dark Iron Pipeweed | 0.3 | 1% | – |
| Master of the Elements | 0.3 | 1% | – |
| Water Shield | 0.2 | 1% | – |
| Tremor Totem | 0.2 | 1% | – |
| Flame Shock | 0.1 | 0% | 0% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1154 | 72% | Lightning Bolt 16.6, Chain Lightning 4.0, Stoneskin Totem 0.7 |
| 5 | 799 | 69% | Lightning Bolt 18.7, Totem of Wrath 0.7, Mana Spring Totem 0.7 |

**Short buff / proc uptime:** Totemic Mastery 88% (1 of 2), Electrical Charge 56%, Clearcasting 56%, Charged 37% (1 of 2), Band of the Eternal Sage 13% (1 of 2)
**Self-buffs up at the pull** (% of 8 boss pulls): Well Fed 88%, Elixir of Draenic Wisdom 50%, Spellpower Elixir 50%
**Usual opener** (most common cast at each step over 10 pulls): Lightning Bolt → Lightning Bolt → Lightning Bolt → Lightning Bolt → Lightning Bolt → Lightning Bolt → Lightning Bolt → Lightning Bolt

#### Trash (2 players, 34 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Lightning Bolt | 18.7 | 84% | 83% |
| Chain Lightning | 2.3 | 10% | 17% |
| Mana Spring Totem | 0.2 | 1% | – |
| Earth Shock | 0.1 | 1% | 0% |
| Totem of Wrath | 0.2 | 1% | – |
| Wrath of Air Totem | 0.2 | 1% | – |
| Master of the Elements | 0.1 | 0% | – |
| Stoneskin Totem | 0.1 | 0% | – |
| Tremor Totem | 0.1 | 0% | – |
| Master Healthstone | 0.1 | 0% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 1125 | 73% | Lightning Bolt 18.7, Chain Lightning 3.1, Mana Spring Totem 0.2 |
| 22 | 744 | 69% | Lightning Bolt 18.8, Chain Lightning 1.4, Mana Spring Totem 0.3 |

**Short buff / proc uptime:** Totemic Mastery 88% (1 of 2), Clearcasting 50%, Electrical Charge 50%, Charged 22% (1 of 2), Band of the Eternal Sage 14% (1 of 2)
**Compared with bosses** (casts/min): more Lightning Bolt +1.1; less Wrath of Air Totem -0.5, Totem of Wrath -0.5, Mana Spring Totem -0.5

## Shaman — Enhancement

#### Bosses (2 players, 33 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Melee | – | – | 44% |
| Stormstrike | 8.8 | 28% | 6% |
| Earth Shock | 6.2 | 20% | 10% |
| Windfury Attack | – | – | 27% |
| Stormstrike Off-Hand | 4.3 | 14% | 3% |
| Windfury Totem | 2.1 | 7% | – |
| Flame Shock | 1.2 | 4% | 3% |
| Strength of Earth Totem | 1.4 | 5% | – |
| Mana Spring Totem | 1.4 | 5% | – |
| Grace of Air Totem | 1.2 | 4% | – |
| Water Shield | 0.8 | 3% | – |
| Magma Totem | 0.8 | 3% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1219 | 59% | Stormstrike 10.3, Earth Shock 7.5, Stormstrike Off-Hand 5.0 |
| 5 | 1000 | 45% | Stormstrike 7.4, Earth Shock 4.9, Stormstrike Off-Hand 3.6 |

**Short buff / proc uptime:** Water Shield 84% (1 of 2), Flurry 80%, Unleashed Rage 80%, Focused 61%, Lightning Speed 45%, Holy Strength 31% (1 of 2), Siphon Essence 20% (1 of 2), Dire Drunkard 18% (1 of 2)
**Self-buffs up at the pull** (% of 8 boss pulls): Well Fed 50%, Flask of Relentless Assault 50%, Mighty Agility 38%
**Debuff uptime on the boss:** Flame Shock 13%, Stormstrike 10%
**Usual opener** (most common cast at each step over 10 pulls): Flame Shock → Stormstrike → Stormstrike Off-Hand → Stormstrike → Heroism → Stormstrike → Stormstrike → Earth Shock

#### Trash (2 players, 30 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Melee | – | – | 39% |
| Stormstrike | 10.2 | 29% | 7% |
| Earth Shock | 6.4 | 18% | 12% |
| Windfury Attack | – | – | 26% |
| Stormstrike Off-Hand | 4.9 | 14% | 3% |
| Flame Shock | 1.8 | 5% | 4% |
| Windfury Totem | 2.1 | 6% | – |
| Strength of Earth Totem | 2.0 | 6% | – |
| (pet) Fire Nova | – | – | 5% |
| Mana Spring Totem | 1.6 | 5% | – |
| Magma Totem | 1.1 | 3% | – |
| (pet) Magma Totem | – | – | 3% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 1117 | 62% | Stormstrike 10.1, Earth Shock 5.7, Stormstrike Off-Hand 4.8 |
| 22 | 937 | 52% | Stormstrike 10.3, Earth Shock 7.0, Stormstrike Off-Hand 5.0 |

**Short buff / proc uptime:** Unleashed Rage 85%, Flurry 83%, Water Shield 75% (1 of 2), Focused 60%, Lightning Speed 45%, Holy Strength 31% (1 of 2), Dire Drunkard 23% (1 of 2), Rage of the Unraveller 16% (1 of 2)
**Compared with bosses** (casts/min): more Stormstrike +1.4, Fire Nova +0.7, Stormstrike Off-Hand +0.6; less Grace of Air Totem -0.6, Totemic Recall -0.3

## Shaman — Restoration

#### Bosses (1 player, 20 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Chain Heal | 12.3 | 66% | 83% |
| Earth Shield | 1.1 | 6% | 11% |
| Lesser Healing Wave | 1.4 | 7% | 5% |
| Tremor Totem | 0.7 | 4% | – |
| Wrath of Air Totem | 0.7 | 4% | – |
| Mana Spring Totem | 0.6 | 3% | – |
| Healing Wave | 0.3 | 2% | 1% |
| Water Shield | 0.5 | 2% | – |
| Restore Mana | 0.3 | 1% | – |
| Drums of Battle | 0.2 | 1% | – |
| Mana Tide Totem | 0.2 | 1% | – |
| Hopped Up | 0.2 | 1% | – |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 5 | 635 | 62% | Chain Heal 12.3, Lesser Healing Wave 1.4, Earth Shield 1.1 |

**Short buff / proc uptime:** Water Shield 85%
**Self-buffs up at the pull** (% of 4 boss pulls): Well Fed 100%, Healing Power 100%, Elixir of Draenic Wisdom 100%
**Usual opener** (most common cast at each step over 5 pulls): Chain Heal → Chain Heal → Chain Heal → Chain Heal → Chain Heal → Chain Heal → Chain Heal → Chain Heal

#### Trash (1 player, 16 player-minutes)

| Ability | Casts/min | % of casts | % of healing |
|---|---|---|---|
| Chain Heal | 16.1 | 76% | 88% |
| Earth Shield | 1.2 | 6% | 12% |
| Tremor Totem | 0.9 | 4% | – |
| Wrath of Air Totem | 0.8 | 4% | – |
| Mana Spring Totem | 0.8 | 4% | – |
| Water Shield | 0.2 | 1% | – |
| Essence of the Martyr | 0.2 | 1% | – |
| Ancestral Swiftness | 0.2 | 1% | – |
| Hopped Up | 0.2 | 1% | – |
| Grounding Totem | 0.1 | 1% | – |
| Totemic Recall | 0.1 | 1% | – |
| Chain Lightning | 0.1 | 0% | – |

| Pulls | HPS | Active | Most cast |
|---|---|---|---|
| 22 | 902 | 76% | Chain Heal 16.1, Earth Shield 1.2, Tremor Totem 0.9 |

**Short buff / proc uptime:** Water Shield 70%
**Compared with bosses** (casts/min): more Chain Heal +3.8; less Lesser Healing Wave -1.4, Healing Wave -0.3

## Warlock — Destruction

#### Bosses (2 players, 38 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Shadow Bolt | 15.1 | 67% | 83% |
| Seed of Corruption | 0.8 | 4% | 10% |
| Life Tap | 2.6 | 11% | – |
| Searing Pain | 1.3 | 6% | 2% |
| Curse of Doom | 0.3 | 1% | 3% |
| Curse of Agony | 0.4 | 2% | 2% |
| Mental Protection Field | 0.7 | 3% | – |
| Dark Iron Pipeweed | 0.4 | 2% | – |
| Curse of Recklessness | 0.3 | 1% | – |
| Spell Power | 0.2 | 1% | – |
| Destruction | 0.2 | 1% | – |
| Shadowburn | 0.1 | 0% | 0% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1546 | 74% | Shadow Bolt 15.6, Life Tap 2.5, Mental Protection Field 1.4 |
| 5 | 1334 | 76% | Shadow Bolt 14.7, Life Tap 2.6, Searing Pain 2.5 |

**Short buff / proc uptime:** Mental Protection Field 19% (1 of 2), Flameshadow 18%, Dark Iron Pipeweed 16% (1 of 2), Band of the Eternal Sage 11% (1 of 2)
**Self-buffs up at the pull** (% of 8 boss pulls): Well Fed 100%, Major Shadow Power 100%, Elixir of Major Fortitude 50%
**Debuff uptime on the boss:** Curse of Recklessness 69% (1 of 2), Curse of Doom 61% (1 of 2), Shadow and Flame 18%, Curse of Agony 6% (1 of 2)
**Usual opener** (most common cast at each step over 10 pulls): Shadow Bolt → Dark Iron Pipeweed → Shadow Bolt → Shadow Bolt → Shadow Bolt → Shadow Bolt → Shadow Bolt → Shadow Bolt

#### Trash (2 players, 31 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Shadow Bolt | 14.9 | 75% | 82% |
| Seed of Corruption | 2.1 | 11% | 16% |
| Drain Soul | 1.1 | 5% | 0% |
| Life Tap | 0.7 | 3% | – |
| Curse of Agony | 0.3 | 2% | 2% |
| Dark Iron Pipeweed | 0.3 | 1% | – |
| Curse of Recklessness | 0.2 | 1% | – |
| Banish | 0.1 | 0% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 20 | 1223 | 73% | Shadow Bolt 14.1, Seed of Corruption 2.6, Drain Soul 1.3 |
| 22 | 1158 | 75% | Shadow Bolt 15.6, Seed of Corruption 1.7, Drain Soul 0.9 |

**Short buff / proc uptime:** Band of the Eternal Sage 16% (1 of 2), Dark Iron Pipeweed 14% (1 of 2), Flameshadow 14%, Fungal Frenzy 10% (1 of 2)
**Compared with bosses** (casts/min): more Seed of Corruption +1.3, Drain Soul +1.0; less Life Tap -1.9, Searing Pain -1.3, Mental Protection Field -0.7

## Warlock — ranged

#### Bosses (1 player, 19 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Shadow Bolt | 11.9 | 53% | 65% |
| Corruption | 2.8 | 12% | 15% |
| Immolate | 1.7 | 7% | 6% |
| Seed of Corruption | 0.7 | 3% | 8% |
| Siphon Life | 1.2 | 6% | 5% |
| Dark Pact | 1.7 | 8% | – |
| Curse of the Elements | 0.7 | 3% | – |
| Shoot | 0.5 | 2% | 0% |
| Life Tap | 0.4 | 2% | – |
| Blessing of the Silver Crescent | 0.3 | 1% | – |
| Mental Protection Field | 0.2 | 1% | – |
| Shadowburn | 0.1 | 0% | 0% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1075 | 70% | Shadow Bolt 11.9, Corruption 2.8, Dark Pact 1.7 |
**Self-buffs up at the pull** (% of 4 boss pulls): Pure Death of Shattrath 100%, Well Fed 100%
**Debuff uptime on the boss:** Curse of the Elements 82%, Shadow Embrace 66%, Corruption 64%, Siphon Life 51%, Immolate 30%, Shadow and Flame 11%
**Usual opener** (most common cast at each step over 5 pulls): Curse of the Elements → Corruption → Corruption → Siphon Life → Shadow Bolt → Shadow Bolt → Shadow Bolt → Shadow Bolt

#### Trash (1 player, 17 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Shadow Bolt | 10.7 | 44% | 57% |
| Corruption | 3.6 | 15% | 17% |
| Seed of Corruption | 0.9 | 4% | 14% |
| Curse of the Elements | 3.1 | 13% | – |
| Immolate | 1.2 | 5% | 5% |
| Shadowburn | 0.9 | 4% | 4% |
| Drain Life | 1.0 | 4% | 2% |
| Dark Pact | 1.0 | 4% | – |
| Siphon Life | 0.5 | 2% | 1% |
| Drain Soul | 0.5 | 2% | 0% |
| Death Coil | 0.2 | 1% | 0% |
| Life Tap | 0.2 | 1% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 861 | 77% | Shadow Bolt 10.7, Corruption 3.6, Curse of the Elements 3.1 |

**Short buff / proc uptime:** Fungal Frenzy 12%
**Compared with bosses** (casts/min): more Curse of the Elements +2.4, Drain Life +0.9, Corruption +0.8; less Shadow Bolt -1.2, Siphon Life -0.8, Dark Pact -0.7

## Warrior — Fury

#### Bosses (2 players, 38 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Heroic Strike | 9.6 | 39% | 23% |
| Melee | – | – | 35% |
| Bloodthirst | 4.8 | 19% | 16% |
| Whirlwind | 3.4 | 14% | 7% |
| Execute | – | – | 8% |
| Cleave | 1.0 | 4% | 3% |
| Sunder Armor | 1.4 | 6% | – |
| Whirlwind Off-Hand | – | – | 4% |
| Bloodrage | 0.8 | 3% | – |
| Deep Wounds | – | – | 3% |
| Berserker Rage | 0.8 | 3% | – |
| Battle Shout | 0.5 | 2% | – |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 5 | 1138 | 52% | Heroic Strike 10.8, Bloodthirst 5.2, Whirlwind 4.0 |
| 5 | 957 | 43% | Heroic Strike 8.5, Bloodthirst 4.4, Whirlwind 2.8 |

**Short buff / proc uptime:** Flurry 63%, Lightning Speed 59%, Bloodthirst 27%, Dragonspine Flurry 24% (1 of 2), Berserker Rage 21% (1 of 2), Dire Drunkard 16%, Speed Infusion 14% (1 of 2), Bloodrage 13%
**Self-buffs up at the pull** (% of 8 boss pulls): Berserker Stance 100%, Well Fed 100%, Battle Shout 62%, Relentless Assault of Shattrath 50%, Flask of Relentless Assault 50%
**Debuff uptime on the boss:** Deep Wounds 61%, Demoralizing Shout 12% (1 of 2), Sunder Armor 7%
**Usual opener** (most common cast at each step over 10 pulls): Sunder Armor → Sunder Armor → Sunder Armor → Sunder Armor → Dire Drunkard → Sunder Armor → Bloodthirst → Heroic Strike

#### Trash (2 players, 32 player-minutes)

| Ability | Casts/min | % of casts | % of damage |
|---|---|---|---|
| Bloodthirst | 6.2 | 23% | 13% |
| Melee | – | – | 34% |
| Heroic Strike | 6.5 | 24% | 10% |
| Whirlwind | 4.8 | 17% | 9% |
| Cleave | 3.9 | 14% | 10% |
| Sweeping Strikes | 1.1 | 4% | 9% |
| Whirlwind Off-Hand | – | – | 6% |
| Execute | – | – | 6% |
| Dire Drunkard | 1.0 | 4% | – |
| Bloodrage | 0.9 | 3% | – |
| Battle Shout | 0.7 | 3% | – |
| Deep Wounds | – | – | 3% |

| Pulls | DPS | Active | Most cast |
|---|---|---|---|
| 22 | 1190 | 51% | Bloodthirst 5.8, Heroic Strike 5.8, Whirlwind 5.1 |
| 22 | 1138 | 58% | Heroic Strike 7.2, Bloodthirst 6.6, Whirlwind 4.4 |

**Short buff / proc uptime:** Flurry 77%, Lightning Speed 55%, Bloodthirst 34%, Berserker Rage 31% (1 of 2), Dire Drunkard 27%, Dragonspine Flurry 19% (1 of 2), Bloodrage 19%, Band of the Eternal Champion 16% (1 of 2)
**Compared with bosses** (casts/min): more Cleave +2.9, Bloodthirst +1.4, Whirlwind +1.4; less Heroic Strike -3.1, Sunder Armor -0.7, Hamstring -0.4
