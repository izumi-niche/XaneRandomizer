import os
import random
import shutil

from data.chapters import *
from data.portraits import *
from data.dumbnames import * 
from data.characterdata import *
from data.classes import *
from data.items import *

from lists.classpool import *
from lists.enemies import *
from lists.itempool import *
from lists.playable import *
from lists.weaponpool import *

from basicfunctions import *
from logfunctions import *

from tkinter import *
from tkinter import filedialog


fe3rom = open('dummy.deleteme', 'w')
changelog = open('dummy.deleteme', 'w')

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
	if mode == 0:
		for unit in PlayableUnits:
			unit = CharacterDataList[unit]
			UnitLocation = UnitDataCalc(unit)
			for x in range(8):
				fe3rom.seek(FirstDec + unit + 9 + x)
				growth = fe3rom.read(1)
				growth = ByteToInt(growth)
				growth = growth + random.randint(statrange * -1, statrange)
				if growth < 5:
					growth = 5
				elif growth > 100:
					growth = 100
				growth = bytes([growth])
				fe3rom.seek(FirstDec + unit + 9 + x)
				fe3rom.write(growth)
	# Full mode
	if mode == 1:
		for unit in PlayableUnits:
			unit = CharacterDataList[unit]
			for x in range(8):
				growth = random.randint(1, 20)
				growth = growth * 5
				growth = bytes([growth])
				fe3rom.seek(FirstDec + unit + 9 + x)
				fe3rom.write(growth)
	print('Done!')

###########################################
############## Enemy Options ##############
###########################################
# Randomizing enemy units.
# Will look for portraits to determine if it is a enemy unit.
def RandomizeEnemyUnits():
	EnemyList = GetPortraits(GenericPortraits)
	UnitList = SearchForUnits()
	UnitWrite = []
	for unit in UnitList:
		if UnitList[unit]['portrait'] in EnemyList:
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
		HexRead = bytes([HexRead])
		fe3rom.seek(unit + 2)
		fe3rom.write(HexRead)
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
		NewMight = random.randint(0, 15)
		NewMight = bytes([NewMight])
		fe3rom.seek(FirstDec + WeaponPosition + 3)
		fe3rom.write(NewMight)
		# Randomize Hitrate
		NewHit = random.randint(10, 20)
		NewHit = bytes([NewHit])
		fe3rom.seek(FirstDec + WeaponPosition + 4)
		fe3rom.write(NewHit)
		# Randomize Crit
		NewCrit = random.randint(0, 10)
		NewCrit = bytes([NewCrit])
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
	MagicSilver.append('Aura')
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

#############################################
############## Support Options ##############
#############################################



#############################################################
############## Map Data unit randomization ##################
#############################################################
###### Function for finding units, than adding them into a dict.
def SearchForUnits():
	FoundDict = {}
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

						fe3rom.seek(ChapterCalc + 3)
						HexRead = fe3rom.read(1)
						HexRead = ByteToInt(HexRead)
						FoundDict[ChapterCalc]['name'] = HexRead

						fe3rom.seek(ChapterCalc + 7)
						HexRead = fe3rom.read(1)
						HexRead = ByteToInt(HexRead)
						FoundDict[ChapterCalc]['portrait'] = HexRead
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

					fe3rom.seek(ChapterCalc + 3)
					HexRead = fe3rom.read(1)
					HexRead = ByteToInt(HexRead)
					FoundDict[ChapterCalc]['name'] = HexRead

					fe3rom.seek(ChapterCalc + 7)
					HexRead = fe3rom.read(1)
					HexRead = ByteToInt(HexRead)
					FoundDict[ChapterCalc]['portrait'] = HexRead
					i += 1 
	return FoundDict

# Randomizing playable units.
# Will look for the character data to determine if it is a playable unit.
def RandomizePlayableUnits():
	CharacterList = GetCharacter(PlayableUnits)
	UnitList = SearchForUnits()
	UnitWrite = [] 
	for unit in UnitList:
		if UnitList[unit]['character'] in CharacterList:
			UnitWrite.append(unit)
	# Write
	for unit in UnitWrite:
		RandomizePlayableClasses(unit)
		GiveWeapons(unit,'player')


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

