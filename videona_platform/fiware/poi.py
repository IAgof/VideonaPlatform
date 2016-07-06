# -*- coding: utf-8 -*-
"""
    videona_platform.fiware.poi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fiware POI GE client
"""
import requests
from flask import current_app, json

from videona_platform.core import db
from videona_platform.fiware import fiware_settings
from videona_platform.fiware import models as fiware_models
from videona_platform.fiware.fiware_services import fiware_poi_service
from videona_platform.fiware.fiware_settings import POI_VIDEO_CATEGORY


class POIClient(object):
    POI_URL = '%s:%s' % (fiware_settings.POI_HOST, fiware_settings.POI_PORT)
    POI_ADD_POI_URL = '%s/%s' % (POI_URL, fiware_settings.POI_ADD_POI_ENDPOINT)
    POI_UPDATE_POI_URL = '%s/%s' % (POI_URL, fiware_settings.POI_UPDATE_POI_ENDPOINT)
    POI_RADIAL_SEARCH_URL = '%s/%s' % (POI_URL, fiware_settings.POI_RADIAL_SEARCH_ENDPOINT)
    JSON_HEADERS = {"content-type": "application/json"}

    def create(self, data, category):
        current_app.logger.debug('Creating POI with data %s' % str(data))
        response = requests.post(self.POI_ADD_POI_URL, data=json.dumps(self.__build_poi(data, category)),
                                 headers=self.JSON_HEADERS)
        current_app.logger.debug(response)
        current_app.logger.debug(response.content)
        return response

    def radial_search(self, lat, lon, radius):
        params = {'lat': lat, 'lon': lon, 'radius': radius, 'component': 'fw_core'}
        current_app.logger.debug('radial_search: %s' % str(params))
        return requests.get(self.POI_RADIAL_SEARCH_URL, params=params, headers=self.JSON_HEADERS)

    def __build_poi(self, data, category):
        poi = {
            "fw_core": {
                "location": {
                    "wgs84": {
                        "latitude": float(data['location']['lat']),
                        "longitude": float(data['location']['lon'])
                    }
                },
                "name": {
                    "": str(data['name'])
                },
                "categories": ["ap", category],
                "description": {
                    "": str(data.get('description', '#VideonaTime!'))
                }
            }
        }

        # if last_update is not 0:
        #     poi["fw_core"]["last_update"] = {"timestamp": last_update}
        current_app.logger.debug('[POIClient.__build_poi] Building POI %s' % str(poi))
        return poi


poi_client = POIClient()


def fiware_send_video_poi(video):
    if not current_app.config.get('FIWARE_INSTALLED'):
        return
    if video.lat and video.lon:
        data = {'name': video.id, 'description': video.title,
                'location': {'lat': video.lat, 'lon': video.lon}}
        poi_response = poi_client.create(data, POI_VIDEO_CATEGORY)
        if poi_response.status_code == 200:
            current_app.logger.debug('creating local poi association')
            json_poi = poi_response.json()
            new_poi = fiware_poi_service.create(poi_uuid=json_poi['created_poi']['uuid'],
                                      timestamp=json_poi['created_poi']['timestamp'],
                                      category=fiware_models.POI_CATEGORY_VIDEO)
            new_poi.videos.append(video)
            db.session.commit()
            current_app.logger.debug('Created poi: %s' % new_poi)
        return poi_response
