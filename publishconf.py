#!/usr/bin/env python
# publishconf.py — usar antes de subir pro servidor
# Comando: pelican content -s publishconf.py

from pelicanconf import *

SITEURL = 'https://chiicones.github.io/'
RELATIVE_URLS = False

FEED_ALL_ATOM      = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True
