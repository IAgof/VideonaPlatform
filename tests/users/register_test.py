# -*- coding: utf-8 -*-
"""
    register tests
    ~~~~~

    tests for user register endpoint
"""
import json

from hamcrest import *
import mock

from flask import url_for

from videona_platform.api.users import register_user
from videona_platform.users import models as user_models
from tests.factories import UserFactory

A_VALID_MAIL = 'ovidio@videona.com'
A_VALID_PASSWORD = 'azerty'


class TestRegisterEndpoint(object):
    @mock.patch('videona_platform.users.user_service.users.register')
    @mock.patch('videona_platform.api.users.request')
    def test_register_endpoint_calls_user_service_register(self, flask_request, user_service_register, client):
        new_user_post_data = {
            'username': A_VALID_MAIL,
            'password': A_VALID_PASSWORD
        }
        flask_request.json = new_user_post_data

        register_user()

        user_service_register.assert_called_once_with(email=A_VALID_MAIL, password=A_VALID_PASSWORD)

    @mock.patch('videona_platform.api.users.request')
    @mock.patch('videona_platform.api.users.jsonify', mock.Mock())
    def test_register_endpoint_creates_user(self, flask_request, push_context, session):
        new_user_post_data = {
            'username': A_VALID_MAIL,
            'password': A_VALID_PASSWORD
        }
        flask_request.json = new_user_post_data

        register_user()

        assert_that(user_models.User.query.count(), is_(1))
        saved_user = user_models.User.query.all()[0]
        assert_that(saved_user.email, is_(A_VALID_MAIL))
        assert_that(saved_user.password, is_not(A_VALID_PASSWORD))

    def test_register_endpoint_handles_duplicate_users(self, push_context, session, client):
        email = A_VALID_MAIL
        existing_user = UserFactory.create(email=email)
        new_user_data = dict(username=email, password=A_VALID_PASSWORD)

        response = client.post(url_for('users.register_user'), data=json.dumps(new_user_data),
                               content_type='application/json')

        assert_that(user_models.User.query.count(), is_(1))
        assert_that(response.status_code, is_(400))
        assert_that(response.json['error'], is_('User already exists'))

    def test_register_endpoint_returns_200_if_no_error(self, push_context, session, client):
        email = A_VALID_MAIL
        new_user_data = dict(username=email, password=A_VALID_PASSWORD)

        response = client.post(url_for('users.register_user'), data=json.dumps(new_user_data),
                               content_type='application/json')

        assert_that(response.status_code, is_(200))
        assert_that(response.json['result'], is_('User created'))
