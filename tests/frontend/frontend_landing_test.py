# -*- coding: utf-8 -*-
import pytest
from hamcrest import *
from flask import Blueprint, url_for
from videona_platform.frontend.frontend import front_page_blueprint


class TestLandingRoutes(object):
    def test_frontend_blueprint_definition(self, app):
        assert_that(front_page_blueprint, not_none())
        assert_that(front_page_blueprint, instance_of(Blueprint))
        assert_that(front_page_blueprint.name, is_("front_page"))
        assert_that(front_page_blueprint.url_prefix, none())
        assert_that(front_page_blueprint.name, is_in(app.blueprints))

    def test_bp_main_route(self, client):
        response = client.get(url_for('front_page.hello_world'))

        assert_that(response.status_code, is_(200))