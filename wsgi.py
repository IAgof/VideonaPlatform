# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    videona_platform wsgi module
"""

from flask import request
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

import videona_platform.frontend.factory
import videona_platform.api.factory
from videona_platform import default_settings


application = DispatcherMiddleware(videona_platform.frontend.factory.create_app(),
    {default_settings.API_ENDPOINT: videona_platform.api.factory.create_app()})


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
