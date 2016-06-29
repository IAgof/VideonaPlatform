# -*- coding: utf-8 -*-
"""
    api app test
    ~~~~~

    tests for the api app
"""
import json

import pytest
from hamcrest import *
from flask import Blueprint, url_for

from videona_platform.api.users import users_blueprint

class TestAPIAppSetUp(object):
    def test_api_app(self, api_app):
        assert_that(api_app, not_none())


    def test_api_users_blueprint_definition(self, api_app):
        assert_that(users_blueprint, not_none())
        assert_that(users_blueprint, instance_of(Blueprint))
        assert_that(users_blueprint.name, is_("users"))
        assert_that(users_blueprint.url_prefix, is_("/v1/users"))
        assert_that(users_blueprint.name, is_in(api_app.blueprints))


    def test_users_blueprint_register_route(self, session, client):
        new_user_data = dict(username='e@ma.il', password='azerty')
        post_response = client.post(url_for('users.register_user'), data=json.dumps(new_user_data),
                                    content_type='application/json')
        get_response = client.get(url_for('users.register_user'))

        assert_that(get_response.status_code, is_(405))
        assert_that(post_response.status_code, is_(200))

