#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END

"""\
class for ribbon prototype managing log operations
(CRITICAL ERROR WARNING INFO STEP TRACE DEBUG)
for now (temporary or not) get singleton logger matix or iradina
"""

__pushpopLevels__ = [] # singleton mutable
_currentLogger = []    # singleton mutable

def getLoggerRibbon():
  if len(_currentLogger) == 0: #do only one time
    # set salome_custom if present
    try:
      from salome_custom import simple_log
      return simple_log
    except:
      pass

    try:
      import iradinapy.loggingIra as LOG
    except:
      import xyzpy.loggingXyz as LOG

    # print("getLoggerRibbon LOG.__file__ %s" % LOG.__file__)
    logger = LOG.getLogger()
    _currentLogger.append(logger)
    logger.debug("get ribbon logger %s" % logger.name)
    return logger
  else:
    return _currentLogger[0]

def setLevel(level):
  getLoggerRibbon().setLevel(level)

def pushLevel(level):
  __pushpopLevels__.append(getLoggerRibbon().level)
  setLevel(level)

def popLevel(warning=True):
  if len(__pushpopLevels__) > 0:
    level = __pushpopLevels__.pop()
    try:
      if "Level" in level: # python 3 may be 'Level 123' if level numeric as not in levels
        level = level.split()[1]
    except: # python 2 may be integer 123 if level numeric as not in levels
      pass
    setLevel(level)
  else:
    if warning:
      getLoggerRibbon().warning("Pop logger level empty")
