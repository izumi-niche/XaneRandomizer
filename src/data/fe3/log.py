from data.fe3.fe3 import *
import xml.etree.ElementTree as ET
from table import *
from common import *

script = """
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}
"""

html = False
head = False
body = False
units = False
index = False
fe3rom = False
globaldata = False

# Start the log
def startlog(location, search, rom, data):
	global html, units, index, fe3rom, globaldata, body, head

	globaldata = data
	fe3rom = rom
	html = ET.Element('html')
	head = ET.SubElement(html, 'head')
	ET.SubElement(head, 'style').text = script

	body = ET.SubElement(html, 'body')
	units = search
	index = ET.SubElement(body, 'index')
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
			fe3rom.changelocation('Unit', unit)
			data[x][unit] = {}
			current = data[x][unit]
			for y in ['Name', 'Class', 'Level', 'Character', 'Weapon1', 'Weapon2', 'Weapon3', 'Weapon4', 'Item1', 'Item2']:
				current[y] = fe3rom.readtable('Unit', y)

	# Get the stats.
	# 1. Get character bases: Strength, Skill, Speed, Defense, Resistance, HP*, Luck*, WpnLvl*
	# * If character stat is 255 (0xFF), set to be '-', if not just use Character Base. If HP, set to 0.
	# 2. Get the class bases: Strength, Skill, Speed, Defense, Resistance and HP
	# 3. Get the class growths: Same as above ^
	# Stat calc = Character Base + Class Base + ( (Level - 1) * (100 / Class Growth) )
	# For Luck and WpnLvl = Character Base
	unitdata = {}
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

			#debug(current, unit['Class'])
			#debug('Bases:', bases)
			#debug('Growths:', classgrowths)
			#debug('ClassBases:', classbases)

			# Calc for the other stats
			# Character Base + Class Base + ( (Level - 1) * (100 / Class Growth) )
			for y in ['Strength', 'Skill', 'Speed', 'Defense', 'Resistance', 'HP']:
				total[y] = bases[y] + classbases[y] + ((unit['Level'] - 1) * (100 / classgrowths[y]))

			unit['total'] = total
			unitdata[current] = unit.copy()


	# Organize units by chapter
	ET.SubElement(body, 'h2').text = 'Enemy Data'
	
	# Create index title and description
	ET.SubElement(index, 'h2').text = 'Enemy Data'
	ET.SubElement(index, 'p').text = 'Click below to check Bosses/Enemies for each chapter.'

	# Create index table
	indextable = ET.SubElement(index, 'table', style='width:50%')
	indextr = ET.SubElement(indextable, 'tr')
	count = -1

	for x in chapters:
		if x == 'reinforcement': chaptername = 'Reinforcements'
		else: chaptername = globaldata['Chapters'][str(x)]['name']

		# add title
		ET.SubElement(ET.SubElement(body, 'h3'), 'a', name=chaptername.replace(' ', '_')).text = chaptername

		# add to the index
		if count >= 5:
			count = 0
			indextr = ET.SubElement(indextable, 'tr')
			ET.SubElement(ET.SubElement(indextr, 'td'), 'a', href='#' + chaptername.replace(' ', '_')).text = chaptername
		else:
			ET.SubElement(ET.SubElement(indextr, 'td'), 'a', href='#' + chaptername.replace(' ', '_')).text = chaptername
			count += 1

		# create table for the units
		table = ET.SubElement(body, 'table', style='width:50%')
		tr = ET.SubElement(table, 'tr')

		# create the first row
		for y in ['Level', 'Name', 'Class', 'Weapon', 'Weapon', 'Item', 'Item']:
			ET.SubElement(tr, 'th').text = y

		# for each unit in the chapter
		for y in chapters[x]:
			tr = ET.SubElement(table, 'tr')
			# skip if it is playable character
			if 'playable' in globaldata['Character'][unitdata[y]['Character']]['tags']:
				continue

			unit = unitdata[y]
			# Level
			ET.SubElement(tr, 'td', style='text-align:center').text = str(unit['Level'])
			# Name
			ET.SubElement(tr, 'td', style='text-align:center').text = globaldata['Name'][unit['Name']]['name']
			# Class
			ET.SubElement(tr, 'td', style='text-align:center').text = globaldata['Class'][unit['Class']]['name']

			unit = unitdata[y]
			for z in ['Weapon1', 'Weapon2', 'Item1', 'Item2']:
				if unit[z] == 255:
					itemname = '-'
				else:
					itemname = globaldata['Item'][unit[z]]['name']
				ET.SubElement(tr, 'td', style='text-align:center').text = itemname

def writelog():
	tree = ET.ElementTree(html)
	tree.write(location)