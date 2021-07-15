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

WORKDIR /app

RUN apt-get -y update && apt-get -y install gcc wget
RUN python3 -m pip install poetry

RUN wget -qnc https://dl.pyroscope.io/static-libs/bf8582b/linux-amd64/libpyroscope.pyspy.a -O libpyroscope.pyspy.a
RUN wget -qnc https://dl.pyroscope.io/static-libs/bf8582b/linux-amd64/libpyroscope.pyspy.h -O libpyroscope.pyspy.h
RUN wget -qnc https://dl.pyroscope.io/static-libs/bf8582b/linux-amd64/librustdeps.a -O librustdeps.a

COPY LICENSE README.md build.py pyproject.toml agent.c ./
COPY pyroscope/ ./pyroscope/

RUN poetry build
ENTRYPOINT ["/usr/local/bin/poetry"]

