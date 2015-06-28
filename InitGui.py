#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2015 microelly <microelly2@freecadbuch.de>              * 
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCAD

FreeCAD.Console.PrintMessage("Mod pluginloader InitGui.py starting ...\n")

App=FreeCAD

global sys,traceback
import FreeCAD,os,FreeCADGui,time,sys,traceback


import Draft

global PySide
import PySide
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
from PySide.QtCore import * 

from configmanager import ConfigManager
global ConfigManager


global QtGui,QtCore,QtSvg
global myDialog,say,myDialoge



global EventFilter
class EventFilter(QtCore.QObject):
  def eventFilter(self, o, e):
	if not hasattr(FreeCAD,'MM'):
		FreeCAD.MM=0
	# http://doc.qt.io/qt-5/qevent.html
	z=str(e.type())
	if z == 'PySide.QtCore.QEvent.Type.ChildAdded' or z == 'PySide.QtCore.QEvent.Type.ChildRemoved':
		
		# return False
		return QtGui.QWidget.eventFilter(self, o, e)
	if z == 'PySide.QtCore.QEvent.Type.User'  or z == 'PySide.QtCore.QEvent.Type.Paint' or \
	z == 'PySide.QtCore.QEvent.Type.LayoutRequest' or z == 'PySide.QtCore.QEvent.Type.UpdateRequest'   :
		# FreeCAD.Console.PrintMessage(z+" ")
		# return False
		return QtGui.QWidget.eventFilter(self, o, e)
	if z == 'PySide.QtCore.QEvent.Type.KeyPress':
		FreeCAD.Console.PrintMessage("\n")
		FreeCAD.Console.PrintMessage(e.type())
		FreeCAD.Console.PrintMessage(e.key())
		FreeCAD.MM=0
	if z == 'PySide.QtCore.QEvent.Type.Enter' or z == 'PySide.QtCore.QEvent.Type.Leave':
		try:
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage(e.type())
			#FreeCAD.Console.PrintMessage(dir(e))
			FreeCAD.Console.PrintMessage(o)
			FreeCAD.Console.PrintMessage("!\n")
			#FreeCAD.Console.PrintMessage(e.key())
			FreeCAD.MM=0
		except:
			sayexc()
	if z == 'PySide.QtCore.QEvent.Type.HoverMove' :
		if FreeCAD.MM == 0:
			# http://doc.qt.io/qt-5/qhoverevent.html
			FreeCAD.Console.PrintMessage("\n")
			FreeCAD.Console.PrintMessage(e.oldPos())
			FreeCAD.Console.PrintMessage(e.pos())
			FreeCAD.Console.PrintMessage("\n")
		FreeCAD.MM=1
	# return False
	event=e
	
	if event.type() == QtCore.QEvent.MouseButtonPress or \
		event.type() == QtCore.QEvent.MouseButtonRelease or event.type()== QtCore.QEvent.Type.Wheel or \
		event.type() == QtCore.QEvent.MouseButtonDblClick:
		FreeCAD.Console.PrintMessage(str(event.type())+ '\n')
		if event.button() == QtCore.Qt.MidButton or  event.button() == QtCore.Qt.MiddleButton:
			#If image is left clicked, display a red bar.
			FreeCAD.Console.PrintMessage('middle \n')
		if event.button() == QtCore.Qt.LeftButton:
			#If image is left clicked, display a red bar.
			FreeCAD.Console.PrintMessage('one left\n')
		elif event.button() == QtCore.Qt.RightButton:
			FreeCAD.Console.PrintMessage('one right\n')
		if event.type() == QtCore.QEvent.MouseButtonDblClick:
			#If image is double clicked, remove bar.
			FreeCAD.Console.PrintMessage('\ntwo\n')

	try:
			if event.type() == QtCore.QEvent.MouseButtonPress:
				if event.button() == QtCore.Qt.LeftButton:
					#If image is left clicked, display a red bar.
					FreeCAD.Console.PrintMessage('one left\n')
				elif event.button() == QtCore.Qt.RightButton:
					FreeCAD.Console.PrintMessage('one right\n')
				elif event.type() == QtCore.QEvent.MouseButtonDblClick:
					#If image is double clicked, remove bar.
					FreeCAD.Console.PrintMessage('two\n')
				#FreeCAD.Console.PrintMessage('event Filter ' + str(event.type()) + '\n' + str(event.button()) + '\n')
				FreeCAD.Console.PrintMessage(' event Filter MouseButtonPress')
				# return super(MyWidget, self).eventFilter(obj, event)
			if event.type() == QtCore.QEvent.MouseButtonRelease:
				FreeCAD.Console.PrintMessage(' event Filter MouseButtonRelease')
	except:
			sayexec()
	return QtGui.QWidget.eventFilter(self, o, e)



def myDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,"Plugin Manager",msg )
    diag.exec_()

def myDialoge(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,"Plugin Manager Error",msg )
    diag.exec_()

def say(s):
		App.Console.PrintMessage(str(s)+"\n")


global __version__
__version__='0.24 (2015/06/23)'

global sayexc

def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))

	
import re
import os

global pathMacro
def pathMacro(s):
	'''
	replace shortname by os path
	'''
# if True:
	kk=('Linux', 'Arch', '4.0.1-1-ARCH', '#1 SMP PREEMPT Wed Apr 29 12:00:26 CEST 2015', 'x86_64')
	import os
	try:
		kk=os.uname()
	except:
		kk="NOUNAME"
	match = re.search('ARCH', kk[2])
	if match:
		arch=True
	else:
		arch=False
	for k in ["UserHomePath","UserAppData","AppHomePath"]:
		pat=r"(.*)"+k+"/"+"(.*)"
		m = re.match(pat, s)
		if m:
			pre=m.group(1)
			post=m.group(2)
			inn=FreeCAD.ConfigGet(k)
			if arch:
				if k == "AppHomePath": #Force sensible Plugin folder
					if inn == "/usr/":
						inn=inn+"share/freecad/"
					if inn == "/usr/bin/":
						inn="/usr/share/freecad/"
				if k == "UserHomePath":
					s2=pre+inn+"/"+post
				else:
					s2=pre+inn+post
			else:
				if k == "UserHomePath":
					s2=pre+inn+"/"+post
				else:
					s2=pre+inn+post
			s=s2
	return s


global runscript
def runscript(fn):
	import os
	if os.path.exists(fn) and os.path.isfile(fn):
		try:
			d={};exec(open(fn).read(),d,d)
		except:
			sayexc("exec error file:" + fn ) 
	else:
		print ("kein zugriff auf " + fn)
		sayexc("kein zugriff auf" + fn) 


global runextern
def runextern(fn,arg1="",arg2=""):
	import os
	if os.path.exists(fn) and os.path.isfile(fn):
		try:
			#d={};exec(open(fn).read(),d,d)
			import subprocess
			DETACHED_PROCESS = 0x00000008
			windows=False
			if windows:
				pid = subprocess.Popen([fn,arg1,arg2],creationflags=DETACHED_PROCESS).pid
			else:
				pid = subprocess.Popen([fn,arg1,arg2]).pid
		except:
			sayexc("exec error file:" + fn ) 
	else:
		print ("kein zugriff auf " + fn)
		sayexc("kein zugriff auf" + fn) 




global MyAction2
class MyAction2():
	def __init__(self,method):
		self.cmd=method

	def run(self):
			say("!"+self.cmd+"!")
			import re 
			pat=r"FreeCADGui.activateWorkbench\(\"(.*)\"\)"
			m = re.match(pat, self.cmd)
			if m:
				pre=m.group(1)
				if not pre in FreeCADGui.listWorkbenches():
					myDialoge("The Workbench \n\n*** " + pre + " ***\n\nis not available \nplease \n\n1. install it and \n2. restart FreeCAD!") 
					return
			try:
				exec(self.cmd)
			except:
				sayexc(self.cmd)

