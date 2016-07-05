# -*- coding: utf-8 -*-
"""
    api/factory
    ~~~~~~~~~~~

    Api app factory
"""
from functools import wraps

from flask import jsonify

import videona_platform
from videona_platform import factory
from videona_platform.api.users import users_blueprint
from videona_platform.api.videos import videos_blueprint
from videona_platform.core import VideonaError
from videona_platform.helpers import JSONEncoder


def create_app(settings_override=None, register_security_blueprint=False):
    """Returns the Videona API application instance"""
    app = factory.create_app(__name__, videona_platform.api.__path__, settings_override,
                             register_security_blueprint=register_security_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(videos_blueprint)
    factory.jwt.init_app(app)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # # Register custom error handlers
    app.errorhandler(VideonaError)(on_videona_error)
    # app.errorhandler(VideonaFormError)(on_videona_form_error)
    app.errorhandler(404)(on_404)

    return app


def on_videona_error(videona_error):
    return jsonify(dict(error=videona_error.msg)), 400


def on_404(args):
    return jsonify(dict(error='Not found')), 404