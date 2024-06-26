"""Script for adding geo data."""

import os
from typing import Optional

import click
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

GEOAPIFY_TOKEN = os.environ.get("GEOAPIFY_TOKEN", "")
GEOAPIFY_URL = "https://api.geoapify.com/v1/geocode/search"

# column names
ADDRESS_FEATURE = "physical address"
LATITUDE_FEATURE = "lat"
LATITUDE_INDEX = 1
LONGITUDE_FEATURE = "lon"
LONGITUDE_INDEX = 2


def get_coordinates_with_geoapify_by_address(address: str) -> Optional[tuple[float, float]]:
    """Get coordinates with geocoding api.

    :param address: street and house number
    :return: latitude and longitude
    """
    if GEOAPIFY_TOKEN == "":
        raise ValueError("No GEOAPIFY_TOKEN in environment")
    response = requests.get(
        GEOAPIFY_URL,
        params={
            "text": address,
            "lang": "en",
            "filter": "circle:56.23038809152956,58.04059914692331,20000",
            "format": "json",
            "apiKey": GEOAPIFY_TOKEN,
        },
    )
    data = response.json()
    result = None
    for item in data["results"]:
        if item["rank"]["match_type"] == "full_match":
            result = (item["lat"], item["lon"])
            break
    return result


@click.command()
@click.argument("input_feature_file", type=click.Path(readable=True))
@click.argument("output_feature_file", type=click.Path(writable=True))
def cli(input_feature_file: str, output_feature_file: str) -> None:
    """Add coordinates to data.

    :param input_feature_file: input filepath
    :param output_feature_file: output filepath
    :return: nothing
    """
    df = pd.read_csv(input_feature_file)
    df = df[[ADDRESS_FEATURE]]
    df.drop_duplicates(inplace=True)
    #
    df[LATITUDE_FEATURE] = None
    df[LONGITUDE_FEATURE] = None
    for index in range(len(df)):
        if index % 100 == 0:
            click.echo(f"{round(index / len(df) * 100, 2)}%")
        address = df.iloc[index][ADDRESS_FEATURE]
        try:
            coordinates = get_coordinates_with_geoapify_by_address(address)
        except Exception as ex:
            click.echo(f"error: {ex} with address: {address}")
            continue
        if not coordinates:
            continue
        lat, lon = coordinates
        df.iat[index, LATITUDE_INDEX] = lat
        df.iat[index, LONGITUDE_INDEX] = lon
    click.echo("100%")
    # save
    df.to_csv(output_feature_file, index=False)


if __name__ == "__main__":
    cli()
