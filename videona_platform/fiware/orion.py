# -*- coding: utf-8 -*-
"""
    videona_platform.fiware.orion
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fiware Orion (context broker) client and helpers
"""
import requests
from flask import json
from flask.globals import current_app

from videona_platform.fiware import fiware_settings


class OrionClient(object):
    ORION_URL = '%s:%s' % (fiware_settings.ORION_HOST, fiware_settings.ORION_PORT)
    ORION_ENTITIES_URL = '%s/%s' % (ORION_URL, fiware_settings.ORION_ENTITIES_ENDPOINT)
    JSON_HEADERS = {'Content-Type': 'application/json'}
    JSON_HEADERS_ACCEPT = {'Accept': 'application/json'}

    def create_video_entity(self, video):
        orion_response = requests.post(self.ORION_ENTITIES_URL, data=json.dumps(self.__build_video_entity(video)),
                                       headers=self.JSON_HEADERS)
        current_app.logger.debug('Orion response received: %s %s' % (orion_response, orion_response.headers))
        return orion_response

    def query_video_entities(self):
        orion_response = requests.get('%s?type=Video' % self.ORION_ENTITIES_URL, headers=self.JSON_HEADERS_ACCEPT)
        current_app.logger.debug('Orion response received: %s %s' % (orion_response, orion_response.json()))
        return orion_response

    def __build_video_entity(self, video):
        entity = {
            "id": "Video_%s" % video.id,
            "type": "Video",
            "location": {
                "type": "geo:point",
                "value": "%s, %s" % (video.lat, video.lon)
            },
            "height": {
                "value": video.height,
                "type": "Number"
            },
            "width": {
                "value": video.width,
                "type": "Number"
            },
            "duration": {
                "value": video.duration,
                "type": "Number"
            },
            "description": {
                "value": video.title or ''
            }
        }
        return entity


orion_client = OrionClient()


def fiware_send_video_context_info(video):
    if current_app.config.get('FIWARE_INSTALLED') is not True:
        return
    if video.lat and video.lon:
        current_app.logger.debug('Sending Orion new video context info')
        orion_response = orion_client.create_video_entity(video)
    if orion_response.status_code == 200:
        current_app.logger.debug('creating local poi association')
    return orion_response
