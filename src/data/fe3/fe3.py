from data.fe3.content import *
from table import *
from common import *
import random
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
##################################
# Load everything important, and set up the tables.
##################################
def loadeverything():
	global globaldata
	global fe3rom
	debug('Loading globaldata...')
	globaldata = LoadData()
	debug('Loading ROM...')
	fe3rom = rom(config['rom'])
	debug('Loading tables...')
	for x in globaldata['Tables']:
		fe3rom.createtable(x, globaldata['Tables'][x])
##################################
# Obligatory things to change before any randomizing process.
# 1. Give the Lord class a exp of 32.
# 2. Remove the transformation event for B1!Tiki/Morzas/Xemcel/Khozel.
##################################
##################################
# Find units.
# globaldata must be set up fist.
##################################
def searchunits():
	debug('Searching for units...')
	data = {}
	for x in globaldata['Unit']:
		unit = globaldata['Unit'][x]
		if unit['type'] == 'table':
			start = unit['start']
			end = unit['endpoint']
			while True:
				if fe3rom.read(start) == 255:
					if start >= end:
						break
					else:
						start += 1
						continue
				y = 0
				while True:
					fe3rom.changelocation('Unit', start)
					character = fe3rom.readtable('Unit', 'Character', y)
					if not character == 255:
						name = fe3rom.tablelocation('Unit', 'Character', y)
						data[name] = {}
						for stat in ['Character', 'Class', 'Level', 'Name', 'X', 'Y', 'Portrait', 
						'Weapon1', 'Weapon2', 'Weapon3', 'Weapon4', 'Item1', 'Item2', 'Ai1', 'Ai2', 'Ai3']:
							data[name][stat] = fe3rom.readtable('Unit', stat, y)
						data[name]['Reinforcement'] = False
						y += 1
					else:
						start = start + (y * 19)
						y = 0
						break
		if unit['type'] == 'reinforcement':
			start = unit['start']
			y = 0
			while True:
				if fe3rom.readtable('Unit','Character', y) == 255:
					break
				name = fe3rom.tablelocation('Unit', 'Character', y)
				data[name] = {}
				for stat in ['Character', 'Class', 'Level', 'Name', 'X', 'Y', 'Portrait', 
				'Weapon1', 'Weapon2', 'Weapon3', 'Weapon4', 'Item1', 'Item2', 'Ai1', 'Ai2', 'Ai3']:
					data[name][stat] = fe3rom.readtable('Unit', stat, y)
				data[name]['Reinforcement'] = True
				y += 1

	return data

######################################################
###################### Playable ######################
######################################################
##################################
# Randomize bases
# The bases will be changed on number, if the number is 3, the range will be added a number from -3 to 3.
##################################
def playable_bases(base):
	debug('Randomizing bases...')
	for x in globaldata['Character']:
		if 'playable' in globaldata['Character'][x]['tags']:
			debug('Randomizing bases of character ', x)
			for stat in ['BaseStrength', 'BaseSkill', 'BaseSpeed', 'BaseLuck', 'BaseDefense', 'BaseResistance',
			'BaseHP', 'BaseWpnLvl']:
				oldstat = fe3rom.readtable('Character', stat, x)
				oldstat += random.randint(base * -1, base)
				if oldstat < 0:
					oldstat = 0
				fe3rom.writetable('Character', stat, x, oldstat)
##################################
# Randomize growths
# Two modes:
# Range = Random number between -x and x, then add to the growth.
# Full = Random number between 5 and 100.
##################################
def playable_growth(growth, mode):
	find = ['GrowthStrength', 'GrowthSkill', 'GrowthSpeed', 'GrowthLuck', 'GrowthDefense',
			'GrowthResistance', 'GrowthHP', 'GrowthWpnLvl']
	# Range
	if mode == 1:
		for x in globaldata['Character']:
			if 'playable' in globaldata['Character'][x]['tags']:
				for stat in find:
					oldstat = fe3rom.readtable('Character', stat, x)
					oldstat += random.randint(growth * -1, growth)
					if oldstat < 0:
						oldstat = 0
					fe3rom.writetable('Character', stat, x, oldstat)
	elif mode == 2:
		for x in globaldata['Character']:
			if 'playable' in globaldata['Character'][x]['tags']:
				for stat in find:
					oldstat = fe3rom.readtable('Character', stat, x)
					oldstat = random.randint(5, 100)
					fe3rom.writetable('Character', stat, x, oldstat)
##################################
if __name__ == "__main__":
	config['rom'] = 'Fire Emblem - Monshou no Nazo (J) (V1.1).smc'
	config['baserange'] = 3
	loadeverything()
	print(searchunits())