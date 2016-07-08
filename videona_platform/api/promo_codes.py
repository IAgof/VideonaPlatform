# -*- coding: utf-8 -*-
"""
    videona_platform/api/promo_codes.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Promo codes API endpoints
"""
from flask import jsonify
from flask.blueprints import Blueprint
from flask_jwt import jwt_required

from videona_platform.promo_codes.promo_codes_service import promo_codes_service

promo_codes_blueprint = Blueprint('promo_codes', __name__, url_prefix='/v1/promo_codes')


@promo_codes_blueprint.route('/<code>', methods=['GET'])
@jwt_required()
def validate_promo_code(code):
    # TODO(jliarte) 20160708: refactor this code
    valid_code = False
    campaign = ''
    result_status_code = 404
    retrieved_code = promo_codes_service.validate_code(code)
    if retrieved_code is not None:
        result_status_code = 200
        valid_code = True
        campaign = retrieved_code.campaign or ''
    return jsonify(dict(valid_code=valid_code, campaign=campaign)), result_status_code