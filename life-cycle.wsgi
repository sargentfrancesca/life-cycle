#!/usr/bin/python                                                               
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)

PROJECT_DIR = "/var/www/html/life-cycle/"
activate_this = os.path.join(PROJECT_DIR, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

sys.path.append(PROJECT_DIR)
from app import create_app
application=create_app(os.getenv('FLASK_CONFIG') or 'default')
application.secret_key = 'hard to guess string'