class MyDock(QtGui.QDockWidget):
	def __init__(self,master):
		QtGui.QDockWidget.__init__(self,master)
		self.setStyleSheet("{background-color:white;color:brown;}")
		#dock=self
		self.labels={}
		self.setMinimumSize(200, 185)
		master.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
		self.setWindowTitle('Plugin Manager')
		self.setObjectName('Pluginloader')
		self.centralWidget = QtGui.QWidget(self)
		self.centralWidget.setMaximumHeight(800)
		self.centralWidget.setStyleSheet("\
				QWidget { background-color: lightblue}\
				QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
				background-color: lightblue;text-align:left;;padding:6px;padding-left:4px;color:brown; }\
								\
				")
		self.centralWidget.setObjectName("centralWidget")
		self.centralWidget.setGeometry(5,5, 150,60 )
		
		
		layout = QtGui.QVBoxLayout()
		self.centralWidget.setLayout(layout)
		
		self.scroll=QtGui.QScrollArea()
		
		
		self.liste=QtGui.QWidget()
		#self.liste.setStyleSheet("QPushButton { margin-left:0px;margin-right:0px;\
		#		background-color: lightblue;text-align:left;padding:1px;padding-left:2px }");
		self.lilayout=QtGui.QVBoxLayout()
		self.liste.setLayout(self.lilayout)
		
		##self.layout.setSpacing(0)
		##self.lilayout.setSpacing(0)
		
		
		#myform = QtGui.QFormLayout()
		#mygroupbox.setLayout(myform)
		#self.scroll.setWidget(mygroupbox)
		#self.scroll.setWidgetResizable(True)
		#myform.addWidget(self.liste)
		
		#------------------
		
		mygroupbox = QtGui.QGroupBox()
		mygroupbox.setStyleSheet("\
				QWidget { background-color: lightblue;margin:0px;padding:0px;}\
				QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
				background-color: lightblue;text-align:left;;padding:6px;padding-left:4px;color:brown; }\
								\
				")
		
		
		self.mygroupbox=mygroupbox
		myform = QtGui.QFormLayout()
		
		self.myform=myform
		self.myform.setSpacing(0)
