import os
import sys

# This file needs to be at this level of the hierarchy so that relative links work when running using test server and live.
sys.path.append('/opt/themortgagemeter/website/django/themortgagemeter')
#sys.path.append('..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
