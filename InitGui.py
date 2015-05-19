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

FreeCAD.Console.PrintError("mod/plugins/InitGui start A"+"\n")

App=FreeCAD

global sys,traceback
import FreeCAD,os,FreeCADGui,time,sys,traceback


import PySide
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
from PySide.QtCore import * 


global QtGui,QtCore
global myDialog,say,myDialoge

def myDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,"Plugin Manager",msg )
    diag.exec_()

def myDialoge(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,"Plugin Manager Error",msg )
    diag.exec_()

def say(s):
		App.Console.PrintMessage(str(s)+"\n")


global __version__
__version__='0.12 (2015/05/17) '

global sayexc

def sayexc(mess=''):
	#FreeCAD.Console.PrintMessage("Fehler")
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	#FreeCAD.Console.PrintMessage("Fehler")
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(lls))


global MyAction2
class MyAction2():
	def __init__(self,method):
		self.cmd="say('hallo')"
		self.cmd=method

	def run(self):
			#say("run")
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
				#FreeCAD.Console.PrintMessage("Fehler")
				sayexc(self.cmd)
			#say("done")

class MyDock(QtGui.QDockWidget):
	def __init__(self,master):
		QtGui.QDockWidget.__init__(self,master)
		self.setStyleSheet("background-color:white;")
		dock=self
		self.labels={}
		self.setMinimumSize(200, 185)
		master.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
		self.setWindowTitle('Plugin Manager')
		self.setObjectName('Pluginloader')
		self.centralWidget = QtGui.QWidget(dock)
		self.centralWidget.setMaximumHeight(800)
		self.centralWidget.setStyleSheet("\
				QWidget { background-color: lightblue}\
				QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
				background-color: lightblue;text-align:left;;padding:6px;padding-left:4px }\
								\
				")
		self.centralWidget.setObjectName("centralWidget")
		self.centralWidget.setGeometry(10,10, 150,100 )
		layout = QtGui.QVBoxLayout()
		self.centralWidget.setLayout(layout)
		
		self.liste=QtGui.QWidget()
		#self.liste.setStyleSheet("QPushButton { margin-left:0px;margin-right:0px;\
		#		background-color: lightblue;text-align:left;padding:1px;padding-left:2px }");
		self.lilayout=QtGui.QVBoxLayout()
		self.liste.setLayout(self.lilayout)
		
		self.pushButton01 = QtGui.QPushButton(QtGui.QIcon('/usr/lib/freecad/Mod/mylib/icons/mars.png'),"Plugin Loader     Version " + __version__)
		#self.pushButton01.setGeometry(10, 10,140, 50)
		self.pushButton01.clicked.connect(self.start) 
		#self.pushButton01.setText()
		layout.addWidget(self.pushButton01)
		layout.addWidget(self.liste)
		self.pluginloaderCMD=self.myFunction
		if 0 :
			self.pushButton02 = QtGui.QPushButton()
			#self.pushButton02.setGeometry(10, 60,140, 50)		
			self.pushButton02.clicked.connect(self.myFunction2) 
			self.pushButton02.setText('label2')
			self.lilayout.addWidget(self.pushButton02)
		if 0 :
			self.pushButton03 = QtGui.QPushButton()
			#self.pushButton03.setGeometry(10, 120,140, 50)	
			#self.pushButton03.clicked.connect(fun3) 
			self.pushButton03.setText('label3')
			self.lilayout.addWidget(self.pushButton03)
			

		dock.setWidget(self.centralWidget)

	FreeCAD.Console.PrintError("mod/plugins/ INITGUI plugins 2"+"\n")
	def start(self):
			say("pluginloader started ...")
			exec 'say("super")'
			self.pluginloaderCMD()
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
		cf=self.pluginloader.config
		say("gentoolbars ...")

		if self.pluginloader.config3["toolbars"].has_key(workbench):
			say("toolbars sind da            ----------------------" + workbench)
			for ky in sorted(self.pluginloader.config3["toolbars"][workbench].keys()):
				say(ky)
				try:
					mw=FreeCAD.Gui.getMainWindow()
					
					#toolbarBox = mw.addToolBar('Exit TB')
					#self.toolbar.addAction(exitAction)

					#toolbarBox = QtGui.QToolBar(mw)
					#toolbarBox.setWindowTitle(ky)
					
					#mw.addToolBar(QtCore.Qt.TopToolBarArea, toolbarBox)
					
					say("2")
					#se=FreeCAD.Gui.getMainWindow()
					#exitAction = QtGui.QAction('Exit 2', se)
					#exitAction.setShortcut('Ctrl+Q')
					#exitAction.triggered.connect(QtGui.qApp.quit)
					say("3")
					mw.toolbar = mw.addToolBar(workbench +': ' + ky)
					mw.toolbar.setWindowTitle("Personal " + workbench +': ' +ky)
					#mw.toolbar.addAction(exitAction)
					mw.toolbar.show()
					say("4")
					#self.tb=se.toolbar
					#self.ac=exitAction
					say("5")
					#FreeeCAD.tb=se.toolbar
					say("6")
					toolbarBox=mw.toolbar
				except Exception:
					say("ERRRRRRRRRRRRRRRR")
					say(Exception)
				# say(self.tb)
				
				for tool in sorted(self.pluginloader.config3["toolbars"][workbench][ky].keys()):
					say(tool)
					yy=self.pluginloader.config3["toolbars"][workbench][ky][tool]
					myAction2=QtGui.QAction(QtGui.QIcon(yy['icon']),tool ,mw)
					myAction2.setToolTip(tool)
					
					try:
						cmd=yy['exec']
					except:
						cmd="say('"+str(yy)+"')"
					say("cmd="+cmd)
					yy=MyAction2(cmd)
					myAction2.yy=yy
					myAction2.triggered.connect(yy.run) 
					
					toolbarBox.addAction(myAction2)
				say("ok")
				toolbarBox.show()
				
				# say(toolbarBox.Title())
				#self.toolbarBox=toolbarBox
				self.toolbars.append(toolbarBox)
				say("ky done "+ky)



	def genlabels(self):
		cf=self.pluginloader.config
		##+
		if self.pluginloader.config3.has_key("tabs"):
			say("tabs sind da            ----------------------")
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
				say(ky)
				import re
				tab1= QtGui.QWidget()
				pat=r"[0123456789]+ +(.*)"
				m = re.match(pat, ky)
				if m:
					kyk=m.group(1)
				else:
					kyk=ky
				tabs.addTab(tab1,kyk)
				
				
