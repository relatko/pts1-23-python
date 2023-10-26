check_and_test: FORCE
	mypy azul --strict
	mypy test --strict
	python3 -m unittest 
lint: FORCE
	pylint azul/
	pylint test/

format: FORCE
	autopep8 -i azul/*.py
	autopep8 -i test/*.py
FORCE: ;
