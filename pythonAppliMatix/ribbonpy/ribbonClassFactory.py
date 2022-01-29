#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


"""\
factory Classes of ribbon:

- define and store commons inherited classes of ribbon etc...
"""

import pprint as PP
import traceback
import json
from PyQt5 import QtCore


from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()

__dictOfRibbonClasses__ = {}

_store = {}

verbose = False
verboseOnInitJson = False


def numerote_lines(aStr):
  lines = aStr.split('\n')
  return "".join(["%4i %s\n" % (i+1, l) for i, l in enumerate(lines)])


def json_loads(aJsonStr):
  try:
    aDict = json.loads(aJsonStr)
    return aDict
  except Exception as e:
    num = numerote_lines(aJsonStr)
    RT.error("Json problem '%s' in (fix it)\n%s" % (e, num))
    return None


class _ribbonBase(object):
  """
  | base of previous elementary widget classes of ribbonpy package
  | begin with _, because have not be instancied directly
  | exists for multiple inheritages as 'class Xxx(QObjet, _ribbonBase)'
  | if done, cause error...
  """
  def __init__(self, *args, **kwargs):
    self.className = self.__class__.__name__
    self.objectNameIni = "%s%s" % (self.className, str(self.index))
    # if verbose: RT.info("_ribbonBase.__init__ %s %s" % (self.__class__.__name__, self.objectNameIni))
    self.setObjectName(self.objectNameIni)
    self.index[0] += 1  # unambigous objectName
    self.prefixShortcut = "Ctrl+"
    self.tabsWidgets = []
    try:  # no valid for QToolButton or else Qt Objects...
      self.setTabPosition(self.North)
      self.setWindowModality(QtCore.Qt.NonModal)
      self.setWindowTitle(self.objectName())
    except:
      pass
    self.args = args
    self.kwargs = kwargs
    if verboseOnInitJson:
      RT.debug("%s:\n  args:\n%s\n  kwargs:\n%s" % (self.objectName(), args, PP.pformat(kwargs)))
    # self.setContentsMargins(1,1,1,1)
    
  def setFromJson(self, valuesJson=None):
    RT.warning("virtual method _ribbonBase.setFromJson: have to be implemented in inherided classes")
    
  def getRibbonPath(self):
    """
    path on ribbonWidget.objectName() as 'root.tutu.truc', without whitespaces
    includes root name, as absolute path
    """
    res = self.objectName()
    parent = self.parent()
    while (parent != None):
      if hasattr(parent, "getRibbonPath"):
        pname = parent.objectName()
        if "//" in pname:
          RT.warning("objectName '%s' with '//' forbidden for RibbonPath, have to fix it" % pname)
          pname.replace("//", "_")
        #if " " in pname:
        #  RT.warning("objectName '%s' with whitespace forbidden for RibbonPath, have to fix it" % pname)
        #  pname.replace(".", "")
        res = pname + "//" + res
      parent = parent.parent()
    RT.debug("getRibbonPath '%s'" % res)
    return res
  
  def getRibbonRoot(self):
    """find maset item of ribbon searching throught parents last getRibbonRoot method"""
    #FAQ 1135 get root ribbon widget from ribbon sub widget
    lastRibbonItem = self
    parent = self.parent()
    while (parent != None):
      if hasattr(parent, "getRibbonRoot"):
        lastRibbonItem = parent
      parent = parent.parent()
    RT.debug("getRibbonRoot of '%s' is '%s'" % (self.getRibbonPath(), lastRibbonItem.objectName()))
    return lastRibbonItem
  
  def getItemFromRibbonPath(self, path, verbose=True):
    """iterative algorithm, not recursive"""
    #FAQ 1140 get sub widget from ribbon path
    res = None
    pathsplit = path.split("//")
    imax = len(pathsplit)
    if imax > 10: 
      RT.warning("ribbon path with too much '//', have to fix it:\n%s" % PP.pformat(pathsplit))
      return None
    currenttab = self
    #print "it",path
    for i in range(imax):
      name = pathsplit[i]
      if name == "": continue # skip if ".toto..tutu.", as 'toto.tutu"
      #print "  ct",name
      if name == currenttab.objectName() and imax == 1:
        return currenttab
      for tab in currenttab.tabsWidgets:
        #print "    ta",tab.objectName(),i,imax
        if tab.objectName() == name:
          currenttab = tab
          if i == imax-1:
            return tab #found item, return
          else:
            continue #not yet found, iterate next i
    if verbose: RT.warning("getItemFromRibbonPath item not found: '%s'" % path)
    return res #not found

  def getAllPathsFromRoot(self):
    #FAQ 1150 get all absolute paths of ribbon sub widgets
    root = self.getRibbonRoot()
    return root.getAllPaths()

  def getAllPaths(self):
    #FAQ 1155 get all relative paths of ribbon sub widgets
    res = [self.getRibbonPath()]
    for t in self.tabsWidgets:
        if hasattr(t, "getAllPaths"):
          res_t = t.getAllPaths()
          res.extend(res_t)
        else:
          res.append(self.getRibbonPath()+"//"+t.objectName()) # leaf as standard qt widget
    return res
    
  def splitPath(self, path):
    """
    returns ('titi', 'toto//tutu//tata') from 'titi//toto//tutu//tata'
    here for EZ convenience
    """
    ps = path.split("//")
    return (ps[0], "//".join(ps[1:]))


  def ggetFromValuesOrDefault(self, valuesJson, tag, default, searchInParents=False):
    """
    search tag in parents if not found
    interprets tag "RibbonWidget//minimumSize" as values["RibbonWidget"]["minimumSize"]
    """
    if "//" in tag:
      RT.error("ggetFromValuesOrDefault( tag '%s' default '%s' in" % (tag, default), valuesJson)
    else:
      # RT.info("getFromValuesOrDefault tag '%s' default '%s' in" % (tag, default), valuesJson)
      pass

    items = tag.split("//")
    # vv = valuesJson
    vv = self.kwargs["setFromJson"]

    #if self.parent() is None:
    #  RT.error("gggget %s parent is" % self, self.parent())
    #  raise Exception("gggget %s parent is None" % self)

    p1 = PP.pformat(valuesJson)
    p2 = PP.pformat(vv)
    if p1 != p2:
      RT.warning("fix it get Json obsolete is", valuesJson)
      RT.warning("have to be equal vv is", vv)
      raise Exception("fix it surprise")

    try:
      for i in items:
        vv = vv[i]
      ok = True
    except:
      ok = False

    if ok:
      # RT.debug("""valuesJson["%s"] found:""" % tag, vv)
      return vv
    else:
      if searchInParents is True:
        return self._getFromValuesInParents(tag, default)
      else:
        return default


  def _getFromValuesInParents(self, tag, default):
    """iterative part of ggetFromValuesOrDefault throught parents"""
    selfcurrent = self
    for i in range(10):  # avoid infinite loop
      parent = selfcurrent.parent()
      if parent is None:
        msg = """valuesJson["%s"] not found in parents""" % tag
        if msg not in _onlyOne:
          RT.error(msg)
          _onlyOne.append(msg)
        return default

      parentJson = parent.kwargs["setFromJson"]
      try:
        res = parent.ggetFromValuesOrDefault(parentJson, tag, "nooothing", searchInParents=False)
      except Exception as e:
        # unkown problem
        RT.error("search in parent unknown problem, default is %s\n%s" % (default, e))
        return default

      if res == "nooothing":
        selfcurrent = parent
        continue
      else:
        # RT.info("search in parent found %s %s" % (tag, res))
        return res

    raise Exception("_getFromValuesInParents nothing todo here")


