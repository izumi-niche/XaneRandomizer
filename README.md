# Xane Randomizer
Xane Randomizer is a randomizer for the game Fire Emblem: Mystery of the Emblem for the SNES, also know as FE3.

For more information how to use it and other stuff, read more below.

## Checklist
All things need to be done to version v1.0
- [x] Randomize Playable Units
- [x] Randomize Playable Bases
- [x] Randomize Playable Growths

- [x] Randomize enemy units
- [x] Randomize boss units
- [x] Increase enemy level
- [x] Increase boss level
- [x] Increase bases and growths
- [x] Chance to add a dropable item

- [x] Support Randomization

- [x] Randomize Weapons (Note: It may be done, but I want to add more options to it)
- [x] Break Weapons Locks
- [x] Astral Shard Randomization
- [x] 0% growths
- [x] Shop randomization

- [x] Add the options to the GUI
- [x] Complete the goddamn readme

## Code
This is my first project, which as expected, the code is a bit messy more than I care to admit. I may rewrite
this thing in the extremely long future, but for now the main structure will stay like that. Well if you are not here for the source code, continue reading since everything after this is actual information!

## What ROM to use? And what translation patch?
When using the randomizer, you will need to choose a ROM. In fact, it can be (almost) any ROM!

IMPORTANT: You need a headered version of the ROM!

If you can't find a headered version anywhere, you can simply just download a software like [TUSH](https://www.romhacking.net/utilities/608/) and add a header easily.

This is compatible with a totally clean japanese FE3 ROM, both version 1.0 and 1.1. Also, it works with translations patches. 

The randomizer will use whatever ROM you choose, so to use a translated ROM you need to have one first. Same thing if you want to play with a clean ROM in japanese.

Compatible translations patches:

