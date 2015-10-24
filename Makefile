update: github heroku
github:
	git commit -a -m "Update"
	git push
heroku:
	git push heroku master

lint:
	yapf -i dcpython/*/*.py
#	flake8 dcpython/*/*.py
