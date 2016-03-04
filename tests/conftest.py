# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~~~~~~

    Defines our app fixture
"""
import pytest
from alembic.command import upgrade
from alembic.config import Config
from videona_platform.factory import create_app
from videona_platform.core import db as _db
import test_settings


ALEMBIC_CONFIG = 'migrations/alembic.ini'


@pytest.fixture(scope='session')
def app():
    app = create_app(test_settings)
    return app


def apply_migrations():
    """ Applies all alembic migrations. """
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')


@pytest.fixture(scope='session')
def db(app, request):
    """
    Create session-wide test database
    :param app: app fixture
    :param request:
    :return:
    """
    def teardown():
        _db.drop_all()

    _db.app = app
    # Apply already created migrations
    apply_migrations()
    # And create pending models, not already as migrations, for testing purposes
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request, monkeypatch):
    """
    Creates a new database session for a test
    :param db: db fixture
    :param request:
    :return:
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    # Patch Flask-SQLAlchemy to use our connection instead of replacing the whole session
    # See https://github.com/mitsuhiko/flask-sqlalchemy/pull/249
    monkeypatch.setattr(_db, 'get_engine', lambda *args: connection)

    def teardown():
        _db.session.remove()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    return _db.session
