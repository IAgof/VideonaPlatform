# -*- coding: utf-8 -*-
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy


#: Flask-SQLAlchemy and Flask-Migrate extension instance for db
db = SQLAlchemy()
migrate = Migrate()

#: Flask-Security extension instance
security = Security()