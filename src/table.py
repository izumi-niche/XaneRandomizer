import sys
import random

def ByteToInt(number):
	return int.from_bytes(number, byteorder=sys.byteorder)

class rom:
	def __init__(self, location):
		self.rom = open(location, 'rb+')
		self.data = {}

	def read(self, location, number=1):
		if number == 1:
			self.rom.seek(location)
			temp = ByteToInt(self.rom.read(1))
		else:
			temp = []
			for x in range(number):
				self.rom.seek(location + x)
				temp.append(ByteToInt(self.rom.read(1)))
		return temp

	def write(self, location, number):
		if not number is list:
			if number is int: 
				number = bytes([number])
			self.rom.seek(location)
			self.rom.write(number)
		else:
			for x in range(len(number)):
				if number[x] is int:
					temp = bytes([number[x]])
				else: temp = number[x]
				self.rom.seek(location + x)
				self.rom.write(temp)

	def createtable(self, name, newdata):
		self.data[name] = {}
		for x in newdata:
			self.data[name][x] = newdata[x]
	
	def readtable(self, table, parameter, number, lenght=1):
		numbers = []
		for x in range(lenght):
			return self.read((self.data[table]['start'] +
			(self.data[table]['size'] * number) +
			self.data[table][parameter]))
		if len(numbers) == 1:
			numbers = int(numbers[0])
		return numbers

	def writetable(self, table, parameter, number, replace):
		self.write((self.data[table]['start'] +
			(self.data[table]['size'] * number) +
			self.data[table][parameter]), replace)

	def changelocation(self, table, number):
		self.data[table]['start'] = number
		return 'Changed ' + table + ' start position to ' + str(number)
