# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    videona_platform wsgi module
"""

from werkzeug.serving import run_simple

from videona_platform import create_app

application = create_app()

if __name__ == "__main__":
    run_simple('0.0.0.0', 8000, application, use_reloader=True, use_debugger=True)
