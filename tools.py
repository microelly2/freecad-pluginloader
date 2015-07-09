

import FreeCAD,PySide,os,FreeCADGui,time, sys,traceback
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 

global myDialog,say,myDialoge

def say(s):
	FreeCAD.Console.PrintMessage(str(s)+"\n")

def saye(s):
	FreeCAD.Console.PrintError(str(s)+"\n")



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
