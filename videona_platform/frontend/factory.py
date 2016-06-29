# -*- coding: utf-8 -*-
"""
    frontend/factory
    ~~~~~~~~~~~~~~~~

    Videona Platform Frontend app factory
"""
import videona_platform
from videona_platform import factory
from videona_platform.frontend.frontend import front_page_blueprint


def create_app(settings_override=None):
    """Returns the Videona platform frontend application instance"""
    # app = factory.create_app(__name__, __path__, settings_override)
    app = factory.create_app(__name__, videona_platform.frontend.__path__, settings_override)
    app.register_blueprint(front_page_blueprint)

    # # Set the default JSON encoder
    # app.json_encoder = JSONEncoder

    # # Register custom error handlers
    # app.errorhandler(VideonaError)(on_videona_error)
    # app.errorhandler(VideonaFormError)(on_videona_form_error)
    # app.errorhandler(404)(on_404)

    return app