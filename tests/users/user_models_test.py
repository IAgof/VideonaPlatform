# -*- coding: utf-8 -*-
"""
    user_models_test
    ~~~~~~~~~~~~~

    Tests for Videona Platform user Models and configuration
"""
import pytest
from datetime import datetime, timedelta

from flask_security import UserMixin, RoleMixin
from hamcrest import *

from tests import factories
from videona_platform.core import VideonaError
from videona_platform.users import models


class TestUserModels(object):
    def test_user_model(self, session):
        now = datetime.utcnow()
        user = models.User(
            username='Username',
            email='test@email.com',
            password='pass',
            active=True,
            confirmed_at=now,
            # For Trackable logins with Flask-Security
            last_login_at=now - timedelta(days=1),
            current_login_at=now - timedelta(hours=1),
            last_login_ip='127.0.0.42',
            current_login_ip='127.2.0.1',
            login_count=5
        )

        session.add(user)
        session.commit()

        assert_that(user, not_none())
        assert_that(models.User.query.count(), is_(1))

        saved_user = models.User.query.all()[0]
        assert_that(saved_user.id, greater_than(0))
        assert_that(saved_user.username, is_('Username'))
        assert_that(saved_user.email, is_('test@email.com'))
        assert_that(saved_user.password, is_('pass'))
        assert_that(saved_user.active, is_(True))
        assert_that(saved_user.confirmed_at, is_(now))
        assert_that(saved_user.last_login_at, is_(now - timedelta(days=1)))
        assert_that(saved_user.current_login_at, is_(now - timedelta(hours=1)))
        assert_that(saved_user.last_login_ip, is_('127.0.0.42'))
        assert_that(saved_user.current_login_ip, is_('127.2.0.1'))
        assert_that(saved_user.login_count, is_(5))

    def test_user_model_has_user_mixin(self):
        assert_that(issubclass(models.User, UserMixin))

    def test_user_email_validates(self):
        user = None
        with pytest.raises(VideonaError) as e_info:
            user = models.User(
                username='Username',
                email='@invalid.email.com',
                password='pass',
            )

        assert_that(e_info.value.msg, is_(models.User.USER_ERROR_EMAIL_NOT_VALID))
        assert_that(user, none())

    def test_user_password_validates(self):
        user = None
        with pytest.raises(VideonaError) as e_info:
            user = models.User(
                username='Username',
                email='valid@email.com',
                password='',
            )

        assert_that(e_info.value.msg, is_(models.User.USER_ERROR_EMAIL_NOT_VALID))
        assert_that(user, none())

    def test_user_model_repr(self):
        user = models.User(
            username='Username',
            email='test@email.com',
            password='pass',
        )

        assert_that(str(user), is_('<User: Username>'))


    def test_role_model(self, session):
        role = models.Role(name='Role name',
                           description='A long description')
        session.add(role)
        session.commit()

        assert_that(role, not_none())
        assert_that(models.Role.query.count(), is_(1))

        saved_user = models.Role.query.all()[0]
        assert_that(saved_user.id, greater_than(0))
        assert_that(saved_user.name, is_('Role name'))
        assert_that(saved_user.description, is_('A long description'))


    def test_role_model_has_role_mixin(self):
        assert_that(issubclass(models.Role, RoleMixin))


    def test_role_model_repr(self):
        role = models.Role(
            name='Role name',
            description='Role description',
        )

        assert_that(str(role), is_('<Role: Role name>'))


    def test_roles_has_many_users(self, session):
        role = factories.RoleFactory()
        users = factories.UserFactory.create_batch(2)

        role.users.append(users[0])
        role.users.append(users[1])
        session.commit()
        assert_that(models.Role.query.count(), is_(1))
        saved_role = models.Role.query.all()[0]

        assert_that(len(saved_role.users.all()), is_(2))
        assert_that(saved_role.users[0], is_in(users))
        assert_that(saved_role.users[1], is_in(users))


    def test_users_have_roles(self, session):
        user = factories.UserFactory()
        roles = factories.RoleFactory.create_batch(2)

        user.roles.append(roles[0])
        user.roles.append(roles[1])

        assert_that(models.User.query.count(), is_(1))
        assert_that(user, not_none())
        assert_that(user.id, greater_than(0))

        saved_user = models.User.query.all()[0]
        assert_that(len(saved_user.roles), is_(2))
        assert_that(saved_user.roles[0], is_in(roles))
        assert_that(saved_user.roles[1], is_in(roles))