"""Script for downloading features with overpass api."""

import json

import click
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
AREA_BOUND = (57.90171502586015, 55.813316787298895, 58.147518599073585, 56.552147353705145)  # for Perm
ITEMS_KEY = "elements"


def get_search_data(amenities: list[str], bound: tuple[float, float, float, float]) -> str:
    """Build search data for request.

    :param amenities: list of amenity
    :param bound: tuple of coordinates
    :return: data as text
    """
    amenity_string = "|".join(amenities)
    data = f"""
        [out:json];
        node
          ["amenity"~"{amenity_string}"]
          {bound};
        out;
    """
    return data


@click.command()
@click.option("--amenities", "-a", type=click.STRING, help="Type of amenity, i.e. cafe", multiple=True, default=[])
@click.argument("output_feature_file", type=click.Path(writable=True))
def cli(amenities: list[str], output_feature_file: str) -> None:
    """Download amenity features.

    :param amenities: list of amenity
    :param output_feature_file: out filepath
    :return: nothing
    """
    res = requests.post(OVERPASS_URL, data=get_search_data(amenities, AREA_BOUND))
    res_data = json.loads(res.content)
    with open(output_feature_file, "w", encoding="utf-8") as f:
        json.dump(res_data[ITEMS_KEY], f)


if __name__ == "__main__":
    cli()
