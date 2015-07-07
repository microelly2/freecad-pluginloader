# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- event filter
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


from PySide import QtGui,QtCore
import FreeCAD,tools,sys
from tools import *

def info(obj):
	c=str(obj.__class__)
	import re
#	say(c)
	pat=r"<type 'PySide.QtGui.(.*)'>"
	m = re.match(pat, c)
	if m:
		c=m.group(1)
	else:
		c=''
#	say(c)
	l=str(obj.objectName())
#	say(l)
#	say(obj.parent())
#	say(obj.parent().parent())
#	k=obj

	return[c,l]


<<<<<<< HEAD
#import infodock
#infodock.start()

=======
>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8

class EventFilter(QtCore.QObject):

	def __init__(self):
		QtCore.QObject.__init__(self)
		self.keypressed=False
		self.stack=[]
		self.editmode=False
		self.pos=None
<<<<<<< HEAD
		self.debug=False
		self.debug=True
=======
>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8
		
	def eventFilter(self, o, e):
		z=str(e.type())
		try:
			# not used events
			if z == 'PySide.QtCore.QEvent.Type.ChildAdded' or \
					z == 'PySide.QtCore.QEvent.Type.ChildRemoved'or \
					z == 'PySide.QtCore.QEvent.Type.User'  or \
					z == 'PySide.QtCore.QEvent.Type.Paint' or \
					z == 'PySide.QtCore.QEvent.Type.LayoutRequest' or\
					z == 'PySide.QtCore.QEvent.Type.UpdateRequest'   :
				return QtGui.QWidget.eventFilter(self, o, e)
			
			if z == 'PySide.QtCore.QEvent.Type.HoverMove' :
				self.pos=e.pos()
				# say(self.pos)
			
			if z == 'PySide.QtCore.QEvent.Type.KeyPress':
				# ignore editors
				if self.editmode:
					return QtGui.QWidget.eventFilter(self, o, e)
				
<<<<<<< HEAD
				# FreeCAD.Console.PrintMessage(" --> kkkey "+str(e.key()) +"!!"+ e.text() +" \n" )
				
=======
>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8
				# only first time key pressed
				if not self.keypressed:
					text=e.text()
					if 0 or text <>'':
						self.keypressed=True
						key=''
						if e.modifiers() & QtCore.Qt.SHIFT:
							#FreeCAD.Console.PrintMessage("SHIFT ")
							key +="SHIFT+"
						if e.modifiers() & QtCore.Qt.CTRL:
							#FreeCAD.Console.PrintMessage("CTRL ")
							key +="CTRL+"
						if e.modifiers() & QtCore.Qt.ALT:
							#FreeCAD.Console.PrintMessage("ALT ")
							key +="ALT+"
						key +=PySide.QtGui.QKeySequence(e.key()).toString() 
<<<<<<< HEAD
						FreeCAD.Console.PrintMessage(" "+str(key)  +" \n" )
						
						pos=self.pos
						#if e.key()== QtCore.Qt.Key_F10:
						#	key += "F10#"
=======
						# FreeCAD.Console.PrintMessage(" "+str(key)  +" \n" )
						
						pos=self.pos
						
>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8
						
						ll=[key]
						k=qApp.widgetAt(pos)
						# say("--------------get windows list")
						try:
							while k:
								r=info(k)
								# say(r)
								ll.append(r)
								# say(ll)
								k=k.parent()
								#say(k)
						except:
							sayexc()
						#say ("okay######################################################")
						
						#say("##################################################################send")
						
						if len(ll)>1:
<<<<<<< HEAD
							if self.debug: FreeCAD.Console.PrintMessage( key + " at mouse position: " +str(pos) + "\n")
							if self.debug: say("*** message to server:");say(ll)
=======
							FreeCAD.Console.PrintMessage( key + " at mouse position: " +str(pos) + "\n")
							say(ll)
>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8
							FreeCAD.EventServer.speakList.emit(ll)
						else:
							self.keypressed=False
						#say("----------------done")


			# end of a single key pressed
			if z == 'PySide.QtCore.QEvent.Type.KeyRelease':
				if self.keypressed:
					# FreeCAD.Console.PrintMessage(z)
					pass
				self.keypressed=False
		except:
			sayexc()

		return QtGui.QWidget.eventFilter(self, o, e)

<<<<<<< HEAD
#infodock.addtext("keyfilter")
=======
>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8


def start():
	mw=QtGui.qApp
	import eventserver
	reload(eventserver)
	eventserver.start()
<<<<<<< HEAD
=======

>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8
	ef=EventFilter()
	FreeCAD.keyfilter=ef
	mw.installEventFilter(ef)


def stop():
	mw=QtGui.qApp
	ef=FreeCAD.keyfilter
	mw.removeEventFilter(ef)
<<<<<<< HEAD
	#infodock.settext("eventfilter stopped")
=======
>>>>>>> 864bd93c55800cbb5d0482aadaf8fae25e73b3c8


