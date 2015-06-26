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
# global config3
global MyAction,say,saye
# global PluginManager

from configmanager import ConfigManager

import WebGui
__vers__=' version 0.13'


import sys, os, zipfile
import sys, traceback

def say(s):
	FreeCAD.Console.PrintMessage(str(s)+"\n")

def saye(s):
	FreeCAD.Console.PrintError(str(s)+"\n")


try:
	__dir__ = os.path.dirname(__file__)
except:
	from os.path import expanduser
	home = expanduser("~")
	__dir__=home+ '/.FreeCAD/Mod/pluginloader'

from os.path import expanduser
home = expanduser("~")
__dir__=home+ '/.FreeCAD/Mod/pluginloader'
__dir__=FreeCAD.ConfigGet('AppHomePath')+"/Mod/plugins"


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



def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	saye(mess + "\n" +"-->  ".join(lls))

def dlgexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	lls2=eval(ttt)
	l=len(lls)
	l2=lls[(l-1):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(lls2))
	msg=mess + "\n\n" +"-->  ".join(l2)
	diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Plugin Loader Error",msg )
	diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
	diag.exec_()


#----------------
#
# Plugin loader  - install macros, libraries and extra workbenches 
#
#-----------------


import time
def timeString():
	localtime   = time.localtime()
	timeString  = time.strftime("%Y-%m-%dT%H:%M:%SZ", localtime)
	return timeString

# read from file and converted to python
import yaml,urllib
import re
import os

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

def set_defaults(conf):
	for key in conf['plugins'].keys():
		for att in conf['defaults'].keys():
			if not conf['plugins'][key].has_key(att):
				conf['plugins'][key][att]=conf['defaults'][att]
	return(conf)

ta=FreeCAD.ParamGet('User parameter:Plugins')
fn=ta.GetString("configfile")

# where am I ?
where=ta.GetString("whereAmI")
if where == 'stick':
	__dir__="e:/FreeCAD_0.16.4924_x86_dev_bin/Mod/plugins"
	saye("I am on my windows stick")
if where == 'home':
	saye('I am at home')
	fn=0
#------------------------------

if not fn:
	fn=__dir__+"/pluginloaderconfig.yaml"
	ta.SetString("configfile",fn)


#---------------------

import platform
os=platform.system()

import pprint
#pprint.pprint(config3)




class MyAction( QtGui.QAction):
	def __init__(self, name,t,method,*args):
		#QtGui.QWidget.__init__(self, *args)
		QtGui.QAction.__init__(self,QtGui.QIcon('icons:breakpoint.svg'),name, t)
		self.cmd="say('hallo')"
		self.cmd=method
		
	def run(self):
			say("run")
			say("!"+self.cmd+"!")
			exec(self.cmd)
			say("done")

from datetime import datetime
#today = datetime.date.today()
#print today

