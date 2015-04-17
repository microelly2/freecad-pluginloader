# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- plugin loader
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,PySide,os,FreeCADGui,time
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 

__vers__='0.3'


import sys

import os

try:
	__dir__ = os.path.dirname(__file__)
	say(__dir__)
	say(__file__)
except:
	__dir__='/usr/lib/freecad/Mod/mylib'




def say(s):
	FreeCAD.Console.PrintMessage(str(s)+"\n")

def saye(s):
	FreeCAD.Console.PrintError(str(s)+"\n")


def dlge(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()

def dlgi(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,u"Plugin Loader",msg )
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()


#----------------
#
# Plugin loader  - install macros, libraries and extra workbenches 
#
#-----------------


# read from file and converted to python
import yaml

#fn="/home/thomas/Dokumente/freecad_buch/b134_pluginloader/pluginloaderconfig.yaml"

fn=__dir__+"/pluginloaderconfig.yaml"
stream = open(fn, 'r')
config3 = yaml.load(stream)
say(config3)


import urllib



class MyWidget(QtGui.QWidget):
	def __init__(self, master,*args):
		QtGui.QWidget.__init__(self, *args)
		self.master=master
		self.config=master.config
		self.vollabel = QtGui.QLabel('1. Select Packages ...')
		self.vollabel2 = QtGui.QLabel('2. Install/Update ...')
#		self.volvalue = QtGui.QLineEdit()
#		self.checkBox = QtGui.QCheckBox()

		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.clicked.connect(self.on_pushButton02_clicked) 
		self.pushButton02.setText("Run ")
		self.listWidget = QListWidget() 
#		FreeCAD.tu=self.listWidget
		self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		for k in self.config.keys():
			item = QListWidgetItem(k)
			self.listWidget.addItem(item)
			FreeCAD.tk=item
#		self.listWidget.itemEntered.connect(self.entered)
		#	item.itemEntered.connect(self.entered)

		layout = QtGui.QGridLayout()
		layout.addWidget(self.vollabel, 0, 0)
		layout.addWidget(self.vollabel2, 4, 0)
#		layout.addWidget(self.volvalue, 0, 1)
#		layout.addWidget(self.checkBox, 0, 2)
		layout.addWidget(self.pushButton02, 5, 0,1,4)
		layout.addWidget(self.listWidget, 3, 0,1,4)

		self.setLayout(layout)
		self.setWindowTitle("Plugin Loader")

#	def entered(self):
#		saye("enterd")

	def on_pushButton02_clicked(self):
		seli=[]
		if len(self.listWidget.selectedItems())==0:
			dlge("nothing selected - nothing to do")
		else:
			saye("selected ...")
			self.hide()
			for sel in self.listWidget.selectedItems():
				seli.append(sel.text())
				say(sel.text())
				self.master.install(sel.text())
			pass
			self.show()
			say("fertig")






class PluginLoader(object):

	def __init__(self):
		say("init")
		self.config=config3['plugins']
		self.keys=self.config.keys


	def start1(self):
		saye("luginloader started ...")
		self.install("sipoc")



	def start(self):
		saye("luginloader started ...")
		s=MyWidget(self)
		self.s=s
		s.show()
	
#check the version local against the web

	def getwebVersionDate(self,plugin):
		# get the date of the last update of the master
		fn="/tmp/release"
		tg=urllib.urlretrieve(self.config[plugin]['timestamp'],fn)
		try:
			f = open(fn)
			lines = f.readlines()
			rc=lines[0]
		except:
			rc=''
		return rc

	def getlocalVersionDate(self,plugin):
		# get the date of the last localk sync
		try:
			fn=self.config[plugin]['destdir']+"/release"
			f = open(fn)
			lines = f.readlines()
			rc=lines[0]
		except:
			rc='99999999999999999999999'
		return rc


#if os.path.exists(config[plugin]['destdir'] +".bak"):
#	saye("Backup for last update " + config[plugin]['destdir'] +".bak" +" still exists --> aborted")
#else:

	def install(self,item):
#		say(self.config[item])
		plugin=item
#		saye(plugin) 
		if self.config[plugin]['status'] == 'ignore':
				saye('ignore')
				return

		localVersion=self.getlocalVersionDate(plugin)
		webVersion=self.getwebVersionDate(plugin)

		#say("Local Version: "+localVersion)
		#say("Web Version  : "+webVersion)

		needUpdate = localVersion < webVersion

		if needUpdate:
				saye("Need Update")
		else:
				saye("No Update")

		# download if needed
		zipfilename="/tmp/my.zip"
		if needUpdate:
			say(self.config[plugin]['source'])
			tg=urllib.urlretrieve(self.config[plugin]['source'],zipfilename)
			say(tg)
			targetfile=tg[0]
			say(targetfile)

			import zipfile
			# extract
			fh = open(zipfilename, 'rb')
			zfile = zipfile.ZipFile(fh)
			zfile.extractall("/tmp/zipout")

			# positionieren
			source="/tmp/zipout/"+self.config[plugin]['sourcedir']
			say(source)
			destination=self.config[plugin]['destdir']
			say(destination)
			# hier muss fehlerhandlich verbessert werden !!
			try:
				os.rename(destination,destination+".bak."+str(time.time()))
			except:
				os.mkdir(destination)
			os.rename(source, destination)
			# result dir content
			os.listdir(destination)
		dlgi(str(item) + " ist fertig")




if False:
	#reload the plugins
	say("import plugins ..")

	import plugins
	reload(plugins)

	# use the plugins
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	plugins.plugin3.sipoc.createSipoc("MySipoc",[],[])


say("reloaded")

plulo=PluginLoader()
plulo.start()
