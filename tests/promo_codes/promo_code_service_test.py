# -*- coding: utf-8 -*-
"""
    tests/promo_codes/promo_codes_service_test.py
    ~~~~~

    PromoCode service tests
"""
from hamcrest import *
import mock

from videona_platform.core import Service
from videona_platform.promo_codes import models
from videona_platform.promo_codes.promo_codes_service import PromoCodesService, promo_codes_service


class TestPromoCodesService(object):
    def test_promo_codes_service_is_a_service(self):
        assert_that(issubclass(PromoCodesService, Service))
        assert_that(PromoCodesService.__model__, equal_to(models.PromoCode))

    @mock.patch('videona_platform.core.Service.first')
    def test_promo_codes_service_validate_calls_first(self, first, push_context):
        first.return_value = promo_code_returned = mock.Mock()
        code = 'fslkdsfs'

        returned_code = promo_codes_service.validate_code(code)

        first.assert_called_once_with(code=code)
        assert_that(returned_code, is_(promo_code_returned))

