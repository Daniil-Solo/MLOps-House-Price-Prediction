# ML-project

## Организация проекта
```

    ├── README.md                <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs                     <- A default quarto documentation
    │
    ├── models                   <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks                <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                              the creator's initials, and a short `-` delimited description, e.g.
    │                              `1.0-jqp-initial-data-exploration`.
    │
    ├── references               <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports                  <- Generated analysis as HTML, PDF, LaTeX, etc.
    │
    ├── src                      <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    ├── Makefile                 <- Scripts for development
    ├── .env.example             <- Env variables for example
    ├── pyproject.toml           <- Installed libraries, config for liters, formatters
    └── poetry.lock              <- locks for libraries
```

Проект базируется на шаблоне [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science/)
со следующими изменениями:
- requirements.txt заменен на poetry
- удалены setup.py, test_environment.py, tox.ini
- переработан Makefile
- переход от Sphinx к Quarto документации