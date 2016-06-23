# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    videona_platform wsgi module
"""

from flask import request
from werkzeug.serving import run_simple

import videona_platform.frontend.factory
from videona_platform import default_settings
from videona_platform import frontend
# from videona_platform.factory import create_app


application = videona_platform.frontend.factory.create_app()


def is_jwt(request):
    return request.path == default_settings.JWT_AUTH_URL_RULE


# @application.before_request
# def check_csrf():
#     if not is_jwt(request):
#         application.csrf.protect()


if __name__ == "__main__":
    print 'running videona app in main process.....'
    application.debug = True
    run_simple('0.0.0.0', 8000, application, use_reloader=True, use_debugger=True)
