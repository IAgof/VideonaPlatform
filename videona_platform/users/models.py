# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~

    Videona Platform user related models
"""
import re

from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import validates

from videona_platform.core import db, VideonaError
from videona_platform.helpers import JSONSerializer
from videona_platform.default_settings import MINIMUN_PASSWORD_LENGTH

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class UserJSONSerializer(JSONSerializer):
    __json_public__ = ['id', 'username', 'email']


class User(db.Model, UserJSONSerializer, UserMixin):
    USER_ERROR_EMAIL_NOT_VALID = 'Email not valid'
    USER_ERROR_PASSWORD_TOO_SHORT = 'Password too short. Type at least ' + str(MINIMUN_PASSWORD_LENGTH) + ' characters'

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
    videos = db.relationship('Video', backref='user', lazy='dynamic')
    redeemed_codes = db.relationship('PromoCode', backref='redeemed_by',
                                lazy='dynamic')

    def __repr__(self):
        return '<User %s: %s - %s>' % (self.id, self.username, self.email)

    @validates('email')
    def validate_email(self, key, address):
        if not re.match('[^@]+@[^@]+\.[^@]+', address):
            raise VideonaError(User.USER_ERROR_EMAIL_NOT_VALID)
        return address

    @validates('password')
    def validate_password_length(self, key, password):
        if len(password) < MINIMUN_PASSWORD_LENGTH:
            raise VideonaError(User.USER_ERROR_PASSWORD_TOO_SHORT)
        return password


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role: %s>' % self.name
