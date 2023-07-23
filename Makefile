setup:
	python -m venv .venv
	source .venv/bin/activate

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	ruff check app/*.py

test:
	python -m pytest -vv --cov=app tests/

format:
	isort --profile black app/*.py  && black app/*.py

run:
	python app/main.py

test: 
	install lint format test

deploy:
	install lint format run
