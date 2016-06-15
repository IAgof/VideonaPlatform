# -*- coding: utf-8 -*-
"""
    factory
    ~~~~~~~~~~~~~

    Videona Platform app Factory
"""
from flask import Flask
from flask_jwt import JWT
from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import verify_password
from flask_wtf.csrf import CsrfProtect

from core import migrate, security
from videona_platform.core import db
from videona_platform.frontend.frontend import front_page_blueprint
from videona_platform.users import models


def authenticate(username, password):
    user = user_datastore.find_user(email=username)
    if user and verify_password(password, user.password):
        return user
    return None

def load_user():
    pass


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
jwt = JWT(authentication_handler=authenticate, identity_handler=load_user)


def create_app(settings_override=None):
    app = Flask(__name__)
    app.config.from_object('videona_platform.default_settings')
    app.config.from_object(settings_override)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    app.user_datastore = user_datastore
    security.init_app(app, app.user_datastore)
    app.csrf = CsrfProtect(app)
    app.csrf.exempt(app.blueprints['security'])
    jwt.init_app(app)

    # app.logger.debug('Flask instance path is %s' % app.instance_path)
    app.register_blueprint(front_page_blueprint)
    return app