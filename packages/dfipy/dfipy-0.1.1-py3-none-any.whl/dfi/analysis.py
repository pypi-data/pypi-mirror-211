"""
Class with DFI analytic methods, leveraging on the python api wrappers to gain analytical informations.
Composition of the class DFIConnection.
"""

from datetime import datetime, timedelta
from functools import partial
from typing import List

import branca  # pylint: disable=import-error
import geopandas as gpd
import h3.api.numpy_int as h3
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from shapely.wkt import loads
from tqdm import tqdm

from dfi.connection import DFIConnect
from dfi.getters import DFIGet
from dfi.logging import setup_logger

logger = setup_logger(__file__)


class DFIAnalyse:
    """
    Analytical methods to build use case on top of the queries from DFI.
    Not part of the DFI API wrapper, but handy to have it embedded there for demo and functionalities.
    """

    def __init__(self, dfi_conn):
        self.dfi_conn: DFIConnect = dfi_conn
        self.dfi_get: DFIGet = DFIGet(self.dfi_conn)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dfi_conn!r})({self.dfi_get!r}) {self.__dict__}"

    def __str__(self):
        return f"""DFI Python API: instance of {self.__class__.__name__}
                   composed with {self.dfi_conn!r} and instantiating {self.dfi_get!r}"""

    @staticmethod
    def summarise_by_day(df_history: pd.DataFrame) -> pd.DataFrame:
        df_summary = df_history.copy()
        df_summary["time"] = df_summary["timestamp"].dt.time  # extract time only
        df_summary.set_index("timestamp", inplace=True)
        # group by 'group' column and apply aggregation functions
        df_summary = df_summary.groupby(pd.Grouper(freq="D")).agg(
            min_value=("time", "min"), max_value=("time", "max"), count=("time", "count")
        )
        # reset index to get the group column as a regular column again
        df_summary = df_summary.reset_index()
        return df_summary

    def pings_in_hexagons(
        self,
        uid: str,
        resolution: int,
        period: int,
        start_time: datetime = None,
        end_time: datetime = None,
        vertices: List[List[float]] = None,
    ) -> pd.DataFrame:
        if vertices is None:
            df_history = self.dfi_get.history(uid, start_time=start_time, end_time=end_time)
        else:
            df_history = self.dfi_get.polygon_history(
                include_list=[uid], vertices=vertices, start_time=start_time, end_time=end_time
            )
        if len(df_history) == 0:
            logger.warning("No history fund for entity %s", uid)
            return None, None
        if period not in [1, 5, 10, 15, 30]:
            raise ValueError("Period must be one of 1, 5, 10, 15, 30]")
        if resolution < 1 or resolution > 15:
            raise ValueError("Resolution is incorrect")
        df_hexagons = df_history.copy()
        for row in range(len(df_hexagons)):
            hex_id = h3.geo_to_h3(
                df_hexagons.at[row, "latitude"],
                df_hexagons.at[row, "longitude"],
                resolution,
            )
            df_hexagons.at[row, "hex_id"] = hex(hex_id)[2:]
            df_hexagons.at[row, "hex_polygon"] = Polygon(h3.h3_to_geo_boundary(hex_id, geo_json=True))
            df_hexagons.at[row, "period_start"] = df_hexagons.at[row, "timestamp"].round(f"{period}min")
        df_hexagons["hex_polygon"] = df_hexagons["hex_polygon"].astype(str)
        df_hexagons["hex_id"] = df_hexagons["hex_id"].astype(str)
        df_hexagons = df_hexagons.drop_duplicates(subset=["hex_id", "period_start"])
        df_hexagons = df_hexagons.drop(["entity_id", "latitude", "longitude", "timestamp"], axis=1)
        df_hexagons = df_hexagons.assign(
            period_end=lambda df: df.period_start + timedelta(minutes=period),
        )
        df_hexagons = df_hexagons.sort_values(by="period_start", ascending=True)
        return df_history, df_hexagons

    def pings_in_hexagons_bbox(
        self,
        uid: str,
        resolution: int,
        period: int,
        min_lon: float,
        min_lat: float,
        max_lon: float,
        max_lat: float,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> pd.DataFrame:
        _, df_hexagons = self.pings_in_hexagons(uid, resolution, period, start_time=start_time, end_time=end_time)
        logger.warning("We found %i hexagons", len(df_hexagons))

        # Bounding box to Polygon
        bounding_box = Polygon(
            [
                (min_lon, min_lat),
                (max_lon, min_lat),
                (max_lon, max_lat),
                (min_lon, max_lat),
            ]
        )

        df_subset = pd.DataFrame(columns=["hex_id", "hex_polygon", "period_start", "period_end"])
        # Loop through the hexagons and check if they fit within the bounding box
        for _, row in tqdm(df_hexagons.iterrows(), total=len(df_hexagons)):
            # Convert the H3 hexagon to a Polygon object
            hexagon_polygon = loads(row["hex_polygon"])
            # Check if the Polygon object intersects with the bounding box
            if bounding_box.intersects(hexagon_polygon):
                new_row = {
                    "hex_id": row["hex_id"],
                    "hex_polygon": row["hex_polygon"],
                    "period_start": row["period_start"],
                    "period_end": row["period_end"],
                }
                df_subset = pd.concat([df_subset, pd.DataFrame([new_row])], ignore_index=True, axis=0)
        logger.warning("number of hexagons: %i", len(df_subset))
        min_time_range = df_subset.period_start.min()
        max_time_range = df_subset.period_start.max()
        logger.info("Min time range: %s", str(min_time_range))
        logger.info("Max time range: %s", str(max_time_range))
        return df_subset, min_time_range, max_time_range

    def colocated_records(self, uid: str, hexagons_df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Colocated records: querying hexagons ...")
        df_records = pd.DataFrame(columns=["hex_id", "longitude", "latitude", "entity_id", "timestamp"])
        for _, row in tqdm(hexagons_df.iterrows(), total=len(hexagons_df)):
            polygon_vertices = list(loads(row.hex_polygon).exterior.coords)  # pylint: disable=no-member
            data = self.dfi_get.neighbours(
                row.hex_id,
                polygon_vertices,
                min_time=row.period_start,
                max_time=row.period_end,
            )
            df_data = pd.DataFrame(data)
            if len(df_data) > 0:
                df_data = df_data[df_data["entity_id"] != uid]
            df_records = pd.concat([df_records, df_data], ignore_index=True, axis=0)
            # logger.info(f"    - HexId: {row.hex_id}, {row.period_start} found {len(df_data)} records")
        return df_records

    @staticmethod
    def from_bbox_to_polygon_list(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> List[List[float]]:
        return [[max_lon, max_lat], [max_lon, min_lat], [min_lon, min_lat], [min_lon, max_lat], [max_lon, max_lat]]

    @staticmethod
    def aggregate_h3_hexes(
        df_input: pd.DataFrame,
        resolution: int,
        colorscale_col: str = "num_pings",
        colorscale_log_transform: bool = True,
    ) -> gpd.GeoDataFrame:
        return (
            df_input.assign(
                hex_id=lambda df: [
                    h3.geo_to_h3(lat, lon, resolution=resolution) for lat, lon in zip(df["latitude"], df["longitude"])
                ]
            )
            .pipe(_aggregate_pings, "hex_id")
            .assign(
                hex_id=lambda df: df.hex_id.map(hex).str[2:],
                color=lambda df: _assign_colors(df[colorscale_col], colorscale_log_transform=colorscale_log_transform),
            )
        )


def _aggregate_pings(df_input: pd.DataFrame, hex_id: str) -> pd.DataFrame:
    return (
        df_input.groupby(hex_id)
        .agg(
            num_pings=("entity_id", "count"),
            num_devices=("entity_id", "nunique"),
            first_ping=("timestamp", "min"),
            last_ping=("timestamp", "max"),
        )
        .reset_index()
    )


def _assign_colors(df_input: pd.Series, colorscale_log_transform: bool) -> pd.Series:
    if not df_input.empty:
        if colorscale_log_transform:
            df_input = _transform_to_log(df_input)
        colormap = _create_colormap(df_input)
        return df_input.map(partial(_count_to_rgb_tuple, colormap=colormap))
    else:
        return df_input


def _transform_to_log(df_input: pd.Series) -> pd.Series:
    """normalise and transform a series to log scale"""
    return pd.Series(np.log(1 + df_input / 2))


def _create_colormap(df_input: pd.Series) -> branca.colormap.StepColormap:
    legend_steps = np.linspace(0, df_input.max(), 100)
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 100)  # pylint: disable=no-member
    return colormap.to_step(index=legend_steps)


def _count_to_rgb_tuple(count: int, colormap: branca.colormap.StepColormap) -> str:
    hex_color = colormap(count).lstrip("#")
    return tuple(int(hex_color[i : i + 2], base=16) for i in (0, 2, 4))
