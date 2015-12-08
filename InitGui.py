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

global __version__
__version__='0.35 B (2015/12/09)'


import FreeCAD

FreeCAD.Console.PrintMessage("Mod pluginloader InitGui.py starting ...\n")


global sys,traceback
import FreeCAD,os,FreeCADGui,time,sys,traceback
global re
import re
import os



import Draft
import Part


global PySide
import PySide
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
from PySide.QtCore import * 

from configmanager import ConfigManager
global ConfigManager


global QtGui,QtCore,QtSvg
global myDialog,say,myDialoge



def myDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,"Plugin Manager",msg )
    diag.exec_()

def myDialoge(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,"Plugin Manager Error",msg )
    diag.exec_()

def say(s):
	App.Console.PrintMessage(str(s)+"\n")



global sayexc
def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))


global pathMacro
def pathMacro(s):
	'''
	replace shortname by os path
	'''
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
	for k in ["UserHomePath","UserAppData","UserAppData"]:
		pat=r"(.*)"+k+"/"+"(.*)"
		m = re.match(pat, s)
		if m:
			pre=m.group(1)
			post=m.group(2)
			inn=FreeCAD.ConfigGet(k)
			if arch:
				if k == "UserAppData": #Force sensible Plugin folder
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
		sayexc("no access to " + fn) 


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

		sayexc("no access to " + fn) 


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
		self.labels={}
		self.setMinimumSize(200, 185)
		master.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
		self.setWindowTitle('Plugin Manager')
		self.setObjectName('Pluginloader')
		self.centralWidget = QtGui.QWidget(self)
		self.centralWidget.setMaximumHeight(800)
		self.centralWidget.setStyleSheet("QWidget { background-color: lightblue}\
			QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
			background-color: lightblue;text-align:left;;padding:6px;padding-left:4px;color:brown; }")
		self.centralWidget.setObjectName("centralWidget")
		self.centralWidget.setGeometry(5,5, 150,60 )
		
		layout = QtGui.QVBoxLayout()
		self.centralWidget.setLayout(layout)
		
		self.scroll=QtGui.QScrollArea()

		self.liste=QtGui.QWidget()
		self.lilayout=QtGui.QVBoxLayout()
		self.liste.setLayout(self.lilayout)
		
		mygroupbox = QtGui.QGroupBox()
		mygroupbox.setStyleSheet("QWidget { background-color: lightblue;margin:0px;padding:0px;}\
				QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
				background-color: lightblue;text-align:left;;padding:6px;padding-left:4px;color:brown; }")
		self.mygroupbox=mygroupbox

		myform = QtGui.QFormLayout()
		self.myform=myform
		self.myform.setSpacing(0)
		mygroupbox.setLayout(myform)

		scroll = QtGui.QScrollArea()
		scroll.setWidget(mygroupbox)
		scroll.setWidgetResizable(True)
		self.lilayout.addWidget(scroll)
		
		self.pushButton00 = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'),"Plugin Manager Version " + __version__)
		self.pushButton01 = QtGui.QPushButton(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+'/Mod/mylib/icons/mars.png'),"Plugin Loader"     )
		self.pushButton01.clicked.connect(self.start) 

		layout.addWidget(self.pushButton00)
		layout.addWidget(self.liste)
		layout.addWidget(self.pushButton01)

		self.pluginloaderCMD=None # self.myFunction
		self.setWidget(self.centralWidget)

		#self.setMouseTracking(True)

	def start(self):
			say("pluginloader started ...")
			exec "self.pluginloaderCMD()"


	def gentoolbars(self,workbench='init'):
		global pathMacro
		cf=self.pluginloader.config
		say("gentoolbars ...")
		if self.pluginloader.config3["toolbars"].has_key(workbench):
			for ky in sorted(self.pluginloader.config3["toolbars"][workbench].keys()):
				say("ky:"+str(ky))
				cma=ConfigManager("__toolbars__/" + workbench +"/" + ky)
				funhide=cma.get("_hide_",False)
				if funhide:
					say("toolbar ignore item " + ky)
					continue

				try:
					mw=FreeCAD.Gui.getMainWindow()
					mw.toolbar = mw.addToolBar(workbench +': ' + ky)
					mw.toolbar.setWindowTitle("Personal " + workbench +': ' +ky)
					mw.toolbar.show()
					toolbarBox=mw.toolbar
				except Exception:
					sayexc("exception add Tool Bar")
				for tool in sorted(self.pluginloader.config3["toolbars"][workbench][ky].keys()):
					say("tool, ky, yy ...")
					say(tool)
					say(ky)
					yy=self.pluginloader.config3["toolbars"][workbench][ky][tool]
					say(yy)
					FreeCAD.yy=yy
					FreeCAD.tb=toolbarBox
					
					myAction2=QtGui.QAction(QtGui.QIcon(yy['icon']),tool ,mw)
					myAction2.setToolTip(tool)
					toolbarBox.addAction(myAction2)
					try:
						cmd=yy['exec']
					except:
						cmd="say('"+str(yy)+"')"
					yy=MyAction2(pathMacro(cmd))
					myAction2.yy=yy
					myAction2.triggered.connect(yy.run) 
					
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
						pushButton1 = QtGui.QPushButton(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+'/Mod/plugins/icons/sun.png'),funk)
					if ff.has_key('info'): 
						pushButton1.setToolTip(ff['info'])
					try:
						cmd=ff['exec']
					except:
						cmd="say('"+str(ff)+"')"
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
						pushButt_2 = QtGui.QPushButton(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+'/Mod/plugins/icons/help.png'),'')
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
		self.myform.addWidget(tabs)
		# aktiver tab
		cm=ConfigManager("PluginManager")
		ix=cm.get("PluginTabIndex",0)
		tabs.setCurrentIndex(ix)
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
		FreeCAD.Console.PrintMessage("PluginManager reload done"+"\n")


#------------------------ main --------------------------

global PluginManager

try:
	PluginManager.hide()
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
			if name <>"NoneWorkbench":
				PluginManager.gentoolbars(name)
		except:
			sayexc("function runme on changed workbench")
	PluginManager.toolbar +=1
	self=FreeCAD.Gui.getMainWindow()
	self.show()



t=FreeCADGui.getMainWindow()
t.workbenchActivated.connect(runme)


#import eventfilter
#try:
#	FreeCAD.EventServer.speakWord.emit("hallo  Eventserver ...")
#except:
#	pass

if FreeCAD.ParamGet('User parameter:Plugins').GetBool('autoStartEventFilter'):
	try:
		import keyfilter
		say("start keyfilter ... ")
		reload(keyfilter)
		keyfilter.start()
	except:
		pass
		sayexc("autostart keyfilter module")
