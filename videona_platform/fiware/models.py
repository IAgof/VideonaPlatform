# -*- coding: utf-8 -*-
"""
    videona_platform.fiware.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fiware models
"""
from videona_platform.core import db


POI_CATEGORY_VIDEO = 'video_poi'
POI_CATEGORY_USER = 'user_poi'

pois_users = db.Table('pois_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('poi_id', db.Integer(), db.ForeignKey('fiware_poi.id')))

pois_videos = db.Table('pois_videos',
                       db.Column('video_id', db.Integer(), db.ForeignKey('video.id')),
                       db.Column('poi_id', db.Integer(), db.ForeignKey('fiware_poi.id')))


class FiwarePoi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poi_uuid = db.Column(db.String(100), unique=True)
    timestamp = db.Column(db.Integer())
    category = db.Column(db.Enum(POI_CATEGORY_VIDEO, POI_CATEGORY_USER, name='poi_category'))
    videos = db.relationship('Video', secondary=pois_videos,
                            backref=db.backref('videos', lazy='dynamic'))
    users = db.relationship('User', secondary=pois_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<POI %s: %s>' % (self.id, self.poi_uuid)
