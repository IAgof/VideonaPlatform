# -*- coding: utf-8 -*-
"""
    videona_platform.settings
    ~~~~~~~~~~~~~~~

    videona_platform settings module
"""
import os


DEBUG = os.environ.get('DEBUG', False)
SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres:5432/postgres'
CELERY_BROKER_URL = 'redis://33.33.33.10:6379/0'

MAIL_DEFAULT_SENDER = 'info@videona.com'
MAIL_SERVER = 'smtp.postmarkapp.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'

SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_PASSWORD_HASH = 'plaintext'
SECURITY_PASSWORD_SALT = 'password_salt'
SECURITY_REMEMBER_SALT = 'remember_salt'
SECURITY_RESET_SALT = 'reset_salt'
SECURITY_RESET_WITHIN = '5 days'
SECURITY_CONFIRM_WITHIN = '5 days'
SECURITY_SEND_REGISTER_EMAIL = False
