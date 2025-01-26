.PHONY: phony

install: phony
ifndef VIRTUAL_ENV
	$(error install can only be run inside a Python virtual environment)
endif
	@echo Installing dependencies...
	pip install -e .

test: phony
	pytest
