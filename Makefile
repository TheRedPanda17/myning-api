run:
	python app.py
	
venv:
	pyenv install 3.10.8 --skip-existing
	pyenv virtualenv -f 3.10.8 myning-api
	pyenv local myning-api
	pip install -r requirements.txt

psql:
	psql -U dev -h localhost myning

db-migrate:
	yoyo apply -c yoyo/${api_env}.ini