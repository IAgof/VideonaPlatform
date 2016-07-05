# -*- coding: utf-8 -*-
"""
    fiware.keyrock
    ~~~~~~~~~~~~~~

    fiware keyrock module for integrating IDM login and registration
"""
from __future__ import print_function

from flask import json, current_app
import requests

from videona_platform.fiware import fiware_settings
from videona_platform.fiware.fiware_settings import KEYROCK_ADMIN_USER, KEYROCK_ADMIN_PASSWORD

KEYROCK_URL = '%s:%s' % (fiware_settings.KEYROCK_HOST, fiware_settings.KEYROCK_PORT)
KEYROCK_TOKEN_URL = '%s/%s' % (KEYROCK_URL, fiware_settings.KEYROCK_TOKEN_ENDPOINT)
KEYROCK_USERS_URL = '%s/%s' % (KEYROCK_URL, fiware_settings.KEYROCK_USERS_ENDPOINT)

class KeyrockClient(object):
    apitoken = ''

    def keyrock_login(self, username, password):
        current_app.logger.debug('[keyrock_login]Authenticating user: %s' % username)
        payload = self.build_login_payload(username, password)
        current_app.logger.debug('login_payload: %s' % str(payload))
        headers = {'content-type': 'application/json'}
        response = requests.post(KEYROCK_TOKEN_URL, headers=headers, data=json.dumps(payload))
        current_app.logger.debug('response: %s' % str(response.content))
        return response

    def check_user_id(self, user_id):
        #TODO exceptions + logger
        self.validate_api_token()
        headers = {'X-Auth-Token': self.apitoken}
        response = requests.get('%s/%s' % (KEYROCK_USERS_URL, user_id), headers=headers)
        return response

    def user_info(self, user_id):
        self.validate_api_token()
        # TODO exceptions + logger
        headers = {'X-Auth-Token': self.apitoken}
        response = requests.get('%s/%s' % (KEYROCK_USERS_URL, user_id), headers=headers)
        if response.status_code == 200:
            return response.json()

    def activate_user(self, user_id):
        self.validate_api_token()
        headers = {'X-Auth-Token': self.apitoken, 'content-type': 'application/json'}
        payload = {'user': {'enabled': True}}
        response = requests.patch('%s/%s' % (KEYROCK_USERS_URL, user_id), headers=headers, data=json.dumps(payload))
        return response

    def find_user_id_by_email(self, email):
        self.validate_api_token()
        users = self.user_info('')
        if users == None:
            return
        users = users['users']
        current_app.logger.debug('Found %s users' % len(users))
        current_app.logger.debug(users)
        found_users = filter(lambda u: u.get('name') == email, users)
        current_app.logger.debug('Filtered %s users by email: %s' % (len(found_users), email))
        if len(found_users) > 0:
            return found_users[0].get('username')


    def validate_api_token(self):
        current_app.logger.debug('Original apitoken: ' + self.apitoken)
        headers = {'X-Auth-Token': self.apitoken, 'X-Subject-Token': self.apitoken}
        response = requests.head(KEYROCK_TOKEN_URL, headers=headers)
        #if not valid then login uPark RESTAPI and obtain API-TOKEN
        if not (200 <= response.status_code < 300):
            current_app.logger.debug('Requesting new token')
            payload = self.build_login_payload(KEYROCK_ADMIN_USER, KEYROCK_ADMIN_PASSWORD)
            headers = {'content-type': 'application/json'}
            response = requests.post(KEYROCK_TOKEN_URL, headers=headers,
                data=json.dumps(payload))
            self.apitoken = response.headers['x-subject-token']
            #TODO catch exception login fail, launch exception API token
            #validation fail.
        current_app.logger.debug('Valid apitoken: '+self.apitoken)

    def build_login_payload(self, username, password):
        return {
            "auth": {
                "identity": {
                    "methods": [ "password" ],
                    "password": {
                        "user": {
                            "id": username,
                            "password": password
                        }
                    }
                }
            }
        }

keyrock_client = KeyrockClient()


def fiware_authenticate_from_jwt(username, password):
    keyrock_user_id = None
    if keyrock_client.keyrock_login(username, password).status_code == 201:
        current_app.logger.debug('first auth correct')
        keyrock_user_id = username
    else:
        keyrock_user_id = keyrock_client.find_user_id_by_email(username)
        current_app.logger.debug('found keyrock user_id: %s' % keyrock_user_id)
    return keyrock_user_id
    # if keyrock_user_id != None:
    #     users.register(username, keyrock_user_id, password)
        # keyrock_user = keyrock_client.user_info(keyrock_user_id)['user']


# def create_videona_platform_user_from_keyrock(keyrock_user, password):
#     users.register(username=, email=, password=password)