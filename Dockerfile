FROM python:3.11-slim

EXPOSE 8000

WORKDIR /app

ENV PYTHONUNBUFFERED=1


RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		libpq-dev \
		libgdal-dev \
		python-dev \
		wait-for-it \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
RUN pip install poetry==1.4.0

COPY pyproject.toml .
COPY poetry.lock .

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install pip==23.0.1 && \
    poetry install -n --no-ansi --no-root

COPY . .
