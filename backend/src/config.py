"""Module for config."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Class for loading the necessary env variables."""

    GEOAPIFY_TOKEN: str = ""
    DISTRICTS_GEOJSON_PATH: str = ""
    AMENITY_DIR_PATH: str = ""

    MLFLOW_TRACKING_URI: str = ""
    MLFLOW_S3_ENDPOINT_URL: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    MODEL_NAME: str = ""
    MODEL_VERSION: str = ""

    LOGGING_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env")


app_config = Config()
