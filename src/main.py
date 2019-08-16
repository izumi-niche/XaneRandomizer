import os
import random
import shutil

from data.chapters import *
from data.portraits import *
from data.characterdata import *
from data.classes import *
from data.items import *

from lists.classpool import *
from lists.enemies import *
from lists.itempool import *
from lists.playable import *
from lists.weaponpool import *
from lists.replacedata import *

from basicfunctions import *
from logfunctions import *

from tkinter import *
from tkinter import filedialog


fe3rom = ''
changelog ='' 

def ReadHex(location):
	fe3rom.seek(location)
	HexRead = fe3rom.read(1)
	return ByteToInt(HexRead)
##############################################
############## Playable options ##############
##############################################
# Randomize bases for playable characters.
# Range mode = Bases will be increased or decreased between a range (3 being the default)
# Hightest mode = Every stat will be randomized between 0 and the hightest base stat excluding HP.
# (Example) Marth hightest non-HP base is 7 in luck, so every stat will be between 0 and 7.
def RandomizePlayableBases(statrange):
	print('Randomzing playable bases...')
	FirstDec = 267265
	
	# Get the unit data for playable characters
	PlayableData = []


	for unit in PlayableData:
		UnitLocation = UnitDataCalc(unit)
		for stat in range(7):
			NewStat = random.randint(statrange * -1, statrange)
			fe3rom.seek(FirstDec + stat + UnitLocation)
			OldStat = fe3rom.read(1)
			OldStat = ByteToInt(OldStat)
			NewStat = NewStat + OldStat
			if NewStat < 0:
				NewStat = 0
			NewStat = bytes([NewStat])
			fe3rom.seek(FirstDec + stat + UnitLocation)
			fe3rom.write(NewStat)
	print('Done!')

# The growths be randomized in two ways:
# Range: The growths be increased or decreased between 30 (default number, can be changed)
# Full: The growths be randomly chosen between 5 and 100.
def RandomizePlayableGrowths(mode, statrange):
	print('Randomizing playable growths...')
	FirstDec = 267265
	# Range mode
	if mode == 1:
		for unit in PlayableUnits:
			y = CharacterDataList[unit]
			y = UnitDataCalc(y)
			for x in range(8):
				fe3rom.seek(FirstDec + y + 9 + x)
				growth = fe3rom.read(1)
				growth = ByteToInt(growth)
				growth = growth + random.randint(statrange * -1, statrange)
				if growth < 5:
					growth = 5
				elif growth > 100:
					growth = 100
				growth = bytes([growth])
				fe3rom.seek(FirstDec + y + 9 + x)
				fe3rom.write(growth)
	# Full mode
	if mode == 0:
		for unit in PlayableUnits:
			y = CharacterDataList[unit]
			y = UnitDataCalc(y)
			for x in range(8):
				growth = random.randint(1, 20)
				growth = growth * 5
				growth = bytes([growth])
				fe3rom.seek(FirstDec + y + 9 + x)
				fe3rom.write(growth)
	print('Done!')

# Randomizing playable units.
# Will look for the character data to determine if it is a playable unit.
def RandomizePlayableUnits(thief):
	CharacterList = GetCharacter(PlayableUnits)
	if thief == 1:
		for x in ['Julian', 'Julian2', 'Rickard', 'Rickard2', 'RickardE']:
			CharacterList.remove(CharacterDataList[x])
	for x in ['Xane', 'Xane2', 'Marth2']:
		CharacterList.remove(CharacterDataList[x])
	UnitList = SearchForUnits()
	UnitWrite = [] 
	for unit in UnitList:
		if UnitList[unit]['character'] in CharacterList:
			UnitWrite.append(unit)
	# Marth only class randomization
	Marth = 264766
	RandomClassMarth(Marth)
	GiveWeapons(Marth, 'player')
	# Write
	for unit in UnitWrite:
		RandomizePlayableClasses(unit)
		GiveWeapons(unit,'player')

def CopyUnitItems(unit):
	Thingy = {}
	for x in [1, 8, 9, 10, 11, 12, 13]:
		fe3rom.seek(unit + x)
		HexRead = fe3rom.read(1)
		Thingy[x] = HexRead
	return Thingy

def PlayableCopyUnits():
	UnitList = SearchForUnits()
	PlayableCharacters = GetCharacter(PlayableUnits)
	DataCollected = {}
	SpecialCopy = {}
	for unit in ReplaceData:
		SpecialCopy[CharacterDataList[ReplaceData[unit][1]]] = CharacterDataList[ReplaceData[unit][2]]
		SpecialCopy[CharacterDataList[ReplaceData[unit][2]]] = CharacterDataList[ReplaceData[unit][1]]
	for unit in UnitList:
		y = UnitList[unit]['character']
		if y in DataCollected:
			for x in DataCollected[y]:
				fe3rom.seek(unit + x)
				fe3rom.write(DataCollected[y][x])
		elif y in SpecialCopy:
			UnitData = CopyUnitItems(unit)
			DataCollected[y] = UnitData
			DataCollected[SpecialCopy[y]] = UnitData
		elif y in PlayableCharacters:
			UnitData = CopyUnitItems(unit)
			DataCollected[y] = UnitData

def PlayableCopyBases():
	for unit in ReplaceData:
		for x in range(8):
			fe3rom.seek(CharacterDec + UnitDataCalc(CharacterDataList[ReplaceData[unit][1]]) + x)
			HexRead = fe3rom.read(1)
			fe3rom.seek(CharacterDec + UnitDataCalc(CharacterDataList[ReplaceData[unit][1]]) + x)
			fe3rom.write(HexRead)

