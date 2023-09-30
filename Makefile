run:
	python app.py
	
venv:
	pyenv install 3.10.8 --skip-existing
	pyenv virtualenv -f 3.10.8 story-api
	pyenv local story-api
	pip install -r requirements.txt

psql:
	psql -U dev -h localhost story

db-migrate:
	yoyo apply -c yoyo/${api_env}.ini