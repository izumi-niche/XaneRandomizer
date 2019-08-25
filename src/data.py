import xml.etree.ElementTree as ET
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def LoadXml(location):
	parser = ET.XMLParser(encoding="utf-8")
	tree = ET.parse(resource_path(location), parser=parser)
	return tree.getroot()
############################
########## Main
############################
def LoadData():
	data = {}
	data['name'] = data_names()
	data['portrait'] = data_portraits()
	data['class'] = data_class()
	data['item'] = data_item()
	data['character'] = data_characters()
	data['unit'] = data_units()
	data['tables'] = data_tables()
	return data
############################
## Names
def data_names():
	data = {}
	xml = LoadXml('data/names.xml')
	for name in xml.findall('names'):
		nameid = int(name.attrib['id'])
		data[nameid] = {}
		data[nameid]['name'] = name.find('name').text
	return data
############################
## Portraits
def data_portraits():
	data = {}
	xml = LoadXml('data/portraits.xml')
	for portrait in xml.findall('portrait'):
		portraitid = int(portrait.attrib['id'])
		data[portraitid] = {}
		data[portraitid]['name'] = portrait.find('name').text
		data[portraitid]['tags'] = []
		for x in ['generic', 'boss']:
			for y in portrait.findall(x):
				data[portraitid]['tags'].append(x)
	return data
#############################
#### Classes
def data_class():
	data = {}
	xml = LoadXml('data/class.xml')
	for job in xml.findall('class'):
		jobid = int(job.attrib['id'])
		data[jobid] = {}
		for x in ['name', 'tier', 'weapon', 'promotion']:
			data[jobid][x] = job.find(x).text
		data[jobid]['tags'] = []
		if not job.find('enemy') == None:
			data[jobid]['tags'].append('enemy')
		if not job.find('ignore') == None:
			data[jobid]['tags'].append('ignore')
	return data
#############################
#### Items
def data_item():
	data = {}
	xml = LoadXml('data/items.xml')
	for item in xml.findall('item'):
		itemid = int(item.attrib['id'])
		data[itemid] = {}
		data[itemid]['name'] = item.find('name').text
		for x in item.findall('weapon'):
			data[itemid]['tier'] = x.attrib['tier']
			try:
				data[itemid]['enemytier'] = x.attrib['enemytier']
			except:
				data[itemid]['enemytier'] = None
		data[itemid]['tags'] = []
		if not item.find('item') == None:
			data[itemid]['tags'].append('item')
			try:
				item.find('item').attrib['key']
				data[itemid]['tags'].append('key')
			except:
				'hi'

	return data
#############################
#### Characters
def data_characters():
	data = {}
	xml = LoadXml('data/characters.xml')
	for character in xml.findall('character'):
		data[int(character.attrib['id'])] = {}
		shortcut = data[int(character.attrib['id'])]
		shortcut['name'] = character.find('name').text
		shortcut['tags'] = []
		if not character.find('playable') == None:
			shortcut['tags'].append('playable')
			shortcut['book'] = int(character.find('book').text)
		if not character.find('child') == None:
			shortcut['child'] = character.find('book').text
	return data
#############################
##### Chapters
def data_units():
	data = {}
	xml = LoadXml('data/unitlocation.xml')
	for unit in xml.findall('unit'):
		data[int(unit.attrib['id'])] = {}
		shortcut = data[int(unit.attrib['id'])]
		if unit.find('type').text == 'table':
			shortcut['type'] = 'table'
			shortcut['start'] = int(unit.find('start').text)
			shortcut['size'] = int(unit.find('size').text)
			shortcut['endpoint'] = int(unit.find('endpoint').text)
		else:
			shortcut['type'] = 'reinforcement'
			shortcut['start'] = unit.find('start').text

	return data
############################
##### Tables
def data_tables():
	data = {}
	xml = LoadXml('data/table.xml')
	for table in xml.findall('table'):
		print(table.attrib['name'])
		data[table.attrib['name']] = {}
		shortcut = data[table.attrib['name']]
		shortcut['start'] = int(table.find('start').text)
		shortcut['size'] = int(table.find('size').text)
		for x in table.findall('data'):
			shortcut[x.attrib['name']] = int(x.attrib['id'])

	return data