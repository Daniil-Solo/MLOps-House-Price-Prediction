"""Script for cleaning data."""

import re
from typing import Optional, Union

import click
import numpy as np
import pandas as pd

# column names
ELEVATOR_FEATURE = "elevator"
FLOORS_FEATURE = "number of floors"
APARTMENT_FLOOR_FEATURE = "apartment floor"
ADDRESS_FEATURE = "physical address"
DISTRICT_FEATURE = "district"
BATHROOM_FEATURE = "bathroom"
AREA_FEATURE = "area of apartment"
HOUSE_TYPE_FEATURE = "type of house"
ROOMS_FEATURE = "number of rooms"
TARGET = "price"
NON_NULL_FEATURES = [
    ADDRESS_FEATURE,
    FLOORS_FEATURE,
    HOUSE_TYPE_FEATURE,
    ROOMS_FEATURE,
    AREA_FEATURE,
    APARTMENT_FLOOR_FEATURE,
    TARGET,
]
REPAIR_FEATURE = "repair"
TERRACE_FEATURE = "terrace"
EXTRA_FEATURE = "extra"
NULL_FEATURES = [REPAIR_FEATURE, TERRACE_FEATURE, EXTRA_FEATURE]
ALL_FEATURES = NON_NULL_FEATURES + NULL_FEATURES + [ELEVATOR_FEATURE, DISTRICT_FEATURE, BATHROOM_FEATURE]


def extract_first_int(number: Union[str, int]) -> int:
    """Extract first int from string or return int if passed int.

    :param number:
    :return: first number
    """
    if isinstance(number, int):
        return number
    numbers = re.findall(r"\d+", number)
    if not numbers:
        raise ValueError(f" '{number}' doesnt contain any integer number")
    return int(numbers[0])


def get_min_elevator_count_by_floor_count(floor_count: int) -> int:
    """Calculate min elevator count on info about floor.

    :param floor_count:
    :return: elevator count
    """
    if isinstance(floor_count, str):
        raise ValueError(floor_count)
    if floor_count <= 5:
        return 0
    elif 6 <= floor_count <= 9:
        return 1
    elif 10 <= floor_count <= 19:
        return 2
    else:
        return 3


def get_district_from_address(address_with_district: str) -> Optional[str]:
    """Extract district from address.

    :param address_with_district:
    :return: district or None
    """
    address_data = address_with_district.split("|")
    if len(address_data) == 1:  # has only address
        return None
    else:
        return address_data[-1].strip()


def get_street_and_house_from_address(address_with_district: str) -> str:
    """Get street and house from address.

    :param address_with_district:
    :return: "street, house number"
    """
    street_part_map = {
        "ул.": "улица",
        "улица": "улица",
        "пр-т": "проспект",
        "пр.": "проезж",
        "ш.": "шоссе",
        "б-р": "бульвар",
    }
    address = address_with_district.split("|")[0]
    perm_string_1 = "Пермский край, "
    perm_string_2 = "Пермь, "
    if address.startswith(perm_string_2):
        address = perm_string_1 + address
    elif not address.startswith(perm_string_1):
        address = perm_string_1 + perm_string_2 + address
    street = address.split(", ")[2].strip()
    for old_part, new_part in street_part_map.items():
        if street.startswith(old_part) or street.endswith(old_part):
            street = new_part + " " + street.strip(old_part).strip()
            break
    address = ", ".join([street] + [item.replace("д.", "").strip() for item in address.split(",")[3:]])
    return address


def get_room_count_by_name(room_name: str) -> int:
    """Get count of rooms by specific name.

    :param room_name:
    :return: count of rooms
    """
    if room_name.isdigit():
        return int(room_name)
    if room_name in ("студия", "своб. планировка"):
        return 1
    raise ValueError(f"Unknown room type: {room_name}, {type(room_name)}")


@click.command()
@click.argument("input_feature_file", type=click.Path(readable=True))
@click.argument("output_feature_file", type=click.Path(writable=True))
def cli(input_feature_file: str, output_feature_file: str) -> None:
    """Clean data.

    :param input_feature_file: input filepath
    :param output_feature_file: output filepath
    :return: nothing
    """
    df = pd.read_csv(input_feature_file)
    # features where we need non-null values
    for feature in NON_NULL_FEATURES:
        df = df[df[feature].notna()]
    # address
    df[DISTRICT_FEATURE] = df[ADDRESS_FEATURE].apply(get_district_from_address)
    df = df[df[DISTRICT_FEATURE].notna()]
    df[ADDRESS_FEATURE] = df[ADDRESS_FEATURE].apply(get_street_and_house_from_address)
    # bathroom
    df[BATHROOM_FEATURE] = df[BATHROOM_FEATURE].fillna("неизвестно")
    df = df[df[BATHROOM_FEATURE].apply(lambda x: len(x) < 20)]  # filter anomaly values
    # type of house
    df = df[df[HOUSE_TYPE_FEATURE].apply(lambda x: len(x) < 20)]  # filter anomaly values
    # area
    df[AREA_FEATURE] = df[AREA_FEATURE].apply(lambda x: float(x[:-3])).astype(np.float64)
    # room count
    df = df[df[ROOMS_FEATURE] != "многокомнатная"]
    df[ROOMS_FEATURE] = df[ROOMS_FEATURE].apply(get_room_count_by_name)
    # floor count
    df[FLOORS_FEATURE] = df[FLOORS_FEATURE].apply(extract_first_int).astype(np.int64)
    df[APARTMENT_FLOOR_FEATURE] = df[APARTMENT_FLOOR_FEATURE].astype(np.int64)
    # features where we allow non-null values
    for feature in NULL_FEATURES:
        df[feature] = df[feature].fillna("нет")
    # repair
    df = df[df[REPAIR_FEATURE].apply(lambda x: len(x) < 20)]  # filter anomaly values
    # elevator
    min_elevator_counts = df[FLOORS_FEATURE].apply(get_min_elevator_count_by_floor_count).values
    df[ELEVATOR_FEATURE] = np.where(df[ELEVATOR_FEATURE].isna(), min_elevator_counts, df[ELEVATOR_FEATURE].values)
    df[ELEVATOR_FEATURE] = df[ELEVATOR_FEATURE].astype(np.int64)
    # extra
    df[EXTRA_FEATURE] = df[EXTRA_FEATURE] == "нет"
    # save
    df[ALL_FEATURES].to_csv(output_feature_file, index=False)
    # logging
    click.echo(df[ALL_FEATURES].info())


if __name__ == "__main__":
    cli()