# Give a dragonstone to prevent Book 1 Tiki from softlocking the game
def FixManakete(manakete):
	ManaketeList = []
	ManaketePortrait = []
	NewDragonStone = '???'
	if manakete == 'player':
		ManaketeList.append(CharacterDataList['Tiki'])
		NewDragonStone = bytes([items['Divinestone']])
	else:
		for x in ['Xemcel', 'Khozel', 'Morzas']:
			ManaketePortrait.append(PortraitList[x])
		NewDragonStone = bytes([items['FireStone']])
	UnitList = SearchForUnits()
	for unit in UnitList:
		if UnitList[unit]['character'] in ManaketeList or UnitList[unit]['portrait'] in ManaketePortrait:
			ItemList = []
			ReplaceItem = []
			for x in range(4):
				NumberSeek = unit + 8 + x
				fe3rom.seek(NumberSeek)
				ItemList.append(fe3rom.read(1))
			ReplaceItem.append(NewDragonStone)
			for x in range(4):
				if not ByteToInt(ItemList[x]) == 255:
					ReplaceItem.append(ItemList[x])
			x = 0
			for y in ReplaceItem:
				fe3rom.seek(unit + 8 + x)
				fe3rom.write(y)
				x += 1

###########################################
############## Enemy Options ##############
###########################################
# Randomizing enemy units.
# Will look for portraits to determine if it is a enemy unit.
def RandomizeEnemyUnits(thief):
	EnemyList = GetPortraits(GenericPortraits)
	UnitList = SearchForUnits()
	UnitWrite = []
	for unit in UnitList:
		if UnitList[unit]['portrait'] in EnemyList:
			if not UnitList[unit]['class'] == 35:
				if thief == 0:
					UnitWrite.append(unit)
				if thief == 1:
					if not UnitList[unit]['item1'] in GetItems(ImportantItems):
						UnitWrite.append(unit)
	# Write
	for unit in UnitWrite:
		RandomizeEnemyClasses(unit)
		GiveWeapons(unit, 'enemy')

# Randomizing boss units.
# Will look for portraits to determine if it is a boss unit.
def RandomizeBossUnits():
	BossList = GetPortraits(BossPortraits)
	UnitList = SearchForUnits()
	UnitWrite = []
	for unit in UnitList:
		if UnitList[unit]['portrait'] in BossList:
			if not UnitList[unit]['class'] == 35:
				UnitWrite.append(unit)
	# Write
	for unit in UnitWrite:
		RandomizeEnemyClasses(unit)
		GiveWeapons(unit, 'enemy')

	for unit in BossBook2:
		RandomizeEnemyClasses(unit)
		GiveWeapons(unit, 'enemy')

# Boost enemy growths/bases
# Will look for the character data through the enemy/boss units
def IncreaseEnemyStats(base, growth, increasebase, increasegrowth):
	# For bases
	if base == 1:
		UnitList = SearchForUnits()
		EnemyList = GetPortraits(BossPortraits)
		EnemyList += GetPortraits(GenericPortraits)
		EnemyData = []
		for unit in UnitList:
			if UnitList[unit]['portrait'] in EnemyList:
				if not UnitList[unit]['character'] in EnemyData:
					EnemyData.append(UnitList[unit]['character'])
		for data in EnemyData:
			for x in range(7):
				CharacterCalc = CharacterDec + UnitDataCalc(data) + x
				fe3rom.seek(CharacterCalc)
				HexRead = ByteToInt(fe3rom.read(1))
				if not HexRead == 255:
					HexRead += increasebase
					HexRead = bytes([HexRead])
					fe3rom.seek(CharacterCalc)
					fe3rom.write(HexRead)
	# For growths
	if growth == 1:
		for classes in ClassList:
			for x in range(6):
				ClassCalc = ClassDec + ClassDataCalc(ClassList[classes]) + x
				fe3rom.seek(ClassCalc)
				HexRead = fe3rom.read(1)
				HexRead = ByteToInt(HexRead)
				HexRead += increasegrowth
				HexRead = bytes([HexRead])
				fe3rom.seek(ClassCalc)
				fe3rom.write(HexRead)

# Increase enemy level
def IncreaseEnemyLevel(mode, levelincrease):
	UnitList = SearchForUnits()
	EnemyList = []
	if mode == 'enemy':
		EnemyList = GetPortraits(GenericPortraits)
	elif mode == 'boss':
		EnemyList = GetPortraits(BossPortraits)
	EnemyData = []
	for unit in UnitList:
		if UnitList[unit]['portrait'] in EnemyList:
			EnemyData.append(unit)
	for unit in EnemyData:
		fe3rom.seek(unit + 2)
		HexRead = fe3rom.read(1)
		HexRead = ByteToInt(HexRead)
		HexRead += levelincrease
		if HexRead > 20:
			HexRead = 20
		HexRead = bytes([HexRead])
		fe3rom.seek(unit + 2)
		fe3rom.write(HexRead)

# Give enemy items
def EnemyItem(mode, itemchance):
	UnitList = SearchForUnits()
	ItemList = GetItems(ShopItems) 
	EnemyList = []
	if mode == 'enemy':
		EnemyList = GetPortraits(GenericPortraits)
	elif mode == 'boss':
		EnemyList = GetPortraits(BossPortraits)
	EnemyData = {}
	for unit in UnitList:
		if UnitList[unit]['portrait'] in EnemyList:
			if UnitList[unit]['item1'] == 255:
				EnemyData[unit] = 0
			elif UnitList[unit]['item2'] == 255:
				EnemyData[unit] = 1
	for unit in EnemyData:
		if random.randint(0, 100) <= itemchance:
			newitem = ItemList[random.randint(0, len(ItemList) - 1)]
			fe3rom.seek(unit + 12 + EnemyData[unit])
			fe3rom.write(bytes([newitem]))

