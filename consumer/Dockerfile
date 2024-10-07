FROM python:3.10-slim-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /code/src

CMD ["python", "src/consumer.py"]