# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- macro manager
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


__Vers__ = '0.1b'
__Status__ = 'alpha'

import FreeCAD,PySide,os,FreeCADGui,time
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
import os,re, ast, _ast 

from configmanager import ConfigManager
cm=ConfigManager("MacroManager")
dir_name=cm.get('macrodir',"/usr/lib/freecad/Mod/plugins/FreeCAD-macros")

docstrings=['__Author__','__Version__','__Comment__','__Wiki__','__Icon__','__Help__']



def getplugin(name=''):
#	''' read the file filenam and create the parsetree '''

	# test data
	if False:
		content='''
		
__Comment__ = 'My macro is a super macro and can be used whenever other macros fail '
__Web__ = "http://forum.freecadweb.org/viewtopic.php?f=8&t=11302"
__Wiki__ = "http://www.freecadweb.org/wiki/index.php?title=Macro_FreeCAD_to_Kerkythea"
__Icon__  = "Part_Common.svg"
__Help__ = "This is the help text of this macro"
__Author__ = "Freek Ad"
__Version__ = 0.1
__Status__ = 'alpha'
__Requires__ = ''

'''
	else:
		content=open(name).read()
	tree = ast.parse(content)
	try:
		# astpp found here
		# http://alexleone.blogspot.de/2010/01/python-ast-pretty-printer.html
		import astpp
		print astpp.dump(tree)
	except:
		pass
	return tree

def getplugindata(files):
	plugindata={}
	for plin in files:
		#print plin
		tree=getplugin(plin)
		doc={}
		for id in docstrings:
			doc[id]=""
		for k in tree.body:
			try:
				for t in k.targets:
					if t.id in docstrings:
						print t.lineno
						print t.id
						if k.value.__class__ == _ast.Str:
							v=k.value.s
						elif k.value.__class__ == _ast.Num:
							v=k.value.n
						elif k.value.__class__ == _ast.Name:
							v=k.value.id
						doc[t.id]=v
			except:
				pass
		plugindata[plin]=doc
	return plugindata


def findfiles(dir_name):
	macrofiles=[]
	for root, dirs, files in os.walk(dir_name, topdown=False):
		print('Found directory: %s' % root)
		for fname in files:
			print('\t%s' % fname)		
			if re.search('\.FCMacro$', fname):  
				s=root+'/'+fname
				macrofiles.append(s)
	print macrofiles
	return macrofiles


def myclick(ak,n):
	FreeCAD.Console.PrintMessage( str(n) + ' '+ str(ak.obj) + "\n")


def layout(widget,files,plugindata):	
	zz=[]
	n=0
	for fe in files:
		print fe
		n += 1
		author=plugindata[fe]['__Author__']
		comment=plugindata[fe]['__Comment__']
		ic=plugindata[fe]['__Icon__']
#		print fe,plugindata[fe]
		base=os.path.basename(fe)
		st=base.upper() + '  ------  '
		if author:
			st += ' ---------  AUTHOR: ' +author
		if comment:
			st += ' COMMENTS:' + comment
		st +=  ' PATH:'  + fe
		ak2 = QtGui.QPushButton(QtGui.QIcon(ic), st  )
		ak2.obj=fe
		ak2.clicked.connect(lambda ak=ak2, arg=n: myclick(ak,arg))
		zz.append(ak2)
		widget.lay.addWidget(ak2)
	return zz



class Widget(QWidget):

	def __init__(self, parent= None):
		super(Widget, self).__init__()
		self.setStyleSheet("QPushButton { text-align:left;background-color: lightblue;text-align:left;}")
		self.setWindowTitle("Macro Manager " + __Vers__)
		self.setObjectName("MacroManager")
		#Container Widget       
		widget = QWidget()
		#Layout of Container Widget
		layout = QVBoxLayout(self)
		layout.setSpacing(0)
		layout.setAlignment(QtCore.Qt.AlignTop)
		self.lay=layout
		widget.setLayout(layout)
		scroll = QScrollArea()
		#scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		#scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scroll.setWidgetResizable(True)
		scroll.setWidget(widget)
		 
		#Scroll Area Layer add
		vLayout = QVBoxLayout(self)
		vLayout.addWidget(scroll)
		self.setLayout(vLayout)

def macroManager():
		files=findfiles(dir_name)
		plugindata=getplugindata(files)
		print plugindata
		ww= Widget()
		buttonlist=layout(ww,files,plugindata)
		ww.show()
		return ww

t=macroManager()
