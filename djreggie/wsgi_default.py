import os, sys

sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.8')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djreggie.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/var/cache/python/.python-eggs")
os.environ.setdefault("TZ", "America/Chicago")

# informix
os.environ['INFORMIXSERVER'] = ''
os.environ['DBSERVERNAME'] = ''
os.environ['INFORMIXDIR'] = ''
os.environ['ODBCINI'] = ''
os.environ['ONCONFIG'] = ''
os.environ['INFORMIXSQLHOSTS'] = ''

os.environ['LD_LIBRARY_PATH'] = ''
os.environ['LD_RUN_PATH'] = ''

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

