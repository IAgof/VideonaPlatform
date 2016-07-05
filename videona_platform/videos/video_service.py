# -*- coding: utf-8 -*-
"""
    videona_platform.videos.video_service
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Video service module
"""
from videona_platform.core import Service
from videona_platform.videos import models


class VideoService(Service):
    __model__ = models.Video
