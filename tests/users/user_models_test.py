# -*- coding: utf-8 -*-
"""
    user_models_test
    ~~~~~~~~~~~~~

    Tests for Videona Platform user Models and configuration
"""
import pytest
from hamcrest import *
from datetime import datetime, timedelta
from flask_security import Security, SQLAlchemyUserDatastore
import videona_platform.default_settings
import videona_platform.core
from videona_platform.users import models
from tests import factories


class TestUserModels(object):
    def test_user_model(False, session):
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


    def test_user_model_repr(self):
        user = models.User(
            username='Username',
            email='test@email.com',
            password='pass',
        )

        assert_that(str(user), is_('<User: Username>'))


    def test_role_model(False, session):
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


class TestSecurityConfig(object):
    def test_security_trackable_option_is_activated(self):
        assert_that(videona_platform.default_settings.SECURITY_TRACKABLE, is_(True))


    def test_secure_extension_declared_in_core(self):
        assert_that(videona_platform.core.security, instance_of(Security))


    def test_app_has_user_datastore(self, app):
        assert_that(app.user_datastore, instance_of(SQLAlchemyUserDatastore))
        assert_that(app.user_datastore.db, is_(videona_platform.core.db))
        assert_that(app.user_datastore.user_model, equal_to(models.User))
        assert_that(app.user_datastore.role_model, equal_to(models.Role))


    def test_app_security_is_initialized(self, app):
        assert_that('security', is_in(app.extensions))
        security = app.extensions['security']

        assert_that(security.app, is_(app))
        assert_that(security.datastore, is_(app.user_datastore))