# Randomize classes for enemy characters
def RandomizeEnemyClasses(unit):
	# Set class lists
	DefaultTier = GetClasses(ClassTier1)
	Tier1 = GetClasses(PoolTier1)
	Tier1.remove(22)
	Tier1Mounted = GetClasses(MountedTier1)
	Tier2 = GetClasses(PoolTier2)
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





















root = Tk()
# Variables
RomLocation = StringVar()
LogVar = IntVar()
PlayerClassVar = IntVar()
# Functions
def SelectFile():
	RomLocation.set(filedialog.askopenfilename(title = "Select FE3 rom...",filetypes = (("SNES .smc files","*.smc"), ("SNES .fig files","*.fig"),("All Files","*.*"))))
def RandomizingProcess():
	global fe3rom
	##############################
	### File Locations routine ###
	##############################
	FileLocation = RomLocation.get()
	if FileLocation == '':
		print('Please, select a FE3 rom first!')
		return
	SaveLocation = filedialog.asksaveasfilename(title = "Choose where to save the randomize rom...",filetypes = (("SNES .smc files","*.smc"),("All Files","*.*")))
	if SaveLocation == '':
		print('Please, select a place to save the FE3 randomized rom! Aborting randomization process...')
		return
	if not '.smc' in SaveLocation:
		SaveLocation += '.smc'
	if LogVar.get() == 1:
		LogLocation = filedialog.asksaveasfilename(title = "Choose where to save the log file...",filetypes = (("HTML File","*.html"),("All Files","*.*")))
		if LogLocation == '':
			print('Please, select a place to save the changelog file! Aborting randomization process...')
			return
		else:
			if not '.html' in LogLocation:
				LogLocation += '.html'
			changelog = open(LogLocation, 'w')
	shutil.copyfile(FileLocation, SaveLocation)
	fe3rom = open(SaveLocation, 'rb+')
	###############################
	### Randomization Functions ###
	###############################
	IncreaseEnemyStats(1, 1, 3, 30)
	if PlayerClassVar.get() == 1:
		RandomizePlayableUnits()
	###################
	### Log Process ###
	###################
	if LogVar.get() == 1:
		CreateLogFile(LogLocation)

		CreateSupportLog(LogLocation, SaveLocation)

		EndLogFile(LogLocation)
#######################################
############## GUI Stuff ##############
#######################################
LabelPlayable = LabelFrame(root, text="Playable Options", width = 220, height = 290)
LabelEnemy = LabelFrame(root, text="Enemy Options")
LabelBoss = LabelFrame(root, text="Bosses Options", width = 284, height = 336)
LabelCustom = LabelFrame(root, text="Custom Options", width = 485, height = 160)
LabelExtras = LabelFrame(root, text="Extra Options", height = 160, width = 284)
LabelUnused = LabelFrame(root, text="Unused Content")
LabelWeapons = LabelFrame(root, text="Weapons and classes")

buttonOpenFile = Button(root, text='Search ROM...', command = SelectFile)
entryOpenFile = Entry(root, width = 100, textvariable = RomLocation)
checkmarkCreateLog = Checkbutton(root, text = 'Create Log', variable = LogVar)
labelReadme = Label(root, text = 'For more information on the options or a fix to possible user errors, please read the Readme.')
buttonRandomize = Button(root, text='Randomize!', width = 108, command = RandomizingProcess)

# Playable
checkmarkRandomizeClassesPlayer = Checkbutton(LabelPlayable, text = 'Randomize classes', variable = PlayerClassVar)

checkmarkRandomizeBasesPlayer = Checkbutton(LabelPlayable, text = 'Randomize bases')
labelBasesRange = Label(LabelPlayable, text = '     Bases Range:')
entryBasesRange = Entry(LabelPlayable, width=5)

