import pytest
from hamcrest import assert_that, is_, instance_of, equal_to, is_in, none
import mock

from flask_security import Security, SQLAlchemyUserDatastore
from flask_jwt import JWT
from datetime import timedelta
import videona_platform.core
import videona_platform.default_settings
# import videona_platform.factory
import videona_platform.factory
from videona_platform.factory import authenticate, load_user
from videona_platform.users import models
from tests import factories


class TestSecurityConfig(object):
    def test_security_trackable_and_registrable_options_are_activated(self):
        assert_that(videona_platform.default_settings.SECURITY_TRACKABLE, is_(True))
        assert_that(videona_platform.default_settings.SECURITY_REGISTERABLE, is_(True))

    def test_secure_extension_declared_in_core(self):
        assert_that(videona_platform.core.security, instance_of(Security))


    def test_app_has_user_datastore(self, api_app):
        assert_that(api_app.user_datastore, instance_of(SQLAlchemyUserDatastore))
        assert_that(api_app.user_datastore.db, is_(videona_platform.core.db))
        assert_that(api_app.user_datastore.user_model, equal_to(models.User))
        assert_that(api_app.user_datastore.role_model, equal_to(models.Role))


    def test_app_security_is_initialized(self, api_app):
        assert_that('security', is_in(api_app.extensions))
        security = api_app.extensions['security']

        assert_that(security.app, is_(api_app))
        assert_that(security.datastore, is_(api_app.user_datastore))


class TestJWTSetup(object):
    def test_jwt_setup_options_are_set(self):
        assert_that(videona_platform.default_settings.JWT_EXPIRATION_DELTA, is_(timedelta(days=30)))
        assert_that(videona_platform.default_settings.JWT_AUTH_URL_RULE, is_('/api/v1/auth'))

    def test_JWT_extension_declared_in_core(self):
        assert_that(videona_platform.factory.jwt, instance_of(JWT))

    def test_JWT_is_initialized(self, api_app):
        assert_that('jwt', is_in(api_app.extensions))
        jwt = api_app.extensions['jwt']

        assert_that(jwt.authentication_callback, is_(authenticate))
        assert_that(jwt.identity_callback, is_(load_user))


class TestJWTHandlers(object):
    @mock.patch('videona_platform.factory.user_datastore.find_user')
    @mock.patch('videona_platform.factory.verify_password', mock.Mock(return_value=True))
    def test_authenticate_looks_for_user_in_datastore(self, find_user, session):
        user_email = 'email@test.com'

        user = authenticate(user_email, 'pwd')

        find_user.assert_called_once_with(email=user_email)


    @mock.patch('videona_platform.factory.user_datastore.find_user')
    def test_authenticate_returns_none_if_no_user_found(self, find_user):
        find_user.return_value = None

        user = authenticate('email@test.com', 'pwd')

        assert_that(user, none())


    @mock.patch('videona_platform.factory.user_datastore.find_user')
    @mock.patch('videona_platform.factory.verify_password')
    def test_authenticate_verify_password_if_user_found(self, verify_password, find_user, api_app, session):
        user = factories.UserFactory()
        find_user.return_value = user

        found_user = authenticate('email@test.com', 'pwd')

        verify_password.assert_called_once_with('pwd', user.password)


    @mock.patch('videona_platform.factory.user_datastore.find_user')
    @mock.patch('videona_platform.factory.verify_password')
    def test_authenticate_returns_user_if_user_found_and_passwornd_valid(self, verify_password, find_user, api_app, session):
        user = factories.UserFactory()
        find_user.return_value = user
        verify_password.return_value = True

        found_user = authenticate('email@test.com', 'pwd')

        assert_that(found_user, is_(user))


    @mock.patch('videona_platform.factory.user_datastore.find_user')
    def test_load_user_find_user_from_datastore(self, find_user):
        payload = {'identity': 'user_id'}

        load_user(payload)

        find_user.assert_called_once_with(id='user_id')


    @mock.patch('videona_platform.factory.user_datastore.find_user')
    def test_load_user_returns_found_user_from_user_datastore(self, find_user):
        user = factories.UserFactory()
        find_user.return_value = user
        payload = {'identity': 'user_id'}

        found_user = load_user(payload)

        assert_that(found_user, is_(user))
