"""
Class with DFI getters, srappers of the DFI python API.
Composition of the class DFIConnection.
"""

import json
from datetime import datetime
from typing import List

import pandas as pd
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from tqdm import tqdm

from dfi import stream
from dfi.connection import DFIConnect
from dfi.logging import setup_logger

logger = setup_logger(__file__)


class DFIGet:
    """
    Getter methods composed with the DFI connection.
    This is a simple wrap of the current DFI api, one method per endpoint.
    """

    def __init__(self, dfi_conn):
        self.dfi_conn: DFIConnect = dfi_conn

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dfi_conn!r}) {self.__dict__}"

    def __str__(self):
        return f"DFI Python API: instance of {self.__class__.__name__} composed with {self.dfi_conn!r}."

    @staticmethod
    def _check_response(response: requests.Response, url: str, headers: dict, params: dict, my_payload: dict = None):
        """Log the response of a request with the given parameters. Raise an error if status code is not 20x."""
        # prevent from showing the user token to terminal and logs
        headers = headers.copy()
        headers["X-API-TOKEN"] = "Bearer XXX"

        msg = f"""Response status code {response.status_code}.
Query URL: {url},
HEADER: {json.dumps(headers, sort_keys=True, indent=4)},
PARAMS: {json.dumps(params, sort_keys=True, indent=4)}
"""
        if my_payload is not None:
            msg += f"PAYLOAD: {json.dumps(my_payload, sort_keys=True, indent=4)}"

        if int(response.status_code / 10) != 20:
            logger.error(msg)
            raise RequestsConnectionError(msg)
        else:
            logger.debug(msg)

    def count(self, start_time: datetime = None, end_time: datetime = None) -> int:
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/count"
        my_headers = self.dfi_conn.streaming_headers
        response = requests.get(
            url=my_url,
            headers=my_headers,
            stream=True,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, my_headers, my_params)
        return stream.receive_count(response, self.dfi_conn.progress_bar)

    def entities(self, start_time: datetime = None, end_time: datetime = None):
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/entities"
        my_headers = self.dfi_conn.streaming_headers
        response = requests.get(
            my_url,
            headers=my_headers,
            stream=True,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, my_headers, my_params)
        return stream.receive_entities(response, self.dfi_conn.progress_bar)

    def entity_count(self, uid: str, start_time: datetime = None, end_time: datetime = None) -> int:
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/entities/{uid}/count"
        my_headers = self.dfi_conn.streaming_headers
        response = requests.get(
            my_url,
            headers=my_headers,
            stream=True,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, my_headers, my_params)
        return stream.receive_count(response, self.dfi_conn.progress_bar)

    def polygon_count(
        self,
        polygon: str = None,
        vertices: List[List[float]] = None,
        include_list: List[any] = None,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> int:
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        my_payload = {}
        if start_time is not None:
            my_payload["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_payload["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if include_list is not None:
            my_payload["include"] = include_list
        if polygon is not None and vertices is not None:
            logger.warning("You cannot specify both Polygon and Vertices. Pick one")
            return
        if polygon is not None:
            my_payload["name"] = polygon
        if vertices is not None:
            my_payload["vertices"] = vertices
        my_url = f"{self.dfi_conn.base_url}/polygon/count"
        my_headers = self.dfi_conn.streaming_headers
        response = requests.post(
            my_url,
            headers=my_headers,
            stream=True,
            json=my_payload,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, my_headers, my_params)
        return stream.receive_count(response, self.dfi_conn.progress_bar)

    def polygon_entities(
        self,
        polygon: str = None,
        vertices: List[List[float]] = None,
        include_list: List[any] = None,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> int:
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        my_payload = {}
        if start_time is not None:
            my_payload["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_payload["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if include_list is not None:
            my_payload["include"] = include_list
        if polygon is not None and vertices is not None:
            logger.warning("You cannot specify both Polygon and Vertices. Pick one")
            return
        if polygon is not None:
            my_payload["name"] = polygon
        if vertices is not None:
            my_payload["vertices"] = vertices
        my_url = f"{self.dfi_conn.base_url}/polygon/entities"
        my_headers = self.dfi_conn.streaming_headers
        response = requests.post(
            my_url,
            headers=my_headers,
            stream=True,
            json=my_payload,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, my_headers, my_params, my_payload)
        return stream.receive_entities(response, self.dfi_conn.progress_bar)

    def polygon_history(
        self,
        polygon: str = None,
        vertices: List[List[float]] = None,
        include_list: List[any] = None,
        start_time: datetime = None,
        end_time: datetime = None,
        parse_payload_as_json=False,
    ) -> int:
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        my_payload = {}
        if start_time is not None:
            my_payload["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_payload["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if include_list is not None:
            my_payload["include"] = include_list
        if polygon is not None and vertices is not None:
            logger.warning("You cannot specify both Polygon and Vertices. Pick one")
            return
        if polygon is not None:
            my_payload["name"] = polygon
        if vertices is not None:
            my_payload["vertices"] = vertices
        my_url = f"{self.dfi_conn.base_url}/polygon/history"
        response = requests.post(
            my_url,
            headers=self.dfi_conn.streaming_headers,
            stream=True,
            json=my_payload,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, self.dfi_conn.streaming_headers, my_params, my_payload)
        data = stream.receive_history(response, self.dfi_conn.progress_bar)
        data_formatted = []
        for item in data:
            if parse_payload_as_json:
                try:
                    payload = json.loads(item["payload"])
                except Exception as e:
                    payload = {}
                    logger.debug(f"Failed to parse payload to JSON: {e}")
            else:
                payload = item["payload"]
            data_formatted.append(
                [
                    item["id"],
                    datetime.strptime(item["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    item["coordinate"][0],
                    item["coordinate"][1],
                    payload,
                ]
            )
        df_uid = pd.DataFrame(data_formatted, columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])
        if start_time is not None and end_time is not None:
            return df_uid[(df_uid["timestamp"] >= start_time) & (df_uid["timestamp"] <= end_time)]
        return df_uid

    def history(
        self, uid: str, start_time: datetime = None, end_time: datetime = None, parse_payload_as_json=False
    ) -> pd.DataFrame:
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/entities/{uid}/history"
        my_headers = self.dfi_conn.streaming_headers
        response = requests.get(
            my_url,
            headers=my_headers,
            stream=True,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, my_headers, my_params)
        data = stream.receive_history(response, self.dfi_conn.progress_bar)
        logger.debug("Uid: %s \nHistory length: %i", uid, len(data))
        data_formatted = []
        for item in data:
            if parse_payload_as_json:
                try:
                    payload = json.loads(item["payload"])
                except Exception as e:
                    payload = {}
                    logger.debug(f"Failed to parse payload to JSON: {e}")
            else:
                payload = item["payload"]
            data_formatted.append(
                [
                    item["id"],
                    datetime.strptime(item["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    item["coordinate"][0],
                    item["coordinate"][1],
                    payload,
                ]
            )
        return pd.DataFrame(data_formatted, columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])

    def histories(
        self, uids: List[str], start_time: datetime = None, end_time: datetime = None, parse_payload_as_json=False
    ) -> pd.DataFrame:
        df_records = pd.DataFrame(columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])
        progress_bar_status = self.dfi_conn.progress_bar
        self.dfi_conn.progress_bar = False
        for uid in tqdm(uids, total=len(uids)):
            df_history = self.history(uid, start_time, end_time, parse_payload_as_json)
            df_records = pd.concat([df_records, df_history], ignore_index=True, axis=0)
        self.dfi_conn.progress_bar = progress_bar_status
        return df_records

    def neighbours(
        self,
        hex_id: str,
        polygon_vertices: List[List[float]],
        min_time,
        max_time,
    ) -> List[any]:
        my_url = f"{self.dfi_conn.base_url}/polygon/history"
        my_payload = {
            "vertices": polygon_vertices,
            "startTime": min_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "endTime": max_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        my_headers = self.dfi_conn.streaming_headers
        my_params = {"instance": f"{self.dfi_conn.namespace}.{self.dfi_conn.instance_name}"}
        response = requests.post(
            my_url,
            json=my_payload,
            headers=my_headers,
            stream=True,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, my_url, my_headers, my_params, my_payload)
        data = stream.receive_history(response, self.dfi_conn.progress_bar)
        if data is None:
            logger.warning("Error in query. Vertices: %s", str(polygon_vertices))
            data = []
        data = [
            {
                "hex_id": hex_id,
                "entity_id": x["id"],
                "timestamp": datetime.strptime(x["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                "longitude": x["coordinate"][0],
                "latitude": x["coordinate"][1],
            }
            for x in data
        ]
        return data
