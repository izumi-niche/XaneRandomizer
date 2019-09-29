import xml.etree.ElementTree as ET
import os
from common import *

############################
########## Main
############################
def LoadData():
	data = {}
	data['Name'] = data_names()
	data['Portrait'] = data_portraits()
	data['Class'] = data_class()
	data['Item'] = data_item()
	data['Character'] = data_characters()
	data['Unit'] = data_units()
	data['Tables'] = data_tables()
	data['Chapters'] = data_chapters()
	return data
############################
## Names
def data_names():
	data = {}
	xml = LoadXml('data/fe3/xml/names.xml')
	for name in xml.findall('names'):
		nameid = int(name.attrib['id'])
		data[nameid] = {}
		data[nameid]['name'] = name.find('name').text
	return data
############################
## Portraits
def data_portraits():
	data = {}
	xml = LoadXml('data/fe3/xml/portraits.xml')
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
	xml = LoadXml('data/fe3/xml/class.xml')
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
	xml = LoadXml('data/fe3/xml/items.xml')
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

		for x in ['dragonstone', 'shop']:
			if not item.find(x) == None:
				data[itemid]['tags'].append(x)

	return data
#############################
#### Characters
def data_characters():
	data = {}
	xml = LoadXml('data/fe3/xml/characters.xml')
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
	xml = LoadXml('data/fe3/xml/unitlocation.xml')
	for unit in xml.findall('unit'):
		data[unit.attrib['id']] = {}
		shortcut = data[unit.attrib['id']]
		if unit.find('type').text == 'pointer':
			shortcut['type'] = 'pointer'
			shortcut['start'] = int(unit.find('start').text)
			shortcut['size'] = int(unit.find('size').text)
		else:
			shortcut['type'] = 'table'
			shortcut['start'] = unit.find('start').text

	return data
############################
##### Tables
def data_tables():
	data = {}
	xml = LoadXml('data/fe3/xml/table.xml')
	for table in xml.findall('table'):
		data[table.attrib['name']] = {}
		shortcut = data[table.attrib['name']]
		shortcut['start'] = int(table.find('start').text)
		shortcut['size'] = int(table.find('size').text)
		for x in table.findall('data'):
			shortcut[x.attrib['name']] = int(x.attrib['id'])

	return data

############################
##### Chapters
def data_chapters():
	data = {}
	xml = LoadXml('data/fe3/xml/chapters.xml')
	for chapter in xml.findall('chapter'):
		data[chapter.attrib['id']] = {}
		shortcut = data[chapter.attrib['id']]
		shortcut['name'] = chapter.find('name').text

	return data