checkmarkRandomizeGrowthsPlayer = Checkbutton(LabelPlayable, text = 'Randomize growths')
radiobuttonGrowthsFullMode = Radiobutton(LabelPlayable, text = 'Full Mode')
radiobuttonGrowthsRangeMode = Radiobutton(LabelPlayable, text = 'Range Mode')
entryGrowthsRange = Entry(LabelPlayable, width=5)

checkmarkAllowEnemyWeapons = Checkbutton(LabelPlayable, text = 'Allow enemy only weapons')

# Enemy
checkmarkRandomizeClassesEnemy = Checkbutton(LabelEnemy, text = 'Randomize classes')

checkmarkIncreaseBaseEnemy = Checkbutton(LabelEnemy, text = 'Increase bases')
labelIncreaseBaseEnemy = Label(LabelEnemy, text = '             Increase by:')
entryIncreaseBaseEnemy = Entry(LabelEnemy, width = 5)

checkmarkIncreaseGrowthEnemy = Checkbutton(LabelEnemy, text = 'Increase growths')
labelIncreaseGrowthEnemy = Label(LabelEnemy, text = '             Increase by:')
entryIncreaseGrowthEnemy = Entry(LabelEnemy, width = 5)

checkmarkEnemyUniqueClasses = Checkbutton(LabelEnemy, text = 'Enemies can use unique classes')
checkmarkEnemyItemDrop = Checkbutton(LabelEnemy, text = 'Have a chance to have droppable items')

checkmarkEnemyMininumWeaponTier = Checkbutton(LabelEnemy, text = 'Minimum Weapon Tier')
radiobuttonEnemyTierIron = Radiobutton(LabelEnemy, text = 'Iron Tier')
radiobuttonEnemyTierSteel = Radiobutton(LabelEnemy, text = 'Steel Tier')
radiobuttonEnemyTierSilver = Radiobutton(LabelEnemy, text = 'Silver Tier')
radiobuttonEnemyTierLegendary = Radiobutton(LabelEnemy, text = 'Legendary Tier')

checkmarkEnemyUpgradeWeapon = Checkbutton(LabelEnemy, text = 'Weapons have a chance to upgrade one tier')

# Boss
checkmarkRandomizeClassesBoss = Checkbutton(LabelBoss, text = 'Randomize classes')

checkmarkIncreaseBaseBoss = Checkbutton(LabelBoss, text = 'Increase bases')
labelIncreaseBaseBoss = Label(LabelBoss, text = '             Increase by:')
entryIncreaseBaseBoss = Entry(LabelBoss, width = 5)

checkmarkIncreaseGrowthBoss = Checkbutton(LabelBoss, text = 'Increase growths')
labelIncreaseGrowthBoss = Label(LabelBoss, text = '             Increase by:')
entryIncreaseGrowthBoss = Entry(LabelBoss, width = 5)

checkmarkBossUniqueClasses = Checkbutton(LabelBoss, text = 'Enemies can use unique classes')
checkmarkBossItemDrop = Checkbutton(LabelBoss, text = 'Have a chance to have droppable items')

checkmarkBossMininumWeaponTier = Checkbutton(LabelBoss, text = 'Minimum Weapon Tier')
radiobuttonBossTierIron = Radiobutton(LabelBoss, text = 'Iron Tier')
radiobuttonBossTierSteel = Radiobutton(LabelBoss, text = 'Steel Tier')
radiobuttonBossTierSilver = Radiobutton(LabelBoss, text = 'Silver Tier')
radiobuttonBossTierLegendary = Radiobutton(LabelBoss, text = 'Legendary Tier')

checkmarkBossUpgradeWeapon = Checkbutton(LabelBoss, text = 'Weapons have a chance to upgrade one tier')

# Custom
checkmarkCreateMiniboss = Checkbutton(LabelCustom, text = 'Create minibosses')

LabelFirstChapter = Label(LabelCustom, text = 'Chapter they first appear:')
entryFirstChapter = Entry(LabelCustom, width = 5)

