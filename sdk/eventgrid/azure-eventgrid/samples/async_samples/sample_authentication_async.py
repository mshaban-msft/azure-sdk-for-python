# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
FILE: sample_authentication_async.py
DESCRIPTION:
    These samples demonstrate authenticating an EventGridPublisherClient.
USAGE:
    python sample_authentication_async.py
    Set the environment variables with your own values before running the sample:
    1) EG_ACCESS_KEY - The access key of your eventgrid account.
    2) EG_TOPIC_HOSTNAME - The topic hostname. Typically it exists in the format
    "<YOUR-TOPIC-NAME>.<REGION-NAME>.eventgrid.azure.net".
    3) EVENTGRID_SAS - The shared access signature that is to be used to authenticate the client.
"""
# [START client_auth_with_key_cred_async]
import os
from azure.eventgrid.aio import EventGridPublisherClient
from azure.core.credentials import AzureKeyCredential

topic_key = os.environ["EG_ACCESS_KEY"]
endpoint = os.environ["EG_TOPIC_HOSTNAME"]

credential = AzureKeyCredential(topic_key)
client = EventGridPublisherClient(endpoint, credential)
# [END client_auth_with_key_cred_async]

# [START client_auth_with_sas_cred_async]
import os
from azure.eventgrid.aio import EventGridPublisherClient
from azure.core.credentials import AzureSasCredential

signature = os.environ["EVENTGRID_SAS"]
endpoint = os.environ["EG_TOPIC_HOSTNAME"]

credential = AzureSasCredential(signature)
client = EventGridPublisherClient(endpoint, credential)
# [END client_auth_with_sas_cred_async]