def appendAllRibbonClasses(localsDictOrlistOfclasses):
  """
  factory pattern using ribbonpy.ribbonClassFactory.__dictOfRibbonClasses__ :
  
  - tricky way to get access to (future) user defined classes, in others packages.
    but it works.
  - with one more line in end of future (...other packages) user files ribbon*.py
    (please use this sort of name)
  
  usage:
  
  >>> #simply add this ended line:
  >>> import ribbonpy.ribbonClassFactory as RCF
  >>> RCF.appendAllClasses( locals() )
  >>> #or
  >>> RCF.appendAllClasses( [oneUserRibbonClass, anotherOneUserRibbonClass,...] )
  >>> #and so associated with
  >>> RCF.getAllRibbonClasses()
  """
  # make user classes widgets known by ribbon factory
  currentlistOfclasses = None
  if isinstance(localsDictOrlistOfclasses, dict):
    keys = [key for key in list(localsDictOrlistOfclasses.keys()) if "Ribbon" in key]
    currentlistOfclasses = [ localsDictOrlistOfclasses[key] for key in keys]
  elif isinstance(localsDictOrlistOfclasses, list):
    currentlistOfclasses = localsDictOrlistOfclasses
  else:
    raise Exception("unknown type for parameter: " + str(type(localsDictOrlistOfclasses)))
  for iclass in currentlistOfclasses:
    name = iclass.__name__
    if name in list(__dictOfRibbonClasses__.keys()):
      raise Exception("appendAllRibbonClasses class known yet: '%s'" % name)
    else:
      RT.debug("appendAllRibbonClasses '%s'" % name)
      __dictOfRibbonClasses__[name] = iclass
  return


