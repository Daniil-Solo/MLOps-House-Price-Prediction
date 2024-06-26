"""Module for working with districts."""

import json
from typing import Any, Dict

from shapely.geometry import Point, Polygon


class NoDistrictException(Exception):
    """Exception if no districts."""

    pass


class GeoJSONException(Exception):
    """Exception if geojson contains invalid fields."""

    pass


def get_district_name(lat: float, lon: float, district_geojson_data: Dict[str, Any]) -> str:
    """Get districts name.

    :param lat: latitude
    :param lon: longitude
    :param district_geojson_data: dict with info about districts
    :return:
    """
    point = Point([lon, lat])
    try:
        for feature in district_geojson_data["features"]:
            district_name: str = feature["properties"]["name"]
            geometry_type = feature["geometry"]["type"]
            coordinate_group = feature["geometry"]["coordinates"]
            for coordinates in coordinate_group:
                poly = Polygon(coordinates) if geometry_type == "Polygon" else Polygon(coordinates[0])  # MultiPolygon
                if point.within(poly):
                    return district_name
    except Exception:
        raise GeoJSONException() from Exception
    raise NoDistrictException()


def load_districts_data(filepath: str) -> Dict[str, Any]:
    """Load districts data.

    :param filepath: to districts geojson
    :return: dict with info about districts
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)
    return data
