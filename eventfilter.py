# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- event filter
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

__Version__='huhu'

__Author__="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

from PySide import QtGui,QtCore
import FreeCAD,tools,sys
from tools import *

# https://wiki.qt.io/Signals_and_Slots_in_PySide


def runextern(fn,arg1="",arg2=""):
	''' 
	start an extern program with max 2 arguments
	'''
	
	import os
	if os.path.exists(fn) and os.path.isfile(fn):
		try:
			import subprocess
			DETACHED_PROCESS = 0x00000008
			windows=False
			if windows:
				pid = subprocess.Popen([fn,arg1,arg2],creationflags=DETACHED_PROCESS).pid
			else:
				pid = subprocess.Popen([fn,arg1,arg2]).pid
		except:
			sayexc("exec error file: " + fn ) 
	else:
		sayexc("no access to file: " + fn) 

import eventserver
reload(eventserver)
eventserver.start()



#-----------------------------

# trace

global tron
tron=False

global lastEvent
lastEvent=None

global keyPressed2
keyPressed2=False

global editmode
editmode=False


class EventFilter(QtCore.QObject):

	def init(self):
		self.enterleave=False
		self.enterleave=True
		
	def eventFilter(self, o, e):
		global tron
		global lastEvent
		global keyPressed2
		global editmode
		if not hasattr(FreeCAD,'MM'):
			FreeCAD.MM=0
		# http://doc.qt.io/qt-5/qevent.html
		z=str(e.type())

		# not used events
		if z == 'PySide.QtCore.QEvent.Type.ChildAdded' or \
				z == 'PySide.QtCore.QEvent.Type.ChildRemoved'or \
				z == 'PySide.QtCore.QEvent.Type.User'  or \
				z == 'PySide.QtCore.QEvent.Type.Paint' or \
				z == 'PySide.QtCore.QEvent.Type.LayoutRequest' or\
				z == 'PySide.QtCore.QEvent.Type.UpdateRequest'   :
			return QtGui.QWidget.eventFilter(self, o, e)

		if z == 'PySide.QtCore.QEvent.Type.KeyPress':
			# http://doc.qt.io/qt-4.8/qkeyevent.html

			# ignore editors
			if editmode:
				return QtGui.QWidget.eventFilter(self, o, e)
			
			# only first time key pressed
			if not keyPressed2:
				keyPressed2=True
				#FreeCAD.Console.PrintMessage(" "+ str(e.key()) +" " )
				#FreeCAD.Console.PrintMessage(e.modifiers())
				
				# tastennamen ...
				# if e.key() == QtCore.Qt.Key_A and (e.modifiers() & QtCore.Qt.SHIFT):

				FreeCAD.MM=0
				try:
					# only two function keys implemented, no modifieres
					if e.key()== QtCore.Qt.Key_F2:
						FreeCAD.EventServer.speakWord.emit("F2")
						say("------------F2-----------------")
						return False
					elif e.key()== QtCore.Qt.Key_F3:
						FreeCAD.EventServer.speakWord.emit("F3")
					else: 
						FreeCAD.EventServer.speakWord.emit(e.text())
				except:
					sayexc()

		# end of a single key pressed
		if z == 'PySide.QtCore.QEvent.Type.KeyRelease':
			keyPressed2=False

		# enter and leave a widget - editor widgets
		if z == 'PySide.QtCore.QEvent.Type.Enter' or z == 'PySide.QtCore.QEvent.Type.Leave':
			try:
				# FreeCAD.Console.PrintMessage("Enter Leave\n")
				#FreeCAD.Console.PrintMessage(e.type())
				#FreeCAD.Console.PrintMessage(o)
				#FreeCAD.Console.PrintMessage("!\n")
				FreeCAD.MM=0
				pass
			except:
				sayexc()
		
		# deactive keys in editors context
		if z == 'PySide.QtCore.QEvent.Type.Enter' and \
			(o.__class__ == QtGui.QPlainTextEdit or o.__class__ == QtGui.QTextEdit):
			editmode=True
		elif z == 'PySide.QtCore.QEvent.Type.Leave' and \
			(o.__class__ == QtGui.QPlainTextEdit or o.__class__ == QtGui.QTextEdit):
			editmode=False

		# mouse movement only leaves and enters
		if z == 'PySide.QtCore.QEvent.Type.HoverMove' :
			if FreeCAD.MM == 0:
				# http://doc.qt.io/qt-5/qhoverevent.html
				FreeCAD.Console.PrintMessage("old Pos: ")
				FreeCAD.Console.PrintMessage(e.oldPos())
				FreeCAD.Console.PrintMessage(", new Pos: ")
				FreeCAD.Console.PrintMessage(e.pos())
				FreeCAD.Console.PrintMessage("\n")
			FreeCAD.MM=1


		event=e
		try:
			if tron:
				FreeCAD.Console.PrintMessage(str(event.type())+ " " + str(o) +'!!\n')
				
			if event.type() == QtCore.QEvent.ContextMenu and o.__class__ == QtGui.QWidget:
					# hier contextmenue rechte maus auschalten
					#	FreeCAD.Console.PrintMessage('!! cancel -------------------------------------context-----------\n')
					#	return True
					pass

			# wheel rotation
			if event.type()== QtCore.QEvent.Type.Wheel:
				# http://doc.qt.io/qt-4.8/qwheelevent.html
				FreeCAD.Console.PrintMessage(str(event.type())+ " " + str(o) +'!!\n')
				FreeCAD.Console.PrintMessage(str(e.delta()) + " " +str(e.pos()) + "\n")
				return False

			# mouse clicks
			if event.type() == QtCore.QEvent.MouseButtonPress or \
					event.type() == QtCore.QEvent.MouseButtonRelease or\
					event.type() == QtCore.QEvent.MouseButtonDblClick:

				FreeCAD.Console.PrintMessage(str(event.type())+ " " + str(o) +'!!\n')
				FreeCAD.Console.PrintMessage( " mouse position: " +str(e.pos()) + "\n")
				FreeCAD.Console.PrintMessage( " widget height: " +str(o.height()) + "\n")
				FreeCAD.Console.PrintMessage( " widget width: " +str(o.width()) + "\n")
				FreeCAD.Console.PrintMessage( " widget position: " +str(o.pos()) + "\n")
				FreeCAD.Console.PrintMessage( " parent widget: " +str(o.parentWidget()) + "\n")
				widget = QtGui.qApp.widgetAt(e.pos())
				if widget:
					FreeCAD.Console.PrintMessage("widget under mouse: " + str(widget) +" !--"+widget.objectName() +"--!\n")
				
				# double clicked
				if event.type() == QtCore.QEvent.MouseButtonDblClick and event.button() == QtCore.Qt.MidButton :
					FreeCAD.Console.PrintMessage('two\n')

				# middle
				if event.button() == QtCore.Qt.MidButton or  event.button() == QtCore.Qt.MiddleButton:
					FreeCAD.Console.PrintMessage('!-------------------------------------!!  X middle \n')
					# return QtGui.QWidget.eventFilter(self, o, es)

				if event.button() == QtCore.Qt.LeftButton:
					FreeCAD.Console.PrintMessage('!! X one left\n')

				# right mouse button when context menue deactivated
				elif event.button() == QtCore.Qt.RightButton:
					FreeCAD.Console.PrintMessage('!! X one right\n')
					
					if event.type() == QtCore.QEvent.MouseButtonPress and o.__class__ == QtGui.QWidget:
						FreeCAD.Console.PrintMessage('!! rechts widget  -------------------------------------dfdfddf-----------\n')
						return True

					if event.type() == QtCore.QEvent.MouseButtonPress and o.__class__ == QtGui.QTextEdit:
						FreeCAD.Console.PrintMessage('!! rechts textfeld  ------------------------------------------------\n')
						return True
		except:
			sayexc()
		return QtGui.QWidget.eventFilter(self, o, e)



def start():
	global keyPressed2
	mw=QtGui.qApp
	ef=EventFilter()
	FreeCAD.eventfilter=ef
	mw.installEventFilter(ef)
	keyPressed2=False


def stop():
	global keyPressed2
	mw=QtGui.qApp
	ef=FreeCAD.eventfilter
	mw.removeEventFilter(ef)
	keyPressed2=False


