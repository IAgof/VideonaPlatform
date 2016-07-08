# -*- coding: utf-8 -*-
"""
    tests/promo_codes/promo_codes_model_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Promo codes model tests
"""
from hamcrest import *
from freezegun.api import freeze_time

from datetime import datetime

from tests.factories import UserFactory
from videona_platform.promo_codes import models



class TestPromoCodeModel(object):
    @freeze_time("2015-01-12 17:34:47+00:00")
    def test_promo_code_model_fields(self, session):
        now = datetime.utcnow()
        fake_now = datetime(2015, 1, 12, 17, 34, 47)  # freezgun isn't working...
        expiration_day = datetime(2020, 1, 12)
        code = 'fiakunfk543iueh32nae2wiukfn423'
        promo_code = models.PromoCode(
            code=code,
            expires_at=expiration_day,
            campaign='wolder',
            redeemed=False
        )
        session.add(promo_code)
        session.commit()

        assert_that(promo_code.id, greater_than(0))
        assert_that(models.PromoCode.query.count(), is_(1))
        saved_promo_code = models.PromoCode.query.all()[0]
        assert_that(saved_promo_code.code, is_(code))
        assert_that(saved_promo_code.created_at, is_(greater_than(now)))
        assert_that(saved_promo_code.expires_at, is_(expiration_day))
        assert_that(saved_promo_code.campaign, is_('wolder'))
        assert_that(saved_promo_code.redeemed, is_(False))

    def test_promo_code_has_redeemed_by(self, session):
        user = UserFactory()
        promo_code = models.PromoCode(
            code='fiakunfk543iueh32nae2wiukfn423',
            campaign='wolder',
            redeemed=False
        )

        promo_code.redeemed_by = user
        session.add(promo_code)
        session.commit()

        saved_promo_code = models.PromoCode.query.filter_by(redeemed_by=user).first()
        assert_that(saved_promo_code, not_none())
        assert_that(saved_promo_code.redeemed_by, is_(user))

    def test_promo_code_repr(self):
        code = 'fiakunfk543iueh32nae2wiukfn423'
        promo_code = models.PromoCode(
            code=code,
            campaign='wolder',
            redeemed=False
        )

        assert_that(str(promo_code), is_('<PromoCode %s>' % code))
