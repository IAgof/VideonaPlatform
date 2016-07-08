# -*- coding: utf-8 -*-
"""
    videona_platform/promo_codes/promo_codes_service.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    PromoCodes Service
"""
from videona_platform.core import Service
from videona_platform.promo_codes import models


class PromoCodesService(Service):
    __model__ = models.PromoCode

    def validate_code(self, code):
        return self.first(code=code)


promo_codes_service = PromoCodesService()
