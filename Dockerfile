FROM python:3.9-slim-buster

ENV PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.5 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get -y update && apt-get -y install gcc vim
RUN python3 -m pip install poetry

WORKDIR /app

COPY LICENSE README.md build.py pyproject.toml pyroscope.c ./
COPY pyroscope/ ./pyroscope/

COPY --from=pyroscope_static /libpyroscope.pyspy.a ./
COPY --from=pyroscope_static /librustdeps.a ./
COPY --from=pyroscope_static /libpyroscope.pyspy.h ./

RUN poetry build
