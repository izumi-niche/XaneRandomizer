import sys
import random
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

def UnitDataCalc(number):
	return number * 17

def ItemDataCalc(number):
	return number * 14
	
def ChapterUnitCalc(number):
	return number * 19

def SupportCalc(number):
	return number * 3

def ClassDataCalc(number):
	return number * 6

def ClassDataBaseCalc(number):
	return number * 9

def ByteToInt(number):
	return int.from_bytes(number, byteorder=sys.byteorder)

def GetCharacter(things):
	DummyList = []
	for x in things:
		DummyList.append(CharacterDataList[x])
	return DummyList

def GetItems(things):
	DummyList = []
	for x in things:
		DummyList.append(items[x])
	return DummyList

def GetClasses(things):
	DummyList = []
	for x in things:
		DummyList.append(ClassList[x])
	return DummyList

def GetPortraits(things):
	DummyList = []
	for x in things:
		DummyList.append(PortraitList[x])
	return DummyList

def ReverseDict(olddict):
	newdict = {}
	for i in olddict:
		newdict[olddict[i]] = i
	return newdict


##############################################################
############## Item randomization functions ##################
##############################################################
def RandomizeSwords(tier, mode):
	Broken = GetItems(SwordBroken)
	Iron = GetItems(SwordIron)

	Steel = []
	Silver = []
	if mode == 'player':
		Steel = GetItems(SwordSteel)
		Silver = GetItems(SwordSilver)
	else:
		Steel = GetItems(SwordSteelEnemy)
		Silver = GetItems(SwordSilverEnemy)

	Legendary = GetItems(SwordLegendary)

	NewWeapon = ''
	if tier == 'Broken':
		NewWeapon = Broken[random.randint(0, len(Broken) - 1)]
	elif tier == 'Iron':
		NewWeapon = Iron[random.randint(0, len(Iron) - 1)]
	elif tier == 'Steel':
		NewWeapon = Steel[random.randint(0, len(Steel) - 1)]
	elif tier == 'Silver':
		NewWeapon = Silver[random.randint(0, len(Silver) - 1)]
	elif tier == 'Legendary':
		NewWeapon = Legendary[random.randint(0, len(Legendary) - 1)]

	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeLances(tier):

	Broken = GetItems(LanceBroken)
	Iron = GetItems(LanceIron)
	Steel = GetItems(LanceSteel)
	Silver = GetItems(LanceSilver)
	Legendary = GetItems(LanceLegendary)
	NewWeapon = ''

	if tier == 'Broken':
		NewWeapon = Broken[random.randint(0, len(Broken) - 1)]
	elif tier == 'Iron':
		NewWeapon = Iron[random.randint(0, len(Iron) - 1)]
	elif tier == 'Steel':
		NewWeapon = Steel[random.randint(0, len(Steel) - 1)]
	elif tier == 'Silver':
		NewWeapon = Silver[random.randint(0, len(Silver) - 1)]
	elif tier == 'Legendary':
		NewWeapon = Legendary[random.randint(0, len(Legendary) - 1)]

	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeAxes(tier, mode):

	Broken = GetItems(AxeBroken)
	Iron = GetItems(AxeIron)
	Silver = GetItems(AxeSilver)

	Steel = []
	Legendary = []
	if mode == 'player':
		Steel = GetItems(AxeSteel)
		Legendary = GetItems(AxeLegendary)
	else:
		Steel = GetItems(AxeSteelEnemy)
		Legendary = GetItems(AxeLegendaryEnemy)

	

	if tier == 'Broken':
		NewWeapon = Broken[random.randint(0, len(Broken) - 1)]
	elif tier == 'Iron':
		NewWeapon = Iron[random.randint(0, len(Iron) - 1)]
	elif tier == 'Steel':
		NewWeapon = Steel[random.randint(0, len(Steel) - 1)]
	elif tier == 'Silver':
		NewWeapon = Silver[random.randint(0, len(Silver) - 1)]
	elif tier == 'Legendary':
		NewWeapon = Legendary[random.randint(0, len(Legendary) - 1)]

	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeBows(tier):
	Broken = GetItems(BowBroken)
	Iron = GetItems(BowIron)
	Steel = GetItems(BowSteel)
	Silver = GetItems(BowSilver)
	Legendary = GetItems(BowLegendary)
	NewWeapon = ''

	if tier == 'Broken':
		NewWeapon = Broken[random.randint(0, len(Broken) - 1)]
	elif tier == 'Iron':
		NewWeapon = Iron[random.randint(0, len(Iron) - 1)]
	elif tier == 'Steel':
		NewWeapon = Steel[random.randint(0, len(Steel) - 1)]
	elif tier == 'Silver':
		NewWeapon = Silver[random.randint(0, len(Silver) - 1)]
	elif tier == 'Legendary':
		NewWeapon = Legendary[random.randint(0, len(Legendary) - 1)]

	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeBallistae(tier):

	Iron = GetItems(BallistaeIron)
	Steel = GetItems(BallistaeSteel)
	Silver = GetItems(BallistaeSilver)
	NewWeapon = ''

	if tier in ['Iron', 'Broken']:
		NewWeapon = Iron[random.randint(0, len(Iron) - 1)]
	elif tier == 'Steel':
		NewWeapon = Steel[random.randint(0, len(Steel) - 1)]
	elif tier in ['Silver', 'Legendary']:
		NewWeapon = Silver[random.randint(0, len(Silver) - 1)]

	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeMagic(tier, mode):

	Iron = GetItems(MagicIron)
	Steel = GetItems(MagicSteel)
	
	if mode == 'player':
		Silver = GetItems(MagicSilver)
		Legendary = GetItems(MagicLegendary)
	else:
		Silver = GetItems(MagicSilverEnemy)
		Legendary = GetItems(MagicLegendaryEnemy)

	NewWeapon = ''

	if tier in ['Iron', 'Broken']:
		NewWeapon = Iron[random.randint(0, len(Iron) - 1)]
	elif tier == 'Steel':
		NewWeapon = Steel[random.randint(0, len(Steel) - 1)]
	elif tier == 'Silver':
		NewWeapon = Silver[random.randint(0, len(Silver) - 1)]
	elif tier == 'Legendary':
		NewWeapon = Legendary[random.randint(0, len(Legendary) - 1)]

	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeStaves(tier):

	Iron = GetItems(StaveIron)
	Steel = GetItems(StaveSteel)
	Silver = GetItems(StaveSilver)
	Legendary = GetItems(StaveLegendary)
	NewWeapon = ''

	if tier in ['Iron', 'Broken']:
		NewWeapon = Iron[random.randint(0, len(Iron) - 1)]
	elif tier == 'Steel':
		NewWeapon = Steel[random.randint(0, len(Steel) - 1)]
	elif tier == 'Silver':
		NewWeapon = Silver[random.randint(0, len(Silver) - 1)]
	elif tier == 'Legendary':
		NewWeapon = Legendary[random.randint(0, len(Legendary) - 1)]

	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeStones():
	Stones = GetItems(StoneList)

	NewWeapon = Stones[random.randint(0, len(Stones) - 1)]
	NewWeapon = bytes([NewWeapon])
	return NewWeapon

def RandomizeBreaths():
	Breaths = GetItems(BreathList)

	NewWeapon = Breaths[random.randint(0, len(Breaths) - 1)]
	NewWeapon = bytes([NewWeapon])
	return NewWeapon