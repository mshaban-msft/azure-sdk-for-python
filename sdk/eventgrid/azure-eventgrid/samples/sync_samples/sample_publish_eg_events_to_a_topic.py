# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
FILE: sample_publish_eg_events_to_a_topic.py
DESCRIPTION:
    These samples demonstrate sending an EventGrid Event directly to a topic.
USAGE:
    python sample_publish_eg_events_to_a_topic.py
    Set the environment variables with your own values before running the sample:
    1) EG_ACCESS_KEY - The access key of your eventgrid account.
    2) EG_TOPIC_HOSTNAME - The topic hostname. Typically it exists in the format
    "<YOUR-TOPIC-NAME>.<REGION-NAME>.eventgrid.azure.net".
"""
# [START publish_eg_event_to_topic]
import os
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential

topic_key = os.environ["EG_ACCESS_KEY"]
endpoint = os.environ["EG_TOPIC_HOSTNAME"]

credential = AzureKeyCredential(topic_key)
client = EventGridPublisherClient(endpoint, credential)

client.send([
	EventGridEvent(
		event_type="Contoso.Items.ItemReceived",
		data={
			"itemSku": "Contoso Item SKU #1"
		},
		subject="Door1",
		data_version="2.0"
	)
])
# [END publish_eg_event_to_topic]
