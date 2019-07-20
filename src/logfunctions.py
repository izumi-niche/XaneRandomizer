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