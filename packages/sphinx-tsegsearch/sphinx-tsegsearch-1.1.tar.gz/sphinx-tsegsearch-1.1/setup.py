# coding: utf-8
"""
sphinx-tsegsearch
===================

A Sphinx extension for tokenize japanese query word with TinySegmenter.js

This extension tweaks searchtools.js of sphinx-generated html document
to tokenize Japanese composite words.

Since Japanese is an agglutinative language, query word for document search
usually becomes composite form like 'システム標準' (system standard).
This makes difficult to search pages containing phrase such as
'システムの標準', '標準システム', because TinySegmenter.py (Sphinx's default
Japanese index tokenizer) tokenizes 'システム' and '標準' as indexes.

sphinx-tsegsearch patches searchtools.js to override query tokinization
step so that query input is re-tokenized by TinySegmenter.js (original
JavaScript implementation of TinySegmenter).
As a result, roughly say, this tiny hack improves recall of Japanese
document search in exchange of precision.

Usage:

#. Add 'sphinx_tsegsearch' in conf.extensions
#. Rebuild document.

"""
from setuptools import setup, find_packages
from codecs import open
from os import path
import sys


setup(
    name='sphinx-tsegsearch',
    version='1.1',
    description='Sphinx extension to split searchword with TinySegmenter',
    long_description=sys.modules['__main__'].__doc__,
    url='https://github.com/whosaysni/sphinx-tsegsearch',
    author='Yasushi Masuda',
    author_email='whosaysni@gmail.com',
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation :: Sphinx',
    ],
    keywords='sphinx, japanese, word segmentation, search',
    packages=['sphinx_tsegsearch'],
    package_dir={'sphinx_tsegsearch': 'sphinx_tsegsearch'},
    package_data={
        'sphinx_tsegsearch': ['static/*', 'templates/*'],
    },
    install_requires=['docutils', 'sphinx']
)