class MyWidget(QtGui.QWidget):
	def __init__(self, master,*args):
		QtGui.QWidget.__init__(self, *args)
		self.master=master
		#if hasattr(FreeCAD,"mywidget"):
		#	FreeCAD.mywidget.hide()
		FreeCAD.mywidget=self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.config=master.config
		self.vollabel = QtGui.QLabel('1. Select Packages ...')
		self.vollabel2 = QtGui.QLabel('2. Show Package Info ...')
		self.lab2 = QtGui.QLabel(str(datetime.now()))
		self.vollabel3 = QtGui.QLabel('3. Install/Update ...')
		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.clicked.connect(self.on_pushButton02_clicked) 
		self.pushButton02.setText("Display ")
		self.pushButton03 = QtGui.QPushButton()
		self.pushButton03.clicked.connect(self.on_pushButton03_clicked) 
		self.pushButton03.setText("Run")
		self.listWidget = QtGui.QListWidget() 
		self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		kl=self.config.keys()
		say(kl)
		for k in sorted(kl):
			pcm=ConfigManager(k)
			hide=pcm.get('_hide_',False)
			if not self.config[k]['status'] == "ignore" and not hide:
				item = QtGui.QListWidgetItem(k)
				self.listWidget.addItem(item)
		layout = QtGui.QGridLayout()
		self.setStyleSheet("QListWidget,QPushButton {background-color: lightblue;color:brown;} ")
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
		self.setWindowTitle("Plugin Loader" + __vers__)

	def on_pushButton02_clicked(self):
		text=""
		say("huhu")
		for sel in self.listWidget.selectedItems():
			plugin=sel.text()
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
			
			#fn='https://api.github.com/repos/microelly2/freecad-pluginloader/commits'
			#fn='https://api.github.com/repos/cblt2l/FreeCAD-CuraEngine-Plugin/commits'
			mess=""
			try:
				import re
				source=str(self.config[sel.text()]['source'])
				say(source)
				m = re.match(r"https://github.com/(.*)/archive/master.zip", source)
				say(m)
				gitdate='no date from git'
				if m: 
					fn='https://api.github.com/repos/' + m.group(1) + '/commits'
					import urllib,json
					data=urllib.urlopen(fn).read()
					d = json.loads(data)
					dit=d[0]
					#dit['commit']['committer']['name']
					gitdate=dit['commit']['committer']['date']
				say(gitdate)
				installdate=FreeCAD.ParamGet('User parameter:/Plugins/'+plugin).GetString("installdate")
				if installdate >gitdate:
					mess="--- package " + plugin + " is up to date ---"
				else:
					mess="!!! update for " + plugin + " recommented !!!"
				
				FreeCAD.ParamGet('User parameter:/Plugins/'+plugin).SetString("gitdate",gitdate)
			except:
				sayexc()
				
			text += "my install:  " + FreeCAD.ParamGet('User parameter:/Plugins/'+plugin).GetString("installdate") + "\n"
			text += "git version:  " + FreeCAD.ParamGet('User parameter:/Plugins/'+plugin).GetString("gitdate","not implemented") + "\n"
			text += "\n" + mess + "\n\n"
			say(text)
			say("###")
		self.lab2.setText(text)
		say("web ..")
		if self.config[sel.text()].has_key('web'):
			say("has")
			WebGui.openBrowser( str(self.config[sel.text()]['web']))
		say("done")


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
		
		#---------------------------
		mcf=''
		config3={}
		try:
			say("pluginmanager config file "+ fn)
			stream = open(fn, 'r').read()
		#	mfc=''
			try:
				z=ConfigManager('')
				fn2=z.get('userconfigfile',"/usr/lib/freecad/Mod/plugins/myconfig.yaml")
				say("pluginmanager userconfig file "+ fn2)
				mcf = open(fn2, 'r').read()
			except:
				sayexc("userconfigfile not available")
			all=stream + mcf

			config3 = yaml.load(all)
		#	config3=set_defaults(config3)
		except:
			sayexc()
			pass

		try:
#			say("pluginmanager config file "+ fn)
#			stream = open(fn, 'r')
#			config3 = yaml.load(stream)
			config3=set_defaults(config3)
		except:
			dlgexc("Cannot load configfile " +fn +"\nread console log for details " )

		for plin in config3['plugins'].keys():
			for k in config3['plugins'][plin].keys():
				if config3['plugins'][plin][k] and config3['plugins'][plin][k].__class__ == dict:
					print "dict"
					print config3['plugins'][plin][k]
					if os in config3['plugins'][plin][k].keys():
						# replace
						config3['plugins'][plin][k]=config3['plugins'][plin][k][os]
			for att in ['destdir','exec','icon','backup']:
				config3['plugins'][plin][att]=pathMacro(config3['plugins'][plin][att])
			if plin=='defaulttest':
				pprint.pprint(config3['plugins'][plin])

		for plin in config3['data'].keys():
			for att in ['destdir','exec','icon','backup']:
				if config3['data'][plin].has_key(att):
					config3['data'][plin][att]=pathMacro(config3['data'][plin][att])


		self.config=config3['plugins']
		self.base=config3['base']
		self.config3=config3
		self.keys=self.config.keys
		self.register()


	def start(self):
		s=MyWidget(self)
		self.widget=s
		s.show()

