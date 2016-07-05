# -*- coding: utf-8 -*-
"""
    tests.fiware.api_app_fiware_setup_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    tests module for fiware related api app config
"""
from hamcrest import *


class TestFiwareAPIAppSetup(object):
    def test_api_app_has_keyrock_config(self, api_app_fiware):
        assert_that(api_app_fiware.config.get('FIWARE_INSTALLED'), is_(True))
        assert_that(api_app_fiware.config.get('KEYROCK_HOST'), is_('http://keyrock'))