LabelMinimumPerChapter = Label(LabelCustom, text = 'Minimum per chapter:')
entryMinimumPerChater = Entry(LabelCustom, width = 5)

LabelMaximumPerChapter = Label(LabelCustom, text = 'Maximum per chapter:')
entryMaximumPerChapter = Entry(LabelCustom, width = 5)

checkmarkIncreaseMiniBossChance = Checkbutton(LabelCustom, text = 'Increase chance to have \n more has the game progresses')

checkmarkMinimumWeaponTier = Checkbutton(LabelCustom, text = 'Minimum weapon tier')
radiobuttonMiniBossTierIron = Radiobutton(LabelCustom, text = 'Iron Tier')
radiobuttonMiniBossTierSteel = Radiobutton(LabelCustom, text = 'Steel Tier')
radiobuttonMiniBossTierSilver = Radiobutton(LabelCustom, text = 'Silver Tier')
radiobuttonMiniBossTierLegendary = Radiobutton(LabelCustom, text = 'Legendary Tier')

# Extras
checkmarkRandomizeExtras = Checkbutton(LabelExtras, text = 'Randomize Astral Shards')

checkmarkDoNotCopy = Checkbutton(LabelExtras, text = 'Do not copy units')
checkmarkZeroGrowths = Checkbutton(LabelExtras, text = '0% growths')
checkmarkZeroBases = Checkbutton(LabelExtras, text = '0 bases')

# Unused
checkmarkEnemyUnused = Checkbutton(LabelUnused, text = 'Allow enemies use unused classes')

# Weapon
checkmarkRandomizeWeapons = Checkbutton(LabelWeapons, text = 'Randomize weapon stats')


## PLACE STUFF
buttonOpenFile.grid(row = 0, column = 0, stick=E, columnspan = 3)
entryOpenFile.grid(row = 0, column = 0, columnspan = 3)
checkmarkCreateLog.grid(row = 0, column = 0, columnspan = 3, stick=W)

LabelPlayable.grid(row = 1, column = 0, stick=NW)
LabelPlayable.grid_propagate(0)
LabelBoss.grid(row = 1, column = 2, stick=NW, rowspan = 2)
LabelBoss.grid_propagate(0)
LabelEnemy.grid(row = 1, column = 1, stick=NW, rowspan = 2)
LabelUnused.grid(row = 2, column = 0, stick=NW)
LabelCustom.grid(row = 3, column = 0, stick=NW, columnspan = 2)
LabelCustom.grid_propagate(0)
#LabelWeapons.grid(row = 0, column = 2, stick=W)
LabelExtras.grid(row = 3, column = 2, stick=NW)
LabelExtras.grid_propagate(0)
labelReadme.grid(row = 5, column = 0, columnspan = 3)
buttonRandomize.grid(row = 6, column = 0, columnspan = 3)

#Playable
checkmarkRandomizeClassesPlayer.grid(row = 0, column = 0, stick=W)
checkmarkRandomizeBasesPlayer.grid(row = 1, column = 0, stick=W)
labelBasesRange.grid(row = 2, column = 0)
entryBasesRange.grid(row = 2, column = 0, stick=E)
checkmarkRandomizeGrowthsPlayer.grid(row = 3, column = 0, stick=W)
radiobuttonGrowthsFullMode.grid(row = 4, column = 0, stick=W)
radiobuttonGrowthsRangeMode.grid(row = 5, column = 0, stick=W)
entryGrowthsRange.grid(row = 5, column = 0, stick=E)
checkmarkAllowEnemyWeapons.grid(row = 6, column = 0, stick=W)

#Boss
checkmarkRandomizeClassesBoss.grid(row = 0, column = 0, stick=W)

checkmarkIncreaseBaseBoss.grid(row = 1, column = 0, stick=W)
labelIncreaseBaseBoss.grid(row = 2, column = 0, stick=W)
entryIncreaseBaseBoss.grid(row = 2, column = 0)

