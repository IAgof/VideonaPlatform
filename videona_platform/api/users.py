# -*- coding: utf-8 -*-
"""
    api.users
    ~~~~~~~~~

    Api users module
"""
from flask import Blueprint, request, jsonify
from videona_platform.users.user_service import users

users_blueprint = Blueprint('users', __name__, url_prefix='/v1/users')

@users_blueprint.route('/register', methods=['POST'])
def register_user():
    json_data = request.json
    email = json_data['username']
    password = json_data['password']
    users.register(email=email, password=password)
    status = 'User created'
    return jsonify({'result': status})
