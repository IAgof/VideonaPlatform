# -*- coding: utf-8 -*-
"""
    videona_platform/api/promo_codes.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Promo codes API endpoints
"""
from flask import jsonify
from flask.blueprints import Blueprint
from flask_jwt import jwt_required, current_identity

from videona_platform.promo_codes.promo_codes_service import promo_codes_service, PromoCodeValidationError

promo_codes_blueprint = Blueprint('promo_codes', __name__, url_prefix='/v1/promo_codes')


@promo_codes_blueprint.route('/<code_string>', methods=['GET'])
@jwt_required()
def validate_promo_code(code_string):
    result_status_code = 200
    try:
        retrieved_code = promo_codes_service.validate_code(code_string, current_identity)
        return jsonify(dict(valid_code=True, campaign=retrieved_code.campaign or '')), result_status_code
    except PromoCodeValidationError as validation_error:
        if validation_error.msg is PromoCodeValidationError.MSG_CODE_NOT_FOUND:
            result_status_code = 404
        return jsonify(dict(valid_code=False, campaign='', error=validation_error.msg)), result_status_code
