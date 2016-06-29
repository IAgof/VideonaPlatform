# -*- coding: utf-8 -*-
"""
    core
    ~~~~

    Core module, with main extensions and common classes
"""
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

#: Flask-SQLAlchemy and Flask-Migrate extension instance for db
db = SQLAlchemy()
migrate = Migrate()

#: Flask-Security extension instance
security = Security()


class VideonaError(Exception):
    def __init__(self, msg):
        self.msg = msg