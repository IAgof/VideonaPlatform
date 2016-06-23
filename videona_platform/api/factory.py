# -*- coding: utf-8 -*-
"""
    api/factory
    ~~~~~~~~~~~

    Api app factory
"""
import videona_platform
from videona_platform import factory
from videona_platform.api.users import users_blueprint


def create_app(settings_override=None, register_security_blueprint=False):
    """Returns the Videona API application instance"""
    app = factory.create_app(__name__, videona_platform.api.__path__, settings_override,
                             register_security_blueprint=register_security_blueprint)
    app.register_blueprint(users_blueprint)


    # # Set the default JSON encoder
    # app.json_encoder = JSONEncoder

    # # Register custom error handlers
    # app.errorhandler(VideonaError)(on_videona_error)
    # app.errorhandler(VideonaFormError)(on_videona_form_error)
    # app.errorhandler(404)(on_404)

    return app