###########################################
############## Other Options ##############
###########################################
# Randomize Weapon base stats.
# Uses: Random number between 10-42
# Might: Random number between 5-15
# Weight: Random number between 5-10
# Crit: Random multiplier of 5 between 0-50. (15, 25, 5, etc)
# Hitrate: Random multiplier of 5 between 50-100.
# Weapon Level are not randomized since it might give TONS of unusuble weapons to character since the ranks are changed.
# Weapon Cost needs a good formula.
# Range needs a bit more of research.
# PLANNED: Random sprites and names?

def RandomizeWeapons():
	print('Randomizing Weapons...')
	FirstDec = 272617
	WeaponList = []
	# Get weapon numbers
	for weapon in WeaponItems:
		WeaponList.append(items[weapon])
	# Go through the weapons and randomize
	for weapon in WeaponList:
		WeaponPosition = ItemDataCalc(weapon)
		# Randomize Might
		NewMight = random.randint(5, 15)
		NewMight = bytes([NewMight])
		fe3rom.seek(FirstDec + WeaponPosition + 3)
		fe3rom.write(NewMight)
		# Randomize Hitrate
		NewHit = random.randint(10, 20)
		NewHit = bytes([NewHit * 5])
		fe3rom.seek(FirstDec + WeaponPosition + 4)
		fe3rom.write(NewHit)
		# Randomize Crit
		NewCrit = random.randint(0, 10)
		NewCrit = bytes([NewCrit * 5])
		fe3rom.seek(FirstDec + WeaponPosition + 5)
		fe3rom.write(NewCrit)
		# Randomize Weight
		NewWeight = random.randint(5,10)
		NewWeight = bytes([NewWeight])
		fe3rom.seek(FirstDec + WeaponPosition + 6)
		fe3rom.write(NewWeight)
		# Randomize Uses
		NewUse = random.randint(10, 42)
		NewUse = bytes([NewUse])
		fe3rom.seek(FirstDec + WeaponPosition + 8)
		fe3rom.write(NewUse)
	print('Done!')

# Remove weapon locks
# Change the locks, and then add it to the item pool
# Aura, Excalibur, Rescue, Aum, Aum Book 2 and Thief.
def BreakWeaponLocks():
	print('Removing weapon locks and adding to the item pool...')
	FirstDec = 272617
	# Change Aura wplv to 7
	ItemLocation = ItemDataCalc(items['Aura'])
	fe3rom.seek(FirstDec + ItemLocation + 2)
	fe3rom.write(bytes([7]))
	# Change Excalibur wplv to 8
	ItemLocation = ItemDataCalc(items['Excalibur'])
	fe3rom.seek(FirstDec + ItemLocation + 2)
	fe3rom.write(bytes([8]))
	# Change Rescue wplv to 8
	ItemLocation = ItemDataCalc(items['Rescue'])
	fe3rom.seek(FirstDec + ItemLocation + 2)
	fe3rom.write(bytes([7]))
	# Change Aum and Aum Book 2 wplv to 15
	ItemLocation = ItemDataCalc(items['Aum'])
	fe3rom.seek(FirstDec + ItemLocation + 2)
	fe3rom.write(bytes([15]))
	ItemLocation = ItemDataCalc(items['Aum2'])
	fe3rom.seek(FirstDec + ItemLocation + 2)
	fe3rom.write(bytes([15]))
	# Change Thief to 5
	ItemLocation = ItemDataCalc(items['Thief'])
	fe3rom.seek(FirstDec + ItemLocation + 2)
	fe3rom.write(bytes([5]))
	# Add to the item pool
	MagicSilver.append('Excalibur')
	MagicSilver.append('Aura')
	MagicSilverEnemy.append('Excalibur')
	StaveSilver.append('Rescue')
	StaveSteel.append('Thief')
	StaveLegendary.append('Aum')
	StaveLegendary.append('Aum2')
	print('Done!')

# Make Rapier usable by all characters
# Make Rapier wplv 2
def BreakRapierLock():
	print('Removing rapier lock...')
	FirstDec = 272617
	ItemLocation = ItemDataCalc(items['Rapier'])
	fe3rom.seek(FirstDec + ItemLocation + 2)
	fe3rom.write(bytes([2]))
	SwordSteel.append('Rapier')
	SwordSteelEnemy.append('Rapier')
	print('Done!')	

# Astral Shards randomization
def AstralShard(mode):
	stats = [0, 0, 0, 0, 0, 0, 0, 0]
	if mode == 1:
		score = random.randint(20, 40)
		split = random.randint(1, 8)
		splitstat = score / split
		for x in range(split):
			stats[random.randint(0, len(stats) - 1)] += splitstat
		for x in range(len(stats)):
			if not stats[x] == 0:
				if random.randint(0, 1) == 1:
					stats[x] += random.randint(0, 4) * 5
		for x in range(len(stats)):
			if random.randint(0, 10) <= 2:
				stats[x] = stats[x] * -1
		for x in range(len(stats)):
			stats[x] = int(stats[x])
			stats[x] = SignedByte(stats[x])
		return stats
	else:
		for x in range(len(stats)):
			stats[x] = random.randint(-100, 100)
			stats[x] = SignedByte(stats[x])
		return stats

def RandomizeAstralShard(mode):
	for x in range(12):
		stats = AstralShard(mode)
		for y in range(8):
			fe3rom.seek(AstralShardLocation + y + (x * 8))
			fe3rom.write(stats[y])

# 0 growths
def NoGrowths():
	FirstDec = 267265
	for unit in PlayableUnits:
		y = CharacterDataList[unit]
		y = UnitDataCalc(y)
		for x in range(8):
			growth = 0
			growth = bytes([growth])
			fe3rom.seek(FirstDec + y + 9 + x)
			fe3rom.write(growth)

