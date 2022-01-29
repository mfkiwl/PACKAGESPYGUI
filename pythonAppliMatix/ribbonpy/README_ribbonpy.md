
### Example elementary

```
def test_010():
  import ribbonpy.ribbonQMainWindow as RQM
  import ribbonpy.ribbonClassFactory as RCF
  aJsonValue = RCF.getExampleJsonRibbon()
  fen = RQM.QMainWindowForRibbon(setFromJson=aJsonValue)
  fen.show()
  return fen

fen = test_010()
```


### launch unittests

Prerequisite Salome_960 and + (as python3)

```
bash
salome shell
# to get ribbonpy
cd .../PACKAGESPY
# test ribbonpy
./AllTestLauncher.sh pythonAppliMatix/ribbonpy "test_*.py"
```

```
bash
/volatile2/christian/COMBS_STANDALONE/SALOME-9.6.0-CO7-SRC/salome shell
export PACKAGESPY_ROOT_DIR="/volatile2/christian/COMBS_STANDALONE/PACKAGESPY"
export PYTHONPATH=${PACKAGESPY_ROOT_DIR}:${PYTHONPATH}
cd ${PACKAGESPY_ROOT_DIR}
pwd
./AllTestLauncher.sh pythonAppliMatix/ribbonpy "test_*.py"
```