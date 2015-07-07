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


#import infodock
#infodock.start()


class EventFilter(QtCore.QObject):

	def __init__(self):
		QtCore.QObject.__init__(self)
		self.keypressed=False
		self.stack=[]
		self.editmode=False
		self.pos=None
		self.debug=False
		self.debug=True
		
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
				
				# FreeCAD.Console.PrintMessage(" --> kkkey "+str(e.key()) +"!!"+ e.text() +" \n" )
				
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
						FreeCAD.Console.PrintMessage(" "+str(key)  +" \n" )
						
						pos=self.pos
						#if e.key()== QtCore.Qt.Key_F10:
						#	key += "F10#"
						
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
							if self.debug: FreeCAD.Console.PrintMessage( key + " at mouse position: " +str(pos) + "\n")
							if self.debug: say("*** message to server:");say(ll)
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

#infodock.addtext("keyfilter")


def start():
	mw=QtGui.qApp
	import eventserver
	reload(eventserver)
	eventserver.start()
	ef=EventFilter()
	FreeCAD.keyfilter=ef
	mw.installEventFilter(ef)


def stop():
	mw=QtGui.qApp
	ef=FreeCAD.keyfilter
	mw.removeEventFilter(ef)
	#infodock.settext("eventfilter stopped")


