
_Version__='huhu'

__Author__="AAAAAAAgggggggggggggggggggggggggggAAAAAAAAAAAAAAAAAAAAAAAA"



from tools import *

global buffer
buffer=None
global bufferstring
bufferstring=" "

try:
	#import infodock
	pass
except:
		sayexc()

def saySomething(stuff):
	'''
	event server
	'''
	#say("---------------------------------------------------------------------------------------")
	
	global buffer
	global bufferstring
	debug=False

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
			#say("event server with data list v6")
			#say(stuff)
			#infodock.settext(str(stuff))
			key=stuff.pop(0)
			if debug: say("server got key ->"+str(key)+"<-")


			cfg=FreeCAD.PluginManager.pluginloader.config3['keys']['keyserver']
			found=False

			if key == '-':
				buffer=None
				bufferstring=" "
				if debug: say("reset buffer")
				return
			
			try: 
					
					key=int(key)
					# say("zahl")
			except:
					pass
			# say(key)
			
			if not buffer:
#				say("not buffer ################")
				bufferstring=' '
				for items in stuff:
					[w,t]=items
#					say(str(items) + ' ... ')
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
					if found and found.has_key(key): 
#						say("break " + key )
						break
			else:
				pass
#				say("Buffer")
				found=buffer
#			say("--------------------------")
				
			if found:
				if debug:
					say("*** found:")
					say(found)
					# key=str(key)
				
					say(found.keys())
				if found.has_key(key):
					# say("key found")
					if found[key].__class__ == str:
						if debug: saye("*****Kommentar direkt")
						saye(found[key])
						buffer = None
						bufferstring=" "
						say(bufferstring)
						return
#					say (found[key])
					if found[key].has_key('say'):
						say(found[key]['say'])
					if found[key].has_key('pre'):
						say('*** pre:')
						saye(found[key]['pre']['exec'])
						try:
							exec("App=FreeCAD;Gui=FreeCADGui;\n" + found[key]['pre']['exec'])
						except:
							sayexc()
					if found[key].has_key('exec'):
						#say(found[key]['log'])
						say('*** exec:')
						saye(found[key]['exec'])
						try:
							exec(found[key]['exec'])
						except:
							sayexc()
						if found[key].has_key('post'):
							say('*** post:')
							saye(found[key]['post'])
							try:
								exec("App=FreeCAD;Gui=FreeCADGui;\n" + found[key]['post']['exec'])
							except:
								sayexc()

						buffer = str(key)  +" gefunden"
						buffer = None
						bufferstring += "--> " + str(key)
						bufferstring += ' exec !' + found[key]['exec'] +"!"
						# bufferstring=""
						
					else: 
						if debug: say("*** store")
						if debug: say(found[key])
						buffer = found[key]
						bufferstring += "-->" + str(key)
						if debug: say("buffer = " + str(buffer))
					if found[key].has_key('log') and found[key]['log'] > 0:
						saye(bufferstring)
					
					#infodock.addtext(bufferstring)
					return
				else:
					# say(found.keys())
					if debug: say("*** clear key buffer")
					buffer= None
					bufferstring=" "
					pass
		except:
			sayexc()
		#say(bufferstring)


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
	#infodock.start()
	#infodock.settext("starting ...")

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
	#infodock.addtext("eventserver is running")
	
