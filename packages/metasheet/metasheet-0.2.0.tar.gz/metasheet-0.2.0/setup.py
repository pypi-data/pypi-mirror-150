#!/usr/bin/env python
#
# References:
# https://setuptools.pypa.io/en/latest/userguide/index.html
# https://setuptools.pypa.io/en/latest/userguide/quickstart.html#including-data-files
# https://packaging.python.org/en/latest/guides/using-manifest-in/
# https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
#

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='metasheet',  # Required
    version='0.2.0',  # Required
    description='Metasheet parser, serializers, and repository manager',
    #url='https://github.com/mtna/metasheet',
    author='Pascal Heus',
    author_email='pascal.heus@mtna.us',
    packages=find_packages(),
    include_package_data=True,
    scripts=['bin/metasheet'],
    install_requires=['openpyxl','python_dateutil'],
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    project_urls={  # Optional
        'Maintainer': 'http://www.mtna.us',
    }
    )


