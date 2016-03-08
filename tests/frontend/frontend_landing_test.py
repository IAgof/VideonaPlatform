# -*- coding: utf-8 -*-
import pytest
import mock
from hamcrest import *
from contextlib import contextmanager
from flask import Blueprint, url_for
from videona_platform.frontend.frontend import front_page_blueprint

@contextmanager
def patch_view_function(app, view):
        original_function = app.view_functions[view]
        app.view_functions[view] = patched_function = mock.Mock()
        patched_function.return_value = 'view patched!'

        try:
            yield patched_function
        finally:
            """Unpatch the view."""
            app.view_functions[view] = original_function


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


    def test_root_calls_hello_world_view(self, app, client):
        with patch_view_function(app, 'front_page.hello_world') as hello_world:

            client.get('/')

            assert_that(hello_world.called, is_(True))


    @mock.patch('videona_platform.frontend.frontend.render_template', autospec=True)
    def test_template_used(self, render_template, client):
        render_template.return_value = 'rendered'

        client.get('/')

        assert_that(render_template.called, is_(True))
        render_template.assert_called_once_with('front_page.html')