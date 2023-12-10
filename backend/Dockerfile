FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
