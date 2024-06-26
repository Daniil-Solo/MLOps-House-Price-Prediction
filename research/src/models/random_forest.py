"""Script for training and evaluating model."""

import os

import click
import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

load_dotenv()
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "")
RANDOM_STATE = int(os.environ.get("RANDOM_STATE", "0"))


TARGET = "price"
CAT_FEATURES = ["type of house", "repair", "terrace", "district", "bathroom"]


@click.command()
@click.argument("dataset_file", type=click.Path(readable=True))
def cli(dataset_file: str) -> None:
    """Train and evaluate linear model.

    :param dataset_file: filepath to dataset
    :return: nothing
    """
    df = pd.read_csv(dataset_file)
    # avoid user mistakes when users accidentally add three zero values
    df = df[df[TARGET] < 20_000_000]
    df = pd.get_dummies(df, columns=CAT_FEATURES, prefix=CAT_FEATURES, drop_first=True)
    click.echo(list(df.columns))
    # train test split
    x = df.drop(columns=[TARGET]).values
    y = df[TARGET].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=RANDOM_STATE)
    # MLflow integration
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("ml-project")
    with mlflow.start_run(run_name="random-forest"):
        # model training
        rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=RANDOM_STATE)
        rf_model.fit(x_train, y_train)
        predicts = rf_model.predict(x_test)
        # parameters logging
        mlflow.log_params(rf_model.get_params())
        # metrics logging
        r2_score_value = r2_score(y_test, predicts)
        root_mean_squared_error_value = root_mean_squared_error(y_test, predicts)
        mlflow.log_metric("r2_score", r2_score_value)
        mlflow.log_metric("rMSE", root_mean_squared_error_value)
        # model saving
        mlflow.sklearn.log_model(rf_model, "random_forest")
        # figure saving
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        y_min, y_max = y_test.min(), y_test.max()
        ax.plot([y_min, y_max], [y_min, y_max], c="g")
        ax.scatter(y_test, predicts, c="r")
        mlflow.log_figure(fig, "prediction_result.png")
        del fig
        # figure saving feature importance
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        feature_importance_list = pd.Series(rf_model.feature_importances_, index=[c for c in df.columns if c != TARGET])
        feature_importance_list.nlargest(10).plot(kind="barh", ax=ax)
        mlflow.log_figure(fig, "feature_importance.png")


if __name__ == "__main__":
    cli()
