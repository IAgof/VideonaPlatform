# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~~~~~~

    Defines our app fixture
"""
import pytest
from videona_platform.factory import create_app


@pytest.fixture
def app():
    app = create_app()
    return app