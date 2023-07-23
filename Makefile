setup:
	python3.8 -m venv .venv
	source .venv/bin/activate

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	ruff check app/*.py

format:
	isort --profile black app/*.py  && black app/*.py

run:
	python app/main.py

all: 
	install lint format run
