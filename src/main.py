#import data.fe3.game
from common import *

# Next step: write the gui
import tkinter as tk
from gui import *

root = tk.Tk()

###############
### Playable
###############
LabelPlayable = CreateLabel('Playable Options', 1, 0, 1, 2, root = root)

LabelPlayable.checkbutton('Randomize classes', 'PlayerClass', 0, 0)

LabelPlayable.checkbutton('Ignore Julian and Rickard', 'IgnoreThief', 1, 0, 1)

LabelPlayable.checkbutton('Randomize bases', 'PlayerBases', 2, 0)

LabelPlayable.textlabel('Base Range:', 3 , 0)

LabelPlayable.entry('BasesRange', 5, 3, 0, 3, E)

LabelPlayable.checkbutton('Randomize growths', 'PlayerGrowths', 4, 0)

LabelPlayable.radiobutton(['Full Mode', 'Range Mode'], 'PlayerGrowthMode', 5, 0)

LabelPlayable.textlabel('Growths Range:', 7, 0)

LabelPlayable.entry('GrowthRange', 5, 7, 0, 30, E)
###############
### Support
###############
LabelSupport = CreateLabel('Support Options', 3, 0, root = root)

LabelSupport.checkbutton('Randomize Supports', 'Support', 1, 0)

LabelSupport.textlabel('Minimum characters supported', 2, 0)
LabelSupport.textlabel('by one character:', 3, 0)

LabelSupport.entry('SupportMinCount', 5, 3, 0, 0, E)

LabelSupport.textlabel('Maximum characters supported', 4, 0)
LabelSupport.textlabel('by one character:', 5, 0)

LabelSupport.entry('SupportMaxCount', 5, 5, 0, 3, E)

LabelSupport.textlabel('Minimum bonus:', 6, 0)

LabelSupport.entry('SupportMinBonus', 5, 6, 0, 5, E)

LabelSupport.textlabel('Maximum bonus', 7, 0)

LabelSupport.entry('SupportMaxBonus', 5, 7, 0, 20, E)
##################
#### Global Enemy
##################

LabelEnemy = CreateLabel('Global Enemies', 1, 1, 2, root = root)

LabelEnemy.checkbutton('Increase enemy bases', 'EnemyBase', 0, 0)

LabelEnemy.checkbutton('Increase enemy growths', 'EnemyGrowth', 0, 1)

LabelEnemy.entry('EnemyBaseIncrease', 5, 1, 0, 3, E)
LabelEnemy.textlabel('Increase bases by:', 1, 0)

LabelEnemy.entry('EnemyGrowthIncrease', 5, 1, 1, 15, E)
LabelEnemy.textlabel('Increase growths by:', 1, 1)

################
### Bosses
################
LabelBoss = CreateLabel('Boss options', 2, 2, root = root)
LabelBoss.checkbutton('Randomize classes', 'BossClass', 0, 0)

LabelBoss.checkbutton('Increase level', 'BossLevel', 1, 0)

LabelBoss.entry('BossLevelIncrease', 5, 2, 0, 3, E)

LabelBoss.textlabel('Increase by:', 2, 0)

LabelBoss.checkbutton('Randomize items', 'BossItem', 3, 0)

LabelBoss.textlabel('Item chance:', 4, 0)
LabelBoss.entry('ItemChance', 5, 4, 0, 20, E)
#################
### Generics
#################
LabelGeneric = CreateLabel('Generic options', 2, 1, root = root)
LabelGeneric.checkbutton('Randomize classes', 'GenericClass', 0, 0)

LabelGeneric.checkbutton('Ignore thiefs with sphere/orbs', 'ThiefShard', 1, 0)

LabelGeneric.checkbutton('Increase level', 'GenericLevel', 2, 0)

LabelGeneric.entry('GenericLevelIncrease', 5, 3, 0, 4, E)

LabelGeneric.textlabel('Increase by:', 3, 0)

LabelGeneric.checkbutton('Randomize items', 'GenericItem', 4, 0)
LabelGeneric.textlabel('Item chance:', 5, 0)
LabelGeneric.entry('ItemChance', 5, 5, 0, 20, E)
###############
#### Other options
###############
LabelOther = CreateLabel('Other options', 1, 3, 1, 2, root = root)
LabelOther.checkbutton('Randomize Astral Shard bonuses', 'AstralShard', 0, 0)
LabelOther.radiobutton(['Full Mode', '\'Balanced\' Mode'], 'AstralShardMode', 1, 0)

LabelOther.checkbutton('Remove weapon lock restrictions', 'WeaponLock', 3, 0)
LabelOther.checkbutton('Remove Rapier Lock', 'RapierLock', 4, 0)

LabelOther.checkbutton('Randomize weapons', 'RandomWeapon', 5, 0)

LabelOther.checkbutton('0% growths', '0growths', 6, 0)

LabelOther.checkbutton('Randomize shops', 'Shop', 7, 0)

# They need to be down here since the functions are after the gui stuff
RomLocation = StringVar()
LogVar = IntVar()

buttonOpenFile = Button(root, text='Select FE3 rom...', width=50)
buttonOpenFile.grid(row = 0, column = 1, columnspan = 4)

checkmarkCreateLog = Checkbutton(root, text = 'Create Log', variable = LogVar)
checkmarkCreateLog.grid(row = 0, column = 0, stick=E)

labelReadme = Label(root, text = 'For more information on the options or a fix to possible user errors, please read the Readme.')
labelReadme.grid(row = 4, columnspan = 4, column = 0, sticky=N)

buttonRandomize = Button(root, text='Randomize!', width = 50)
buttonRandomize.grid(row = 5, columnspan = 4, column = 0, sticky=N)

root.title('Xane Randomizer: A FE3 Randomizer')
root.iconbitmap(resource_path('xane.ico'))
root.mainloop()