#				tabs.setStyleSheet("QWidget {background-color: green;margin:0px;padding:2px;}")
				vBoxlayout	= QtGui.QVBoxLayout()
				vBoxlayout.setAlignment(QtCore.Qt.AlignTop)
				head=QtGui.QLabel(kyk.upper())
				vBoxlayout.addWidget(head)
				head.setStyleSheet("QWidget { font: bold 18px;}")
				#font=QtGui.QFont;
				#font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing,10);    
				#head.setFont(font);
				#head.setLetterSpacing(QFont.Expanded,2.0)
				if self.pluginloader.config3['tabs'][ky].has_key("info"):
					info=QtGui.QLabel(self.pluginloader.config3['tabs'][ky]["info"])
					vBoxlayout.addWidget(info)

				for fun in sorted(self.pluginloader.config3["tabs"][ky].keys()):
					ff=self.pluginloader.config3["tabs"][ky][fun]
					say(fun)
					if fun == 'info':
						continue
					import re
					pat=r"[0123456789]+[\.]? +(.*)"
					m = re.match(pat, fun)
					if m:
						funk=m.group(1)
					else:
						funk=fun
#					funk=fun
					if ff.has_key('icon'):
						pushButton1 = QtGui.QPushButton(QtGui.QIcon(ff['icon']),funk)
					else:
						pushButton1 = QtGui.QPushButton(QtGui.QIcon('/usr/lib/freecad/Mod/plugins/icons/sun.png'),funk)
					say(pushButton1)
					say("!!" + fun + " ->" + funk + "<-")
					if ff.has_key('info'): 
						pushButton1.setToolTip(ff['info'])
					try:
						cmd=ff['exec']
					except:
						cmd="say('"+str(ff)+"')"
					say("cmd="+cmd)
					yy=MyAction2(cmd)
					pushButton1.yy=yy
					pushButton1.clicked.connect(yy.run) 
					
#					pushButtonx = QtGui.QPushButton("fun")
#					vBoxlayout.addWidget(pushButtonx)
#					pushButtony = QtGui.QPushButton("fun")
#					vBoxlayout.addWidget(pushButtony)
					if False:
						vBoxlayout.addWidget(pushButton1)
					else:
						#---------------
						hWid= QtGui.QWidget()
						hBoxlayout	= QtGui.QHBoxLayout()
						hBoxlayout.setContentsMargins(0, 0, 0, 0)
						hWid.setLayout(hBoxlayout)
