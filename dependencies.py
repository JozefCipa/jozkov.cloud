# -*- coding: utf-8 -*-

# check if all external modules are installed

try:
    import flask
except ImportError:
    print('Install flask')

try:
    import redis
except ImportError:
    print('Install redis')

try:
    import slugify
except ImportError:
    print('Install unicode-slugify')

try:
    import validators
except ImportError:
    print('Install validators')