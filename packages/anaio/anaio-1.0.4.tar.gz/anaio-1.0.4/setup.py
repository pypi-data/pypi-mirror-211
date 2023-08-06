#!/usr/bin/env python
# encoding: utf-8
"""
setup.py -- setup file for the anaio module
"""
import numpy
from os import path
from numpy.distutils.core import setup, Extension

with open(path.join(path.dirname(__file__), 'README.md'), 'r') as file:
    long_description = file.read()


module_anaio = Extension('_anaio',
                         define_macros=[('MAJOR_VERSION', '1'),
                                        ('MINOR_VERSION', '0')],
                         include_dirs=[numpy.get_include()],
                         extra_compile_args=["-O2", "-ffast-math"],
                         extra_link_args=None,
                         sources=['src/_anaio.c',
                                  'src/anarw.c',
                                  'src/anacompress.c',
                                  'src/anadecompress.c'])

setup(name='anaio',
      version='1.0.4',
      description='Python library for ANA f0 file I/O',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Johannes Hoelken',
      author_email='hoelken@mps.mpg.de',
      url='https://gitlab.gwdg.de/hoelken/anaio',
      license="MIT",
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'
      ],
      # This is for the python wrapper module:
      package_dir={'anaio': 'anaio'},
      packages=['anaio'],
      ext_package='anaio',
      # Python dependency
      install_requires=['wheel', 'setuptools', 'numpy'],
      setup_requires=['wheel', 'setuptools', 'numpy'],
      requires=['wheel', 'setuptools', 'numpy'],
      # This is for the C module
      ext_modules=[module_anaio])
