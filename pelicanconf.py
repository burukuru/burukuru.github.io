#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Thanh'
SITENAME = u'Cloud Magic'
SITEURL = 'https://thanhpham.cloud'
TIMEZONE = 'Europe/London'
DEFAULT_PAGINATION = 10

DEFAULT_LANG = u'en'
DEFAULT_METADATA = {
        'status': 'draft',
        }

PATH = 'content'
STATIC_PATHS = ['upload']
ARTICLES_PATHS = ['upload']

EXTRA_PATH_METADATA = {
        'upload/CNAME': {'path': 'CNAME'},
        }

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Links
LINKS = ()

# Social
SOCIAL = (
        ('github', 'https://github.com/burukuru'),
        ('linkedin', 'https://www.linkedin.com/in/thanh-pham-cloud/'),
        ('medium', 'https://medium.com/@burukuru'),
        ('twitter', 'https://twitter.com/burukuru'),
        ('flickr', 'https://flickr.com/burukuru'),
        )

GOOGLE_ANALYTICS = "UA-165492269-1"

# Flex configuration
THEME = 'Flex'
SITETITLE = 'Cloud Magic'
SITELOGO = '/upload/profile.jpg'
MAIN_MENU = True
MENUITEMS = (
        ('Categories', '/categories.html'),
        ('Tags', '/tags.html'),
        )
