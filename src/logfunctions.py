# A different file for storing the functions for creating log files.
from lists.playable import *
from data.names import *
from basicfunctions import *

def CreateLogFile(changelog):
	changelog = open(changelog, 'a')
	DummyString = """
<!DOCTYPE html>
<html>
<head>
	<title> FE3 Changelog </title>
</head>
<body>
"""
	changelog.write(DummyString)

def EndLogFile(changelog):
	changelog = open(changelog, 'a')
	DummyString = """
</body>
</html>
"""
	changelog.write(DummyString)
#######################
####### Support #######
#######################
def CreateSupportLog(changelog, fe3rom):
	changelog = open(changelog, 'a')
	fe3rom = open(fe3rom, 'rb')
	CharacterDict = ReverseDict(NameDict)
	SupportDec = 282417
	i = 0
	SupportDict = {}
	while True:
		fe3rom.seek(SupportDec + SupportCalc(i))
		HexRead = fe3rom.read(1)
		HexRead = ByteToInt(HexRead)
		if HexRead == 255:
			break
		else:
			SupportDict[i] = []
			SupportDict[i].append(CharacterDict[HexRead])
			fe3rom.seek(SupportDec + SupportCalc(i) + 1)
			HexRead = fe3rom.read(1)
			HexRead = ByteToInt(HexRead)
			SupportDict[i].append(CharacterDict[HexRead])
			fe3rom.seek(SupportDec + SupportCalc(i) + 2)
			HexRead = fe3rom.read(1)
			HexRead = ByteToInt(HexRead)
			SupportDict[i].append(str(HexRead))
			i += 1
	DummyString = """
<h2> Supports </h2>

<table style="width:100%">
	<tr>
		<th>Supporter</th>
		<th>Supported</th> 
		<th>Hit/Avoid/Crit Bonus</th>
	</tr>
"""
	changelog.write(DummyString)
	for i in SupportDict:
		DummyString = """
	<tr>
		<td>{}</td>
		<td>{}</td>
		<td>{}</td>
	</tr>
"""
		DummyString = DummyString.format(SupportDict[i][0], SupportDict[i][1], SupportDict[i][2])
		changelog.write(DummyString)
	DummyString = """
</table>

"""
	changelog.write(DummyString)

########################
##### Playable Units ###
########################
FindStatsCharacter = {
	'basestrength': 0,
	'baseskill': 1,
	'basespeed': 2,
	'baseluck': 3,
	'basedefense': 4,
	'baseresistance': 5,
	'basehp': 6,
	'baseweaponlvl': 7,
	'growthstrenght': 9,
	'growthskill': 10,
	'growthspeed': 11,
	'growthluck': 12,
	'growthdefense': 13,
	'growthresistance': 14,
	'growthhp': 15,
	'growthweaponlvl': 16
}
FindStatsClass = {
	'basestrength': 0,
	'baseskill': 1,
	'basespeed': 2,
	'basedefense': 4,
	'baseresistance': 5
}
def CreatePlayableLog(changelog, fe3rom, unitlist):
	changelog = open(changelog, 'a')
	fe3rom = open(fe3rom, 'rb')
	UnitData = {}
	PlayableCharacters = GetCharacter(PlayableUnits)
	CharacterList = ReverseDict(CharacterDataList)
	ItemList = ReverseDict(items)
	ClassesList = ReverseDict(ClassList)
	CharacterStats = {}
	# Get data for character, class, weapons and items.
	for unit in unitlist:
		if unitlist[unit]['character'] in PlayableCharacters:
			if not unitlist[unit]['character'] in UnitData:
				NewUnit = unitlist[unit]['character']
				UnitData[NewUnit] = {}
				UnitData[NewUnit]['character'] = CharacterList[unitlist[unit]['character']]
				if '2' in UnitData[NewUnit]['character']:
					NewName = UnitData[NewUnit]['character']
					NewName = NewName.replace('2', ' (Book 2)')
					UnitData[NewUnit]['character'] = NewName
				UnitData[NewUnit]['class'] = ClassesList[unitlist[unit]['class']]
				UnitData[NewUnit]['level'] = unitlist[unit]['level']
				for x in ['weapon1', 'weapon2', 'weapon3', 'weapon4', 'item1', 'item2']:
					UnitData[NewUnit][x] = ItemList[unitlist[unit][x]]
				for x in FindStatsCharacter:
					fe3rom.seek(CharacterDec + UnitDataCalc(NewUnit) + FindStatsCharacter[x])
					HexRead = ByteToInt(fe3rom.read(1))
					UnitData[NewUnit][x] = HexRead
				for x in FindStatsClass:
					fe3rom.seek(ClassBasesDec + ClassDataBaseCalc(unitlist[unit]['class']) + FindStatsClass[x])
					HexRead = ByteToInt(fe3rom.read(1))
					UnitData[NewUnit][x] += HexRead
				print(UnitData[NewUnit])
	# Write in the changelog
	DummyString = """
	<h2> Playable Units </h2>
	"""
	changelog.write(DummyString)
	for unit in UnitData:
		NewName =  UnitData[unit]['character']
		if 'E' in NewName[-1:]:
			continue
		DummyString = """
<h3> {} </h3>
<h4> Bases/Growths </h4>
"""
		DummyString = DummyString.format(NewName)
		changelog.write(DummyString)
		DummyString = """
<table style="width:50%">
	<tr>
		<th> Type </th>
		<th> HP </th>
		<th> Str/Mag </th>
		<th> Skill </th>
		<th> Speed </th>
		<th> Luck </th>
		<th> WpnLv </th>
		<th> Defense </th>
		<th> Resistance </th>
	</tr>
	<tr>
		<th> Bases </th>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
	</tr>
"""
		DummyString = DummyString.format(UnitData[unit]['basehp'], UnitData[unit]['basestrength'], UnitData[unit]['baseskill'], UnitData[unit]['basespeed'], UnitData[unit]['baseluck'], UnitData[unit]['baseweaponlvl'], UnitData[unit]['basedefense'], UnitData[unit]['baseresistance'])
		changelog.write(DummyString)
		DummyString = """
<tr>
		<th> Growths </th>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
	</tr>
</table>
"""
		DummyString = DummyString.format(UnitData[unit]['growthhp'], UnitData[unit]['growthstrenght'], UnitData[unit]['growthskill'], UnitData[unit]['growthspeed'], UnitData[unit]['growthluck'], UnitData[unit]['growthweaponlvl'], UnitData[unit]['growthdefense'], UnitData[unit]['growthresistance'])
		changelog.write(DummyString)
		DummyString = """
<table style="width:50%">
<h4> Class and items </h4>
	<tr>
		<th> Class </th>
		<th> Level </th>
		<th> Weapon </th>
		<th> Weapon </th>
		<th> Weapon </th>
		<th> Weapon </th>
		<th> Item </th>
		<th> Item </th>
	</tr>
	<tr>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
		<td style="text-align:center"> {} </td>
	</tr>
</table>
"""
		DummyString = DummyString.format(UnitData[unit]['class'], UnitData[unit]['level'], UnitData[unit]['weapon1'], UnitData[unit]['weapon2'], UnitData[unit]['weapon3'], UnitData[unit]['weapon4'], UnitData[unit]['item1'], UnitData[unit]['item2'])
		changelog.write(DummyString)