def RandomizeShops():
	ShopLocation = 397892
	ItemList = GetItems(ShopItems)
	ShopList = {}
	for x in range(39):
		itemscount = random.randint(1, 7)
		ShopList[x] = []
		# Add the items
		for y in range(itemscount):
			while True:
				NewItem = ItemList[random.randint(0, len(ItemList) - 1)]
				if not NewItem in ShopList[x]:
					ShopList[x].append(NewItem)
					break
		# Fill the rest of shop list with 'Nothing'
		for y in range(7 - itemscount):
			ShopList[x].append(254)
		# Separator
		ShopList[x].append(254)
	for shop in ShopList:
		for x in range(len(ShopList[shop])):
			fe3rom.seek(ShopLocation + (shop * 8) + x)
			fe3rom.write(bytes([ShopList[shop][x]]))

#############################################
############## Support Options ##############
#############################################

def RandomizeSupports(minsupport, maxsupport, minbonus, maxbonus):
	NewSupports = {}
	SupportingUnits = []
	DummyDict = []
	for x in NameDict:
		SupportingUnits.append(NameDict[x])
	z = 0
	for name in NameDict:
		NumberOfSupports = random.randint(minsupport, maxsupport)
		for x in range(NumberOfSupports):
			while True:
				CreateSupport = []
				CreateSupport.append(NameDict[name])
				CreateSupport.append(SupportingUnits[random.randint(0, len(SupportingUnits) - 1)])
				Skip = 0
				for y in NewSupports:
					if NewSupports[y]['supporter'] == CreateSupport[0]:
						if NewSupports[y]['supported'] == CreateSupport[1]:
							Skip = 1
							break
				if Skip == 1:
					continue
				NewSupports[z] = {}
				NewSupports[z]['supporter'] = CreateSupport[0]
				NewSupports[z]['supported'] = CreateSupport[1]
				NewSupports[z]['bonus'] = random.randint(minbonus, maxbonus)
				z += 1
				break
	# Clear the support list
	x = 0
	while True:
		End = 0
		for y in range(3):
			fe3rom.seek(SupportDec + SupportCalc(x) + y)
			HexRead = ByteToInt(fe3rom.read(1))
			if HexRead == 255:
				End = 1
				break
			else:
				fe3rom.seek(SupportDec + SupportCalc(x) + y)
				fe3rom.write(bytes([255]))
				x += 1
		if End == 1:
			break
	# Write the new supports
	x = 0
	for support in NewSupports:
		z = 0
		for y in ['supporter', 'supported', 'bonus']:
			fe3rom.seek(SupportDec + SupportCalc(x) + z)
			fe3rom.write(bytes([NewSupports[support][y]]))
			z += 1
		x += 1
	print('Done!')

#############################################################
############## Map Data unit randomization ##################
#############################################################
###### Function for finding units, than adding them into a dict.
def SearchForUnits():
	FoundDict = {}
	SearchFor = {
	'name': 3,
	'portrait': 7,
	'class': 1,
	'level': 2,
	'weapon1': 8,
	'weapon2': 9,
	'weapon3': 10,
	'weapon4': 11,
	'item1': 12,
	'item2': 13,
	'ai1': 16,
	'ai2': 17,
	'ai3': 18
	}
	for chapter in chapterunits:
		if chapterunits[chapter]['type'] == 'table':
			UnitCount = chapterunits[chapter]['size']
			ChapterDec = chapterunits[chapter]['dec']
			EndPoint = chapterunits[chapter]['endpoint']
			# Loop through the hexes, and find if the character ID is from a playable character.
			# Jump if there is 0xFF, and stop when the dec endpoint reaches.
			while True:
				i = 0
				EndThis = 0
				while True:
					ChapterCalc = ChapterDec + ChapterUnitCalc(i)
					if ChapterCalc >= EndPoint:
						EndThis = 1
						break
					fe3rom.seek(ChapterCalc)
					HexRead = fe3rom.read(1)
					HexRead = ByteToInt(HexRead)
					if HexRead == 255:
						ChapterDec = ChapterCalc + 1
						break
					else:
						FoundDict[ChapterCalc] = {}
						FoundDict[ChapterCalc]['dec'] = ChapterCalc
						FoundDict[ChapterCalc]['character'] = HexRead
						for x in SearchFor:
							fe3rom.seek(ChapterCalc + SearchFor[x])
							HexRead = fe3rom.read(1)
							HexRead = ByteToInt(HexRead)
							FoundDict[ChapterCalc][x] = HexRead
						i += 1 

				if EndThis == 1:
					break
		elif chapterunits[chapter]['type'] == 'unit':
			# Ends when encounters a 0xFF
			ChapterDec = chapterunits[chapter]['dec']
			i = 0
			while True:
				ChapterCalc = ChapterDec + ChapterUnitCalc(i)
				fe3rom.seek(ChapterCalc)
				HexRead = fe3rom.read(1)
				HexRead = ByteToInt(HexRead)
				if HexRead == 255:
					break
				else:
					FoundDict[ChapterCalc] = {}
					FoundDict[ChapterCalc]['dec'] = ChapterCalc
					FoundDict[ChapterCalc]['character'] = HexRead
					for x in SearchFor:
						fe3rom.seek(ChapterCalc + SearchFor[x])
						HexRead = fe3rom.read(1)
						HexRead = ByteToInt(HexRead)
						FoundDict[ChapterCalc][x] = HexRead
					i += 1 
	return FoundDict

############################
### Give weapons routine ###
############################

