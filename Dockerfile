ARG python_version=cp39-cp39
ARG manylinux_version=manylinux2014
ARG manylinux_arch=x86_64

FROM quay.io/pypa/${manylinux_version}_${manylinux_arch}:latest

ARG python_version

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

RUN yum install -y wget

ENV PATH=/opt/python/${python_version}/bin:$PATH
RUN python3 -m pip install poetry==$POETRY_VERSION

COPY LICENSE README.md build.py pyproject.toml agent.c ./
COPY pyroscope_io/ ./pyroscope_io/

RUN poetry build --format wheel
ENTRYPOINT ["/usr/local/bin/poetry"]
