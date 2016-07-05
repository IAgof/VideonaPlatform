# -*- coding: utf-8 -*-
"""
    fiware.fiware_settings
    ~~~~~~~~~~~~~~~~~~~~~~

    Fiware specific settings
"""
import os


KEYROCK_HOST = os.environ.get('KEYROCK_HOST')
KEYROCK_PORT = '7003'
KEYROCK_ADMIN_USER = os.environ.get('KEYROCK_ADMIN_USER', 'idm_user')
KEYROCK_ADMIN_PASSWORD = os.environ.get('KEYROCK_ADMIN_PASSWORD', 'idm')
KEYROCK_TOKEN_ENDPOINT = 'v3/auth/tokens'
KEYROCK_USERS_ENDPOINT = 'v3/users'
