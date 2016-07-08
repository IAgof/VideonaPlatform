# -*- coding: utf-8 -*-
"""
    tests.fiware.fiware_poi_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fiware POI tests package
"""
import pytest
from hamcrest import *
import mock

from videona_platform.fiware.models import FiwarePoi
from videona_platform.fiware.poi import fiware_send_video_poi
from tests.factories import VideoFactory


class TestPOIIntegration(object):
    @mock.patch('requests.post')
    def test_fiware_send_video_poi_creates_fiware_poi(self, post, session, push_context_fiware):
        video = VideoFactory()
        session.add(video)
        session.commit()
        mocked_response = mock.Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = {u'created_poi': {u'timestamp': 1467817834, u'uuid': u'4da507a7-5de3-40ed-ab03-b921441de446'}}
        post.return_value = mocked_response

        fiware_send_video_poi(video)

        pois = FiwarePoi.query.all()
        assert_that(len(pois), is_(1))
        assert_that(pois[0].poi_uuid, is_('4da507a7-5de3-40ed-ab03-b921441de446'))
        assert_that(pois[0].timestamp, is_(1467817834))
        assert_that(len(pois[0].videos), is_(1))
        assert_that(pois[0].videos[0], is_(video))
