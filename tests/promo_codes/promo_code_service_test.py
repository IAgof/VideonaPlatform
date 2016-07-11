# -*- coding: utf-8 -*-
"""
    tests/promo_codes/promo_codes_service_test.py
    ~~~~~

    PromoCode service tests
"""
import pytest
from hamcrest import *
import mock

from datetime import datetime, timedelta

from tests.factories import PromoCodeFactory, UserFactory
from videona_platform.core import Service
from videona_platform.promo_codes import models
from videona_platform.promo_codes.promo_codes_service import PromoCodesService, promo_codes_service, \
    PromoCodeValidationError


A_CODE_STRING = 'a.code'


class TestPromoCodesService(object):
    def test_promo_codes_service_is_a_service(self):
        assert_that(issubclass(PromoCodesService, Service))
        assert_that(PromoCodesService.__model__, equal_to(models.PromoCode))

    @mock.patch('videona_platform.core.Service.first')
    def test_promo_codes_service_validate_calls_first_and_returns_found_code(self, first, session, push_context):
        first.return_value = promo_code_returned = PromoCodeFactory()

        returned_code = promo_codes_service.validate_code(A_CODE_STRING, None)

        first.assert_called_once_with(code=A_CODE_STRING)
        assert_that(returned_code, is_(promo_code_returned))

    @mock.patch('videona_platform.core.Service.first')
    def test_validate_assign_user_to_promo_code(self, first, session):
        code = PromoCodeFactory()
        user = UserFactory()
        first.return_value = code

        returned_code = promo_codes_service.validate_code(code_string=A_CODE_STRING, validated_by=user)

        assert_that(returned_code.redeemed_by, is_(user))

    @mock.patch('videona_platform.core.Service.first')
    def test_validate_raises_error_if_code_already_redeemed(self, first, session):
        code = PromoCodeFactory(redeemed=True)
        first.return_value = code

        with pytest.raises(PromoCodeValidationError) as error_info:
            returned_code = promo_codes_service.validate_code(A_CODE_STRING, None)

            assert_that(error_info.value.msg, is_(PromoCodeValidationError.MSG_CODE_ALREADY_REDEEMED))

    @mock.patch('videona_platform.core.Service.first')
    def test_validate_sets_redeemed_true_to_found_code(self, first, session):
        code = PromoCodeFactory(redeemed=False)
        first.return_value = code

        returned_code = promo_codes_service.validate_code(A_CODE_STRING, None)

        assert_that(returned_code.redeemed, is_(True))

    @mock.patch('videona_platform.core.Service.first')
    def test_validate_raises_error_if_code_has_expired(self, first, session):
        yesterday = datetime.utcnow() - timedelta(days=1)
        code = PromoCodeFactory(expires_at=yesterday)
        first.return_value = code

        with pytest.raises(PromoCodeValidationError) as error_info:
            returned_code = promo_codes_service.validate_code(A_CODE_STRING, None)

            assert_that(error_info.value.msg, is_(PromoCodeValidationError.MSG_CODE_HAS_EXPIRED))

    @mock.patch('videona_platform.core.Service.first')
    def test_validate_raises_error_if_no_code_found(self, first):
        first.return_value = None

        with pytest.raises(PromoCodeValidationError) as error_info:
            returned_code = promo_codes_service.validate_code(A_CODE_STRING, None)

            assert_that(error_info.value.msg, is_(PromoCodeValidationError.MSG_CODE_NOT_FOUND))
