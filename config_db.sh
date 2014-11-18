#!/bin/sh
/vagrant/manage.py syncdb
/vagrant/manage.py migrate
/vagrant/manage.py loaddata /vagrant/dcpython/app/fixtures/debug_data.json
/vagrant/manage.py loaddata /vagrant/dcpython/events/fixtures/debug_data.json
