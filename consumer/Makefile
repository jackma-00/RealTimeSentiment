venv:
	python3 -m venv .venv

install: venv
	. ./.venv/bin/activate && \
    pip install --upgrade pip &&\
    pip install -r requirements.txt

format:
	. ./.venv/bin/activate && \
	black src

build:
	docker build -t consumer .

run:
	docker run -it consumer