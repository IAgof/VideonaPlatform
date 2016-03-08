# -*- coding: utf-8 -*-
from flask import Blueprint

front_page_blueprint = Blueprint('front_page', __name__)


@front_page_blueprint.route('/')
def hello_world():
    return '#VideonaTime!'