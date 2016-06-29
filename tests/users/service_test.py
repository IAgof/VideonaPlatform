# -*- coding: utf-8 -*-
"""
    User service tests
    ~~~~~~~~~~~~~~~~~~

    tests for user service
"""
import pytest
from hamcrest import *

from videona_platform.users.user_service import users, UserService
from videona_platform.users import models as users_models
from videona_platform.core import VideonaError


class TestUserService(object):
    def test_register_creates_new_user(self, push_context, session):
        email = "email@valid.now"
        password = "password"

        users.register(email, password)

        assert_that(users_models.User.query.count(), is_(1))
        saved_user = users_models.User.query.first()
        assert_that(saved_user.email, is_(email))
        assert_that(saved_user.password, is_not(password))

    def test_register_handles_duplicates(self, push_context, session):
        email = 'email@valid.now'
        password = 'password'

        users.register(email, password)
        with pytest.raises(VideonaError) as e_info:
            users.register(email, password)

        assert_that(e_info.value.msg, is_(UserService.ERROR_USER_ALREADY_EXISTS))
        assert_that(users_models.User.query.count(), is_(1))

    def test_register_handles_empty_username(self, push_context, session):
        email = ''
        password = 'qwerty'

        with pytest.raises(VideonaError) as e_info:
            users.register(email, password)

        assert_that(e_info.value.msg, is_(users_models.User.USER_ERROR_EMAIL_NOT_VALID))
