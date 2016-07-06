# -*- coding: utf-8 -*-
"""
    test/api/user details tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    tests for user details endpoint
"""
from hamcrest import *
import mock

from videona_platform.api.users import user_details


class TestUserDetailsEndpoint(object):
    @mock.patch('flask_jwt._jwt_required')
    @mock.patch('videona_platform.api.users.jsonify')
    @mock.patch('videona_platform.api.users.users.get_or_404')
    def test_user_details_endpoint_calls_user_service(self, user_get_or_404, jsonify, _jwt_required, session, push_context):
        jsonify.return_value = 'user details'
        user_get_or_404.return_value = 'user details'

        result = user_details(1)

        user_get_or_404.assert_called_once_with(1)
        assert_that(result, is_(('user details', 200)))
