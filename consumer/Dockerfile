FROM python:3.10-slim-bullseye

COPY requirements.txt /code/

RUN apt-get update && apt-get install -y openjdk-11-jdk procps && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code/

WORKDIR /code


RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
