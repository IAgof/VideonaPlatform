# -*- coding: utf-8 -*-
"""
    tests/promo_codes/promo_codes_generate_command_test.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    PromoCodes generation management command tests
"""
from hamcrest import *
import mock

from datetime import datetime

from videona_platform.promo_codes.commands import GeneratePromoCodesCommand, PromoCodesGenerator
from manage import manager

class TestPromoCodesGenerator(object):
    def test_init(self):
        someday = datetime.utcnow()
        promo_code_generator = PromoCodesGenerator(campaign='wolder', expires_at=someday)

        assert_that(promo_code_generator.campaign, is_('wolder'))
        assert_that(promo_code_generator.expires_at, is_(someday))

    @mock.patch('videona_platform.promo_codes.commands.PromoCodesGenerator._set_campaign_seed')
    def test_init_sets_seed(self, _set_campaign_seed):
        promo_code_generator = PromoCodesGenerator(campaign='wolder', expires_at=None)

        _set_campaign_seed.assert_called_once_with()


    @mock.patch('random.seed')
    def test_set_campaign_seed_sets_seed_if_campaign_is_non_empty_string(self, seed):
        promo_code_generator = PromoCodesGenerator(campaign=None, expires_at=None)

        promo_code_generator._set_campaign_seed()

        seed.assert_not_called()

        promo_code_generator.campaign = ''
        promo_code_generator._set_campaign_seed()

        seed.assert_not_called()

        promo_code_generator.campaign = 'wolder'
        promo_code_generator._set_campaign_seed()

        seed.assert_called_once_with('wolder')

    @mock.patch('videona_platform.core.Service.first', mock.Mock(return_value=None))
    @mock.patch('videona_platform.core.Service.create', mock.Mock())
    @mock.patch('videona_platform.promo_codes.promo_codes_service.PromoCodesService.generate_code_string')
    def test_generate_unique_calls_service__code_generator(self, generate_code_string):
        promo_code_generator = PromoCodesGenerator(campaign='wolder', expires_at=None)

        result = promo_code_generator.generate_unique()

        generate_code_string.assert_called_once_with()

    @mock.patch('videona_platform.core.Service.first', mock.Mock(return_value=None))
    @mock.patch('videona_platform.promo_codes.promo_codes_service.PromoCodesService.generate_code_string')
    @mock.patch('videona_platform.core.Service.create')
    def test_generate_unique_calls_promo_code_service_create(self, create, generate_code_string):
        someday = datetime.utcnow()
        generate_code_string.return_value = 'generated_code'
        create.return_value = created_promo_code = mock.Mock()
        promo_code_generator = PromoCodesGenerator(campaign='wolder', expires_at=someday)

        result = promo_code_generator.generate_unique()

        create.assert_called_once_with(campaign='wolder', expires_at=someday, code='generated_code')
        assert_that(result, is_(created_promo_code))

    @mock.patch('videona_platform.promo_codes.promo_codes_service.PromoCodesService.generate_code_string')
    @mock.patch('videona_platform.core.Service.first')
    @mock.patch('videona_platform.core.Service.create')
    def test_generate_unique_does_not_call_create_until_no_existing_code_found(self, create, first, generate_code_string):
        first.side_effect = [mock.Mock(), None]
        generate_code_string.side_effect = ['code1', 'code2']
        promo_codes_generator = PromoCodesGenerator(campaign='wolder', expires_at=None)

        result = promo_codes_generator.generate_unique()

        assert_that(first.call_count, is_(2))
        first.assert_called_with(code='code2')
        first.assert_any_call(code='code1')
        create.assert_called_once_with(campaign='wolder', expires_at=None, code='code2')

    @mock.patch('videona_platform.promo_codes.commands.PromoCodesGenerator.generate_unique')
    def test_generate_calls_generate_unique_n_times(self, generate_unique):
        code1 = mock.Mock()
        code2 = mock.Mock()
        generate_unique.side_effect = [code1, code2]
        promo_codes_generator = PromoCodesGenerator(campaign='wolder', expires_at=None)

        result = promo_codes_generator.generate(number_of_codes=2)

        assert_that(generate_unique.call_count, is_(2))
        assert_that(result, is_([code1, code2]))


class TestGeneratePromoCodesCommand(object):
    @mock.patch('videona_platform.promo_codes.commands.PromoCodesGenerator.__init__')
    @mock.patch('videona_platform.promo_codes.commands.PromoCodesGenerator.generate')
    def test_command_calls_promo_codes_generator(self, generate, __init__):
        __init__.return_value = None
        someday = datetime.utcnow()

        GeneratePromoCodesCommand().run(number_of_codes=3, campaign='alaleiro', expires_at=someday)

        __init__.assert_called_once_with(campaign='alaleiro', expires_at=someday)
        generate.assert_called_once_with(number_of_codes=3)

    def test_command_is_registered(self):
        assert_that(manager._commands['generate_promo_codes'], is_(GeneratePromoCodesCommand))
