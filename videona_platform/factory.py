# -*- coding: utf-8 -*-
from flask import Flask

from videona_platform import bp
from core import db, migrate

def create_app(settings_override=None):
    app = Flask(__name__)
    app.config.from_object('videona_platform.default_settings')
    app.config.from_object(settings_override)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # app.logger.debug('Flask instance path is %s' % app.instance_path)
    app.register_blueprint(bp)
    return app