
run:
	@uvicorn main:application --port 8000 --reload

install-dep:
	@poetry install

update-dep:
	@poetry update

activate-env:
	@poetry shell

generate_data:
	@export PYTHONPATH=./:$PYTHONPATH
	@.venv/bin/python3.12 helpers/populate_data.py