from tkinter import *
from tkinter import filedialog

class CreateLabel:
	def __init__(self, text, row, column, columnspan=1, rowspan=1, sticky=NW):
		self.label = LabelFrame(root, text= text)
		self.label.grid(row = row, column = column, stick = sticky, columnspan = columnspan, rowspan = rowspan)
		self.VarList = {}
		self.maxcolumn = 0
		self.maxrow = 0

	def check(self, varname):
		return self.VarList[varname].get()

	def checkbutton(self, text, varname, row, column, default=0, sticky=W):
		self.VarList[varname] = IntVar()
		self.VarList[varname].set(default)
		self.checkbuttonFunc = Checkbutton(self.label, text = text, variable = self.VarList[varname])
		self.checkbuttonFunc.grid(row = row, column = column, stick=sticky)

	def button(self, text, command, row, column, sticky=W):
		self.buttonFunc = Button(self.label, text = text, command = command)
		self.buttonFunc.grid(row = row, column = column, stick=sticky)

	def radiobutton(self, text, varname, row, column, sticky=W, default=0):
		self.VarList[varname] = IntVar()
		self.VarList[varname].set(default)
		x = 0
		y = row
		for name in text:
			self.radiobuttonFunc = Radiobutton(self.label, text = name, variable = self.VarList[varname], value = x)
			self.radiobuttonFunc.grid(row = y, column = column, stick=sticky)
			x += 1
			y += 1

	def entry(self, text, width, row, column, default=0, sticky=W):
		self.VarList[text] = IntVar()
		self.VarList[text].set(default)
		self.entryFunc = Entry(self.label, width = width, textvariable = self.VarList[text])
		self.entryFunc.grid(row = row, column = column, stick=sticky)

	def textlabel(self, text, row, column, sticky=W):
		self.labelFunc = Label(self.label, text = text)
		self.labelFunc.grid(row = row, column = column, stick=sticky)

class BasicWindow:
	def __init__(self, text):
		self.window = Toplevel(root)
		self.label = Label(self.window, text = text)
		self.button = Button(self.window, text = 'Ok', command = self.quit)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0)
		self.window.title('Randomizing...')
		self.window.iconbitmap(resource_path('xane.ico'))
	def quit(self):
		self.window.destroy()