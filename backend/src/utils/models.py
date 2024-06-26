"""Module for loading model."""

import os

import catboost
import mlflow

from src.config import Config


def load_model(config: Config) -> catboost.CatBoostRegressor:
    """Load model from MLflow Models Registry.

    :param config: application config
    :return:
    """
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    os.environ["AWS_ACCESS_KEY_ID"] = config.AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = config.AWS_SECRET_ACCESS_KEY
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = config.MLFLOW_S3_ENDPOINT_URL
    return mlflow.pyfunc.load_model(f"models:/{config.MODEL_NAME}/{config.MODEL_VERSION}")
