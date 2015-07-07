from tools import *

def saySomething(stuff):
	'''
	event server
	'''
	#say("---------------------------------------------------------------------------------------")
	
	try:
		FreeCAD.PluginManager
	except:
		sayexc()
	if stuff =="hallo  Eventserver ...":
		# say(stuff + " started")
		return
	if stuff.__class__ == str or stuff.__class__ == unicode:
		try:
			say("key:"+stuff)
			if stuff =='\r':
				return
			say(str(FreeCAD.PluginManager.pluginloader.config3['keys']['global'][str(stuff)]))
			d={}
			
			exec(FreeCAD.PluginManager.pluginloader.config3['keys']['global'][str(stuff)]['exec'])
		except:
			sayexc("no key action")
	if stuff.__class__ == list:
		try:
			# say("event server with data list v6")
			#say(stuff)
			key=stuff.pop(0)
			#say(key)
			cfg=FreeCAD.PluginManager.pluginloader.config3['keys']['keyserver']
			# test
			if False:
				if cfg.has_key("aa"):
					say(cfg['aa'])
					
				if cfg.has_key("bb:cc"):
					say(cfg['bb:cc'])
					
				if cfg.has_key(":dd"):
					say(cfg[':dd'])
				
			for items in stuff:
				[w,t]=items
				#say(str(items) + ' ... ')
				found=False
				if cfg.has_key(w+":"+t):
					#say(items)
					found=cfg[w+":"+t]
				elif cfg.has_key(":"+t):
					#say(t)
					found=cfg[":"+t]
				elif cfg.has_key(w):
					#say(w)
					found=cfg[w]
				
				if found:
					#say("found")
					#say(found['comment'])
					if found.has_key(key):
					#	say (found[key])
						say(found[key]['exec'])
						exec(found[key]['exec'])
						return
					else:
						# say(found.keys())
						pass
		except:
			sayexc()


#
# communication 
#

@QtCore.Slot(int)
@QtCore.Slot(str)
@QtCore.Slot(object)

class Communicate(QtCore.QObject):
	speakNumber = QtCore.Signal(int)
	speakWord = QtCore.Signal(str)
	speakList = QtCore.Signal(object)

def start():
	someone = Communicate()
	# cogssrnnect signal and slot properly
	someone.speakNumber.connect(saySomething)
	someone.speakWord.connect(saySomething)
	someone.speakList.connect(saySomething)
	FreeCAD.EventServer=someone

	# emit each 'speak' signal - test only 
	someone.speakNumber.emit(10)
	someone.speakWord.emit("hallo  Eventserver ...")
	someone.speakList.emit(['1', ['2', '3']])
	FreeCAD.EventServer.speakWord.emit("hallo  Eventserver ...")
