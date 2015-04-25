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

global QtGui
global config3,MyAction,say,saye
__vers__='0.4'


import sys, os, zipfile

def say(s):
	FreeCAD.Console.PrintMessage(str(s)+"\n")

def saye(s):
	FreeCAD.Console.PrintError(str(s)+"\n")


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

def dlge(msg):
	diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Plugin Loader Error",msg )
	diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
	diag.exec_()

def dlgi(msg):
	diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,u"Plugin Loader",msg )
	diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
	diag.exec_()

def dlgyn(msg):
	m=QtGui.QWidget()
	dial = QtGui.QMessageBox.question( m,'Message',  msg, QtGui.QMessageBox.Yes |     QtGui.QMessageBox.No, QtGui.QMessageBox.No)

#----------------
#
# Plugin loader  - install macros, libraries and extra workbenches 
#
#-----------------


# read from file and converted to python
import yaml,urllib


fn=__dir__+"/pluginloaderconfig.yaml"

stream = open(fn, 'r')
config3 = yaml.load(stream)
say(config3)

def set_defaults(conf):
	for key in conf['plugins'].keys():
		say(key)
		say("----")
		for att in conf['defaults'].keys():
			say(att)
			if not conf['plugins'][key].has_key(att):
				say('***')
				say(conf['defaults'][att])
				conf['plugins'][key][att]=conf['defaults'][att]
	return(conf)

config3=set_defaults(config3)


class MyAction( QtGui.QAction):
	def __init__(self, name,t,method,*args):
		#QtGui.QWidget.__init__(self, *args)
		QtGui.QAction.__init__(self,QtGui.QIcon('/usr/lib/freecad/Mod/mylib/icons/sun.png'),name, t)
		self.cmd="say('hallo')"
		self.cmd=method
		
	def run(self):
			say("run")
			say("!"+self.cmd+"!")
			exec(self.cmd)
			say("done")


