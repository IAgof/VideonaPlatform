# -*- coding: utf-8 -*-
"""
    videona_platform.fiware.fiware_services
    ~~~~~

    Fiware services
"""
from videona_platform.core import Service
from videona_platform.fiware.models import FiwarePoi


class FiwarePOIService(Service):
    __model__ = FiwarePoi


fiware_poi_service = FiwarePOIService()