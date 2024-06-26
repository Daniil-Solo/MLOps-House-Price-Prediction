"""Script for downloading raw dataset."""

import click
import pandas as pd

DATASET_URL = "https://raw.githubusercontent.com/Daniil-Solo/Avito-analytics/main/data.csv"


@click.command()
@click.argument("output_dataset_file", type=click.Path(writable=True))
def cli(output_dataset_file: str) -> None:
    """Download data from DATASET_URL.

    :param output_dataset_file: out filepath
    :return: nothing
    """
    df = pd.read_csv(DATASET_URL, delimiter=";")
    df.to_csv(output_dataset_file, index=False)


if __name__ == "__main__":
    cli()
