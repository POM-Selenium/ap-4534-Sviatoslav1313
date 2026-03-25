FROM python:3.10-slim

# Install system dependencies for psycopg2
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/library

EXPOSE 8000

CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
