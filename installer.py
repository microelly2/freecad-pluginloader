# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- plugin loader
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

# 

source='https://github.com/microelly2/freecad-pluginloader/archive/master.zip'
zipfilename='/tmp/tt.zip'
storedir='/tmp/tt'

import  os, urllib, shutil

def st1():
	tg=urllib.urlretrieve(source,zipfilename)
	fh = open(zipfilename, 'rb')
	zfile = zipfile.ZipFile(fh)
	zfile.extractall(storedir)
	path0=storedir+'/freecad-pluginloader-master/'
	for path, dirs, files in os.walk(path0):
		rp= path.replace(path0,'')
		directory='/usr/lib/freecad/Mod/pluginloader2/' + rp
		if not os.path.exists(directory):
			os.makedirs(directory)
		for f in files:
			shutil.move(path + "/"+ f, directory+'/' + f)


