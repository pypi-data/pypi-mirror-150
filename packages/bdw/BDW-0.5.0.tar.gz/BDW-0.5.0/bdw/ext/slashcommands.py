from bdw.comm import *
from bdw.Guild import *
from bdw.Channel import *
from .Interaction import *
from bdw.Message import *

class ActionRow:
  '''
  This is used to hold components. Only requires one argument called, well, components.
  '''
  componentOBJ = {}
  def __init__(self, components):
    self.componentOBJ["type"] = 1
    self.componentOBJ["components"] = []
    for component in components:
      self.componentOBJ["components"].append(component.getOBJ())
  def getOBJ(self):
    return self.componentOBJ

class ButtonType:
  '''
  Contains all button types
  '''
  PRIMARY = 1
  SECONDARY = 2
  SUCCESS = 3
  DANGER = 4
  LINK = 5

class Button:
  '''
  This hold a button object, requires a name and either an id or url, there are also buttontype and enabled which are 1 and True by default.'''
  componentOBJ = {}
  def __init__(self, name, id="", buttontype=1, url="", enabled=True):
    self.componentOBJ["label"] = name
    self.componentOBJ["type"] = 2
    self.componentOBJ["style"] = buttontype
    self.componentOBJ["disabled"] = not enabled
    if not buttontype == ButtonType.LINK:
      self.componentOBJ["custom_id"] = id
    else:
      self.componentOBJ["url"] = url
  def disable(self):
    self.componentOBJ["disabled"] = True
  def enable(self):
    self.componentOBJ["enable"] = True
  def getOBJ(self):
    return self.componentOBJ

class Select:
	componentOBJ = {}
	def __init__(self, options, customID, placeholder="", disabled=False, min=1, max=1):
		self.options = options
		self.componentOBJ["type"] = 3
		self.componentOBJ["custom_id"] = customID
		self.componentOBJ["placeholder"] = placeholder
		self.componentOBJ["disabled"] = disabled
		self.componentOBJ["min_values"] = min
		self.componentOBJ["max_values"] = max
		self.componentOBJ["options"] = []
		for option in self.options:
			self.componentOBJ["options"].append(option.getOBJ())
	def getOBJ(self):
		return self.componentOBJ
	def add_option(self, op):
		self.componentOBJ["options"].append(op.getOBJ())

class SelectOption:
	componentOBJ = {}
	def __init__(self, label, value, desc="", default=False):
		self.componentOBJ["label"] = label
		self.componentOBJ["value"] = value
		self.componentOBJ["emoji"] = None
		self.componentOBJ["description"] = desc
		self.componentOBJ["default"] = False
	def getOBJ(self):
		return self.componentOBJ
class Slashcommand:
  '''
  This creates a slashcommand which requires a name, a description and the bot object. Options are not implemented yet.'''
  def __init__(self, name, description, bot):
    self.bot = bot
    self.SCOBJ = {"name": name,"description":description,"type":1,"options":[]}
  def register(self):
    self.appid = APIcall("/users/@me", "GET",self.bot.auth,{})["id"]
    APIcall(f"/applications/{self.appid}/commands","POST",self.bot.auth,self.SCOBJ)

def registerCommands(cmds, bot):
  '''
  This requires the commands and the bot object, it adds the not registered ones and deletes the removed ones.
  '''
  if len(cmds) == 0:
    return None
  appid = APIcall("/users/@me", "GET",cmds[0].bot.auth,{})["id"]
  alreadyExisting = []
  ASCOBJS = APIcall(f"/applications/{appid}/commands", "GET", cmds[0].bot.auth, {})
  for scobj in ASCOBJS:
    alreadyExisting.append(scobj['name'])
  for cmd in cmds:
    if not cmd.SCOBJ["name"] in alreadyExisting:
      cmd.register()
  ASCOBJS = APIcall(f"/applications/{appid}/commands", "GET", cmds[0].bot.auth, {})
  alreadyExisting = []
  for scobj in ASCOBJS:
    # alreadyExisting.append(scobj['name'])
    qaq = []
    for cmd in cmds:
      qaq.append(cmd.SCOBJ["name"])
    if not scobj['name'] in qaq:
      ASCOBJS = APIcall(f"/applications/{appid}/commands/{scobj['id']}", "DELETE", cmds[0].bot.auth, {})

class TextStyles:
	SHORT = 1
	PARAGRAPH = 2

class TextInput:
	componentOBJ = {}
	def __init__(self, ID, label, style=1, min=1, max=4000, required=True, value="", placeholder=""):
		self.componentOBJ["type"] = 4
		self.componentOBJ["label"] = label
		self.componentOBJ["custom_id"] = ID
		self.componentOBJ["style"] = style
		self.componentOBJ["min_length"] = min
		self.componentOBJ["max_length"] = max
		self.componentOBJ["required"] = required
		self.componentOBJ["value"] = value
		self.componentOBJ["placeholder"] = placeholder
	def getOBJ(self):
		return self.componentOBJ
class Modal:
	componentOBJ = {}
	def __init__(self, id, title, components):
		self.componentOBJ["custom_id"] = id
		self.componentOBJ["title"] = title
		self.componentOBJ["components"] = [ActionRow(components).getOBJ()]
	def addComponent(self, comp):
		self.componentOBJ["components"].append(comp.getOBJ())
	def getOBJ(self):
		print(self.componentOBJ)
		return self.componentOBJ