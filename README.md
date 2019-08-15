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
- [ ] Minimum weapon rank for enemy or bosses
- [ ] Chance to add a dropable item

- [x] Support Randomization

- [x] Randomize Weapons (Note: It may be done, but I want to add more options to it)
- [x] Break Weapons Locks
- [x] Astral Shard Randomization

- [ ] Add the options to the GUI
- [ ] Complete the goddamn readme

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

Every character growth will be randomized with a range. For example, if the range is set to 30, each stat will be increased by a random number from -30 to 30, so if it rolls a 15 and your stat is 20: 20 + 15 = 35%.

The range can be changed, for default it is 30.