# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- plugin loader
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

#  first install

source='https://github.com/microelly2/freecad-pluginloader/archive/master.zip'
import os, tempfile
d=tempfile.mktemp()
os.makedirs(d)
fn = tempfile.mktemp(dir=d)

zipfilename=fn+'.zip'
storedir=fn

import  os, urllib, shutil,zipfile

def st1():
	tg=urllib.urlretrieve(source,zipfilename)
	fh = open(zipfilename, 'rb')
	zfile = zipfile.ZipFile(fh)
	zfile.extractall(storedir)
	path0=storedir+'/freecad-pluginloader-master/'
	for path, dirs, files in os.walk(path0):
		rp= path.replace(path0,'')
		directory=FreeCAD.ConfigGet('AppHomePath')+'/Mod/plugins/' + rp
		print directory
		if not os.path.exists(directory):
			os.makedirs(directory)
		print files
		for f in files:
			shutil.move(path + "/"+ f, directory+'/' + f)
	print zipfilename
	print storedir
		

st1()