#check the version local against the web

	def getwebVersionDate(self,plugin):
		# get the date of the last update of the master
		fn=pathMacro(self.base['tmprelease'])
		say(fn)
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
		
		
		say("---install or update !"+plugin+ "!") 
		if plugin == 'pluginloader':
			say("update MYSELF --------------- "+plugin) 
			fn=FreeCAD.ConfigGet('AppHomePath')+"/Mod/plugins/installer.py";d={};exec(open(fn).read(),d,d)
			now=timeString()
			self.config[plugin]['installed']=now
			FreeCAD.ParamGet('User parameter:/Plugins/'+plugin).SetString("installdate",now)
			return
		
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
				saye("Need Update 3")
		else:
				saye("No Update")

		zipextract=self.base['zipex']
		zipextract=pathMacro(zipextract)
		zipextract2=zipextract
		say(zipextract)
		# directory=zipextract+"/.."
		import os
		directory=os.path.dirname(zipextract)
		try:
			say(os.path.exists(directory))
		except:
			saye("fehelr hier")
		if not os.path.exists(directory):
			say("create dir " + directory)
			os.makedirs(directory)
		if self.config[plugin]['method']=='7z':
			zipfilename=zipextract+".7z"
		else:
			zipfilename=zipextract+".zip"
		
		say("zipfile: " + zipfilename)
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
				say("vor download")
				if self.config[plugin].has_key('format') and self.config[plugin]['format']=='flatfile':
					zipfilename=zipextract+"../a.txt"
					say(zipfilename)
				tg=urllib.urlretrieve(self.config[plugin]['source'],zipfilename)
				targetfile=tg[0]
				say("targetfile:"+targetfile)
				if self.config[plugin].has_key('format') and self.config[plugin]['format']=='flatfile':
					saye(" FlaT FILE")
					zipextract=zipfilename
				else:
					if self.config[plugin]['method']=='7z':
						import subprocess
						# problem geht nicht 
						#subprocess.call(['7z', 'x', zipfilename, zipextract2])
						os.system("cd /home/thomas/tmp; 7z x "+zipfilename+" PCB >/tmp/aa")
						zipextract="/home/thomas/tmp/PCB"
					else:
						fh = open(zipfilename, 'rb')
						zfile = zipfile.ZipFile(fh)
						zfile.extractall(zipextract)
						fh.close()
					say("extrakts")
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
						say("backup " + destination)
						
						say(" to " + self.config[plugin]['backup']+"/bak."+str(time.time()))
						if not os.path.exists(self.config[plugin]['backup']):
							say("create dir " + self.config[plugin]['backup'])
							os.makedirs(self.config[plugin]['backup'])
						# os.rename(destination,"c:/windows/temp/bak"+str(time.time()))
						os.rename(destination,self.config[plugin]['backup']+"/bak."+str(time.time()))
					except:
						sayexc("hier")
						if self.config[plugin].has_key('format') and self.config[plugin]['format']=='flatfile':
							pass
						else:
							pass
							#if not os.path.exists(directory):
							#	os.makedirs(destination)
				say("move")
				say("destination:"+destination+"!")
				say("source:" +source+'!')
				if self.config[plugin].has_key('format') and self.config[plugin]['format']=='flatfile':
					import shutil
					say("move by shutil")
					#src = "C:\\steve_test\\Test_xp\\added"
					#dst = "C:\\steve_test\\Test_xp\\moved"
					shutil.move(source, destination)
				else:
					# os.rename(source, destination)
					import shutil
					say("move by shutil too v3")
					if os.path.exists(directory):
						say("exists dir " + directory)
						
					try:
						directory=os.path.dirname(destination)
						base=os.path.basename(destination)
						sdirectory=os.path.dirname(source)
						sbase=os.path.basename(source)
						dest2=directory+"/"+sbase
						say(directory)
						say(sdirectory)
						say(dest2)
						say(base)
						
						if not os.path.exists(directory):
							say("create dir " + directory)
							os.makedirs(directory)
						say("move "+source+" to "+dest2)
						if  self.config[plugin].has_key('replace'):
							say("REPLACE")
