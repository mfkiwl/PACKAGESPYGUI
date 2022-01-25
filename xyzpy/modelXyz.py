#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END

__all__=[]

import xyzpy.utilsXyz as UXYZ
import xml.etree.ElementTree as ET

verbose = False
verboseEvent = False

########################################################################################
class ModelSimpleXyz(object):
  """
  a simple model, ONLY for example test.
  inherits object, without nothing else to answer request
  user HAVE TO USE BaseFreeXyz _XyzConstrainBase
  """
  index = [0] #unambigous objectName
  
  def __init__(self, nameObject=""):
    self._objectName = "ModelSimpleXyz"+str(self.index)
    self.index[0] += 1 #unambigous objectName
    self._lastReceiveRequest = None #firstly only for unittest
    if nameObject != "": self._objectName = nameObject
    self._controller = None
  
  def setController(self, controller):
    """really could be None if no use in view without MVC pattern"""
    if self._controller == None:
      self._controller = controller
      return
    raise Exception("ModelSimpleXyz.setController done yet for %s as %s" % (self.objectName(), self.getController().objectName()))

  def getController(self):
    return self._controller

  def objectName(self):
    """as Qt objectName"""
    return self._objectName
    
  def toXml(self, **kwargs):
    """kwarg are for optional future option of added details in xml tree"""
    #return UXYZ.toXml(self, **kwargs)
    res = ET.Element("ModelSimpleXyz")
    res.text = "...TODO..."
    return res

  def lastReceiveRequest(self):
    """#firstly only for unittest"""
    return self._lastReceiveRequest
    
  def receiveRequestToModel(self, strXmlRequest):
    """
    asynchronous treatment of a request from a Controller requestToModelSignal QtCore.pyqtSignal
    
    in aController.setModel():
    aController.requestToModelSignal.connect(aModel.receiveRequestToModel)
    
    in aController.sendRequestToController():
    aController.requestToModelSignal.emit(strXmlRequest)
    
    in aView:
    controller = aView.getController()
    aRequest = controller.getRequest("modification") #for example
    aRequest.xmlModel = aView.xmlData #for example
    controller.sendRequestToController(aRequest).getController().
    """
    if verbose: 
      print("ModelSimpleXyz %s receiveRequestToModel:\n" % self.objectName(), strXmlRequest)
    elif verboseEvent: 
      print("ModelSimpleXyz %s receiveRequestToModel" % self.objectName())
    else:
      pass
    self._lastReceiveRequest = strXmlRequest #firstly only for unittest
    aRequest = UXYZ.fromXml(strXmlRequest)
    #print "receiveRequestToModel \n%s\n%s"% (strXmlRequest, aRequest)
    if "TestRequestFromView" in aRequest.typeRequest: #reply the request to views (for test)
      res = self.getController().sendRequestToViews(aRequest)
      if not res: print("ModelSimpleXyz.receiveRequestToModel: Problem in TestRequestFromView")
    return True
