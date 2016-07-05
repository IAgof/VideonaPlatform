# -*- coding: utf-8 -*-
"""
    tests.fiware.jwt_authenticate_with_idm_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    tests for IDM authentication fallback for JWT
"""
from hamcrest import *
import mock

from videona_platform.factory import authenticate
from videona_platform.fiware.keyrock import fiware_authenticate_from_jwt, keyrock_client


class TestJWTAuthenticationIDM(object):
    @mock.patch('videona_platform.factory.fiware_authenticate_from_jwt')
    def test_authenticate_calls_keyrock_auth(self, fiware_authenticate_from_jwt, session):
        authenticate('username', 'password')

        fiware_authenticate_from_jwt.assert_called_once_with('username', 'password')

    @mock.patch('videona_platform.fiware.keyrock.keyrock_client.keyrock_login')
    def test_fiware_authenticate_from_jwt_calls_keyrock_login(self, keyrock_login):
        fiware_authenticate_from_jwt('username', 'password')

        keyrock_login.assert_called_once_with('username', 'password')

    def test_keyrock_response(self, push_context):
        import ipdb; ipdb.set_trace()
        unauthorized_response = keyrock_client.keyrock_login('dsa','dsa')
        authorized_response = keyrock_client.keyrock_login('idm_user', 'idm')

        keyrock_client.validate_api_token()
        user_id = keyrock_client.find_user_id_by_email('idm')

        assert_that(False)


KEYSTONE_VALID_AUTH_RESPONSE = {u'token': {u'audit_ids': [u'-RlnqqgXQWSDxL9gK7ceuw'],
            u'catalog': [{u'endpoints': [{u'id': u'89bb3c5d52f849bbbe31c4706163079f',
                                          u'interface': u'admin',
                                          u'region': u'Spain2',
                                          u'region_id': u'Spain2',
                                          u'url': u'http://127.0.0.1:35357/v3/'},
                                         {u'id': u'd17225dab7074845bb1d237aa63961ae',
                                          u'interface': u'public',
                                          u'region': u'Spain2',
                                          u'region_id': u'Spain2',
                                          u'url': u'http://127.0.0.1:5000/v3/'},
                                         {u'id': u'db9e9d8615224d0db2d35671fa338bb7',
                                          u'interface': u'internal',
                                          u'region': u'Spain2',
                                          u'region_id': u'Spain2',
                                          u'url': u'http://127.0.0.1:35357/v3/'}],
                          u'id': u'2bd49d3c692f48cabe1e767669116062',
                          u'name': u'keystone',
                          u'type': u'identity'}],
            u'expires_at': u'2016-09-29T06:40:01.257322Z',
            u'extras': {},
            u'issued_at': u'2016-07-01T06:40:01.257410Z',
            u'methods': [u'password'],
            u'project': {u'domain': {u'id': u'default', u'name': u'Default'},
                         u'id': u'idm_project',
                         u'name': u'idm'},
            u'roles': [{u'id': u'a0fa50d064e14382b8153ca1a190a258',
                        u'name': u'admin'},
                       {u'id': u'b0d84b87541946eba05519d6404e798d',
                        u'name': u'owner'}],
            u'user': {u'domain': {u'id': u'default', u'name': u'Default'},
                      u'id': u'idm_user',
                      u'name': u'idm'}}}

KEYSTONE_VALID_AUTH_RESPONSE_HEADERS = {'Content-Length': '1054', 'X-Subject-Token': '446e2d2ac3db4f3d9130607d298e7186', 'Vary': 'X-Auth-Token', 'Connection': 'keep-alive', 'Date': 'Fri, 01 Jul 2016 06:40:01 GMT', 'Content-Type': 'application/json'}
