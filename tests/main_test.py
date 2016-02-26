# -*- coding: utf-8 -*-
import pytest
from hamcrest import *

from flask import url_for


class TestMain(object):
    def test_app(self, client):
        response = client.get(url_for('main.hello_world'))

        assert_that(response.status_code, is_(200))