#						hWid.setStyleSheet("background-color: red;padding:2px;margin:0px;")
					#	\
					#QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
					#background-color: lightblue;text-align:left;;padding:6px;padding-left:4px }\
				#					\
				#	")
						say("funk " + funk)
						pushButt_1 = QtGui.QPushButton(funk)
						hBoxlayout.addWidget(pushButton1)
						if ff.has_key('man'):
							pushButt_2 = QtGui.QPushButton(QtGui.QIcon('/usr/lib/freecad/Mod/plugins/icons/help.png'),'')
							pushButt_2.setToolTip('See WebSite Documentation')
							cmdh='say(' +ff['man']+')'
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
					#---------------
				
				#	\
				tab1.setLayout(vBoxlayout)   
		self.lilayout.addWidget(tabs)
# runde 2
		if False:
			plugintab	= QtGui.QWidget()
			tabs.addTab(plugintab,"Plugins")
			self.plugintab=plugintab
			pluginlayout	= QtGui.QVBoxLayout()
			pluginlayout.setAlignment(QtCore.Qt.AlignTop)
			plugintab.setLayout(pluginlayout) 
			self.lilayout.addWidget(tabs)
			say("------------done------------------")
			##-
			
			cf=self.pluginloader.config
			
			for k in sorted(cf.keys()):
				say(k)
				#say(cf[k])
				if False:
					self.pushButton = QtGui.QPushButton()
					self.pushButton.setGeometry(10, 20,140, 50)	
					#self.pushButton03.clicked.connect(fun3) 
					self.pushButton.setText("!"+k)
					self.lilayout.addWidget(self.pushButton)
					pluginlayout.addWidget(self.pushButton)
				if cf[k].has_key('menu'):
						
						menu=cf[k]['menu']
						cmd=cf[k]['exec']
						if cf[k].has_key('icon'):
							icon=cf[k]['icon'] # /usr/lib/freecad/Mod/plugins/icons/master.png
						else:
							icon="/usr/lib/freecad/Mod/plugins/icons/sun.png"
						if menu <> 'defaults':
							self.pushButton = QtGui.QPushButton(QtGui.QIcon(icon),menu)
							#self.pushButton.setGeometry(10, 20,140, 30)
							yy=MyAction2(cmd)
							#say(yy)
							#say(yy.run)
							#say(cmd)
							#try:
							#	yy.run()
							#except:
							#	say("fhelr")
							self.pushButton.clicked.connect(yy.run) 
							self.pushButton.setText(menu)
							## self.lilayout.addWidget(self.pushButton)
							pluginlayout.addWidget(self.pushButton)
							self.labels[menu]=yy
			if False:
				textArea = QtGui.QTextEdit()
				textArea.setGeometry(150, 10,240,100)
				textArea.setObjectName("cqCodeArea")
				textArea.setText("")
				self.lilayout.addWidget(textArea)


		say("done")

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

FreeCAD.Console.PrintError("mod/plugins/InitGui.py done"+"\n")
PluginManager.genlabels()

global re
import re
def runme():
	FreeCAD.Console.PrintError("RUN ME  mod/plugins/InitGui.py started "+ str( PluginManager.toolbar)+"\n")
	if PluginManager.toolbar >= 0:
		FreeCAD.Console.PrintError("RUN ME  mod/plugins/InitGui.py gentooolbars started"+"\n")
		try:
			say("1")
			t=FreeCADGui.getMainWindow()
			say("2")
			wb=FreeCADGui.activeWorkbench()
			say("3")
			say(wb)
			name="TEST"
			FreeCAD.wb=wb
			try:
				say(FreeCADGui.activeWorkbench().name())
				say(wb.name)
				say(wb.name())
				say("!!")
				name=wb.name()
				pass
			except:
				sayexc("except 1")
				wbs='a'+ str(wb)
				say("ex2")
				say(wbs)
				pat=r".*\.(.+) inst.*"
				say(pat)
				import re
				m = re.match(pat, wbs)
				say(m)
				if m:
					name=m.group(1)
					say("!"+name +"!")
					say("m good")
					name=m.group(1)
			say(name)
			say("weiter gentoolbars")
			PluginManager.gentoolbars(name)
			say("5")
		except:
			sayexc("except 2")
			say("schiefgegangen")
			PluginManager.gentoolbars("Robot")
		FreeCAD.Console.PrintError("RUN ME  mod/plugins/InitGui.py gentoolbars done "+"\n")
	PluginManager.toolbar +=1
	self=FreeCAD.Gui.getMainWindow()
	self.show()
	FreeCAD.Console.PrintError("RUN ME  mod/plugins/InitGui.py finished"+"\n")


t=FreeCADGui.getMainWindow()
t.workbenchActivated.connect(runme)



