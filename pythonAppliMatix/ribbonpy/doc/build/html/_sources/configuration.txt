.. _configuration: 

Package Ribbonpy configuration
=================================

This package *could be* a package python, setup.py is not instancied yet, waiting for v1.0.0.

see https://python-packaging.readthedocs.org/en/latest/minimal.html

Get ribbonpy package
-----------------------

At cea/lgls

>>> export MYDIR = `pwd`
>>> git clone /home/matix/GitRepo/ribbonpy.git


Initialise environment
-----------------------

set variable PYTHONPATH

>>> cd $MYDIR/ribbonpy
>>> export PYTHONPATH=`pwd`:$PYTHONPATH


View some ribbon widget example
--------------------------------

>>> cd $MYDIR/ribbonpy/ribbonpy
>>> ribbonWidget.py
>>> ribbonQMainWindow.py

Why *ribbonpy/ribbonpy* ?: the answer is funniest...

see https://python-packaging.readthedocs.org/en/latest/minimal.html

Launch all tests
-------------------

>>> cd $MYDIR/ribbonpy
>>> AllTestLauncher

If binding PyQt4, and more tricks
see file $MYDIR/ribbonpy/README_ribbon.txt

FAQ In Code
------------

Is a programmer FAQ, not a python newbie FAQ.

For a prototype implementation, often modified, 
this packages uses a *Frequently Asked Questions In Code* method.
Questions *are* in the source files code, 
found with a special tag, only one line by question.
Answers are obviously below question, as comment, *or* as code itself.
An indice allow to sort question as a list.
In *future*, automatic dynamic links could be generated in html documentation.

Usage
............

User can reach questions (and answers) in kate with "Find In File" string "#FAQ "

Another way, the user could type in a console a grep-sort command:

>>> cd $MYDIR/ribbonpy
>>> find . -name "*.py" -exec grep -Hni "#FAQ " {} \; | sort -n -k 2.2

A python script exists for EZ better listing format:

>>> cd $MYDIR/ribbonpy
>>> ./faqic


Display the questions, obtain link to reach answer, which is obviously below the tag in file.

Tags Numerotation
...................

0000 to 9999, is a convention:

- 0000-0999  user choice, pertinent question
- 1000-2999  methods
- 3000-3900  classes
- 4000-5900  annexes, not really pertinent


This Documentation configuration
=================================

Fichier Sphinx conf.py
----------------------

Sphinx generates html files from initial configuration file
 `<../../source/conf.py>`_. and .rst files in `<../../source>`_/

Other existing themes
----------------------

* agogo
* bizstyle
* classic
* epub
* haiku
* nature
* pyramid
* scrolls
* sphinxdoc
* traditional


see http://sphinx-doc.org/theming.html#builtin-themes