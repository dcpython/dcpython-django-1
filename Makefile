lint: yapf flake

static:
	python manage.py collectstatic --noinput

yapf:
	yapf -i dcpython/*.py
	yapf -i dcpython/*/*.py

flake:
	flake8 dcpython/*.py
	flake8 dcpython/*/*.py

push:
	git push

github:
	git commit -a -m "Update"

heroku:
	git push heroku master

publish: github push heroku
