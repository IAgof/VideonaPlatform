# -*- coding: utf-8 -*-
"""
    api app test
    ~~~~~

    tests for the api app
"""
import datetime
import pytest
from hamcrest import *
import mock

import json
from flask import Blueprint, url_for

from videona_platform.api.factory import on_videona_error, on_404
from videona_platform.api.users import users_blueprint
from videona_platform.api.videos import videos_blueprint
from videona_platform.core import VideonaError
from videona_platform.helpers import JSONEncoder
from tests.factories import UserFactory


def mock_jwt_required(realm):
    return


class TestAPIAppSetUp(object):
    def test_api_app(self, api_app):
        assert_that(api_app, not_none())

    def test_api_users_blueprint_definition(self, api_app):
        assert_that(users_blueprint, not_none())
        assert_that(users_blueprint, instance_of(Blueprint))
        assert_that(users_blueprint.name, is_("users"))
        assert_that(users_blueprint.url_prefix, is_("/v1/users"))
        assert_that(users_blueprint.name, is_in(api_app.blueprints))

    def test_api_videos_blueprint_definition(self, api_app):
        assert_that(videos_blueprint, not_none())
        assert_that(videos_blueprint, instance_of(Blueprint))
        assert_that(videos_blueprint.name, is_("videos"))
        assert_that(videos_blueprint.url_prefix, is_("/v1/videos"))
        assert_that(videos_blueprint.name, is_in(api_app.blueprints))

    def test_api_app_has_json_serializer(self, api_app):
        assert_that(api_app.json_encoder, equal_to(JSONEncoder))

    def test_api_app_has_videona_error_handler(self, api_app):
        assert_that((VideonaError, on_videona_error), is_in(api_app.error_handlers[None]))

    def test_api_app_has_404_custom_error_handler(self, api_app):
        assert_that(api_app.error_handlers[404], is_(on_404))

    @mock.patch('videona_platform.api.users.users.register')
    def test_users_blueprint_register_route(self, register_user, session, client):
        new_user_data = dict(username='e@ma.il', password='azerty')

        post_response = client.post(url_for('users.register_user'), data=json.dumps(new_user_data),
                                    content_type='application/json')
        get_response = client.get(url_for('users.register_user'))

        assert_that(get_response.status_code, is_(405))
        assert_that(post_response.status_code, is_(200))

    @mock.patch('videona_platform.api.videos.create_video')
    def test_videos_blueprint_create_route(self, create_video, app, session, client):
        now = str(datetime.datetime.utcnow())
        new_video_data = dict(lat=40.502956, lon=-3.887818, height=720, width=1080, rotation=90,
                                           duration=210093, size=890123478, bitrate=5000000,
                                           # date=now,
                                           title='video title')

        post_response = client.post(url_for('videos.create_video'), data=json.dumps(new_video_data),
                                    content_type='application/json')
        get_response = client.get(url_for('videos.create_video'))

        assert_that(get_response.status_code, is_(405))
        assert_that(post_response.status_code, is_(201))

    @mock.patch('flask_jwt._jwt_required')
    @mock.patch('videona_platform.api.users.user_details')
    def test_users_blueprint_user_details_route(self, user_details, _jwt_required, session, client):
        _jwt_required.side_effect = mock_jwt_required
        new_user = UserFactory.create(username='e@ma.il', password='azerty')
        session.add(new_user)
        session.commit()
        new_user_details_url = url_for('users.user_details', user_id=new_user.id)

        post_response = client.post(new_user_details_url, content_type='application/json')
        get_response = client.get(new_user_details_url)

        assert_that(post_response.status_code, is_(405))
        assert_that(get_response.status_code, is_(200))
