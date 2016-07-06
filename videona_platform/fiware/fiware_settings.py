# -*- coding: utf-8 -*-
"""
    fiware.fiware_settings
    ~~~~~~~~~~~~~~~~~~~~~~

    Fiware specific settings
"""
import os


KEYROCK_HOST = os.environ.get('KEYROCK_HOST')
KEYROCK_PORT = '7003'
KEYROCK_ADMIN_USER = os.environ.get('KEYROCK_ADMIN_USER', 'idm_user')
KEYROCK_ADMIN_PASSWORD = os.environ.get('KEYROCK_ADMIN_PASSWORD', 'idm')
KEYROCK_TOKEN_ENDPOINT = 'v3/auth/tokens'
KEYROCK_USERS_ENDPOINT = 'v3/users'


POI_HOST = os.environ.get('POI_HOST', 'http://poi')
POI_PORT = os.environ.get('POI_PORT', 80)
POI_ADD_POI_ENDPOINT = 'poi_dp/add_poi'
POI_UPDATE_POI_ENDPOINT = 'poi_dp/update_poi'
POI_DELETE_POI_ENDPOINT = 'poi_dp/delete_poi'
POI_RADIAL_SEARCH_ENDPOINT = 'poi_dp/radial_search'
POI_VIDEO_CATEGORY = 'video'