def GiveWeapons(unit, mode):
	# Get inventory items
	InventoryItems = GetItems(AllItems)

	# Get weapon tiers
	Broken = GetItems(BrokenTier)
	Iron = GetItems(IronTier)
	Steel = GetItems(SteelTier)
	Silver = GetItems(SilverTier)
	Legendary = GetItems(LegendaryTier)

	# Get classes
	Sword = GetClasses(SwordClass)
	Lances = GetClasses(LanceClass)
	Axe = GetClasses(AxeClass)
	Bow = GetClasses(BowClass)
	Ballistae = GetClasses(BallistaeClass)
	Stave = GetClasses(StaveClass)
	Magic = GetClasses(MagicClass)
	Breath = GetClasses(BreathClass)
	Mounted = GetClasses(MountedClass)
	FreeStaff = GetClasses(FreeStave)
	DragonStone = GetClasses(DragonStoneClass)
	SecondaryStaff = GetClasses(FreeStave)

	# Check the tier and if is there any items.
	CurrentItems = []
	for slot in range(6):
		fe3rom.seek(unit + slot + 8)
		UnknownItem = fe3rom.read(1)
		UnknownItem = ByteToInt(UnknownItem)
		if UnknownItem == 255:
			CurrentItems.append('Nothing!')
		elif UnknownItem in InventoryItems:
			CurrentItems.append('Item!')
		elif UnknownItem in Broken:
			CurrentItems.append('Broken')
		elif UnknownItem in Iron:
			CurrentItems.append('Iron')
		elif UnknownItem in Steel:
			CurrentItems.append('Steel')
		elif UnknownItem in Silver:
			CurrentItems.append('Silver')
		elif UnknownItem in Legendary:
			CurrentItems.append('Legendary')

	# Check the unit class
	fe3rom.seek(unit + 1)
	UnitClass = fe3rom.read(1)
	UnitClass = ByteToInt(UnitClass)
	WeaponChoice = ''
	if UnitClass in Sword:
		WeaponChoice = 'Sword'
	
	elif UnitClass in Lances:
		WeaponChoice = 'Lances'
	
	elif UnitClass in Axe:
		WeaponChoice = 'Axe'
	
	elif UnitClass in Bow:
		WeaponChoice = 'Bow'
	
	elif UnitClass in Ballistae:
		WeaponChoice = 'Ballistae'
	
	elif UnitClass in Stave:
		WeaponChoice = 'Stave'
	
	elif UnitClass in Magic:
		WeaponChoice = 'Magic'
	
	elif UnitClass in Breath:
		WeaponChoice = 'Breath'

	elif UnitClass in DragonStone:
		WeaponChoice = 'Stone'

	# Functios to be used on playable units only.
	# Check if there is any weapons in the item slots, if they don't need Staves or Dragonstones
	StaffTier = ''
	if mode == 'player':
		if not WeaponChoice in ['Stave', 'Stone']:
			for x in range(2):
				TestItem = CurrentItems[4 + x]
				if not TestItem in ['Nothing!', 'Item!']:
					for y in range(3):
						NewItem = CurrentItems[y]
						if NewItem == 'Nothing!':
							CurrentItems[y] = TestItem
							CurrentItems[4 + x] = 'Nothing!'
							break
		# If they use staves or dragonstones, move them to the item slots
		else:
			NewItem = []
			for x in range(4):
				TestItem = CurrentItems[x]
				if not TestItem in ['Nothing!', 'Item!']:
					NewItem.append(TestItem)
					CurrentItems[x] = 'Delete!'
			for item in NewItem:
				for x in range(2):
					TestItem = CurrentItems[4 + x]
					if TestItem == 'Nothing!':
						CurrentItems[4 + x] = item
						break

		# Check if can use Magic and Staves, and place one item in the items slot.
		
		if UnitClass in SecondaryStaff:
			NewItem = ''
			for x in range(3):
				x += 1
				TestItem = CurrentItems[x]
				if not TestItem in ['Nothing!', 'Item!']:
					NewItem = TestItem
					CurrentItems[x] = 'Delete!'
					break
			if not NewItem == '':
				for x in range(2):
					TestItem = CurrentItems[4 + x]
					if TestItem == 'Nothing!':
						CurrentItems[4 + x] = 'SpecialStaff'
						StaffTier = NewItem
						break

		#Check if is a mounted unit, and place a iron sword in the weapon slot.
		if UnitClass in Mounted:
			for x in range(4):
				TestItem = CurrentItems[x]
				if TestItem == 'Nothing!':
					CurrentItems[x] = 'SpecialSword'
					break

	# Finally, start randomizing it
	NewItems = []
	for Item in CurrentItems:
		if Item in ['Broken', 'Iron', 'Steel', 'Silver', 'Legendary']:
			if WeaponChoice == 'Sword':
				NewItems.append(RandomizeSwords(Item, mode))
		
			elif WeaponChoice == 'Lances':
				NewItems.append(RandomizeLances(Item))

			elif WeaponChoice == 'Bow':
				NewItems.append(RandomizeBows(Item))
		
			elif WeaponChoice == 'Axe':
				NewItems.append(RandomizeAxes(Item, mode))

			elif WeaponChoice == 'Ballistae':
				NewItems.append(RandomizeBallistae(Item))

			elif WeaponChoice == 'Stave':
				NewItems.append(RandomizeStaves(Item))

			elif WeaponChoice == 'Magic':
				NewItems.append(RandomizeMagic(Item, mode))

			elif WeaponChoice == 'Breath':
				NewItems.append(RandomizeBreaths())

			elif WeaponChoice == 'Stone':
				NewItems.append(RandomizeStones())
		elif Item in ['Skip!', 'Item!']:
			NewItems.append('Skip!')
		elif Item == 'SpecialStaff':
			NewItems.append(RandomizeStaves(StaffTier))
		elif Item == 'SpecialSword':
			NewItems.append(b'\x00')
		else:
			NewItems.append('Delete!')
	# Writing the items
	for x in range(6):
		ToWrite = NewItems[x]
		if not ToWrite in ['Skip!', 'Delete!']:
			fe3rom.seek(unit + x + 8)
			fe3rom.write(ToWrite)
		elif ToWrite == 'Delete!':
			fe3rom.seek(unit + x + 8)
			fe3rom.write(b'\xff')

