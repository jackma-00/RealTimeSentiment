FROM python:3.10-slim-bullseye

COPY . /code/

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]