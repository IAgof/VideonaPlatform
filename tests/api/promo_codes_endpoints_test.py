# -*- coding: utf-8 -*-
"""
    tests/api/promo_codes_endpoints_test
    ~~~~~

    PromoCodes API endpoints tests
"""
from hamcrest import *
import mock

import json

from tests.conftest import mock_jwt_required
from videona_platform.promo_codes import models as promo_codes_models
from videona_platform.api.promo_codes import validate_promo_code
from videona_platform.promo_codes.promo_codes_service import PromoCodeValidationError


class TestPromoCodesEndpoints(object):
    @mock.patch('videona_platform.api.promo_codes.jsonify', mock.Mock())
    @mock.patch('flask_jwt._jwt_required', mock.Mock(side_effect=mock_jwt_required))
    @mock.patch('videona_platform.api.promo_codes.current_identity')
    @mock.patch('videona_platform.promo_codes.promo_codes_service.promo_codes_service.validate_code')
    def test_validate_calls_service(self, validate_code, current_identity, push_context):

        validate_promo_code('kode')

        validate_code.assert_called_once_with('kode', current_identity)

    @mock.patch('flask_jwt._jwt_required', mock.Mock(side_effect=mock_jwt_required))
    @mock.patch('videona_platform.promo_codes.promo_codes_service.promo_codes_service.first')
    def test_validate_returns_error_if_no_code(self, first, api_app):
        with api_app.test_request_context():
            first.return_value = None

            response, status_code = validate_promo_code('notfoundcode')

            assert_that(status_code, is_(404))
            assert_that(json.loads(response.data), is_({'valid_code': False, 'campaign': '', 'error': PromoCodeValidationError.MSG_CODE_NOT_FOUND}))

    @mock.patch('flask_jwt._jwt_required', mock.Mock(side_effect=mock_jwt_required))
    @mock.patch('videona_platform.api.promo_codes.current_identity', None)
    @mock.patch('videona_platform.promo_codes.promo_codes_service.promo_codes_service.first')
    def test_validate_returns_valid_code_response_if_code_validates(self, first, session, api_app):
        with api_app.test_request_context():
            code = promo_codes_models.PromoCode(code='code', campaign='wolder')
            first.return_value = code

            response, status_code = validate_promo_code(code_string='code')

            assert_that(status_code, is_(200))
            assert_that(json.loads(response.data), is_({'valid_code': True, 'campaign': 'wolder'}))
