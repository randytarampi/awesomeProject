#!/usr/bin/env python
import os, sys

PROJECT_DIR = os.path.dirname(__file__)

# make sure app's modules can be found
sys.path.append(os.path.dirname(PROJECT_DIR))
sys.path.append(PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Switch to the directory of your project. (Optional.)
os.chdir("/home/awesomeadmin/awesomeTechEval")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
