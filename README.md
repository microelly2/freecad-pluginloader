# freecad-pluginloader



Install
-------

create /usr/lib/freecad/Mod/plugins

cp pluginloader.py, pluginloaderconfig.yaml, InitGui.py  into this directory

modify pluginloaderconfig.yaml


Use
---

start FreeCAD

A dockwindow will arise.

The first item starts the installer dialog
 
Select the plugins you want to install

Click Button install/update

Configure
---------

The configruation file pluginloaderconfig.yaml

Section plugins

For each plugin create a subsection with its name.

required attributes:

  source

  sourcedir

  destdir






