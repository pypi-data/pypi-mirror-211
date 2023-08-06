# -*- coding: utf-8 -*-
#! anaconda create -n CLPU python=3.5 && conda activate CLPU && pip install .
"""
This is the setup file for pythonic CLPU utilities.

project             standardized modules for often used python functions at CLPU
acronym             pyCLPU
created on          2022-01-01 00:00:00

@author             Micha (MEmx), CLPU, Villamayor, Spain
@moderator          Eduardo, CLPU, Villamayor, Spain
@updator            Diego (MEmx), CLPU, Villamayor, Spain
            
@contact            mehret@clpu.es

interpreter         python > 3.5
version control     git
url                 https://git.clpu.es/mehret/pyclpu

requires explicitely {
 - setuptools
 - glob
}

execute installation via {
  > pip install .
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/MODULE.py))
  sys.path.append(os.path.abspath(root))
  import MODULE
  from importlib import reload 
  reload(MODULE)
}

"""

# credits to https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

from setuptools import setup

import glob

setup(\
    name="pyclpu",\
    description='CLPU Utilities',\
    author='Michael Ehret',\
    author_email='mehret@clpu.es',\
    url='https://git.clpu.es/mehret/pyclpu',\
    license='MIT',\
    packages=['pyclpu'],
    scripts=glob.glob("pyclpu/*.py"),
    install_requires=[\
        'numpy','scipy',\
        'matplotlib',\
    ],\
    # and build in modules cython, importlib.reload, inspect.getsourcefile, glob, math, opencv, pillow, os, sys, time, warnings
    classifiers=[\
        'Development Status :: 1 - Planning',\
        'Intended Audience :: Science/Research',\
        'Programming Language :: Python :: 3.5',\
    ],\
)