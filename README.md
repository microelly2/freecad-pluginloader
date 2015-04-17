# freecad-pluginloader



Install

create directory ~/.FreeCAD/pluginloader
cp pluginloader.py, pluginloaderconfig.yaml into this directory
modify pluginloaderconfig.yaml


Use

start FreeCAD
Python console:
import pluginloader

A dialog will arise. 
Select the plugins you want to install
Click Button install/update


The configruation file pluginloaderconfig.yaml

Section plugins

For each plugin create a subsection with its name.
required attributes:
  source
  sourcedir
  destdir






