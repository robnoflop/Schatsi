FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./SCHATSI002.py" ]