def getAllRibbonClasses():
  """
  | factory pattern using ribbonpy.__dictOfRibbonClasses__
  | and so we get a set of All current and user trans-package used ribbon classes
  """
  if __dictOfRibbonClasses__ == {}:
     import ribbonpy.ribbonWidget #a minima standart elementaries classes in ribbonWidgets.py
  return __dictOfRibbonClasses__


def getRibbonClassFromName(nameClass):
  """
  return a class instance from his class name string
  
  usage:
  
  >>> import ribbonpy.ribbonClassFactory as RCF
  >>> aClass = RCF.getXyzClassFromName("UserDefinedRibbonClass")
  >>> anInstance = aClass(setFromJson=aDictFromJsonData)
  """
  # FAQ 1120 create [sub]ribbon empty widget instance with factory

  # dictOfClass something like {"RibbonWidget": ribbonWidget, "RibbonQHBoxLayout": RibbonQHBoxLayout}
  dictOfClass = getAllRibbonClasses()
  if type(nameClass) == dict:  # as an attrib from json
    try:
      aNameClass = nameClass["type"]
    except:
      RT.warning('unknown class in nameClass: %s' % str(nameClass))
      return None
  else:  # as a name str
    aNameClass = nameClass
  try:
    typeClass = dictOfClass[aNameClass]
  except:
    RT.warning('unknown class in getAllRibbonClasses: %s' % aNameClass)
    RT.warning("getRibbonClassFromName %s" % PP.pformat(list(dictOfClass.keys())))
    typeClass = None
  return typeClass

_onlyOne = []


def getFromValuesOrDefault(valuesJson, tag, default):
    """
    interprets tag "RibbonWidget//minimumSize" as values["RibbonWidget"]["minimumSize"]
    """
    if "//" in tag:
      RT.warning("getFromValuesOrDefault tag '%s' default '%s' in" % (tag, default), valuesJson)
    else:
       # RT.info("getFromValuesOrDefault tag '%s' default '%s' in" % (tag, default), valuesJson)
       pass

    items = tag.split("//")
    vv = valuesJson

    try:
      for i in items:
        vv = vv[i]
    except:
      msg = """valuesJson["%s"] not found""" % tag
      if msg not in _onlyOne:
        RT.warning("""%s, default is: '%s'""" % (msg, default))
        _onlyOne.append(msg)

      return default
    RT.debug("""valuesJson["%s"] found: '%s'""" % (tag, str(vv)), valuesJson)
    return vv


def getRibbonInstanceClassFromJson(parent, valuesJson=None):
  """
  valuesJson is (a dict) for initialize instance
  """
  #FAQ 1130 create [sub]ribbon Json initialized widget with factory
  if parent.__class__ in [dict, str]:
    RT.error("getRibbonInstanceClassFromJson needs parent None or inherited QTWidget, not %s" %
             parent.__class__)
  nameClass = getFromValuesOrDefault(valuesJson, "type", None)
  aClass = getRibbonClassFromName(nameClass)
  # RT.debug("getRibbonInstanceClassFromJson: type '%s'" % nameClass)
  if aClass == None:
    return None
  try:
    if valuesJson != None:
      if verboseOnInitJson: RT.debug("getRibbonInstanceClassFromJson with valuesJson")  # ,valuesJson
      anInstance = aClass(parent, setFromJson=valuesJson)
    else:
      if verboseOnInitJson: RT.debug("getRibbonInstanceClassFromJson without! valuesJson")
      anInstance = aClass(parent)
    return anInstance
  except Exception as e:
    RT.error("getRibbonInstanceClassFromJson create instance class '%s'\n%s" % (nameClass, e))
    RT.warning("traceback\n%s" % traceback.format_exc())
    return None
    '''if valuesJson != None:
      raise Exception("Problem create instance class '%s' with valuesJson\n%s" %
                      (nameClass, PP.pformat(valuesJson)))
    else:
      raise Exception("Problem create instance class '%s' with no valuesJson" % nameClass)'''


