# -*- coding: utf-8 -*-
"""
    user.user_service
    ~~~~~~~~~~~~~~~~~

    users service
"""
from flask_security.utils import encrypt_password

from videona_platform.factory import user_datastore
from videona_platform.core import db, VideonaError


class UserService(object):
    ERROR_DATABASE_ERROR = 'database error'
    ERROR_USER_ALREADY_EXISTS = 'User already exists'

    def register(self, email, password):
        password = encrypt_password(password)
        if user_datastore.find_user(email=email):
            raise VideonaError(UserService.ERROR_USER_ALREADY_EXISTS)
        try:
            user_datastore.create_user(email=email, password=password)
            user_datastore.commit()
            db.session.commit()
        except VideonaError as videonaError:
            raise videonaError
        except:
            db.session.rollback()
            raise VideonaError(UserService.ERROR_DATABASE_ERROR)
            # db.session.flush()

users = UserService()
