PY = python3

ifeq ($(OS), Windows_NT)
    PY=python
endif

all: check test lint

check_and_test: FORCE
	mypy azul --strict
	mypy test --strict
	$(PY) -m unittest 

lint: FORCE
	pylint azul/
	pylint test/

format: FORCE
	autopep8 -i azul/*.py
	autopep8 -i test/*.py

test: FORCE
	$(PY) -m unittest

check: FORCE
	mypy azul --strict
	mypy test --strict

FORCE: ;
