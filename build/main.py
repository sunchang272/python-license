# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: python-auth
File Name: main.py
Author: sunch
Create Date: 2021/11/12 13:48 
-------------------------------------------------
"""

# python main.py build_ext --inplace
from Cython.Build import cythonize
from distutils.core import setup

setup(
  name='duty-back',
  ext_modules=cythonize([
    '../server/gui.py',
    '../server/func.py',
    '../client/license_getter.py',
    '../client/license_verifier.py'
  ]),
)
