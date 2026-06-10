FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]