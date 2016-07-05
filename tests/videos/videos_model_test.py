# -*- coding: utf-8 -*-
"""
    tests.videos.videos_models_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    videos models tests package
"""
from hamcrest import *
from tests.factories import UserFactory

from datetime import datetime

from videona_platform.videos import models
from videona_platform.users import models as users_models


class TestVideoModels(object):
    def test_video_model(self, session):
        now = datetime.utcnow()
        video = models.Video(
            lat=40.502956,
            lon=-3.887818,
            height=720,
            width=1080,
            rotation=90,
            duration=210093,
            size=890123478,
            bitrate=5000000,
            date=now,
            title='video title',
            video_type=models.RECORDED_VIDEO,
            url='https://s3.amazonaws.com/tiedots/clips/VID_20160303_182238.mp4'
        )

        session.add(video)
        session.commit()

        assert_that(video, not_none())
        assert_that(models.Video.query.count(), is_(1))

        saved_video = models.Video.query.all()[0]
        assert_that(saved_video.id, greater_than(0))
        assert_that(saved_video.lat, is_(40.502956))
        assert_that(saved_video.lon, is_(-3.887818))
        assert_that(saved_video.height, is_(720))
        assert_that(saved_video.width, is_(1080))
        assert_that(saved_video.rotation, is_(90))
        assert_that(saved_video.duration, is_(210093))
        assert_that(saved_video.size, is_(890123478))
        assert_that(saved_video.bitrate, is_(5000000))
        assert_that(saved_video.date, is_(now))
        assert_that(saved_video.title, is_('video title'))
        assert_that(saved_video.video_type, is_(models.RECORDED_VIDEO))
        assert_that(saved_video.url, is_('https://s3.amazonaws.com/tiedots/clips/VID_20160303_182238.mp4'))

    def test_video_model_has_user_field(self, session):
        user = UserFactory()
        session.add(user)
        session.commit()
        video = models.Video()

        video.user = user
        session.add(video)
        session.commit()

        saved_video = models.Video.query.all()[0]
        assert_that(saved_video.user, not_none())
        assert_that(saved_video.user_id, is_(user.id))
        saved_user = users_models.User.query.all()[0]
        assert_that(len(saved_user.videos.all()), is_(1))

    def test_video_json_serializer_fields(self):
        user_json_public_fields = ['id', 'lat', 'lon', 'width', 'height', 'rotation', 'duration', 'size',
                                   'date', 'bitrate', 'title', 'user_id']

        assert_that(models.VideoJSONSerializer.__json_public__, is_(user_json_public_fields))

    def test_video_model_has_video_json_serializer(self):
        assert_that(issubclass(models.Video, models.VideoJSONSerializer))
