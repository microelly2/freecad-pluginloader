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
	from os.path import expanduser
	home = expanduser("~")
	__dir__=home+ '/.FreeCAD/Mod/pluginloader'
	


from os.path import expanduser
home = expanduser("~")
__dir__=home+ '/.FreeCAD/Mod/pluginloader'


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


def testmeth():
	dlge("TEST DIA LOGe")
	
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

class MyAction( QtGui.QAction):
	def __init__(self, name,t,method,*args):
		#QtGui.QWidget.__init__(self, *args)
		QtGui.QAction.__init__(self,QtGui.QIcon('/usr/lib/FreeCAD/Mod/mylib/icons/mars.png'),name, t)
		self.cmd="say('hallo')"
		self.cmd=method
		
	def run(self):
			say("run")
			say(self.cmd)
			exec(self.cmd)
			say("done")

#s=MyAction("myname",cmdstring)
#s.run()


class MyWidget(QtGui.QWidget):
	def __init__(self, master,*args):
		QtGui.QWidget.__init__(self, *args)
		self.master=master
		self.config=master.config
		self.vollabel = QtGui.QLabel('1. Select Packages ...')
		self.vollabel2 = QtGui.QLabel('2. Show Package Info ...')
		self.vollabel3 = QtGui.QLabel('3. Install/Update ...')
#		self.volvalue = QtGui.QLineEdit()
#		self.checkBox = QtGui.QCheckBox()

		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.clicked.connect(self.on_pushButton02_clicked) 
		self.pushButton02.setText("Display ")
		
		self.pushButton03 = QtGui.QPushButton()
		self.pushButton03.clicked.connect(self.on_pushButton03_clicked) 
		self.pushButton03.setText("Run ")

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
		layout.addWidget(self.vollabel3, 6, 0)
#		layout.addWidget(self.volvalue, 0, 1)
#		layout.addWidget(self.checkBox, 0, 2)
		layout.addWidget(self.pushButton02, 5, 0,1,4)
		layout.addWidget(self.pushButton03, 7, 0,1,4)
		layout.addWidget(self.listWidget, 3, 0,1,4)

		self.setLayout(layout)
		self.setWindowTitle("Plugin Loader")

#	def entered(self):
#		saye("enterd")
	def on_pushButton02_clicked(self):
			dlge("not implemented yet")


	def on_pushButton03_clicked(self):
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
		self.register()


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

	def register(self):
		t=FreeCADGui.getMainWindow()
		pp=t.menuBar()
		found=False
		for c in pp.children():
			try:
				if c.title() == "Plugins":
					found=c
					break
			except:
				print c
		if not found:
			p=pp.addMenu("Plugins")
		else: 
			p=found
		for c in p.actions():
			if c.text() == 'pluginloader':
				print ("replace action")
				p.removeAction(c)
				break;
		plina = QtGui.QAction(QtGui.QIcon('/usr/lib/FreeCAD/Mod/mylib/icons/mars.png'),'pluginloader', t)
		a=p.addAction(plina)
		plina.triggered.connect(self.start)


	def registerPlugin(self,name,method):
		t=FreeCADGui.getMainWindow()
		pp=t.menuBar()
		found=False
		for c in pp.children():
			try:
				if c.title() == "Plugins":
					found=c
					break
			except:
				print c
		if not found:
			p=pp.addMenu("Plugins")
		else: 
			p=found
		for c in p.actions():
			if c.text() == name:
				print ("replace action")
				p.removeAction(c)
				break;
		# plina = QtGui.QAction(QtGui.QIcon('/usr/lib/FreeCAD/Mod/mylib/icons/mars.png'),name, t)
		saye("create action"+name)
		plina =MyAction(name,t,method)
#s.run()

		a=p.addAction(plina)
#		say(method)
#		def method2():
#			s=method+""
#			#exec(s)
#		# lambda f=self.setDefaultHeight, arg=obj:f(arg)
		plina.triggered.connect(plina.run)

	def setParams(self):
		ta=FreeCAD.ParamGet('User parameter:Plugins')
		ta.SetString("pluginlist","")
		pluginlist=[]
		for k in self.config.keys():
			t=FreeCAD.ParamGet('User parameter:Plugins/'+k)
			pluginlist.append(k)
			t.SetString("name",self.config[k]["name"])
			#t.SetString("exec","execute this")
			t.SetInt('installed',1)
			itemlist=[]
			if self.config[k].has_key('menuitems'):
				for menu in self.config[k]['menuitems'].keys():
					say(menu)
					itemlist.append(menu)
					tm=FreeCAD.ParamGet('User parameter:Plugins/'+k+'/'+menu)
					tm.SetString("exec",self.config[k]['menuitems'][menu]['exec'])
			else:
				say("keine menuitmes")
			if self.config[k].has_key('menu'):
				say("top menue")
				menu=self.config[k]['menu']
				say(menu)
				itemlist.append(menu)
				say("yy")
				tm=FreeCAD.ParamGet('User parameter:Plugins/'+k+'/'+menu)
				say("rr")
				tm.SetString("exec",self.config[k]['exec'])
			ms=";".join(itemlist)
			say('ii')
			if ms <>"":
				
				t.SetString("menulist",ms)
		ps=";".join(pluginlist)
		ta.SetString("pluginlist",ps)
		say("ll")
		if False:
			try:
				height=t.GetInt('height')
				res=t.GSetFloat('resolution')
				fn=t.GetString('filename')
			except:
				print "kann parameter nicht lesen"

	def getParams(self):
		for k in self.config.keys():
			t=FreeCAD.ParamGet('User parameter:Plugins/'+k)
			status=t.GetInt('installed')
			say(k + " -- Status " + str(status))
			menues=t.GetString("menulist").split(';')
			for menu in menues:
				say("!"+menu)
				if menu =="":
					continue
				#for at in ["name","source"]:
	#			name=t.GetString("name")
	#			souce=t.GetString("source")
				tm=FreeCAD.ParamGet('User parameter:Plugins/'+k+'/'+menu)
				method=tm.GetString("exec")
				
				say(method)
				def ff():
					#exec(method)
					say(method)
				# ff=None
				
				self.registerPlugin(menu,method)
				say("done")

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
# plulo.start()
#plulo.register()
plulo.setParams()
plulo.getParams()