def getExampleJsonRibbon():
  a = getExampleJsonRibbon0()
  b = getExampleJsonRibbon2()
  a["tabs"].extend(b["tabs"])
  return a


def getExampleJsonRibbon0():
  """return dict from Json, so could be EZ direct python code..."""
  #FAQ 0200 example of Json data for an example of ribbonWidget
  RT.warning("TODO getExampleJsonRibbon0: only for example")
  aJsonStr = """
{
  "name": "test_Ribbon_0",
  "type": "RibbonWidget",
  "minimumSize": [200,100],
  "tabPosition": "North",
  "backgroundColor": "#EEddEE",
  "fontSize": 9,
  "actionButtonSize": [20, 25],
  "smallWidget": { "name": "exampleSmallWidget", "type": "RibbonExampleSmallWidget" },
  "tabs": [
    { "name": "Edit",
      "type": "RibbonQHBoxLayout",
      "tabs": [
        { "name": "example0", "type": "RibbonActionButton"},
        { "name": "example8", "type": "RibbonActionButton"},
        { "name": "example9", "type": "RibbonActionButton"}
      ]
    },
    { "name": "Other",
      "type": "RibbonQGridLayout",
      "gridSize": [2,4],
      "tabs": [
        { "name": "example1", "type": "RibbonActionButton"},
        { "name": "example2", "type": "RibbonActionButton"},
        { "name": "example3", "type": "RibbonActionButton"},
        { "name": "example4", "type": "RibbonActionButton"},
        { "name": "example5", "type": "RibbonActionButton"},
        { "name": "example6", "type": "RibbonActionButton"},
        { "name": "separator",
          "type": "RibbonQHBoxLayout",
          "tabs": []
        }
      ]
    },
    { "name": "Advanced",
      "type": "RibbonQHBoxLayout",
      "lineSplitter": "yes",
      "tabs": [
        { "name": "Other1",
          "type": "RibbonQGridLayout",
          "gridSize": [2,3],
          "tabs": [
            { "name": "example1", "type": "RibbonActionButton"},
            { "name": "example2", "type": "RibbonActionButton"},
            { "name": "example3", "type": "RibbonActionButton"},
            { "name": "example4", "type": "RibbonActionButton"},
            { "name": "example5", "type": "RibbonActionButton"},
            { "name": "example6", "type": "RibbonActionButton"}
          ]
        },
        { "name": "Other2",
          "type": "RibbonQGridLayout",
          "gridSize": [2,3],
          "tabs": [
            { "name": "example1", "type": "RibbonActionButton"},
            { "name": "example2", "type": "RibbonActionButton"},
            { "name": "example3", "type": "RibbonActionButton"},
            { "name": "example4", "type": "RibbonActionButton"},
            { "name": "example5", "type": "RibbonActionButton"},
            { "name": "example6", "type": "RibbonActionButton"}
          ]
        },
        { "name": "Other3",
          "type": "RibbonQGridLayout",
          "gridSize": [1,6],
          "tabs": [
            { "name": "example1", "type": "RibbonActionButton"},
            { "name": "example2", "type": "RibbonActionButton"},
            { "name": "example3", "type": "RibbonActionButton"},
            { "name": "example4", "type": "RibbonActionButton"},
            { "name": "example5", "type": "RibbonActionButton"}
          ]
        }
      ]
    }
  ]
}"""
  return json_loads(aJsonStr)


def getExampleJsonRibbon1():
  import json
  aJsonStr = """
{
  "name": "test_Ribbon_1",
  "type": "RibbonWidget",
  "minimumSize": [200, 100],
  "tabPosition": "North",
  "backgroundColor": "#EEddEE",
  "tabs": [
    { "name": "Edit",
      "type": "RibbonQHBoxLayout"
    }
  ]
}"""
  return json_loads(aJsonStr)

