# gunicorn.py
import os

bind = '0.0.0.0:8000'
workers = 2
loglevel = 'info'

if os.environ.get('DEBUG') == True:
    reload = True
    loglevel = 'debug'

