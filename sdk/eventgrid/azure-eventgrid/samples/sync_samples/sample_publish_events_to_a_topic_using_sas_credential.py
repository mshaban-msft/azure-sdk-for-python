# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
FILE: sample_publish_events_to_a_topic_using_sas_credential.py
DESCRIPTION:
    These samples demonstrate sending an EventGrid Event using a shared access signature for authentication.
USAGE:
    python sample_publish_events_to_a_topic_using_sas_credential.py
    Set the environment variables with your own values before running the sample:
    1) EVENTGRID_SAS - The access key of your eventgrid account.
    2) EG_TOPIC_HOSTNAME - The topic hostname. Typically it exists in the format
    "<YOUR-TOPIC-NAME>.<REGION-NAME>.eventgrid.azure.net".
"""
import os
from azure.eventgrid import EventGridPublisherClient, EventGridEvent, generate_sas
from azure.core.credentials import AzureKeyCredential, AzureSasCredential

sas = os.environ["EVENTGRID_SAS"]
endpoint = os.environ["EG_TOPIC_HOSTNAME"]

credential = AzureSasCredential(sas)
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