class MyWidget(QtGui.QWidget):
	def __init__(self, master,*args):
		QtGui.QWidget.__init__(self, *args)
		self.master=master
		#if hasattr(FreeCAD,"mywidget"):
		#	FreeCAD.mywidget.hide()
		FreeCAD.mywidget=self
		self.config=master.config
		self.vollabel = QtGui.QLabel('1. Select Packages ...')
		self.vollabel2 = QtGui.QLabel('2. Show Package Info ...')
		self.lab2 = QtGui.QLabel('')
		self.vollabel3 = QtGui.QLabel('3. Install/Update ...')
		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.clicked.connect(self.on_pushButton02_clicked) 
		self.pushButton02.setText("Display ")
		self.pushButton03 = QtGui.QPushButton()
		self.pushButton03.clicked.connect(self.on_pushButton03_clicked) 
		self.pushButton03.setText("Run 2")
		self.listWidget = QtGui.QListWidget() 
		self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		kl=self.config.keys()
		say(kl)
		for k in sorted(kl):
			if not self.config[k]['status'] == "ignore":
				item = QtGui.QListWidgetItem(k)
				self.listWidget.addItem(item)
		layout = QtGui.QGridLayout()
		line=4
		layout.addWidget(self.vollabel, 0, 0)
		line=3
		layout.addWidget(self.listWidget, line, 0,1,4)
		line+=1
		layout.addWidget(self.vollabel2, line, 0)
		line+=1
		layout.addWidget(self.lab2, line, 0)
		line+=1
		layout.addWidget(self.pushButton02, line, 0,1,4)
		line+=1
		layout.addWidget(self.vollabel3, line, 0)
		line+=1
		layout.addWidget(self.pushButton03, line, 0,1,4)
		line+=1
		line+=1
		self.setLayout(layout)
		self.setWindowTitle("Plugin Loader")

	def on_pushButton02_clicked(self):
		text=""
		say("huhu")
		for sel in self.listWidget.selectedItems():
			text += "*** "+ sel.text() + " ***"
			say(text)
			say(self.config[sel.text()])
			say("ok")
			
			text += "\n" + str(self.config[sel.text()]['author'])
			say(text)
			text += "\n" + str(self.config[sel.text()]['source'])
			say(text)
			text += "\n" + str(self.config[sel.text()]['description'])
			say(text)
			text += "\n"
		self.lab2.setText(text)

	def on_pushButton03_clicked(self):
		seli=[]
		if len(self.listWidget.selectedItems())==0:
			dlge("nothing selected - nothing to do")
		else:
			m=QtGui.QWidget()
			dial = QtGui.QMessageBox.question( m,'Message',    "Are you sure to install?", QtGui.QMessageBox.Yes |     QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if dial==PySide.QtGui.QMessageBox.StandardButton.No: return
			for sel in self.listWidget.selectedItems():
				seli.append(sel.text())
				say(sel.text())
				self.master.install(sel.text())
			pass
			self.show()
			say("run done")

class PluginLoader(object):

	def __init__(self):
		global say
		say("init")
		self.config=config3['plugins']
		self.base=config3['base']
		self.keys=self.config.keys
		self.register()


	def start(self):
		saye("pluginloader started ...")
		s=MyWidget(self)
		self.widget=s
		s.show()

#check the version local against the web

	def getwebVersionDate(self,plugin):
		# get the date of the last update of the master
		fn=self.base['tmprelease']
		try:
			tg=urllib.urlretrieve(self.config[plugin]['timestamp'],fn)
			f = open(fn)
			lines = f.readlines()
			rc=lines[0]
		except:
			saye("no web version info available")
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
			saye("no local version info available")
			rc='99999999999999999999999'
		return rc

	def install(self,item):
		say(self.config[item])
		self.widget.lab2.setText("Install start")
		self.widget.show()
		plugin=item
		saye("install or update "+plugin) 
		if self.config[plugin].has_key('status') and self.config[plugin]['status'] == 'ignore':
				saye('ignore')
				return

		localVersion=self.getlocalVersionDate(plugin)
		webVersion=self.getwebVersionDate(plugin)

		say("Local Version: "+localVersion)
		say("Web Version  : "+webVersion)

		needUpdate = localVersion < webVersion
		needUpdate = True

		if needUpdate:
				saye("Need Update")
		else:
				saye("No Update")

		zipextract=self.base['zipex']
		say(zipextract)
		zipfilename=zipextract+".zip"
		say(zipfilename)
		zipextract += '/'
		if needUpdate:
			if not self.config[plugin].has_key('source'):
				saye("no source given - nothing to download")
			else:
				say(self.config[plugin]['source'])
				if not self.config[plugin].has_key('sourcedir'):
					saye("sourcedir not given - install aborted")
					return
				if not self.config[plugin].has_key('destdir'):
					saye("destdir not given -- install aborted")
					return
				tg=urllib.urlretrieve(self.config[plugin]['source'],zipfilename)
				targetfile=tg[0]
				say(targetfile)
				fh = open(zipfilename, 'rb')
				zfile = zipfile.ZipFile(fh)
				zfile.extractall(zipextract)

				if self.config[plugin]['sourcedir'] =='.':
					source=zipextract
				else:
					source=zipextract+self.config[plugin]['sourcedir']
				say(source)
				destination=self.config[plugin]['destdir']
				say(destination)

				# hier muss fehlerhandlich verbessert werden !!
				if self.config[plugin].has_key('backup'):
					try:
						say("backup")
						os.rename(destination,self.config[plugin]['backup']+".bak."+str(time.time()))
					except:
						os.mkdir(destination)
				say("move")
				os.rename(source, destination)
				say("done install")
				#os.listdir(destination)
		self.widget.lab2.setText(str(item) + " install fertig ----")
		dlgi(str(item) + " ist fertig")
		

	def register(self):
		t=FreeCADGui.getMainWindow()
		pp=t.menuBar()
		self.pp=pp
		say(pp)
		say("register menu 4")
		found=False
		say("q")
		w=FreeCADGui.activeWorkbench()
		say("q2")
		say(w)
		try:
			say(w.name())
		except:
			say("no workbench name")
		say("q3")
		'''
#		say("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
		if  w.name() == 'DraftWorkbench':
			pname='Plugins2'
		else:
			pname='Plugins'
		for c in pp.children():
			try:
				if c.title() == pname:
				#if c.title() == "Help":
					found=c
					#c.hide()
					#found=False
					#break
			except:
				pass
		#found=False
		#self.Menu=None
		w=FreeCADGui.activeWorkbench()
		say(w.name())
		say("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
		if  w.name() == 'DraftWorkbench':
			# found=False
			say("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
		if not found:
			saye("Plugins not found")
			p=pp.addMenu(pname)
			saye(p)
			saye("-------------------------------xxxxxxxxxxxxxxxxxxxxxx")
			self.Menu=p
		else: 
			saye("Plugins found")
			p=found
			self.Menu=p
		'''
		
		t=FreeCADGui.getMainWindow()
		pp=t.menuBar()
		say(pp)
		say("register menu 2")
		found=False
		for c in pp.children():
			say(c)
			try:
				print c.title() 
				if c.title() == "Plugins":
					h=c
					found=c
			except:
				pass
		say("a")
		p=pp.addMenu("Plugins")
		if found:
			say("b")
			for c in h.actions():
				p.addAction(c)
				pp.show()
				h.deleteLater()
		say("c")
		for c in p.actions():
			if c.text() == 'pluginloader':
				say("replace action")
				p.removeAction(c)
				break;
		say("d")
		plina = QtGui.QAction(QtGui.QIcon('/usr/lib/freecad/Mod/mylib/icons/mars.png'),'pluginloader', t)
		a=p.addAction(plina)
		plina.triggered.connect(self.start)
		p.addSeparator()
		
		saye("register menu done")

	def registerPlugin(self,name,method):
		t=FreeCADGui.getMainWindow()
		saye("register menubar")
		pp=t.menuBar()
		found=False
		
		w=FreeCADGui.activeWorkbench()
		say(w.name())
#		say("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
		#if  w.name() == 'DraftWorkbench':
		#pname='Plugins2'
		#else:
		pname='Plugins'
		
		for c in pp.children():
			try:
				if c.title() == pname:
					found=c
					#c.hide()
					#found=False
					#break
			except:
				print c
		
		if not found:
			p=pp.addMenu(pname)
			saye("---------------------------yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
			saye("addmenu ..")
			say(p)
		else: 
			p=found
			say("found 1")
		
		#p=self.Menu
		for c in p.actions():
			if c.text() == name:
				p.removeAction(c)
				break;
		saye("create action "+name)
		plina =MyAction(name,t,method)
		a=p.addAction(plina)
		plina.triggered.connect(plina.run)
		saye("menubar done")


	def setParams(self):
		ta=FreeCAD.ParamGet('User parameter:Plugins')
		ta.SetString("pluginlist","")
		pluginlist=[]
		for k in self.config.keys():
			if not self.config[k]['status'] == 'ignore':
				t=FreeCAD.ParamGet('User parameter:Plugins/'+k)
				pluginlist.append(k)
				say("--")
				say(k)
				say(self.config[k])
				say(self.config[k]["name"])
				t.SetString("name",self.config[k]["name"])
				if self.config[k].has_key("author"): t.SetString("author",self.config[k]["author"])
				t.SetString("destination",self.config[k]["destdir"])
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
					menu=self.config[k]['menu']
					say(menu)
					itemlist.append(menu)
					tm=FreeCAD.ParamGet('User parameter:Plugins/'+k+'/'+menu)
					tm.SetString("exec",self.config[k]['exec'])
				ms=";".join(itemlist)
				if ms <>"":
					t.SetString("menulist",ms)
		ps=";".join(pluginlist)
		ta.SetString("pluginlist",ps)

	def getParams(self):
		for k in self.config.keys():
			if not self.config[k]['status'] == 'ignore':
				t=FreeCAD.ParamGet('User parameter:Plugins/'+k)
				status=t.GetInt('installed')
				say(k + " -- Status " + str(status))
				menues=t.GetString("menulist").split(';')
				for menu in menues:
					say("!"+menu)
					if menu =="":
						continue
					tm=FreeCAD.ParamGet('User parameter:Plugins/'+k+'/'+menu)
					method=tm.GetString("exec")
					say(method)
					self.registerPlugin(menu,method)
					say("done")


def starty(*args):
	say("starty ....")
	plulo=PluginLoader()
	say("2")
	plulo.setParams()
	say("3")
	plulo.getParams()
	say("starty done ....")
# plulo.start()



if False: # still bugy
	t=FreeCADGui.getMainWindow()
	t.workbenchActivated.connect(starty)

'''

import pluginloader
pluginloader.start()

'''
say("start ----------------")


plulo=PluginLoader()
plulo.setParams()
plulo.getParams()
