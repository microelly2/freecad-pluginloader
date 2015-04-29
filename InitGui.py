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

FreeCAD.Console.PrintError("mod/plugins/InitGui start"+"\n")

App=FreeCAD

import FreeCAD,PySide,os,FreeCADGui,time
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 

global QtGui,QtCore
global myDialog,say

def myDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,"My Dialog",msg )
    diag.exec_()

def say(s):
		App.Console.PrintMessage(str(s)+"\n")

global MyAction2
class MyAction2():
	def __init__(self,method):
		#QtGui.QWidget.__init__(self, *args)
		# QtGui.QAction.__init__(self,QtGui.QIcon('/usr/lib/freecad/Mod/mylib/icons/sun.png'),name, t)
		self.cmd="say('hallo')"
		self.cmd=method
		
	def run(self):
			say("run")
			say("!"+self.cmd+"!")
			exec(self.cmd)
			say("done")

class MyDock(QtGui.QDockWidget):
	def __init__(self,master):
		QtGui.QDockWidget.__init__(self,master)
		self.setStyleSheet("background-color:white;")
		dock=self
		self.labels={}
		self.setMinimumSize(200, 185)
		master.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
		self.setWindowTitle('Pluginloader as Dock')
		self.setObjectName('Pluginloader')
		self.centralWidget = QtGui.QWidget(dock)
		self.centralWidget.setStyleSheet(
				"QPushButton { margin-right:10px;margin-left:20px;\
				background-color: lightblue;text-align:left;;padding:10px;padding-left:8px }")
		self.centralWidget.setObjectName("centralWidget")
		self.centralWidget.setGeometry(10,10, 150,100 )
		layout = QtGui.QVBoxLayout()
		self.centralWidget.setLayout(layout)
		
		self.liste=QtGui.QWidget()
		self.liste.setStyleSheet("QPushButton { margin-left:10px;margin-right:0px;\
				background-color: lightblue;text-align:left;padding:4px;padding-left:8px }");
		self.lilayout=QtGui.QVBoxLayout()
		self.liste.setLayout(self.lilayout)
		
		self.pushButton01 = QtGui.QPushButton(QtGui.QIcon('/usr/lib/freecad/Mod/mylib/icons/mars.png'),"Plugin Loader Dialog")
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

	def genlabels(self):
		cf=self.pluginloader.config
		for k in cf.keys():
			say(k)
			#say(cf[k])
			if False:
				self.pushButton = QtGui.QPushButton()
				self.pushButton.setGeometry(10, 20,140, 50)	
				#self.pushButton03.clicked.connect(fun3) 
				self.pushButton.setText("!"+k)
				self.lilayout.addWidget(self.pushButton)
			if cf[k].has_key('menu'):
					
					menu=cf[k]['menu']
					cmd=cf[k]['exec']
					if menu <> 'defaults':
						self.pushButton = QtGui.QPushButton(QtGui.QIcon('/usr/lib/freecad/Mod/mylib/icons/sun.png'),menu)
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
						self.lilayout.addWidget(self.pushButton)
						self.labels[menu]=yy
		if True:
			textArea = QtGui.QTextEdit()
			textArea.setGeometry(150, 10,240,100)
			textArea.setObjectName("cqCodeArea")
			textArea.setText("Test\nmultiline")
			self.lilayout.addWidget(textArea)


		say("done")

#		def closeEvent(self,event):
#			say("closeevent")
#		#	if self.canExit():
#		#		event.accept() # let the window close
#			event.ignore()
# http://www.freecadweb.org/wiki/index.php?title=Embedding_FreeCADGui


#------------------------ main --------------------------

global PluginManager

try:
	PluginManager.hide()
	pass
except:
	pass

PluginManager=MyDock(FreeCAD.Gui.getMainWindow())
FreeCAD.PluginManager=PluginManager


import pluginloader
t=pluginloader.PluginLoader()

PluginManager.pluginloaderCMD=t.start
PluginManager.pluginloader=t
PluginManager.show()

FreeCAD.Console.PrintError("mod/plugins/InitGui.py 1done"+"\n")


PluginManager.genlabels()
