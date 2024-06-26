"""Module for interaction with Geoapify."""

from dataclasses import dataclass
from typing import Any, Dict

import aiohttp

URL = "https://api.geoapify.com/v1/geocode/search"


class NoTokenException(Exception):
    """Exception if no token."""

    pass


class FetchException(Exception):
    """Exception if error in fetch."""

    pass


class IncorrectQueryException(Exception):
    """Exception if error in request."""

    pass


class NoResultsException(Exception):
    """Exception if not results."""

    pass


@dataclass
class Coordinates:
    """Dataclass for coordinates."""

    lon: float
    lat: float


def build_params(address: str, token: str) -> Dict[str, str]:
    """Build query params.

    :param address: city, street, house
    :param token: for access to geoapify
    :return:
    """
    if not token:
        raise NoTokenException()
    return {
        "text": address,
        "lang": "en",
        "filter": "circle:56.23038809152956,58.04059914692331,20000",
        "format": "json",
        "apiKey": token,
    }


async def send_request(url: str, params: Dict[str, str]) -> Dict[str, Any]:
    """Get nearest by address points.

    :param url: url to search
    :param params: query params
    :return: data
    """
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url, params=params)
            if response.status != 200:
                raise IncorrectQueryException()
            data: Dict[str, Any] = await response.json(encoding="UTF-8")
            return data
    except aiohttp.ClientError:
        raise FetchException() from aiohttp.ClientError


async def get_coordinates_by_address(address: str, token: str) -> Coordinates:
    """Get coordinates by address.

    :param address: city, street, house
    :param token: for access to geoapify
    :return: coordinates
    """
    params = build_params(address, token)
    response_data = await send_request(URL, params)
    for item in response_data["results"]:
        if item["rank"]["match_type"] == "full_match":
            return Coordinates(lat=item["lat"], lon=item["lon"])
    raise NoResultsException()