def getExampleJsonRibbon2():
  import json
  aJsonStr = """
{
  "name": "test_Ribbon_2",
  "type": "RibbonWidget",
  "minimumSize": [200, 100],
  "tabPosition": "North",
  "backgroundColor": "#EEddEE",
  "tabs": [
    { "name": "Widgets",
      "type": "RibbonQHBoxLayout",
      "lineSplitter": "yes",
      "tabs": [

        { "name": "Widet1",
          "type": "RibbonQGridLayout",
          "gridSize": [3,1],
          "tabs": [

            { "name": "Combo1",
              "tooltip": "tooltip for RibbonQComboBox1",
              "type": "RibbonQComboBox",
              "items": ["hello", "bonjour", "buenos dias"]
            },
            { "name": "Combo2",
              "tooltip": "tooltip for RibbonQComboBox2",
              "type": "RibbonQComboBox",
              "items": ["bye", "au revoir", "hasta la vista"]
            },
            { "name": "Combo3",
              "tooltip": "tooltip for RibbonQComboBox3",
              "type": "RibbonQComboBox",
              "items": ["hi", "salut", "hola"]
            }

          ]
        },

        { "name": "Widget2",
          "type": "RibbonQGridLayout",
          "gridSize": [3,2],
          "tabs": [

            { "name": "Check1",
              "tooltip": "tooltip for RibbonQCheckBox1",
              "type": "RibbonQCheckBox",
              "text": "check1 text"
            },
            { "name": "Check2",
              "tooltip": "tooltip for RibbonQCheckBox2",
              "type": "RibbonQCheckBox",
              "text": "check2 text"
            },
            { "name": "Check3",
              "tooltip": "tooltip for RibbonQCheckBox3",
              "type": "RibbonQCheckBox",
              "text": "check3 text"
            },
            { "name": "Check5",
              "tooltip": "tooltip for RibbonQCheckBox5",
              "type": "RibbonQCheckBox",
              "text": "check5 text more and more"
            },
            { "name": "Edit6",
              "tooltip": "tooltip for RibbonQLineEdit6",
              "type": "RibbonQLineEdit",
              "text": "Edit me!"
            },
            { "name": "Edit7",
              "tooltip": "tooltip for RibbonQLineEdit6",
              "type": "RibbonQLabel",
              "text": "a text for label...."
            }

          ]
        },
        
        { "name": "Widget3",
          "type": "RibbonQGridLayout",
          "gridSize": [6,1],
          "tabs": [
            { "name": "LabelEdit8",
              "type": "RibbonFormLayoutQLineEdit",
              "tooltip": "tooltip for RibbonFormLayout8",
              "tabs": [
                { "name": "edit1", "label": "label 1 long", "text": "edit me 1 looooooooong" },
                { "name": "edit2", "label": "label 2", "text": "edit me 2" },
                { "name": "edit3", "label": "label 3", "text": "edit me 3" },
                { "name": "edit4", "label": "label 4", "text": "edit me 4" },
                { "name": "edit5", "label": "label 5", "text": "edit me 5" }
              ]
            }
          ]
        }
      ]
    }
  ]
}"""
  return json_loads(aJsonStr)

"""
            { "name": "Edit8",
              "type": "RibbonQVBoxLayout",
              "tabs": [
              
                { "name": "LabelEdit7",
                  "tooltip": "tooltip for RibbonQLineEdit7a",
                  "type": "RibbonQLabel",
                  "text": "edit7 label"
                },
                { "name": "lineEdit7",
                  "tooltip": "tooltip for RibbonQLineEdit7b",
                  "type": "RibbonQLineEdit",
                  "text": "Edit me!"
                }
              
              ]
            }
"""


def store_deleteLater():
  for k, v in _store.items():
    try:
      if "test_" in k:
        RT.info("RCF store_deleteLater %s" % k)
        # RT.scrute("deleteLater %s" % k, v)
        v.deleteLater()
    except Exception as e:
      RT.error("RCF deleteLater %s, %s" % (k, e))
      pass


def test_RibbonExample():
  import ribbonpy.ribbonQMainWindow as RQM

  aJsonValue = getExampleJsonRibbon()
  fen = RQM.QMainWindowForRibbon(setFromJson=aJsonValue)
  fen.show()
  # avoid garbage collecting as desktop may be not existing as not parent
  _store["test_RibbonExample"] = fen
  return fen



