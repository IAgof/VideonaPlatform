import os
from flask import Flask, Blueprint, current_app


def create_app():
    app = Flask(__name__)
    app.config.from_object('videona_platform.default_settings')
    app.logger.debug('Flask instance path is %s' % app.instance_path)
    app.register_blueprint(bp)
    return app

bp = Blueprint('main', __name__)


@bp.route('/')
def hello_world():
    return '#VideonaTime!'