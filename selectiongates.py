

import FreeCAD
import FreeCADGui as Gui


class FGate:
  def allow(self,doc,obj,sub):
    return (sub[0:4] == 'Face')

class VGate:
  def allow(self,doc,obj,sub):
    return (sub[0:6] == 'Vertex')

class EGate:
  def allow(self,doc,obj,sub):
    return (sub[0:4] == 'Edge')


def fselect():
	Gui.Selection.addSelectionGate(FGate())
	FreeCAD.Console.PrintWarning("Face Select Mode\n")

def vselect():
	Gui.Selection.addSelectionGate(VGate())
	FreeCAD.Console.PrintWarning("Vertex Select Mode\n")

def eselect():
	Gui.Selection.addSelectionGate(EGate())
	FreeCAD.Console.PrintWarning("Edge Select Mode\n")


def clear():
	Gui.Selection.removeSelectionGate()
	FreeCAD.Console.PrintWarning("Free Select\n")


'''	
import selectiongates

selectiongates.eselect()
selectiongates.clear()
'''
