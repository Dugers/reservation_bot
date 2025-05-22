FROM python:3.13-alpine

ENV POETRY_VERSION=1.8.4
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /app

COPY . .
RUN poetry install --no-interaction --no-ansi

ENTRYPOINT [ "poetry", "run", "prod" ]