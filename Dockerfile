# -------- BUILD STAGE --------
FROM python:3.12-alpine AS build

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache \
    gcc musl-dev linux-headers libffi-dev postgresql-dev \
    cargo rust bash findutils

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /bin/

RUN pip install poetry poetry-plugin-export

WORKDIR /build

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt

RUN uv venv $VIRTUAL_ENV
RUN uv pip install --no-cache -r requirements.txt

COPY . .

# -------- RUNTIME STAGE --------
FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --no-cache postgresql-client bash

COPY --from=build /opt/venv /opt/venv
COPY --from=build /build /var/www/html

WORKDIR /var/www/html

RUN mkdir -p storage/media logs alembic/versions \
    && chmod +x init_db.sh

EXPOSE 8000

CMD sh -c "./init_db.sh && exec uvicorn src.main:app --host 0.0.0.0 --port 8000"
