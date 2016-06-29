# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~

    Videona Platform user related models
"""
import re
from sqlalchemy.orm import validates

from videona_platform.core import db, VideonaError
from flask_security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    USER_ERROR_EMAIL_NOT_VALID = 'Email not valid'

    # __tablename__ = ''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User: %s>' % self.username

    @validates('email')
    def validate_email(self, key, address):
        if not re.match('[^@]+@[^@]+\.[^@]+', address):
            raise VideonaError(User.USER_ERROR_EMAIL_NOT_VALID)
        return address


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role: %s>' % self.name
