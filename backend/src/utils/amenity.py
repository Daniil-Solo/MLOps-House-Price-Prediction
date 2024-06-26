"""Module for working with amenities."""

import json
import os
from math import asin, cos, pi, sin, sqrt
from typing import Dict, List

DISTANCES = [500, 1500, 3000]


def calculate_distances(lat: float, lon: float, amenities: List[Dict[str, float | str]]) -> Dict[str, int]:
    """Calculate distances from point to all amenities.

    :param lat: latitude
    :param lon: longitude
    :param amenities:
    :return: dict with distances
    """
    distance_data: Dict[str, int] = dict()
    for amenity_item in amenities:
        calculated_distance = get_distance(lon, lat, float(amenity_item["lon"]), float(amenity_item["lat"]))
        for distance in DISTANCES:
            key: str = str(amenity_item["type"]) + "_" + str(distance)
            distance_data[key] = distance_data.get(key, 0)
            if calculated_distance < distance:
                distance_data[key] += 1
    return distance_data


def get_distance(llong1: float, llat1: float, llong2: float, llat2: float) -> float:
    """Calculate distance.

    :param llong1: longitude
    :param llat1: latitude
    :param llong2: longitude
    :param llat2: latitude
    :return: distance in meters
    """
    rad = 6372795
    lat1 = llat1 * pi / 180.0
    lat2 = llat2 * pi / 180.0
    long1 = llong1 * pi / 180.0
    long2 = llong2 * pi / 180.0
    delta_long = long2 - long1
    delta_lat = lat2 - lat1
    ad = 2 * asin(sqrt(sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2))
    dist = ad * rad
    return dist


def load_amenities_data(dir_path: str) -> List[Dict[str, float]]:
    """Load amenities.

    :param dir_path: dir with files
    :return: dict with amenities
    """
    amenities = []
    for root, _, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            name, _ = os.path.splitext(filename)
            with open(filepath, "r", encoding="utf-8") as f:
                amenity_data = json.load(f)
            for item in amenity_data:
                amenity_item = dict(lon=item["lon"], lat=item["lat"], type=name)
                amenities.append(amenity_item)
    return amenities
