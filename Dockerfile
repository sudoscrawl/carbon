# syntax=docker/dockerfile:1.22
FROM python:3.14.5-alpine3.22 AS base

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

WORKDIR /carbon

# -- Build Stage --
FROM base as builder

ENV \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=off \
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR="/var/cache/pypoetry" \
  POETRY_HOME="/usr/local"

COPY . .

RUN apk update \
    && apk add --no-cache gettext \
    && rm -rf /var/cache/apk/* \
    && pip install poetry \
    && poetry install --no-interaction --no-ansi --no-root --only main \
    && poetry run pybabel compile -d locales \
    && find /carbon/.venv \
        -type d \( -name test -o -name tests \) -exec rm -rf {} + \
    && find /carbon/.venv \
        -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

# -- Final Stage --
FROM base AS final

ENV \
  PATH="/carbon/.venv/bin:$PATH"

RUN apk cache clean \
  && rm -rf /var/cache/apk/* \
  && addgroup -S app \
  && adduser -S -D -H -G app carbon

COPY --from=builder /carbon/.venv ./.venv

COPY \
  --from=builder \
  --exclude="**/*.po" \
  --exclude="**/*.pot" \
  /carbon/locales ./locales

COPY --from=builder /carbon/app ./app/
COPY --from=builder /carbon/main.py ./

USER carbon

CMD ["python", "main.py"]
