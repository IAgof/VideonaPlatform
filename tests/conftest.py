# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~~~~~~

    Defines our app fixture
"""
import pytest
from alembic.command import upgrade
from alembic.config import Config

import videona_platform.api.factory
import videona_platform.frontend.factory
from videona_platform import core
from videona_platform.fiware import fiware_settings
import test_settings


ALEMBIC_CONFIG = 'migrations/alembic.ini'


@pytest.fixture(scope='session')
def frontend_app():
    app = videona_platform.frontend.factory.create_app(test_settings)
    return app


@pytest.fixture(scope='session')
def api_app():
    app = videona_platform.api.factory.create_app(test_settings)
    return app


@pytest.fixture(scope='session')
def app(api_app):
    # Default app fixture. Seems to be asked by client fixture
    return api_app


@pytest.fixture(scope='session')
def api_app_fiware():
    settings = test_settings
    settings.FIWARE_INSTALLED = True
    app = videona_platform.api.factory.create_app(settings)
    app.config.from_object(fiware_settings)
    return app


@pytest.fixture
def push_context(api_app, request):
    context = api_app.app_context()
    context.push()

    def teardown():
        context.pop()

    request.addfinalizer(teardown)
    return context


def apply_migrations():
    """ Applies all alembic migrations. """
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')


@pytest.fixture(scope='session')
def db(api_app, request):
    """
    Create session-wide test database
    :param api_app: api app fixture
    :param request:
    :return:
    """
    def teardown():
        core.db.drop_all()

    core.db.app = api_app
    # Apply already created migrations
    with api_app.app_context():
        apply_migrations()
        # And create pending models, not already as migrations, for testing purposes
        core.db.create_all()

        request.addfinalizer(teardown)
    return core.db


@pytest.fixture(scope='function')
def session(api_app, db, request, monkeypatch):
    """
    Creates a new database session for a test
    :param db: db fixture
    :param request:
    :return:
    """
    with api_app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

    # Patch Flask-SQLAlchemy to use our connection instead of replacing the whole session
    # See https://github.com/mitsuhiko/flask-sqlalchemy/pull/249
    monkeypatch.setattr(core.db, 'get_engine', lambda *args: connection)

    def teardown():
        core.db.session.remove()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    return core.db.session
