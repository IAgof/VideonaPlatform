# -*- coding: utf-8 -*-
"""
    tests.api.video_endpoints_test
    ~~~~~

    video enponts tests
"""
from flask import json
from hamcrest import *
import mock

from datetime import datetime

from videona_platform.api.videos import create_video


class TestVideoEndpoints(object):
    @mock.patch('videona_platform.api.videos.videos.create')
    @mock.patch('videona_platform.api.videos.request')
    @mock.patch('videona_platform.api.videos.jsonify')
    def test_video_create_endpoint_calls_video_service_create(self, jsonify, flask_request, video_service_create, push_context):
        jsonify.return_value = 'return'
        now = datetime.utcnow()
        new_video_post_data = {'lat': 40.502956, 'lon': -3.887818, 'height': 720, 'width': 1080, 'rotation': 90,
                                           'duration': 210093, 'size': 890123478, 'bitrate': 5000000, 'date': now,
                                           'title': 'video title'}
        flask_request.json = new_video_post_data

        create_video()

        video_service_create.assert_called_once_with(lat=40.502956, lon=-3.887818, height=720, width=1080, rotation=90,
                                                     duration=210093, size=890123478, bitrate=5000000, date=now,
                                                     title='video title')
