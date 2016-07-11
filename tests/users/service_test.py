# -*- coding: utf-8 -*-
"""
    User service tests
    ~~~~~~~~~~~~~~~~~~

    tests for user service
"""
import pytest
from hamcrest import *
import mock

from tests.factories import UserFactory
from videona_platform.users.user_service import UserService, UserRegistrationError
from videona_platform.api.users import users
from videona_platform.users import models as users_models
from videona_platform.core import VideonaError, Service


class TestUserService(object):
    def test_user_service_is_a_service(self):
        assert_that(issubclass(UserService, Service))
        assert_that(UserService.__model__, equal_to(users_models.User))

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

        assert_that(e_info.value.msg, is_(UserRegistrationError.ERROR_USER_ALREADY_EXISTS))
        assert_that(users_models.User.query.count(), is_(1))

    def test_register_handles_empty_username(self, push_context, session):
        email = ''
        password = 'qwerty'

        with pytest.raises(VideonaError) as e_info:
            users.register(email, password)

        assert_that(e_info.value.msg, is_(users_models.User.USER_ERROR_EMAIL_NOT_VALID))

    @mock.patch('videona_platform.core.Service.get_or_404')
    def test_user_get_or_404_calls_service(self, get_or_404):
        users.get_or_404(2)

        get_or_404.assert_called_once_with(2)

    def test_user_get_or_404_retrieves_existing_user(self, session):
        new_user = UserFactory()
        session.add(new_user)
        session.commit()

        retrieved_user = users.get_or_404(new_user.id)

        assert_that(retrieved_user, is_(new_user))