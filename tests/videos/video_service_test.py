# -*- coding: utf-8 -*-
"""
    tests.videos.video_service_test
    ~~~~~

    Video service tests module
"""
from hamcrest import *

from videona_platform.core import Service
from videona_platform.videos import models as videos_models
from videona_platform.videos.video_service import VideoService

class TestVideoService(object):
    def test_video_service_is_a_service(self):
        assert_that(issubclass(VideoService, Service))
        assert_that(VideoService.__model__, equal_to(videos_models.Video))
