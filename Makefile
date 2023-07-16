install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	ruff check app/*.py

format:
	isort --profile black app/*.py  && black app/*.py

run:
	python app/main.py

dstart:
	docker start

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

all: 
	install lint format run
