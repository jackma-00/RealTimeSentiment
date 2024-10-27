FROM python:3.10-slim-bullseye

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install -y openjdk-11-jdk procps && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
ENV PYTHONPATH="/code/src:${PYTHONPATH}"

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
