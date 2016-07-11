# -*- coding: utf-8 -*-
"""
    user.user_service
    ~~~~~~~~~~~~~~~~~

    users service
"""
from flask import current_app
from flask_security.utils import encrypt_password

from videona_platform.default_settings import MINIMUN_PASSWORD_LENGTH
from videona_platform.users import models as users_models
from videona_platform.core import db, VideonaError, Service


class UserRegistrationError(VideonaError):
    ERROR_USER_ALREADY_EXISTS = 'User already exists'

class UserService(Service):
    ERROR_DATABASE_ERROR = 'Database error'
    __model__ = users_models.User

    def __init__(self, user_datastore):
        self.user_datastore = user_datastore

    def register(self, email, password, username=None):
        UserService._check_password_lenght(password)
        password = encrypt_password(password)
        if self.user_datastore.find_user(email=email):
            raise UserRegistrationError(UserRegistrationError.ERROR_USER_ALREADY_EXISTS)
        try:
            user = self.user_datastore.create_user(email=email, password=password)
            self.save(user)
            current_app.logger.debug('User with email %s created' % email)
            return user
        except VideonaError as videona_error:
            raise UserRegistrationError(videona_error.msg)
        except:
            db.session.rollback()
            raise VideonaError(UserService.ERROR_DATABASE_ERROR)
            # db.session.flush()

    @staticmethod
    def _check_password_lenght(password):
        if len(password) < MINIMUN_PASSWORD_LENGTH:
            raise VideonaError(users_models.User.USER_ERROR_PASSWORD_TOO_SHORT)
