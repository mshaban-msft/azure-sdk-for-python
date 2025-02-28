#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import logging
import sys
import os
import json
import pytest
import uuid
from datetime import datetime, timedelta
from msrest.serialization import UTC
import datetime as dt

from devtools_testutils import AzureMgmtTestCase, CachedResourceGroupPreparer

from azure_devtools.scenario_tests import ReplayableTest
from azure.core.credentials import AzureKeyCredential, AzureSasCredential
from azure.core.messaging import CloudEvent
from azure.core.serialization import NULL
from azure.eventgrid import EventGridPublisherClient, EventGridEvent, generate_sas
from azure.eventgrid._helpers import _cloud_event_to_generated

from eventgrid_preparer import (
    CachedEventGridTopicPreparer
)

class EventGridPublisherClientTests(AzureMgmtTestCase):
    FILTER_HEADERS = ReplayableTest.FILTER_HEADERS + ['aeg-sas-key']

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_event_grid_event_data_dict(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        eg_event = EventGridEvent(
                subject="sample", 
                data={"sample": "eventgridevent"}, 
                event_type="Sample.EventGrid.Event",
                data_version="2.0"
                )
        client.send(eg_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_event_grid_event_data_as_list(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        eg_event1 = EventGridEvent(
                subject="sample", 
                data=u"eventgridevent",
                event_type="Sample.EventGrid.Event",
                data_version="2.0"
                )
        eg_event2 = EventGridEvent(
                subject="sample2", 
                data=u"eventgridevent2",
                event_type="Sample.EventGrid.Event",
                data_version="2.0"
                )
        client.send([eg_event1, eg_event2])

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_event_grid_event_data_str(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        eg_event = EventGridEvent(
                subject="sample", 
                data=u"eventgridevent",
                event_type="Sample.EventGrid.Event",
                data_version="2.0"
                )
        client.send(eg_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_event_grid_event_data_bytes(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        eg_event = EventGridEvent(
                subject="sample", 
                data=b"eventgridevent", 
                event_type="Sample.EventGrid.Event",
                data_version="2.0"
                )
        with pytest.raises(TypeError, match="Data in EventGridEvent cannot be bytes*"):
            client.send(eg_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_event_grid_event_dict_data_bytes(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        eg_event = {
                "subject":"sample", 
                "data":b"eventgridevent", 
                "eventType":"Sample.EventGrid.Event",
                "dataVersion":"2.0",
                "id": uuid.uuid4(),
                "eventTime": datetime.now()
        }
        with pytest.raises(TypeError, match="Data in EventGridEvent cannot be bytes*"):
            client.send(eg_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_event_grid_event_dict_data_dict(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        eg_event = {
                "subject":"sample", 
                "data":{"key1": "Sample.EventGrid.Event"}, 
                "eventType":"Sample.EventGrid.Event",
                "dataVersion":"2.0",
                "id": uuid.uuid4(),
                "eventTime": datetime.now()
        }
        client.send(eg_event)


    ### CLOUD EVENT TESTS

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_dict(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = {"sample": "cloudevent"},
                type="Sample.Cloud.Event"
                )
        client.send(cloud_event)

    @pytest.mark.skip("https://github.com/Azure/azure-sdk-for-python/issues/16993")
    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_NULL(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = NULL,
                type="Sample.Cloud.Event"
                )
        
        def callback(request):
            req = json.loads(request.http_request.body)
            assert req[0].get("data") is None

        client.send(cloud_event, raw_request_hook=callback)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_base64_using_data(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = b'cloudevent',
                type="Sample.Cloud.Event"
                )

        def callback(request):
            req = json.loads(request.http_request.body)
            assert req[0].get("data_base64") is not None
            assert req[0].get("data") is None

        client.send(cloud_event, raw_response_hook=callback)

    def test_send_cloud_event_fails_on_providing_data_and_b64(self):
        with pytest.raises(ValueError, match="Unexpected keyword arguments data_base64.*"):
            cloud_event = CloudEvent(
                    source = "http://samplesource.dev",
                    data_base64 = b'cloudevent',
                    data = "random data",
                    type="Sample.Cloud.Event"
                    )

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_none(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = None,
                type="Sample.Cloud.Event"
                )
        client.send(cloud_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_str(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = "cloudevent",
                type="Sample.Cloud.Event"
                )
        client.send(cloud_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_bytes(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = b"cloudevent",
                type="Sample.Cloud.Event"
                )
        client.send(cloud_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_as_list(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = "cloudevent",
                type="Sample.Cloud.Event"
                )
        client.send([cloud_event])

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_data_with_extensions(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event = CloudEvent(
                source = "http://samplesource.dev",
                data = "cloudevent",
                type="Sample.Cloud.Event",
                extensions={
                    'reasoncode':204,
                    'extension':'hello'
                    }
                )
        client.send([cloud_event])
        internal = _cloud_event_to_generated(cloud_event).serialize()
        assert 'reasoncode' in internal
        assert 'extension' in internal
        assert internal['reasoncode'] == 204

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='cloudeventgridtest')
    def test_send_cloud_event_dict(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        cloud_event1 = {
                "id": "1234",
                "source": "http://samplesource.dev",
                "specversion": "1.0",
                "data": "cloudevent",
                "type": "Sample.Cloud.Event"
        }
        client.send(cloud_event1)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_signature_credential(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        expiration_date_utc = dt.datetime.now(UTC()) + timedelta(hours=1)
        signature = generate_sas(eventgrid_topic_endpoint, eventgrid_topic_primary_key, expiration_date_utc)
        credential = AzureSasCredential(signature)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, credential)
        eg_event = EventGridEvent(
                subject="sample", 
                data={"sample": "eventgridevent"}, 
                event_type="Sample.EventGrid.Event",
                data_version="2.0"
                )
        client.send(eg_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='eventgridtest')
    def test_send_NONE_credential(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        with pytest.raises(ValueError, match="Parameter 'self._credential' must not be None."):
            client = EventGridPublisherClient(eventgrid_topic_endpoint, None)
        
    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='customeventgridtest')
    def test_send_custom_schema_event(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        custom_event = {
                    "customSubject": "sample",
                    "customEventType": "sample.event",
                    "customDataVersion": "2.0",
                    "customId": "1234",
                    "customEventTime": dt.datetime.now(UTC()).isoformat(),
                    "customData": "sample data"
                    }
        client.send(custom_event)

    @CachedResourceGroupPreparer(name_prefix='eventgridtest')
    @CachedEventGridTopicPreparer(name_prefix='customeventgridtest')
    def test_send_custom_schema_event_as_list(self, resource_group, eventgrid_topic, eventgrid_topic_primary_key, eventgrid_topic_endpoint):
        akc_credential = AzureKeyCredential(eventgrid_topic_primary_key)
        client = EventGridPublisherClient(eventgrid_topic_endpoint, akc_credential)
        custom_event1 = {
                    "customSubject": "sample",
                    "customEventType": "sample.event",
                    "customDataVersion": "2.0",
                    "customId": "1234",
                    "customEventTime": dt.datetime.now(UTC()).isoformat(),
                    "customData": "sample data"
                    }
        custom_event2 = {
                    "customSubject": "sample2",
                    "customEventType": "sample.event",
                    "customDataVersion": "2.0",
                    "customId": "12345",
                    "customEventTime": dt.datetime.now(UTC()).isoformat(),
                    "customData": "sample data 2"
                    }
        client.send([custom_event1, custom_event2])

    def test_send_throws_with_bad_credential(self):
        bad_credential = "I am a bad credential"
        with pytest.raises(ValueError, match="The provided credential should be an instance of AzureSasCredential or AzureKeyCredential"):
            client = EventGridPublisherClient("eventgrid_endpoint", bad_credential)
