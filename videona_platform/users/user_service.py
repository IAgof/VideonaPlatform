# -*- coding: utf-8 -*-
"""
    user.user_service
    ~~~~~~~~~~~~~~~~~

    users service
"""
from flask_security.utils import encrypt_password

from videona_platform.default_settings import MINIMUN_PASSWORD_LENGTH
# from videona_platform.factory import user_datastore
from videona_platform.users import models as users_models
from videona_platform.core import db, VideonaError, Service


class UserService(Service):
    __model__ = users_models.User

    def __init__(self, user_datastore):
        self.user_datastore = user_datastore

    ERROR_DATABASE_ERROR = 'Database error'
    ERROR_USER_ALREADY_EXISTS = 'User already exists'

    def register(self, email, password, username=None):
        self._check_password_lenght(password)
        password = encrypt_password(password)
        if self.user_datastore.find_user(email=email):
            raise VideonaError(UserService.ERROR_USER_ALREADY_EXISTS)
        try:
            user = self.user_datastore.create_user(email=email, password=password)
            self.user_datastore.commit()
            db.session.commit()
            print 'User %s created' % email
            return user
        except VideonaError as videonaError:
            raise videonaError
        except:
            db.session.rollback()
            raise VideonaError(UserService.ERROR_DATABASE_ERROR)
            # db.session.flush()

    def _check_password_lenght(self, password):
        if len(password) < MINIMUN_PASSWORD_LENGTH:
            raise VideonaError(users_models.User.USER_ERROR_PASSWORD_TOO_SHORT)


# users = UserService()