#							       files: .qss
#       pattern:  [PATH_TO_IMAGES] 
#       data:  UserAppData/Gui/Stylesheets/images/

							p= self.config[plugin]['replace']['pattern']
							d= self.config[plugin]['replace']['data']
							f= self.config[plugin]['replace']['files']
							say(f)
#							for gg in f:
#								say(gg)
							# f= "/tmp/dark-green.qss"
#							say(p)
							d=pathMacro(d)
							say(d)
#							say(f)
#							say(base)
							for fil in f:
								try:
									cmd="sed -e 's#"+str(p)+"#"+str(d)+"#' " + source + "/" + fil + ">" + source + "/"+fil+".sed" 
									say(cmd)
									os.system(cmd)
									os.rename(source + "/"+fil+".sed" , source + "/" + fil)
								except:
									sayexc("q")
						shutil.move(source, dest2)
						say ("rename " +dest2+" to "+destination)
						try: 
							os.rename(dest2, destination)
						except:
							sayexc("1")
							os.rename(destination,destination+".err")
							say("exc 2")
							os.rename(dest2, destination)
							shutil.rmtree(destination+".err")
					except:
						sayexc("somethin wrong")
						
				say("done install")
				#os.listdir(destination)
		self.widget.lab2.setText(str(item) + " install fertig ----")
		dlgi(str(item) + " ist fertig")
		now=timeString()
		self.config[plugin]['installed']=now
		FreeCAD.ParamGet('User parameter:/Plugins/'+plugin).SetString("installdate",now)

		

	def register(self):
		t=FreeCADGui.getMainWindow()
		return
		#
		# deaktivieren
		#
		saye("register menu done")

	def registerPlugin(self,name,method):
		t=FreeCADGui.getMainWindow()
		saye("register menubar")
		pp=t.menuBar()
		found=False
		
		w=FreeCADGui.activeWorkbench()
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
		#p.show()
		
		saye("menubar done")


	def setParams(self):
		ta=FreeCAD.ParamGet('User parameter:Plugins')
		ta.SetString("pluginlist","")
		pluginlist=[]
		for k in self.config.keys():
			if not self.config[k]['status'] == 'ignore':
				t=FreeCAD.ParamGet('User parameter:Plugins/'+k)
				pcm=ConfigManager(k)
				hide=pcm.get('_hide_',False)
				if hide:
					continue
				pluginlist.append(k)
				#say("--")
				#say(k)
				#say(self.config[k])
				#say(self.config[k]["name"])
				t.SetString("name",self.config[k]["name"])
				if self.config[k].has_key("author"): t.SetString("author",self.config[k]["author"])
				t.SetString("destination",self.config[k]["destdir"])
				t.SetInt('installed',1)
				itemlist=[]
				if self.config[k].has_key('menuitems'):
					for menu in self.config[k]['menuitems'].keys():
						#say(menu)
						itemlist.append(menu)
						tm=FreeCAD.ParamGet('User parameter:Plugins/'+k+'/'+menu)
						tm.SetString("exec",self.config[k]['menuitems'][menu]['exec'])
				else:
					#say("keine menuitmes")
					pass
				if self.config[k].has_key('menu'):
					menu=self.config[k]['menu']
					#say(menu)
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
	plulo.start()
	say("gui started")
	FreeCAD.plulo=plulo
#	t=FreeCADGui.getMainWindow()
#	t.workbenchActivated.connect(hello)
#	t.workbenchActivated.connect(starty)
	say("signals activated")


def hello(*args):
	saye("HELLO-----22------------------------------------------------------------")
	FreeCAD.plulo.start()
	
	plulo=pluginloader.PluginLoader()
	say("2")
	plulo.setParams()
	say("3")
	plulo.getParams()
	say("starty done ....")
	
	saye("plulo gestartet")


def initreload(*args): # still bugy
	saye("init reload")
	t=FreeCADGui.getMainWindow()
	t.workbenchActivated.connect(hello)
	t.workbenchActivated.connect(starty)
	saye("done")


#pprint.pprint(config3)
#pprint.pprint(config3['plugins']['defaulttest'])
