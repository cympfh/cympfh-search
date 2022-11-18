FROM python:3.9-slim

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN apt update && apt install -y git \
 && pip install -U pip setuptools wheel poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-dev
ENV X_GIT_DIR=/git/cympfh.github.io/
COPY . .
CMD ["uvicorn", "search:app", "--port", "8083", "--host", "0.0.0.0"]
