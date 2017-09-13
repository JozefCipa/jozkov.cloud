#!/usr/bin/python
import sys
import logging
import configparser

config = configparser.ConfigParser()
config = config.read('config.ini')
config = config['DEFAULT']

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,config['baseDir'])

import app as application
application.secret_key = config['appKey']