# Randomize classes for playable characters
def RandomizePlayableClasses(unit):
	# Set class lists
	DefaultTier = GetClasses(ClassTier1)
	Tier1 = GetClasses(PoolTier1)
	Tier1 += GetClasses(MountedTier1)
	Tier2 = GetClasses(PoolTier2)
	Tier2 += GetClasses(MountedTier2)

	# See if it is a tier 1 unit
	fe3rom.seek(unit + 1)
	BaseClass = fe3rom.read(1)
	BaseClass = ByteToInt(BaseClass)
	if BaseClass in DefaultTier:
		NewClass = Tier1[random.randint(0, len(Tier1) - 1)]
	else:
		NewClass = Tier2[random.randint(0, len(Tier2) - 1)]
	NewClass = bytes([NewClass])
	fe3rom.seek(unit + 1)
	fe3rom.write(NewClass)

# Marth book 2 only randomization
def RandomClassMarth(unit):
	# Set class lists
	Tier1 = GetClasses(['Lord', 'Cavalier', 'Pegasus Knight', 'Hunter', 'Mage M', 'Mage F', 'Dancer', 'Thief'])
	NewClass = Tier1[random.randint(0, len(Tier1) - 1)]
	NewClass = bytes([NewClass])
	fe3rom.seek(unit + 1)
	fe3rom.write(NewClass)

# Randomize classes for enemy characters
def RandomizeEnemyClasses(unit):
	# Set class lists
	DefaultTier = GetClasses(ClassTier1)
	Tier1 = GetClasses(PoolTier1)
	Tier1.remove(22)
	Tier1Mounted = GetClasses(MountedTier1)
	Tier2 = GetClasses(PoolTier2)
	Tier2.remove(15)
	Tier2Mounted = GetClasses(MountedTier2)

	# See if it is a tier 1 unit
	fe3rom.seek(unit + 1)
	BaseClass = fe3rom.read(1)
	BaseClass = ByteToInt(BaseClass)
	if BaseClass in DefaultTier:
		# Check if the unit is mounted
		if BaseClass in Tier1Mounted:
			DummyList = Tier1 + Tier1Mounted
			NewClass = DummyList[random.randint(0, len(DummyList) - 1)]
		# If not, just use the normal classpool
		else:
			NewClass = Tier1[random.randint(0, len(Tier1) - 1)]
	else:
		# Same  as above
		if BaseClass in Tier2Mounted:
			DummyList = Tier2 + Tier2Mounted
			NewClass = DummyList[random.randint(0, len(DummyList) - 1)]
		else:
			NewClass = Tier2[random.randint(0, len(Tier2) - 1)]
	NewClass = bytes([NewClass])
	fe3rom.seek(unit + 1)
	fe3rom.write(NewClass)

#######################################
############## GUI Stuff ##############
#######################################
root = Tk()

class CreateLabel:
	def __init__(self, text, row, column, columnspan=1, rowspan=1, sticky=NW):
		self.label = LabelFrame(root, text= text)
		self.label.grid(row = row, column = column, stick = sticky, columnspan = columnspan, rowspan = rowspan)
		self.VarList = {}
		self.maxcolumn = 0
		self.maxrow = 0

	def check(self, varname):
		return self.VarList[varname].get()

	def checkbutton(self, text, varname, row, column, default=0, sticky=W):
		self.VarList[varname] = IntVar()
		self.VarList[varname].set(default)
		self.checkbuttonFunc = Checkbutton(self.label, text = text, variable = self.VarList[varname])
		self.checkbuttonFunc.grid(row = row, column = column, stick=sticky)

	def button(self, text, command, row, column, sticky=W):
		self.buttonFunc = Button(self.label, text = text, command = command)
		self.buttonFunc.grid(row = row, column = column, stick=sticky)

	def radiobutton(self, text, varname, row, column, sticky=W, default=0):
		self.VarList[varname] = IntVar()
		self.VarList[varname].set(default)
		x = 0
		y = row
		for name in text:
			self.radiobuttonFunc = Radiobutton(self.label, text = name, variable = self.VarList[varname], value = x)
			self.radiobuttonFunc.grid(row = y, column = column, stick=sticky)
			x += 1
			y += 1

	def entry(self, text, width, row, column, default=0, sticky=W):
		self.VarList[text] = IntVar()
		self.VarList[text].set(default)
		self.entryFunc = Entry(self.label, width = width, textvariable = self.VarList[text])
		self.entryFunc.grid(row = row, column = column, stick=sticky)

	def textlabel(self, text, row, column, sticky=W):
		self.labelFunc = Label(self.label, text = text)
		self.labelFunc.grid(row = row, column = column, stick=sticky)

###############
### Playable
###############
LabelPlayable = CreateLabel('Playable Options', 1, 0, 1, 2)

LabelPlayable.checkbutton('Randomize classes', 'PlayerClass', 0, 0)

LabelPlayable.checkbutton('Ignore Julian and Rickard', 'IgnoreThief', 1, 0, 1)

LabelPlayable.checkbutton('Randomize bases', 'PlayerBases', 2, 0)

