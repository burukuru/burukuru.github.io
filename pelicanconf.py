#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Thanh'
SITENAME = u'Cloud Magic'
SITEURL = 'https://thanhpham.cloud'
PATH = 'content'
STATIC_PATHS = ['upload']
ARTICLES_PATHS = ['upload']

EXTRA_PATH_METADATA = {
    'upload/CNAME': {'path': 'CNAME'},
    }

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Links
LINKS = ()

# Social
SOCIAL = (('github', 'https://github.com/burukuru'),
	('linkedin', 'https://www.linkedin.com/in/thanh-pham-cloud/'),
	('medium', 'https://medium.com/@burukuru'),
	('twitter', 'https://twitter.com/burukuru'),
	('flickr', 'https://flickr.com/burukuru'),
	)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = 'Flex'
SITETITLE = 'Cloud Magic'
SITELOGO = 'https://thanhpham.cloud/upload/profile.jpg'
MAIN_MENU = True
MENUITEMS = (('Categories','categories.html'),
	('Tags','tags.html'),
	)
