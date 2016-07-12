# -*- coding: utf-8 -*-
"""
    videona_platform/promo_codes/commands.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    PromoCodes managemen commands
"""
import random

from flask_script.commands import Command, Option

from videona_platform.promo_codes.promo_codes_service import PromoCodesService, promo_codes_service


class PromoCodesGenerator(object):
    def __init__(self, campaign, expires_at):
        self.campaign = campaign
        self.expires_at = expires_at
        self._set_campaign_seed()

    def _set_campaign_seed(self):
        if self.campaign and len(self.campaign) > 0:
            random.seed(self.campaign)

    def generate_unique(self):
        generated_code = PromoCodesService.generate_code_string()
        if promo_codes_service.first(code=generated_code) is not None:
            return self.generate_unique()
        return promo_codes_service.create(code=generated_code, campaign=self.campaign, expires_at=self.expires_at)

    def generate(self, number_of_codes):
        return [self.generate_unique() for index in range(0, number_of_codes)]


class GeneratePromoCodesCommand(Command):
    "Generates a number of promo codes for a given campaign"

    def get_options(self):
        return [
            Option('-n', '--number_of_codes', dest='number_of_codes', default=0),
            Option('-c', '--campaign', dest='campaign'),
            Option('-e', '--expires_at', dest='expires_at', default=None),
        ]

    def run(self, number_of_codes, campaign, expires_at):
        promo_codes_generator = PromoCodesGenerator(campaign=campaign, expires_at=expires_at)
        generated_codes = promo_codes_generator.generate(number_of_codes=int(number_of_codes))
        print 'code string;campaign;expires_at'
        for code in generated_codes:
            print '%s;%s;%s' % (code.code, code.campaign, code.expires_at)
