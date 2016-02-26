#!/bin/bash
if [ "$FLASK_ENV" == "development" ]; then
    python wsgi.py
else
    /usr/local/bin/gunicorn --config=/usr/src/app/gunicorn.py wsgi
fi