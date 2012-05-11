import os
import sys
sys.stdout = sys.stderr
import site
site.addsitedir('/var/wsgi/lunch_it/env/lib/python2.6/site-packages')

import os
os.environ['PYTHON_EGG_CACHE'] = '/var/wsgi/lunch_it/mod_wsgi/egg-cache'

sys.path.append('/var/wsgi/lunch_it/lunch_it/lunch_it')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