[Updated translation patch v1.3 by Quirino](https://forums.serenesforest.net/index.php?/topic/49096-updated-mystery-of-the-emblem-fan-translation-version-014-released/)

[Bugfix update by Robert of Normandy (recommended)](https://forums.serenesforest.net/index.php?/topic/88484-fe3-translation-patch-bugfix-update/)

![thiefmarth](/images/thiefmarth.png)

*Marth randomized into a thief in a clean 1.0 ROM*

![gazzak](/images/gazzak.png)

*Gazzak randomized into a Knight with increased levels in a 1.1 ROM with Robert of Normandy's bugfix patch*

![pegasus](/images/pegasus.png)

*Generic enemy randomized into a pegasus in a 1.1 ROM with Quirino's patch*

## Options
## Important!

Since FE3 is not that popular (well, almost nobody played it) in the english community, understanding how FE3 works is a bit... scarce. Not to mention that it has it's fair share of woke coding, so the randomizer will do some stuff to prevent the game from exploding.

Book 1 Tiki, the manakete bosses (Xemcel, Khorzas and Morzas) will always transform in a cutscene at the start of the map even if they are not a manakete. Good news is that they can change classes, but they NEED a dragonstone on the first weapon slot or the game softlocks. If you give the dragonstone and change their class, the transforming animation will be a bit weird, but it doesn't softlock! Tiki will transform to a divine dragon even if she is not a manakete, but when Bantu recruits her she will go back to the class she has randomized in (and with a free dragonstone from her inventory)! Sadly for the bosses they will transform into a dragon and will only show up with their randomized class in battle prepations.

If you choose the option to remove the lock from the Rapier, every sword class can use it. But your in-battle animation will be just be Marth standing still and mentally damaging the enemy. Well, the rapier still works but the animation will be weird. The map animation will still work without problems.

In vanilla FE3, the dancer class can use the Falchion, but Feena is hardcoded to not able to use it. So every dancer and lord can use the Rapier/Falchion, with the exception mentioned above.

From the start of this randomizer i'm trying to get a way to enemy-only classes (Emperor, Ice Dragon etc) to work in all maps. Sadly, it is still not possible :( . All enemies and playable characters will randomized into classes that works in all maps (all playable classes, and Soldier). Sorry to say this, but Wyvern Gordin is still a dream.

Even thought the name is *Xane* Randomizer, Xane cannot be randomized and the freelancer class doesn't work properly on other people! The transforming mechanic can be used with the freelancer class, but to turn back to normal is hard-coded to be locked to Xane. So pretty much if anyone is a freelancer and transform, they will be stuck forever as that character, even completing the chapter does not reset that. Also, due to the hard-coded thing, Xane will "untransform" even when he is not a freelancer at the end of the chapter, bringing him to 0 stats in everything and changing his class to Lord.

Ballistician are ignored since their AI causes to them in every class use their weapon as a siege weapon, and some animations cause a softlock.
### Playable characters
#### Randomize classes

Randomize classes of playable characters. Promoted characters will be only randomized into promoted classes, and same for unpromoted characters into unpromoted classes.

Manaketes are considered promoted, Dancer, Lord, Thief and Fighter are considered unpromoted.

##### Ignore Julian/Rickard

When randomizing classes, Julian and Rickard will be ignored and their classes will not be randomized. They will still be affected by others options like bases randomization if enabled.

Recommended and enabled by default since it is possible to just lose the True Ending if the game decides to not throw characters with the thief class at you early on.

#### Randomize bases

Every character base will be randomized with a range. For example, if the range is set to 3, each stat will be increased by a random number from -3 to 3, so if it rolls a -2 and your stat is 5: 5 + -2 = 3.

The range can be changed, for default it is 3.

#### Randomize growths

Two options for randomizing growths:

##### Full Mode

Every single growth will be picked randomly between 5 and 100. Totally random.

##### Range Mode

Every character growth will be randomized with a range. For example, if the range is set to 30, each growth will be increased by a random number from -30 to 30, so if it rolls a 15 and your growth is 20: 20 + 15 = 35%.

The range can be changed, for default it is 30.

### Global Enemy Options

As the name says, this option will effect ALL enemies, bosses or generic.

#### Increase enemy bases

Increase enemy bases by a X ammount. Default is 3.

#### Increae enemy growths

Increase enemy growths by a X ammount. Default is 15.

### Generic/Boss options

Applies for both the Generic Options and Boss Options, since they do the same thing but for different enemies. Except for one what is generic-only.

#### Randomize classes

Randomize classes for generic/boss units.

#### Increase level

Level will be increased by X for generic/boss units. Increasing the level will also increase their stats.

#### Randomize Items

Generic/bosses will have a random chance of getting a droppable item.

Default is 20%, even though it seems low, it is rolled for every generic/boss.

#### Ignore thiefs with sphere/orbs

Thiefs that carry a sphere or orb will not have their classes randomized. Good for preventing getting into a situation that the player can't catch them.

Recommended.

### Support Options

Randomize supports between playable characters.

Options are pretty much self-explanatory.

Minimum characters supported by one character: Default is 0;

Maximum characters supported by one character: Default is 3;

Minimum bonus: Default is 5;

Maximum bonus: Default is 20.

### Other options

#### Randomize Astral Shard bonuses

Randomize the growths that the Astral Shards gives when in inventory.

NOTE: Does not affect the Starsphare/Star Orb.

#### Full Mode

The growths are totally random and each growth is a random number varrying from -100 and 100. Pretty much garanted to make things totally busted or totally crap.

#### 'Balanced' Mode

The growths will be randomized trying to be more 'balanced'. Not guarranted to be a totally balanced experience, since there is still a bit of 'random' on it.

#### Break weapon locks

Excalibur, Aura, Rescue, Thief, Aum (both books) will be usable by anyone. Also, they will be added to the pool of items used by enemies.

If the randomized weapons option is enabled, this is not necessary. See below.

#### Break Rapier lock

Rapier will become usable by anyone and will be added to the pool used by enemies. This is a separate option from the above one since the Rapier can cause some funky animations, but it is still 100% usable without the game crashing.

If the randomized weapons option is enabled, this is not necessary. See below.

#### Randomized weapons

Weapon stats will be randomized, with the exception of Weapon Level.

Since the weapon locks are tied to the weapon uses and this will also be randomized, all weapon locks will be broken automatically.

#### 0% growths

All characters will be set to have 0% growths in everything, including weapon level.

If the randomize growths option is enabled, this option will overwrite it.

#### Randomize shops

Shops will be randomized to have random contents.

## Log 

You can choose to create a log that will tell what changed in your ROM.

It contains, if that options is enabled in the randomization:

Playable characters stats, items and class;

Supports;

Astral Shard bonuses.