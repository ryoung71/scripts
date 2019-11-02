#!/usr/bin/env python

# Copyright (C) 2016 SignalFx, Inc. All rights reserved.
# This script is a mod of orginal script found here https://github.com/signalfx/signalfx-python/blob/master/examples/generic_usecase.py
# Will continuously send 2 metrics (pytest.latency and pytest.errcount) to SignalFx API, until aborted by user
# In metrics finder, search for pytest.latency and pytest.errcount to interact with the metrics
# Following requirements:
# 1. Organization Access Token  
# 2. Ingest Endpoint is set to use the correct Realm (us1, us0, etc.) if other than us1, update ingest_endpoint URL.
# USAGE: python send_datapoints.py <ACCESS_TOKEN>



import argparse
import os
import logging
import sys
import time

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..'))
import signalfx  # noqa


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='SignalFx metrics reporting demo')
    parser.add_argument('token', help='Your SignalFx API access token')
    options = parser.parse_args()
    client = signalfx.SignalFx(ingest_endpoint='https://ingest.us1.signalfx.com')
    ingest = client.ingest(options.token)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    try:
        i = 0
        while True:
            ingest.send(
              gauges=[{
                'metric': 'pytest.latency',
                'value': i % 10,
                'dimensions': {'host': 'myhost', 'environment': 'preprod','team': 'L1' }}],
              counters=[{
                'metric': 'pytest.errcount',
                'value': i % 2,
                'dimensions': {'host': 'myhost', 'environment': 'proprod','team': 'L1' }}])
            i += 1
            if i % 10 == 0:  # Factoring for reduced activity for events
                version = '{date}-{version}'.format(
                    date=time.strftime('%Y-%m-%d'), version=i)
                ingest.send_event(event_type='deployments',
                                  category='USER_DEFINED',
                                  dimensions={
                                      'host': 'myhost',
                                      'environment': 'preprod',
                                      'team': 'L1'},
                                  properties={'version': version},
                                  timestamp=time.time() * 1000)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass