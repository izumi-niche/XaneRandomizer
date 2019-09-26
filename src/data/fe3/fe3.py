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
	location = 295424
	size = 47
	for s in range(size):
		fe3rom.rom.seek(location + (2 * s))
		print( fe3rom.getpointer(fe3rom.rom.read(2), location + (2 * s) ))

########################
# Give items
# Give a item to the specfied location.
########################
def give_item(location):
	fe3rom.changelocation('Unit', location)
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
# Full = Random number between 5 and 100.
##################################
def playable_growth(growth, mode):
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
					oldstat += random.randint(growth * -1, growth)
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
					oldstat = random.randint(5, 100)
					fe3rom.writetable('Character', stat, x, oldstat)
##################################
config['rom'] = 'Fire Emblem - Monshou no Nazo (J) (V1.1).smc'
config['baserange'] = 3
loadeverything()
newsearchunits()