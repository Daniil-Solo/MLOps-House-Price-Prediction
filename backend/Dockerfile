FROM python:3.11-bookworm
RUN pip install poetry
ADD pyproject.toml .
RUN poetry install --no-dev
COPY /src /src
WORKDIR .