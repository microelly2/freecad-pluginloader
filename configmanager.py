# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- configuration loader
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD

class ConfigManager():

	def __init__(self,name):
		if name=='':
			self.name="Plugins"
		else:
			self.name="Plugins/"+name

	def get(self,param,default,defaultWindows=None,defaultMac=None):
		if not defaultWindows:
			defaultWindows=default
		if not defaultMac:
			defaultMac=default
		if default.__class__ == int:
			v=FreeCAD.ParamGet('User parameter:'+self.name).GetInt(param)
			if not v:
				FreeCAD.ParamGet('User parameter:'+self.name).SetInt(param,default)
		if default.__class__ == float:
			v=FreeCAD.ParamGet('User parameter:'+self.name).GetFloat(param)
			if not v:
				FreeCAD.ParamGet('User parameter:'+self.name).SetFloat(param,default)
		if default.__class__ == str:
			v=FreeCAD.ParamGet('User parameter:'+self.name).GetString(param)
			if not v:
				FreeCAD.ParamGet('User parameter:'+self.name).SetString(param,default)
		if default.__class__ == bool:
			v=FreeCAD.ParamGet('User parameter:'+self.name).GetBool(param)
			if not v:
				FreeCAD.ParamGet('User parameter:'+self.name).SetBool(param,default)
		if not v:
			v=default
		return v