LabelPlayable.textlabel('Base Range:', 3 , 0)

LabelPlayable.entry('BasesRange', 5, 3, 0, 3, E)

LabelPlayable.checkbutton('Randomize growths', 'PlayerGrowths', 4, 0)

LabelPlayable.radiobutton(['Full Mode', 'Range Mode'], 'PlayerGrowthMode', 5, 0)

LabelPlayable.textlabel('Growths Range:', 7, 0)

LabelPlayable.entry('GrowthRange', 5, 7, 0, 30, E)
###############
### Support
###############
LabelSupport = CreateLabel('Support Options', 3, 0)

LabelSupport.checkbutton('Randomize Supports', 'Support', 1, 0)

LabelSupport.textlabel('Minimum characters supported', 2, 0)
LabelSupport.textlabel('by one character:', 3, 0)

LabelSupport.entry('SupportMinCount', 5, 3, 0, 0, E)

LabelSupport.textlabel('Maximum characters supported', 4, 0)
LabelSupport.textlabel('by one character:', 5, 0)

LabelSupport.entry('SupportMaxCount', 5, 5, 0, 3, E)

LabelSupport.textlabel('Minimum bonus:', 6, 0)

LabelSupport.entry('SupportMinBonus', 5, 6, 0, 5, E)

LabelSupport.textlabel('Maximum bonus', 7, 0)

LabelSupport.entry('SupportMaxBonus', 5, 7, 0, 20, E)
##################
#### Global Enemy
##################

LabelEnemy = CreateLabel('Global Enemies', 1, 1, 2)

LabelEnemy.checkbutton('Increase enemy bases', 'EnemyBase', 0, 0)

LabelEnemy.checkbutton('Increase enemy growths', 'EnemyGrowth', 0, 1)

LabelEnemy.entry('EnemyBaseIncrease', 5, 1, 0, 3, E)
LabelEnemy.textlabel('Increase bases by:', 1, 0)

LabelEnemy.entry('EnemyGrowthIncrease', 5, 1, 1, 15, E)
LabelEnemy.textlabel('Increase growths by:', 1, 1)

################
### Bosses
################
LabelBoss = CreateLabel('Boss options', 2, 2)
LabelBoss.checkbutton('Randomize classes', 'BossClass', 0, 0)

LabelBoss.checkbutton('Increase level', 'BossLevel', 1, 0)

LabelBoss.entry('BossLevelIncrease', 5, 2, 0, 3, E)

LabelBoss.textlabel('Increase by:', 2, 0)

LabelBoss.checkbutton('Randomize items', 'BossItem', 3, 0)

LabelBoss.textlabel('Item chance:', 4, 0)
LabelBoss.entry('ItemChance', 5, 4, 0, 20, E)
#################
### Generics
#################
LabelGeneric = CreateLabel('Generic options', 2, 1)
LabelGeneric.checkbutton('Randomize classes', 'GenericClass', 0, 0)

LabelGeneric.checkbutton('Ignore thiefs with sphere/orbs', 'ThiefShard', 1, 0)

LabelGeneric.checkbutton('Increase level', 'GenericLevel', 2, 0)

LabelGeneric.entry('GenericLevelIncrease', 5, 3, 0, 4, E)

LabelGeneric.textlabel('Increase by:', 3, 0)

LabelGeneric.checkbutton('Randomize items', 'GenericItem', 4, 0)
LabelGeneric.textlabel('Item chance:', 5, 0)
LabelGeneric.entry('ItemChance', 5, 5, 0, 20, E)
###############
#### Other options
###############
LabelOther = CreateLabel('Other options', 1, 3, 1, 2)
LabelOther.checkbutton('Randomize Astral Shard bonuses', 'AstralShard', 0, 0)
LabelOther.radiobutton(['Full Mode', '\'Balanced\' Mode'], 'AstralShardMode', 1, 0)

LabelOther.checkbutton('Remove weapon lock restrictions', 'WeaponLock', 3, 0)
LabelOther.checkbutton('Remove Rapier Lock', 'RapierLock', 4, 0)

LabelOther.checkbutton('Randomize weapons', 'RandomWeapon', 5, 0)

LabelOther.checkbutton('0% growths', '0growths', 6, 0)

LabelOther.checkbutton('Randomize shops', 'Shop', 7, 0)
##################################################################
########################### Functions ############################
##################################################################
class BasicWindow:
	def __init__(self, text):
		self.window = Toplevel(root)
		self.label = Label(self.window, text = text)
		self.button = Button(self.window, text = 'Ok', command = self.quit)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0)
		self.window.title('Randomizing...')
		self.window.iconbitmap('xane.ico')
	def quit(self):
		self.window.destroy()

class FinishWindow:
	def __init__(self):
		self.window = Toplevel(root)
		self.label = Label(self.window, text = 'Randomization finished! \n You can find the ROM and the log in the place where you saved it. \n The randomizer will close now...')
		self.button = Button(self.window, text = 'Ok!', command = self.quit)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0)
		self.window.title('Finished!')
		self.window.iconbitmap('xane.ico')
	def quit(self):
		self.window.destroy()
		root.destroy()
		sys.exit()

def SelectFile():
	RomLocation.set(filedialog.askopenfilename(title = "Select FE3 rom...",filetypes = [("All Files","*.*")]))
def RandomizingProcess():
	global fe3rom
