# -*- coding: utf-8 -*-

# check if all external modules are installed

ok = True
try:
    import flask
except ImportError:
    print('Install flask')
    ok = False

try:
    import redis
except ImportError:
    print('Install redis')
    ok = False

try:
    import slugify
except ImportError:
    print('Install unicode-slugify')
    ok = False

try:
    import validators
except ImportError:
    print('Install validators')
    ok = False

try:
    import uwsgi
except ImportError:
    print('Install uwsgi')
    ok = False

if ok:
	print('OK, everything is installed.')