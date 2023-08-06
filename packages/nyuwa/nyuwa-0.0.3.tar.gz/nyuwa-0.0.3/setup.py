#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: gisok
# Mail: gisok@126.com
# Created Time:  2022.3.2
#############################################
import os
path = os.path.abspath(os.path.dirname(__file__))

try:
  with open(os.path.join(path, 'README.md')) as f:
    long_description = f.read()
except Exception as e:
  long_description = "GIS 算法。待扩展。"
  
from setuptools import setup, find_packages

setup(
    name = "nyuwa", 
    version = "0.0.3",
    keywords = ("pip", "nyuwa","featureextraction"),
    description = "GIS 算法",
    long_description = long_description,
    long_description_content_type='text/markdown',
    license = "MIT Licence",
    python_requires=">=3.5.0",

    url = "https://github.com/",     #项目相关文件地址，github
    author = "gisok",
    author_email = "gisok@126.com",
    
    # exclude=['nyuwa', 'nyuwagis']
    packages = find_packages(),
    include_package_data = True,
    
    platforms = "any",
    install_requires = ["numpy"]      #第三方库
)
