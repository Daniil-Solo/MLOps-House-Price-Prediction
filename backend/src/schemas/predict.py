"""Module with schemas."""

from enum import Enum

from pydantic import BaseModel


class HouseType(Enum):
    """House type values."""

    Panel = "панельный"
    Brick = "кирпичный"
    Monolith = "монолитный"
    Block = "блочный"


class RepairType(Enum):
    """Repair type values."""

    Cosmetic = "косметический"
    Design = "дизайнерский"
    No = "нет"
    Euro = "евро"


class TerraceType(Enum):
    """Terrace type values."""

    Balkon = "балкон"
    Lodge = "лоджия"
    No = "нет"


class BathroomType(Enum):
    """Bathroom type values."""

    Together = "совмещенный"
    Divide = "раздельный"
    Many = "несколько"


class BasePredictionIn(BaseModel):
    """Base class for input prediction."""

    number_of_floors: int
    type_of_house: HouseType
    number_of_rooms: int
    area_of_apartment: float
    apartment_floor: int
    repair: RepairType
    terrace: TerraceType
    extra: bool
    elevator: int
    bathroom: BathroomType


class PredictionWithAddressIn(BasePredictionIn):
    """Prediction class with address field."""

    address: str = "г. Пермь, ул. Ординская, д. 10, корп. 2"


class PredictionWithCoordinatesIn(BasePredictionIn):
    """Prediction class with coordinates field."""

    lat: float
    lon: float


class PredictionOut(BaseModel):
    """Prediction result."""

    value: float