#		labellist = []
#		combolist = []
#		val=20
#		for i in range(val):
#			labellist.append(QtGui.QLabel('mylabel'))
#			combolist.append(QtGui.QComboBox())
#			myform.addRow(labellist[i],combolist[i])
		mygroupbox.setLayout(myform)
		scroll = QtGui.QScrollArea()
		scroll.setWidget(mygroupbox)
		scroll.setWidgetResizable(True)
		#scroll.setFixedHeight(400)
		#layout = QtGui.QVBoxLayout(self)
		self.lilayout.addWidget(scroll)
		
		#-----------------
		self.pushButton00 = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'),"Plugin Manager Version " + __version__)
		self.pushButton01 = QtGui.QPushButton(QtGui.QIcon(FreeCAD.ConfigGet('AppHomePath')+'/Mod/mylib/icons/mars.png'),"Plugin Loader"     )
		#self.pushButton01.setGeometry(10, 10,140, 50)
		
		self.pushButton01.clicked.connect(self.start) 
		#latestart=lambda: self.start()
		#self.pushButton01.clicked.connect(latestart) 
		
		#self.pushButton01.setText()
		layout.addWidget(self.pushButton00)
		layout.addWidget(self.liste)
		layout.addWidget(self.pushButton01)
		##layout.addWidget(self.scroll)
		self.pluginloaderCMD=self.myFunction
		self.setWidget(self.centralWidget)


		self.setMouseTracking(True)
		self.installEventFilter(self)
		self.activateWindow()
		self.setFocus()
		
		say("activated")
		say(self.isActiveWindow())

	def eventFilter(self,widget,ev):
		event=ev
		# try:
		if event.type() == QtCore.QEvent.MouseButtonPress or \
			event.type() == QtCore.QEvent.MouseButtonRelease or event.type()== QtCore.QEvent.Type.Wheel or \
			event.type() == QtCore.QEvent.MouseButtonDblClick or \
			event.type() == QtCore.QEvent.MouseClick:
				FreeCAD.Console.PrintMessage(str(event.type())+ '\n')
				if event.button() == QtCore.Qt.MidButton or  event.button() == QtCore.Qt.MiddleButton:
					#If image is left clicked, display a red bar.
					FreeCAD.Console.PrintMessage('middle \n')
				if event.button() == QtCore.Qt.LeftButton:
					#If image is left clicked, display a red bar.
					FreeCAD.Console.PrintMessage('one left\n')
				elif event.button() == QtCore.Qt.RightButton:
					FreeCAD.Console.PrintMessage('one right\n')
				if event.type() == QtCore.QEvent.MouseButtonDblClick:
					#If image is double clicked, remove bar.
					FreeCAD.Console.PrintMessage('\ntwo\n')
				#return True
				#FreeCAD.Console.PrintMessage('event Filter ' + str(event.type()) + '\n' + str(event.button()) + '\n')
		#		FreeCAD.Console.PrintMessage(' event Filter MouseButtonPress')
				# return super(MyWidget, self).eventFilter(obj, event)
		#if event.type() == QtCore.QEvent.MouseButtonRelease:
		#		FreeCAD.Console.PrintMessage(' event Filter MouseButtonRelease')
		try:
			# say(" c gfgdfgfd nter event")
			t=ev.type()
			if t == PySide.QtCore.QEvent.Type.KeyPress and t != PySide.QtCore.QEvent.Type.ChildAdded:
				say(ev.type())
				say(ev.key())
			#FreeCAD.Console.PrintMessage("event filter pm! " + str(ev.type()) + " " + str(ev.key()) + "!\n")
		except:
			sayexc();
		return QtGui.QWidget.eventFilter(self, widget, ev)


	def enterEvent(self,ev):
		FreeCAD.Console.PrintMessage("++ Mouse Enter")
		#say(self.isActiveWindow())


	def mousePressEvent(self, event):
		FreeCAD.Console.PrintMessage("++ Mouse pressed")
		#say(self.isActiveWindow())


	def start(self):
			say("pluginloader started ...")
			exec 'say("super")'
			exec "self.pluginloaderCMD()"
			exec 'say("super ende")'
	#		s=MyWidget(self)
	#		say(s)
	#		self.widget=s
	#		
	#		s.show()
			say("widget shown")
			#s.hide()

	def  myFunction(self):
			say("myFunction called")

	def myFunction2(self):
		#myDialog("myFunction 2 called")
		exec 'say("super")'
		self.pluginloaderCMD()
		exec 'say("super ende")'


	def gentoolbars(self,workbench='init'):
		global pathMacro
		cf=self.pluginloader.config
		say("gentoolbars ...")
		if self.pluginloader.config3["toolbars"].has_key(workbench):
			# say("toolbars for            ----------------------" + workbench)
			for ky in sorted(self.pluginloader.config3["toolbars"][workbench].keys()):
				#say(ky)
				cma=ConfigManager("__toolbars__/" + workbench +"/" + ky)
				funhide=cma.get("_hide_",False)
				if funhide:
					say("toolbar ignore item " + ky)
					continue

				try:
					mw=FreeCAD.Gui.getMainWindow()
					mw.toolbar = mw.addToolBar(workbench +': ' + ky)
					mw.toolbar.setWindowTitle("Personal " + workbench +': ' +ky)
					#exitAction = QtGui.QAction('Exit 2', FreeCAD.Gui.getMainWindow())
					#exitAction.setShortcut('.')
					#exitAction.triggered.connect(QtGui.qApp.quit)
					#mw.toolbar.addAction(exitAction)
					mw.toolbar.show()
					toolbarBox=mw.toolbar
				except Exception:
					sayexc("exception add Tool Bar")
				for tool in sorted(self.pluginloader.config3["toolbars"][workbench][ky].keys()):
					say(tool)
					yy=self.pluginloader.config3["toolbars"][workbench][ky][tool]
					myAction2=QtGui.QAction(QtGui.QIcon(yy['icon']),tool ,mw)
					myAction2.setToolTip(tool)
					try:
						cmd=yy['exec']
					except:
						cmd="say('"+str(yy)+"')"
					
					yy=MyAction2(pathMacro(cmd))
					myAction2.yy=yy
					myAction2.triggered.connect(yy.run) 
					toolbarBox.addAction(myAction2)
				toolbarBox.show()
				self.toolbars.append(toolbarBox)
				say(ky +" done")



	def genlabels(self):
		cf=self.pluginloader.config
		try:
			self.tabs.deleteLater()
		except:
			pass
			
		if self.pluginloader.config3.has_key("tabs"):
			tabs= QtGui.QTabWidget()
			kl=sorted(self.pluginloader.config3["tabs"].keys())
			# where to place the tabs -  still hard coded
			mode="north"
			if self.pluginloader.config3['base'].has_key('tablocation'):
				mode= self.pluginloader.config3['base']['tablocation']
			if mode =="west":
				tabs.setTabPosition(QtGui.QTabWidget.West)
				kl.reverse()
			if mode =="east":
				tabs.setTabPosition(QtGui.QTabWidget.East)
				kl.reverse()
			
			for ky in kl:
				import re
				
				cmt=ConfigManager("__tabs__/" + ky)
				hide=cmt.get("_hide_",False)
				if hide:
						say("ignore tab " + ky)
						continue
				
				tab1= QtGui.QWidget()
				pat=r"[0123456789]+ +(.*)"
				m = re.match(pat, ky)
				if m:
					kyk=m.group(1)
				else:
					kyk=ky
				tabs.addTab(tab1,kyk)
				vBoxlayout	= QtGui.QVBoxLayout()
				vBoxlayout.setAlignment(QtCore.Qt.AlignTop)
				head=QtGui.QLabel(kyk.upper())
				vBoxlayout.addWidget(head)
				head.setStyleSheet("QWidget { font: bold 18px;color:brown;}")
				if self.pluginloader.config3['tabs'][ky].has_key("info"):
					info=QtGui.QLabel(self.pluginloader.config3['tabs'][ky]["info"])
					vBoxlayout.addWidget(info)

				for fun in sorted(self.pluginloader.config3["tabs"][ky].keys()):
					cma=ConfigManager("__tabs__/" + ky +"/" + fun)
					funhide=cma.get("_hide_",False)
					if funhide:
						say("ignore item " + fun)
						continue
					ff=self.pluginloader.config3["tabs"][ky][fun]
					if fun == 'info':
						continue
					import re
					pat=r"[0123456789]+[\.]? +(.*)"
					m = re.match(pat, fun)
					if m:
						funk=m.group(1)
					else:
						funk=fun
					if ff.has_key('icon'):
						pushButton1 = QtGui.QPushButton(QtGui.QIcon(ff['icon']),funk)
					else:
						pushButton1 = QtGui.QPushButton(QtGui.QIcon(FreeCAD.ConfigGet('AppHomePath')+'/Mod/plugins/icons/sun.png'),funk)
					#say("!!" + fun + " ->" + funk + "<-")
					if ff.has_key('info'): 
						pushButton1.setToolTip(ff['info'])
					try:
						cmd=ff['exec']
					except:
						cmd="say('"+str(ff)+"')"
					#say("cmd="+cmd)
					yy=MyAction2(cmd)
					yy=MyAction2(pathMacro(cmd))
					pushButton1.yy=yy
					pushButton1.clicked.connect(yy.run) 
					hWid= QtGui.QWidget()
					hBoxlayout	= QtGui.QHBoxLayout()
					hBoxlayout.setContentsMargins(0, 0, 0, 0)
					hWid.setLayout(hBoxlayout)
					pushButt_1 = QtGui.QPushButton(funk)
					hBoxlayout.addWidget(pushButton1)
					if ff.has_key('man'):
						pushButt_2 = QtGui.QPushButton(QtGui.QIcon(FreeCAD.ConfigGet('AppHomePath')+'/Mod/plugins/icons/help.png'),'')
						pushButt_2.setToolTip('See WebSite Documentation')
						cmdh='import WebGui; WebGui.openBrowser( "' +ff['man'] + '")'
						yh=MyAction2(cmdh)
						pushButt_2.yh=yh
						pushButt_2.clicked.connect(yh.run) 
						hBoxlayout.addWidget(pushButt_2)
						pushButton1.setFixedWidth(250)
					else:
						pushButton1.setFixedWidth(290)
					hBoxlayout.setAlignment(QtCore.Qt.AlignLeft)
					vBoxlayout.addWidget(hWid)
					vBoxlayout.setSpacing(0)
				tab1.setLayout(vBoxlayout)   
		#self.lilayout.addWidget(tabs)
		self.myform.addWidget(tabs)
		
		# aktiver tab
		cm=ConfigManager("PluginManager")
		ix=cm.get("PluginTabIndex",0)
		tabs.setCurrentIndex(ix) # private testing
		# tabs.setCurrentIndex(10)  # == Favorites
		self.tabs=tabs
	
	def reload(self):
		FreeCAD.Console.PrintMessage("PluginManager reload ... "+"\n")
		import pluginloader
		reload (pluginloader)
		t=pluginloader.PluginLoader()
		self.pluginloaderCMD=t.start
		self.pluginloader=t
		t.setParams()
		self.genlabels()
