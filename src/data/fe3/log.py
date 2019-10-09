from data.fe3.fe3 import *
import xml.etree.ElementTree as ET
from table import *
from common import *

html = ''
units = ''
index = ''
fe3rom = ''

class createindex:
	def __init__(self):
		self.index = ET.SubElement(html, 'index')

	def addtable(self, tablename, contents):
		self.newtable = ET.SubElement(self.index, tablename.replace(' ', '_'))
		ET.SubElement(self.newtable, 'h2').text = tablename
		self.tr = ET.SubElement(self.newtable, 'tr')
		for x in contents:
			self.th = ET.SubElement(self.tr, 'th')
			ET.SubElement(self.th, 'a', href='#' + x.replace(' ', '_')).text = x

def startlog(location, search, rom):
	global html
	global units
	global index
	global fe3rom
	fe3rom = rom
	html = ET.Element('html')
	units = search
	index = createindex()
##################
# Create log for enemy units in each chapter.
# TODO: For some reason it is getting the wrong class ID.
# TODO: Fix above and actually finish the thing
def enemyunits():
	chapters = {}
	data = {}
	chapters['reinforcement'] = []
	for x in units:
		unit = units[x]
		if 'chapter' in unit:
			if not unit['chapter'] in chapters:
				chapters[unit['chapter']] = []
				chapters[unit['chapter']].append(x)
			else:
				chapters[unit['chapter']].append(x)
		else:
			chapters['reinforcement'].append(x)

	# Get class, name, character, weapons and items for the unit
	for x in chapters:
		data[x] = {}
		for unit in chapters[x]:
			data[x][unit] = {}
			current = data[x][unit]
			fe3rom.changelocation('Unit', unit)
			for y in ['Name', 'Class', 'Level', 'Character', 'Weapon1', 'Weapon2', 'Weapon3', 'Weapon4', 'Item1', 'Item2']:
				current[y] = fe3rom.readtable('Unit', y)

	# Get the stats.
	# 1. Get character bases: Strength, Skill, Speed, Defense, Resistance, HP*, Luck*, WpnLvl*
	# * If character stat is 255 (0xFF), set to be '-', if not just use Character Base. If HP, set to 0.
	# 2. Get the class bases: Strength, Skill, Speed, Defense, Resistance and HP
	# 3. Get the class growths: Same as above ^
	# Stat calc = Character Base + Class Base + ( (Level - 1) * (100 / Class Growth) )
	# For Luck and WpnLvl = Character Base
	for x in data:
		for current in data[x]:
			unit = data[x][current]

			# Character Bases
			bases = {}
			for y in ['BaseStrength', 'BaseSkill', 'BaseSpeed', 'BaseLuck', 'BaseDefense', 'BaseResistance', 'BaseHP', 'BaseWpnLvl']:
				bases[y.replace('Base', '')] = fe3rom.readtable('Character', y, unit['Character'])

			# Class Bases
			classbases = {}
			for y in ['Strength', 'Skill', 'Speed', 'Defense', 'Resistance', 'HP']:
				classbases[y] = fe3rom.readtable('ClassBase', y, unit['Class'])

			# Class Growths
			classgrowths = {}
			for y in ['Strength', 'Skill', 'Speed', 'Defense', 'Resistance', 'HP']:
				classgrowths[y] = fe3rom.readtable('ClassGrowth', y, unit['Class'])
				if classgrowths[y] == 0:
					classgrowths[y] = 1

			# Get the total stats
			total = {}
			# Luck/WpnLvl check for bases
			for y in ['Luck', 'WpnLvl']:
				if bases[y] == 255:
					total[y] = '-'
				else:
					total[y] = bases[y]
			# HP check, if 255 set to 0:
			if bases['HP'] == 255:
				bases['HP'] = 0
			print(current, unit['Class'])
			print('Bases:', bases)
			print('Growths:', classgrowths)
			print('ClassBases:', classbases)
			# Calc for the other stats
			# Character Base + Class Base + ( (Level - 1) * (100 / Class Growth) )
			for y in ['Strength', 'Skill', 'Speed', 'Defense', 'Resistance', 'HP']:
				total[y] = bases[y] + classbases[y] + ((unit['Level'] - 1) * (100 / classgrowths[y]))

			print(total)