# -*- coding: utf-8 -*-
"""
    videona_platform/promo_codes/promo_codes_service.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    PromoCodes Service
"""
from datetime import datetime

from videona_platform.core import Service, VideonaError
from videona_platform.promo_codes import models


class PromoCodeValidationError(VideonaError):
    MSG_CODE_NOT_FOUND = 'Code not found'
    MSG_CODE_HAS_EXPIRED = 'Code has already expired'
    MSG_CODE_ALREADY_REDEEMED = 'Code has been already redeemed'


class PromoCodesService(Service):
    __model__ = models.PromoCode

    def validate_code(self, code_string, validated_by):
        found_code = self.first(code=code_string)
        if found_code is None:
            raise PromoCodeValidationError(PromoCodeValidationError.MSG_CODE_NOT_FOUND)
        self.__validate_code_redeemed(found_code)
        self.__validate_code_expiration(found_code)
        self.update(found_code, redeemed_by=validated_by, redeemed=True, redeemed_at=datetime.utcnow())
        return found_code

    def __validate_code_redeemed(self, code):
        if code is not None and code.redeemed:
            raise PromoCodeValidationError(PromoCodeValidationError.MSG_CODE_ALREADY_REDEEMED)

    def __validate_code_expiration(self, found_code):
        if found_code is not None and found_code.expires_at is not None and found_code.expires_at < datetime.utcnow():
            raise PromoCodeValidationError(PromoCodeValidationError.MSG_CODE_HAS_EXPIRED)


promo_codes_service = PromoCodesService()
