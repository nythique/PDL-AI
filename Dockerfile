FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    tesseract-ocr \
    tesseract-ocr-fra \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/PDL-AI

RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction

COPY . .

CMD ["poetry", "run", "python", "run.py"]