checkmarkIncreaseGrowthBoss.grid(row = 3, column = 0, stick=W)
labelIncreaseGrowthBoss.grid(row = 4, column = 0, stick=W)
entryIncreaseGrowthBoss.grid(row = 4, column = 0)

checkmarkBossUniqueClasses.grid(row = 5, column = 0, stick=W)
checkmarkBossItemDrop.grid(row = 6, column = 0, stick=W)

checkmarkBossMininumWeaponTier.grid(row = 7, column = 0, stick=W)
radiobuttonBossTierIron.grid(row = 8, column = 0, stick=W)
radiobuttonBossTierSteel.grid(row = 9, column = 0, stick=W)
radiobuttonBossTierSilver.grid(row = 10, column = 0, stick=W)
radiobuttonBossTierLegendary.grid(row = 11, column = 0, stick=W)

checkmarkBossUpgradeWeapon.grid(row = 12, column = 0, stick=W)
#Enemy
checkmarkRandomizeClassesEnemy.grid(row = 0, column = 0, stick=W)

checkmarkIncreaseBaseEnemy.grid(row = 1, column = 0, stick=W)
labelIncreaseBaseEnemy.grid(row = 2, column = 0, stick=W)
entryIncreaseBaseEnemy.grid(row = 2, column = 0)

checkmarkIncreaseGrowthEnemy.grid(row = 3, column = 0, stick=W)
labelIncreaseGrowthEnemy.grid(row = 4, column = 0, stick=W)
entryIncreaseGrowthEnemy.grid(row = 4, column = 0)

checkmarkEnemyUniqueClasses.grid(row = 5, column = 0, stick=W)
checkmarkEnemyItemDrop.grid(row = 6, column = 0, stick=W)

checkmarkEnemyMininumWeaponTier.grid(row = 7, column = 0, stick=W)
radiobuttonEnemyTierIron.grid(row = 8, column = 0, stick=W)
radiobuttonEnemyTierSteel.grid(row = 9, column = 0, stick=W)
radiobuttonEnemyTierSilver.grid(row = 10, column = 0, stick=W)
radiobuttonEnemyTierLegendary.grid(row = 11, column = 0, stick=W)

checkmarkEnemyUpgradeWeapon.grid(row = 12, column = 0, stick=W)

#Custom
checkmarkCreateMiniboss.grid(row = 0, column = 0, stick=W)
LabelFirstChapter.grid(row = 1, column = 0, stick=W)
entryFirstChapter.grid(row = 1, column = 0, stick=E)
LabelMinimumPerChapter.grid(row = 2, column = 0, stick=W)
entryMinimumPerChater.grid(row = 2, column = 0, stick=E)
LabelMaximumPerChapter.grid(row = 3, column = 0, stick=W)
entryMaximumPerChapter.grid(row = 3, column = 0, stick=E)
checkmarkIncreaseMiniBossChance.grid(row = 4, column = 0, stick=W, rowspan=2)

checkmarkMinimumWeaponTier.grid(row = 0, column =  1, stick=W)
radiobuttonMiniBossTierIron.grid(row = 1, column = 1, stick=W)
radiobuttonMiniBossTierSteel.grid(row = 2, column = 1, stick=W)
radiobuttonMiniBossTierSilver.grid(row = 3, column = 1, stick=W)
radiobuttonMiniBossTierLegendary.grid(row = 4, column = 1, stick=W)
#Extras
checkmarkRandomizeExtras.grid(row = 0, column = 0, stick=W)

checkmarkDoNotCopy.grid(row = 0, column = 1, stick=W)
checkmarkZeroBases.grid(row = 1, column = 0, stick=W)
checkmarkZeroGrowths.grid(row = 1, column = 1, stick=W)

#Unused
checkmarkEnemyUnused.grid(row = 0, column = 0)

checkmarkRandomizeWeapons.grid(row = 0, column = 0)

root.title('Xane Randomizer: A FE3 Randomizer')
root.iconbitmap('xane.ico')
root.mainloop()
