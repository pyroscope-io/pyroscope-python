ARG python_version="3.9"
FROM python:$python_version-slim-buster

ENV PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.7 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

WORKDIR /app

RUN apt-get -y update && apt-get -y install gcc wget
RUN python3 -m pip install poetry==$POETRY_VERSION

COPY LICENSE README.md build.py pyproject.toml agent.c ./
COPY pyroscope_io/ ./pyroscope_io/

RUN poetry build --format wheel
ENTRYPOINT ["/usr/local/bin/poetry"]
