#!/usr/bin/env python

# Copyright (C) 2016 SignalFx, Inc. All rights reserved.
#README:  This script sends 1 datapoint into SignalFx ingest API.  In metrics finder, you can search for 'pytest.datapoint1'.
# Following requirements:
# 1. Organization Access Token  
# 2. Ingest Endpoint is set to use the correct Realm (us1, us0, etc.) if other than us1, update ingest_endpoint URL.
# USAGE: python send_a_datapoint.py <ACCESS_TOKEN>

import argparse
import os
import logging
import sys
import time
import signalfx

#Variables
timestamp=time.time()*1000

#Parse access token 
parser = argparse.ArgumentParser(
    description='SignalFx metrics reporting demo')
parser.add_argument('token', help='Your SignalFx API access token')
options = parser.parse_args()
#debugging - comment out to silence
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#Create SignalFx object
client = signalfx.SignalFx(ingest_endpoint='https://ingest.us1.signalfx.com')
ingest = client.ingest(options.token)

#send datapoint

ingest.send(
    gauges=[{
    'metric': 'pytest.datapoint1',
    'value': 777,
    'timestamp':timestamp,
    'dimensions': {'host': 'server1', 'environment': 'development','team': 'L1' }}])

# When you no longer need the client instance, make sure you call .stop() on it to ensure the queue is fully drained.
ingest.stop()

