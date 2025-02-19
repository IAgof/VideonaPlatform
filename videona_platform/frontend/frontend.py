# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


front_page_blueprint = Blueprint('front_page', __name__, template_folder='templates',
                                 static_folder='static', static_url_path='/frontend/static')


@front_page_blueprint.route('/')
def hello_world():
    return render_template('front_page.html')