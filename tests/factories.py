# -*- coding: utf-8 -*-
"""
    factories
    ~~~~~~~~~~~~~

    Factories for testing videona platform (using factory boy)
"""
import factory
from factory import alchemy
from videona_platform.users import models as user_models
from videona_platform.core import db

class UserFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = user_models.User
        sqlalchemy_session = db.session # the SQLAlchemy session object

    username = factory.Sequence(lambda n: u'User %d' % n)


class RoleFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = user_models.Role
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: u'Role %d' % n)
    description = factory.Sequence(lambda n: u'Role description %d' % n)