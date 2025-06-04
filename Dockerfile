FROM python:3.12-slim

WORKDIR /app/PDL-AI

COPY upload.txt .

RUN apt-get update && apt-get install -y tesseract-ocr

RUN pip install --no-cache-dir -r upload.txt

COPY . .

CMD ["python", "run.py"]