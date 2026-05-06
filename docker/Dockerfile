FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY scripts ./scripts

RUN python -m pip install --upgrade pip \
    && python -m pip install -e ".[dev]"

USER appuser

CMD ["python", "-m", "pytest"]

