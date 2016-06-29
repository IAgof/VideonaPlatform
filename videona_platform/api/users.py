# -*- coding: utf-8 -*-
"""
    api.users
    ~~~~~~~~~

    Api users module
"""
from flask import Blueprint, request, jsonify

from videona_platform.core import VideonaError
from videona_platform.users.user_service import users

users_blueprint = Blueprint('users', __name__, url_prefix='/v1/users')

ERROR_MISSING_PARAMETERS = 'Missing request parameters'
STATUS_USER_CREATED = 'User created'

@users_blueprint.route('/register', methods=['POST'])
def register_user():
    try:
        json_data = request.json
        email = json_data['username']
        password = json_data['password']
        users.register(email=email, password=password)
        return jsonify({'result': STATUS_USER_CREATED})
    except KeyError:
        raise VideonaError(ERROR_MISSING_PARAMETERS)
