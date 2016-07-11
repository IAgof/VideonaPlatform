# -*- coding: utf-8 -*-
"""
    api.users
    ~~~~~~~~~

    Api users module
"""
from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

from videona_platform.core import VideonaError
from videona_platform.factory import user_datastore
from videona_platform.users.user_service import UserService, UserRegistrationError

users = UserService(user_datastore)

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
    except UserRegistrationError as registration_error:
        return jsonify(dict(error=registration_error.msg)), 200
    except KeyError:
        raise VideonaError(ERROR_MISSING_PARAMETERS)


@users_blueprint.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def user_details(user_id):
    user = users.get_or_404(user_id)
    return jsonify(dict(data=user)), 200