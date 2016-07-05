# -*- coding: utf-8 -*-
"""
    videona_platform.api.videos
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Videona Plaform videos API
"""
from flask import request, jsonify
from flask.blueprints import Blueprint

from videona_platform.videos.video_service import VideoService

videos_blueprint = Blueprint('videos', __name__, url_prefix='/v1/videos')

videos = VideoService()

@videos_blueprint.route('/', methods=['POST'])
def create_video():
    created_video = videos.create(**request.json)
    return jsonify(dict(video=created_video)), 201
