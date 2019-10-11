from data.fe3.content import *
from table import *
from common import *
import random
import data.fe3.log as log
##################################
# Set up global variables for data and rom.
##################################
globaldata = ''
fe3rom = ''
config = {}
##################################
# Functions to other modules change variables
##################################
def load_rom(location):
	debug('Rom location set to: ', location)
	config['rom'] = location

def load_config(stuff):
	debug('Loading FE3 config...')
	for x in stuff:
		config[x] = stuff[x]
##################################
# Load everything important, and set up the tables.
##################################
def loadeverything():
	global globaldata
	global fe3rom
	debug('Loading globaldata...')
	globaldata = LoadData()
	debug('Loading ROM...')
	fe3rom = sfcrom(config['rom'])
	debug('Loading tables...')
	for x in globaldata['Tables']:
		fe3rom.createtable(x, globaldata['Tables'][x])
##################################
# Obligatory things to change before any randomizing process.
# 1. Give the Lord class a exp of 32.
# 2. Remove the transformation event for B1!Tiki/Morzas/Xemcel/Khozel.
##################################
def obligatory():
	# Lord exp
	fe3rom.writetable('ClassBase', 'Experience', 0)
##################################
# Find units.
# globaldata must be set up fist.
##################################
def searchunits():
	data = {}
	for x in globaldata['Unit']:
		units = globaldata['Unit'][x]
		start = units['start']
		if units['type'] == 'pointer':
			for size in range(units['size']):
				position = start + (2 * size)
				fe3rom.rom.seek(position)
				location = fe3rom.getpointer(fe3rom.rom.read(2), position)
				fe3rom.changelocation('Unit', location)
				y = 0
				while True:
					if not fe3rom.readtable('Unit', 'Character', y) == 255:
						data[fe3rom.tablelocation('Unit', 'Character', y)] = {}
						unit = data[fe3rom.tablelocation('Unit', 'Character', y)]
						for z in globaldata['Tables']['Unit']:
							if z == 'start' or z == 'size':
								continue
							unit[z] = fe3rom.readtable('Unit', z, y)

						unit['type'] = x
						unit['chapter'] = size
						y += 1
					else:
						break

		elif units['type'] == 'table':
			start = units['start']
			fe3rom.changelocation('Unit', int(start))
			y = 0
			while True:
				if not fe3rom.readtable('Unit', 'Character', y) == 255:
					data[fe3rom.tablelocation('Unit', 'Character', y)] = {}
					unit = data[fe3rom.tablelocation('Unit', 'Character', y)]
					for z in globaldata['Tables']['Unit']:
						if z == 'start' or z == 'size':
							continue
						unit[z] = fe3rom.readtable('Unit', z, y)

					unit['type'] = x
					y += 1
				else:
					break


	return data

########################
# Give items
# Give a item to the specfied location.
# 1. Get unit items
# 2. Get weapon wpnlvl/tier
# 3. Get weapon tier
# 3. Get character wpnlvl and class
# 4. See if the class can use any class locked weapons in the tier
# 4a. See if the class can use Mage/Staff or Lance/Sword, then split the weapon distribution
# 5. Search for a weapon that the character can use with their wpnlvl
# 6a. If not found, try using a lower tier.
# 7. If it is a player, move staves and dragonstones to the item slot.
# 8. If character class is a Cavalier/Paladin/Wyvern/Pegasus and is not gave a sword, give it a iron sword.
########################
def give_item(location, chapter, playable=True):
	# set table location to the unit
	fe3rom.changelocation('Unit', location)

	# get items/weapons
	unit_items = []
	for x in ['Weapon1', 'Weapon2', 'Weapon3', 'Weapon4', 'Item1', 'Item2']:
		temp = fe3rom.readtable('Unit', x)
		print(temp)
		if temp == 255:
			continue
		unit_items.append([temp])

	# get item wpnlvl and tier
	# if unit is playable get wpnlvl and tier normally
	itemlist = globaldata['Item']
	for x in unit_items:
		item = x[0]
		# check if it is a weapon first
		# if not, skip
		if not 'weapon' in itemlist[item]:
			x.append('Item')
			continue
		
		if playable:
			x.append(fe3rom.readtable('Item', ))

	# get unit wpnlvl and class
	# if it is enemy, set wpnlvl to 255
	if playable:
		unit_wpnlvl = fe3rom.readtable('Character', 'BaseWpnLvl', fe3rom.readtable('Unit', 'Character'))
	else:
		unit_wpnlvl = 255
	unit_class = fe3rom.readtable('Unit', 'Class')
######################################################
###################### Playable ######################
######################################################
##################################
# Randomize bases
# The bases will be changed on number, if the number is 3, the range will be added a number from -3 to 3.
##################################
def playable_bases(base):
	debug('Randomizing bases...')

	find = ['GrowthStrength', 'GrowthSkill', 'GrowthSpeed', 'GrowthLuck', 'GrowthDefense',
			'GrowthResistance', 'GrowthHP', 'GrowthWpnLvl']

	for x in globaldata['Character']:
		if 'playable' in globaldata['Character'][x]['tags']:
			debug('Randomizing bases of character', x)
			for stat in find:
				oldstat = fe3rom.readtable('Character', stat, x)
				oldstat += random.randint(base * -1, base)
				if oldstat < 0:
					oldstat = 0
				fe3rom.writetable('Character', stat, x, oldstat)
##################################
# Randomize growths
# Two modes:
# Range = Random number between -x and x, then add to the growth.
# Full = Random number between X and X.
##################################
def playable_growth(range_growth, min_full, max_full, mode):
	debug('Randomizing growths...')
	find = ['GrowthStrength', 'GrowthSkill', 'GrowthSpeed', 'GrowthLuck', 'GrowthDefense',
			'GrowthResistance', 'GrowthHP', 'GrowthWpnLvl']
	# Range
	if mode == 1:
		debug('Growth mode: Range')
		for x in globaldata['Character']:
			if 'playable' in globaldata['Character'][x]['tags']:
				debug('Randomizing growths for character', x)

				for stat in find:
					oldstat = fe3rom.readtable('Character', stat, x)
					oldstat += random.randint(range_growth * -1, range_growth)
					if oldstat < 0:
						oldstat = 0
					fe3rom.writetable('Character', stat, x, oldstat)
	# Full
	elif mode == 2:
		debug('Growth mode: Full')
		for x in globaldata['Character']:
			if 'playable' in globaldata['Character'][x]['tags']:
				debug('Randomizing growths for character', x)

				for stat in find:
					oldstat = fe3rom.readtable('Character', stat, x)
					oldstat = random.randint(min_full, max_full)
					fe3rom.writetable('Character', stat, x, oldstat)
	# Redistribution
	elif mode == 3:
		debug('Growth mode: Redistribution')
##################################
config['rom'] = 'Fire_Emblem_-_Monshou_no_Nazo_J_V1.1.smc'
config['baserange'] = 3
config['log'] = 'dummy.xml'
loadeverything()
log.startlog('dummy.xml', searchunits(), fe3rom, globaldata)
log.enemyunits()
log.writelog()