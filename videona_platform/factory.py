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
from videona_platform.fiware.keyrock import fiware_authenticate_from_jwt
from videona_platform.users import models
from videona_platform.fiware import fiware_settings
from videona_platform.users.user_service import UserService


def create_app(package_name, package_path, settings_override=None,
               register_security_blueprint=True):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the Videona platform.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered. Defaults
                                        to `True`.
    """
    app = Flask(package_name)
    app.config.from_object('videona_platform.default_settings')
    app.config.from_object(settings_override)
    app.logger.debug('Fiware installed is %s ' % app.config.get('FIWARE_INSTALLED'))
    if app.config.get('FIWARE_INSTALLED') is True:
        app.logger.debug('Fiware enabled, loading fiware settings...')
        app.config.from_object(fiware_settings)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    app.user_datastore = user_datastore
    security.init_app(app, app.user_datastore, register_blueprint=register_security_blueprint)
    app.csrf = CsrfProtect(app)
    if register_security_blueprint:
        app.csrf.exempt(app.blueprints['security'])

    app.logger.debug('Flask instance path is %s' % app.instance_path)
    # app.register_blueprint(front_page_blueprint)
    return app


def authenticate(username, password):
    print '- authenticating user -'
    user = user_datastore.find_user(email=username)
    if user and verify_password(password, user.password):
        return user
    if fiware_authenticate_from_jwt(username, password) is not None:
        return UserService(user_datastore).register(username, password)
    return None


def load_user(payload):
    user = user_datastore.find_user(id=payload['identity'])
    return user


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
jwt = JWT(authentication_handler=authenticate, identity_handler=load_user)