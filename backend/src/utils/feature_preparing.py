"""Module for preparing features."""

from typing import Dict

import pandas as pd

from src.schemas.predict import BasePredictionIn

COLUMNS = [
    "number of floors",
    "type of house",
    "number of rooms",
    "area of apartment",
    "apartment floor",
    "repair",
    "terrace",
    "extra",
    "elevator",
    "district",
    "bathroom",
    "lat",
    "lon",
    "eat_500",
    "eat_1500",
    "eat_3000",
    "culture_500",
    "culture_1500",
    "culture_3000",
    "edu_500",
    "edu_1500",
    "edu_3000",
    "health_500",
    "health_1500",
    "health_3000",
]


def make_features_dataframe(
    apartment_data: BasePredictionIn, lat: float, lon: float, district: str, distance_data: Dict[str, int]
) -> pd.DataFrame:
    """Compose features.

    :param apartment_data: user data
    :param lat: latitude
    :param lon: longitude
    :param district: name of district
    :param distance_data: dict with distances
    :return: feature dataframe
    """
    prediction_data = {
        "lat": lat,
        "lon": lon,
        "district": district,
        "number of floors": apartment_data.number_of_rooms,
        "type of house": apartment_data.type_of_house.value,
        "number of rooms": apartment_data.number_of_rooms,
        "area of apartment": apartment_data.area_of_apartment,
        "apartment floor": apartment_data.apartment_floor,
        "repair": apartment_data.repair.value,
        "terrace": apartment_data.terrace.value,
        "extra": apartment_data.extra,
        "elevator": apartment_data.elevator,
        "bathroom": apartment_data.bathroom.value,
    }
    prediction_data = dict(**prediction_data, **distance_data)
    df = pd.DataFrame(data=[prediction_data], columns=COLUMNS)
    return df
