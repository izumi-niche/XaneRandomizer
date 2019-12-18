import data.fe3.data.chapters as chapters
import data.fe3.data.characters as characters
import data.fe3.data.items as items
import data.fe3.data.job as job
import data.fe3.data.names as names
import data.fe3.data.portraits as portraits
import data.fe3.data.table as table
import data.fe3.data.units as units

############################
########## Main
############################
def LoadData():
	data = {}
	data['Name'] = names.data.copy()
	data['Portrait'] = portraits.data.copy()
	data['Class'] = job.data.copy()
	data['Item'] = items.data.copy()
	data['Character'] = characters.data.copy()
	data['Unit'] = units.data.copy()
	data['Tables'] = table.data.copy()
	data['Chapters'] = chapters.data.copy()
	return data