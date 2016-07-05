# -*- coding: utf-8 -*-
"""
    videona_platform.models
    ~~~~~~~~~~~~~~~~~~~~~~~

    Video models
"""
from videona_platform.core import db
from videona_platform.helpers import JSONSerializer


class VideoJSONSerializer(JSONSerializer):
    __json_public__ = ['id', 'lat', 'lon', 'width', 'height', 'rotation', 'duration', 'size',
                                   'date', 'bitrate', 'title', 'user_id']

EDITED_VIDEO = "Edited"
RECORDED_VIDEO = "Recorded"
GALLERY_VIDEO = "Gallery"

# VideoType = enum.Enum(EDITED_VIDEO, RECORDED_VIDEO, GALLERY_VIDEO)


class Video(db.Model, VideoJSONSerializer):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())
    width = db.Column(db.Integer())
    height = db.Column(db.Integer())
    rotation = db.Column(db.Integer())
    duration = db.Column(db.BigInteger())
    size = db.Column(db.BigInteger())
    date = db.Column(db.DateTime())
    bitrate = db.Column(db.Integer())
    title = db.Column(db.String(500))
    url = db.Column(db.String(500))
    video_type = db.Column(db.Enum(EDITED_VIDEO, RECORDED_VIDEO, GALLERY_VIDEO, name='video_types'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Video: %s>' % self.title
