#!/usr/bin/env python

# Copyright 2019 Bruno P. Kinoshita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
from time import sleep

import click
import urllib3
import vcr

from .queries import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def false_matcher(r1, r2):
    """We never match a URL. Every request is a new request. This
    way we can record the GraphQL state changes."""
    return False


my_vcr = vcr.VCR(
    serializer="yaml",
    record_mode="all",
    match_on=["false_matcher"]
)
my_vcr.register_matcher('false_matcher', false_matcher)
logger.info(my_vcr.record_mode)
http = urllib3.PoolManager()


def record_suite_state(url: str, workflow: str):
    """Record a Cylc suite state.

    Args:
        url (str): GraphQL URL
        workflow (str): workflow name
    """
    params = {
        "operationName": None,
        "variables": None,
        "query": QUERY_SUITE_STATE
    }

    encoded_data = json.dumps(params).encode('utf-8')

    cassette = f'cassettes/{workflow}/suite.yaml'
    logger.info(f"Recording suite cassette {cassette}...")
    with my_vcr.use_cassette(cassette) as cass:
        response = http.request(
            'POST',
            url,
            body=encoded_data,
            headers={'Content-Type': 'application/json'}
        ).data
        assert response is not None
        # cass should have at least 1 request inside it
        assert len(cass) >= 1


def record_suite_tasks_state(url: str, workflow: str, seconds: float):
    """Periodically record a Cylc suite tasks state.

    Args:
        url (str): GraphQL URL
        workflow (str): workflow name
        seconds (float): period
    """
    params = {
        "operationName": None,
        "variables": None,
        "query": QUERY_SUITE_TASKS_STATE
    }

    encoded_data = json.dumps(params).encode('utf-8')

    idx = 0  # used for the cassette file name
    while True:
        persisted_file = f'cassettes/{workflow}/tasks-{idx}.yaml'
        logger.info(f"Recording suite tasks cassette {persisted_file}...")
        with my_vcr.use_cassette(persisted_file) as cassette:
            response = http.request(
                'POST',
                url,
                body=encoded_data,
                headers={'Content-Type': 'application/json'}
            ).data
            assert response is not None
            # cass should have at least 1 request inside it
            assert len(cassette) >= 1
        idx += 1
        sleep(seconds)


@click.command()
@click.option('--url', required=True, help='GraphQL endpoint URL.')
@click.option('--interval', required=True, type=float, help='Interval to wait before querying tasks states.')
@click.option('--workflow', required=True, help='Workflow name.')
def main(url: str, interval: float, workflow: str):
    logger.info(f"Recording cassettes for workflow '{workflow}'', using URL '{url}'' and interval '{interval}'")

    record_suite_state(url, workflow)
    record_suite_tasks_state(url, workflow, interval)

    logger.info("Done")
