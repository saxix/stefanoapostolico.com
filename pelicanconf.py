#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

HERE = os.path.dirname(__file__)

PLUGIN_PATHS = ['pelican-plugins', 'pelican-plugins/pelican_youtube']
PLUGINS = ['interlinks',
           'pelican_fontawesome',
           'related_posts',
           'html_rst_directive',
           'summary',
           'code_include',
           'pelican_youtube',
           # 'sitemap',
           'simple_footnotes']

ARTICLE_EXCLUDES = ['extras']
USE_FOLDER_AS_CATEGORY = False
AUTHOR = u'Stefano Apostolico'
SITENAME = u"Stefano Apostolico's Blog"
SITEURL = 'http://localhost:8000'
THEME = 'themes/sa'

PATH = 'content'

TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

INTERNET_DEFENSE_LEAGUE = True
# GOOGLE_ANALYTICS = 'UA-11207015-9'
# DISQUS_SITENAME = 'stefanoapostolico.disqus.com'
USER_LOGO_URL = '/images/me.jpg'
# WITH_FUTURE_DATES = False
DEFAULT_DATE = 'fs'


# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
# ('Python.org', 'http://python.org/'),
# ('Jinja2', 'http://jinja.pocoo.org/'),
# ('You can modify those links in your config file', '#'),)
LINKS = ()
MENUITEMS = ()

LINKEDIN = 'https://www.linkedin.com/pub/stefano-apostolico/1/683/814'
TWITTER = 'https://twitter.com/s_apostolico'
TWITTER_USERNAME = 's_apostolico'
GITHUB_URL = 'https://github.com/saxix'
EMAIL = 's.apostolico@gmail.com'

# Social widget
SOCIAL = (('twitter', TWITTER),
          ('linkedin', LINKEDIN),
          ('github', GITHUB_URL),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True

TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 1

STATIC_PATHS = ['images',
                'files',
                'extras/README.rst',
                'extras/CNAME',
                'extras/robots.txt']

EXTRA_PATH_METADATA = {
    'extras/README.rst': {'path': 'README.rst'},
    'extras/CNAME': {'path': 'CNAME'},
    'extras/robots.txt': {'path': 'robots.txt'},
}

INTERLINKS = {
    'plugins': 'https://github.com/getpelican/pelican-plugins',
}

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'

# FILENAME_METADATA = '(?P<day>\d{2}).*'
PATH_METADATA = '\A(?P<category>[^/]+)/(?P<date>\d{4}/\d{2}/\d{2})-(?P<slug>.*)(.md|.rst)'

YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'

RELATED_POSTS_MAX = 5

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
IGNORE_FILES = ['_template.rst', '_template.md']
