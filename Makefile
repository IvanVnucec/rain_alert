run: init
	. venv/bin/activate; python rain_alert/main.py

PHONY: init
init: venv

PHONY: test
test: venv
	. venv/bin/activate; python tests/test_example.py

PHONY: clean
clean:
	rm -rf venv
	find -iname "*.pyc" -delete

.PHONY: list
list:
	@echo "run   - Run app,"
	@echo "init  - Install all the dependancies with virtualenv,"
	@echo "test  - Run unit tests,"
	@echo "clean - Clean virtualenv directory."
	@echo "list  - List all the makefile commands."

venv: venv/touchfile

venv/touchfile: requirements.txt
	python3 -m pip install virtualenv
	test -d venv || python -m virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/touchfile
