## -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import  find_packages
setup(
    name="qiu_utils",
    version='1.0.1',
    description='工作中相关的一些定义以及一些常用函数封装',
    author='qiufengfeng',
    author_email='544855237@qq.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={'qiu_utils': ['data/*']},
    license='LGPL',
)