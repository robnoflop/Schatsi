FROM python:3.10-slim-bullseye

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config && \
    apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
COPY data /data

CMD [ "python", "./main.py" ]
