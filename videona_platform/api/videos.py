# -*- coding: utf-8 -*-
"""
    videona_platform.api.videos
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Videona Plaform videos API
"""
from flask import request, jsonify
from flask.blueprints import Blueprint

from videona_platform.fiware.poi import fiware_send_video_poi
from videona_platform.videos.video_service import VideoService

videos_blueprint = Blueprint('videos', __name__, url_prefix='/v1/videos')

videos = VideoService()

@videos_blueprint.route('/', methods=['POST'])
def create_video():
    created_video = videos.create(**request.json)
    fiware_send_video_poi(created_video)
    return jsonify(dict(video=created_video)), 201
