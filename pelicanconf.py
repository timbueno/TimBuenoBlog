#!/usr/bin/env python
from __future__ import unicode_literals

AUTHOR = 'Tim Bueno'
SITENAME = 'Tim Bueno'
SITEURL = 'http:/www.timbueno.com'
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

# Theme
THEME = '/Users/timbueno/Dropbox/Blog/themes/mythemes/timbueno'
# THEME = '/root/Dropbox/Blog2/themes/pelican-mockingbird'

SUMMARY_MAX_LENGTH = 50

FILES_TO_COPY = (('extras/robots.txt', 'robots.txt'),)
DELETE_OUTPUT_DIRECTORY = True

GOOGLE_ANALYTICS = 'UA-32818972-1'

# RSS / Atom feed settings
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_MAX_ITEMS = 10

USE_FOLDER_AS_CATEGORY = False

# Blogroll
#LINKS =  (('Github', 'http://www.github.com/timbueno'),)

# Social widget
SOCIAL = (('Twitter', 'http://www.twitter.com/timbueno'),
		  ('Github', 'http://www.github.com/timbueno'),)

DEFAULT_PAGINATION = 5
RELATIVE_URLS = True

# Permalink Structure of posts
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_LANG_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_LANG_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}.html'

PAGE_URL = '{slug}'
PAGE_LANG_URL = '{slug}-{lang}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_LANG_SAVE_AS = '{slug}-{lang}.html'