######################
### File Locations ###
######################
	FileLocation = RomLocation.get()
	if FileLocation == '':
		PopUpBox = BasicWindow('Please, select a FE3 rom first!')
		return
	SaveLocation = filedialog.asksaveasfilename(title = "Choose where to save the randomize rom...",filetypes = [("SNES .smc files","*.smc")])
	if SaveLocation == '':
		PopUpBox = BasicWindow('Please, select a place to save the FE3 randomized rom! Aborting randomization process...')
		return
	if not '.smc' in SaveLocation:
		SaveLocation += '.smc'
	if LogVar.get() == 1:
		LogLocation = filedialog.asksaveasfilename(title = "Choose where to save the log file...",filetypes = [("HTML File","*.html")])
		if LogLocation == '':
			PopUpBox = BasicWindow('Please, select a place to save the changelog file! Aborting randomization process...')
			return
		else:
			if not '.html' in LogLocation:
				LogLocation += '.html'
			changelog = open(LogLocation, 'w')


	shutil.copyfile(FileLocation, SaveLocation)
	fe3rom = open(SaveLocation, 'rb+')
	print(SearchForUnits())
	PopUpBox = BasicWindow('The ROM is now being randomized! Please, wait a bit.')
###############################
### Randomization Functions ###
###############################
# Playable class randomization
	if LabelPlayable.check('PlayerClass') == 1:
		RandomizePlayableUnits(LabelPlayable.check('IgnoreThief'))
		FixManakete('player')
		PlayableCopyUnits()
# Playable bases randomization
	if LabelPlayable.check('PlayerBases') == 1:
		print(LabelPlayable.check('BasesRange'))
		RandomizePlayableBases(LabelPlayable.check('BasesRange'))
		PlayableCopyBases()
# Playable growths randomization
	if LabelPlayable.check('PlayerGrowths') == 1:
		RandomizePlayableGrowths(LabelPlayable.check('PlayerGrowthMode'), LabelPlayable.check('GrowthRange'))
# Support Randomization
	if LabelSupport.check('Support') == 1:
		RandomizeSupports(LabelSupport.check('SupportMinCount'), LabelSupport.check('SupportMaxCount'), LabelSupport.check('SupportMinBonus'), LabelSupport.check('SupportMaxBonus'))
# Generic unit randomization
	if LabelGeneric.check('GenericClass') == 1:
		RandomizeEnemyUnits(LabelGeneric.check('ThiefShard'))
# Increase enemy level
	if LabelGeneric.check('GenericLevel') == 1:
		IncreaseEnemyLevel('enemy', LabelGeneric.check('GenericLevelIncrease'))
# Randomize generic items
	if LabelGeneric.check('GenericItem') == 1:
		EnemyItem('enemy', LabelBoss.check('ItemChance'))
# Boss unit randomization
	if LabelBoss.check('BossClass') == 1:
		RandomizeBossUnits()
# Boss level increase
	if LabelBoss.check('BossLevel') == 1:
		IncreaseEnemyLevel('boss', LabelBoss.check('BossLevelIncrease'))
# Randomize boss items
	if LabelBoss.check('BossItem') == 1:
		EnemyItem('boss', LabelBoss.check('ItemChance'))
# All enemies increase base or/and growth
	if LabelEnemy.check('EnemyBase') == 1 or LabelEnemy.check('EnemyGrowth') == 1:
		IncreaseEnemyStats(LabelEnemy.check('EnemyBase') , LabelEnemy.check('EnemyGrowth'), LabelEnemy.check('EnemyBaseIncrease'), LabelEnemy.check('EnemyGrowthIncrease'))
# Astral Shards
	if LabelOther.check('AstralShard') == 1:
		RandomizeAstralShard(LabelOther.check('AstralShardMode'))
# Break Weapon Locks
	if LabelOther.check('WeaponLock') == 1:
		BreakWeaponLocks()
# Break Rapier lock
	if LabelOther.check('RapierLock') == 1:
		BreakRapierLock()
# Weapon stats
	if LabelOther.check('RandomWeapon') == 1:
		RandomizeWeapons()
# 0 growths
	if LabelOther.check('0growths') == 1:
		NoGrowths()
# Shop Randomization
	if LabelOther.check('Shop') == 1:
		RandomizeShops()
###################
### Log Process ###
###################
	fe3rom.close()
	fe3rom = open(SaveLocation, 'rb+')
	if LogVar.get() == 1:
		CreateLogFile(LogLocation)
		if LabelPlayable.check('PlayerBases') or LabelPlayable.check('PlayerGrowths') == 1 or LabelPlayable.check('PlayerClass') == 1:
			CreatePlayableLog(LogLocation, SaveLocation, SearchForUnits())
		if LabelSupport.check('Support') == 1:
			CreateSupportLog(LogLocation, SaveLocation)
		if LabelOther.check('AstralShard') == 1:
			CreateAstralLog(LogLocation, SaveLocation)
		EndLogFile(LogLocation)
		changelog.close()
	fe3rom.close()
	try:
		PopUpBox.quit()
	except:
		'hi'
	done = FinishWindow()
###########################
########## Other ##########
###########################
# They need to be down here since the functions are after the gui stuff
RomLocation = StringVar()
LogVar = IntVar()

buttonOpenFile = Button(root, text='Select FE3 rom...', command = SelectFile, width=50)
buttonOpenFile.grid(row = 0, column = 1, columnspan = 4)

checkmarkCreateLog = Checkbutton(root, text = 'Create Log', variable = LogVar)
checkmarkCreateLog.grid(row = 0, column = 0, stick=E)

labelReadme = Label(root, text = 'For more information on the options or a fix to possible user errors, please read the Readme.')
labelReadme.grid(row = 4, columnspan = 4, column = 0, sticky=N)

buttonRandomize = Button(root, text='Randomize!', width = 50, command = RandomizingProcess)
buttonRandomize.grid(row = 5, columnspan = 4, column = 0, sticky=N)

root.title('Xane Randomizer: A FE3 Randomizer')
root.iconbitmap('xane.ico')
root.mainloop()