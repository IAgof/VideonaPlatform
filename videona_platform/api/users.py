# -*- coding: utf-8 -*-
"""
    api.users
    ~~~~~~~~~

    Api users module
"""
from flask import Blueprint


users_blueprint = Blueprint('users', __name__, url_prefix='/v1/users')

@users_blueprint.route('/register')
def register_user():
    return 'holaaa'
