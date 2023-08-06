"""
Auxiliary methods for streamed data.
"""

import json
from time import sleep
from typing import List

import requests
import sseclient  # pylint: disable=import-error
from tqdm import tqdm

from dfi.logging import setup_logger

logger = setup_logger(__file__)


def receive_entities(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    client = sseclient.SSEClient(response)
    results = []
    if progress_bar:
        previous = 0
        for event in (pbar := tqdm(client.events())):  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += [json.loads(event.data)]
                len_results = len(results)
                if len_results != previous and len_results % 50 == 0:
                    previous = len(results)
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)  # to avoid Google Colab being overwhelmed
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    else:
        for event in client.events():  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += [json.loads(event.data)]
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    return results


def receive_history(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    client = sseclient.SSEClient(response)
    results = []
    if progress_bar:
        previous = 0
        for event in (pbar := tqdm(client.events())):  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += json.loads(event.data)
                len_results = len(results)
                if len_results != previous and len_results % 50 == 0:
                    previous = len(results)
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    else:
        for event in client.events():  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += json.loads(event.data)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    return results


def receive_count(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    client = sseclient.SSEClient(response)
    results = []
    if progress_bar:
        previous = 0
        for event in (pbar := tqdm(client.events())):  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results = json.loads(event.data)
                if results != previous and results % 50 == 0:
                    previous = results
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    else:
        for event in client.events():  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results = json.loads(event.data)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    return results
