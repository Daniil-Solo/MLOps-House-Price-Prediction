"""Script for building data from different sources."""

import json
import os
from math import asin, cos, pi, sin, sqrt

import click
import pandas as pd

# column names
LAT_FEATURE = "lat"
LON_FEATURE = "lon"
ADDRESS_FEATURE = "physical address"
DISTANCES = [500, 1500, 3000]


def get_distance(llong1: float, llat1: float, llong2: float, llat2: float) -> float:
    """Calculate distance between two points.

    :param llong1: lon of first point
    :param llat1: lat of first point
    :param llong2: lon of second point
    :param llat2: lat of second point
    :return: distance
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


def load_amenity_data(amenity_files: list[str]) -> dict[str, list[dict[str, float]]]:
    """Load amenity data from files.

    :param amenity_files: list of filepath
    :return: dict with amenity as key and list coordinates as value
    """
    amenity_data = dict()
    for amenity_filepath in amenity_files:
        file_name = os.path.basename(amenity_filepath)
        name, _ = os.path.splitext(file_name)
        with open(amenity_filepath, encoding="utf-8") as f:
            data = json.load(f)
        data_coordinates = []
        for item in data:
            data_coordinates.append(dict(lat=item["lat"], lon=item["lon"]))
        amenity_data[name] = data_coordinates
    return amenity_data


@click.command()
@click.argument("input_feature_file", type=click.Path(readable=True))
@click.argument("coordinates_file", type=click.Path(readable=True))
@click.argument("output_feature_file", type=click.Path(writable=True))
@click.option("--amenity-files", "-af", type=click.STRING, help="Files with amenity info", multiple=True, default=[])
def cli(input_feature_file: str, coordinates_file: str, output_feature_file: str, amenity_files: list[str]) -> None:
    """Build dataset.

    :param input_feature_file: input filepath
    :param coordinates_file: file
    :param output_feature_file: output filepath
    :param amenity_files: amenity filepaths
    :return: nothing
    """
    # open data
    df = pd.read_csv(input_feature_file)
    coordinates_df = pd.read_csv(coordinates_file)
    amenity_data = load_amenity_data(amenity_files)
    # drop rows without coordinates
    coordinates_df.dropna(subset=[LAT_FEATURE, LON_FEATURE], inplace=True)
    coordinates_df.reset_index(drop=True, inplace=True)
    # add amenity data to coordinate data
    for amenity in amenity_data:
        for distance in DISTANCES:
            key = amenity + "_" + str(distance)
            coordinates_df[key] = 0
    for index in range(len(coordinates_df)):
        if index % 100 == 0:
            click.echo(f"{round(index / len(coordinates_df) * 100, 2)}%")
        for amenity in amenity_data:
            for item in amenity_data[amenity]:
                lon1, lat1 = coordinates_df.iloc[index][LON_FEATURE], coordinates_df.iloc[index][LAT_FEATURE]
                lon2, lat2 = item["lon"], item["lat"]
                calculated_distance = get_distance(lon1, lat1, lon2, lat2)
                for distance in DISTANCES:
                    if calculated_distance < distance:
                        key = amenity + "_" + str(distance)
                        coordinates_df.at[index, key] = coordinates_df.loc[index][key] + 1
    # merge data
    merged_df = pd.merge(df, coordinates_df, on=[ADDRESS_FEATURE])
    merged_df.drop(columns=[ADDRESS_FEATURE], inplace=True)
    # save
    merged_df.to_csv(output_feature_file, index=False)


if __name__ == "__main__":
    cli()