# 		self.installEventFilter(self)
		self.activateWindow()
		self.setFocus()

		FreeCAD.Console.PrintMessage("filter okay")

		FreeCAD.Console.PrintMessage("PluginManager reload done"+"\n")


#------------------------ main --------------------------

global PluginManager


try:
	PluginManager.hide()
	pass
except:
	pass


PluginManager=MyDock(FreeCAD.Gui.getMainWindow())
PluginManager.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
FreeCAD.PluginManager=PluginManager



import pluginloader
t=pluginloader.PluginLoader()

PluginManager.pluginloaderCMD=t.start
PluginManager.pluginloader=t
t.setParams()

PluginManager.show()
PluginManager.toolbar=0
PluginManager.toolbars=[]

if FreeCAD.ParamGet('User parameter:Plugins').GetBool('showdock'):
	PluginManager.show()

FreeCAD.Console.PrintMessage("Mod pluginloader InitGui.py done"+"\n")
PluginManager.genlabels()


global re
import re
def runme():
	if PluginManager.toolbar >= 0:
		try:
			t=FreeCADGui.getMainWindow()
			wb=FreeCADGui.activeWorkbench()
			name="TEST"
			try:
				name=wb.name()
			except:
				wbs='a'+ str(wb)
				pat=r".*\.(.+) inst.*"
				import re
				m = re.match(pat, wbs)
				if m:
					name=m.group(1)
			import Part
			PluginManager.gentoolbars(name)
		except:
			sayexc("except 2")
			PluginManager.gentoolbars("Robot")
	PluginManager.toolbar +=1
	self=FreeCAD.Gui.getMainWindow()
	self.show()
	#PluginManager.activateWindow()
	#PluginManager.setFocus()
	# return
	
	try:
		
		from PySide import QtCore
		from PySide import QtGui
		mw=FreeCADGui.getMainWindow()
		say(mw)
		#views=mw.findChildren(QtGui.QMainWindow)
		#say
		#views[0].metaObject().className()
		#view=views[0]
		say("ss")
		ef=EventFilter()
		#view.installEventFilter(ef)
		mw=FreeCADGui.getMainWindow()
		FreeCAD.ef=ef
		mw.installEventFilter(ef)
		mw.setMouseTracking(True)
		say("okay")
	except:
		sayexc()




t=FreeCADGui.getMainWindow()
t.workbenchActivated.connect(runme)


#try:
#	import sys;sys.path.append(FreeCAD.ConfigGet('AppHomePath')+'/Mod/plugins/WorkFeature');import WorkFeature;reload(WorkFeature);m=WorkFeature.WorkFeatureTab() 
#except:
#	FreeCAD.Console.PrintWarning("Work Feasture Autostart failed"+"\n")

try:
	say("eventfilter")
	ef=EventFilter()
	t.installEventFilter(ef)
	t.setMouseTracking(True)
	say("gemacht")
except:
	sayexc()
say("good")




#--------------------------------

