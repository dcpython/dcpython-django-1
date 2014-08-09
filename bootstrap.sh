export PYTHONPATH=$PYTHONPATH:/vagrant

# set utf locale for postgres
export LANGUAGE="en_US.UTF-8"
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

# update everything
sudo apt-get update
sudo apt-get upgrade

# install Heroku
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

# install postgres packages
sudo apt-get install postgresql postgresql-server-dev-all -y
# install python packages
sudo apt-get install python-dev python-pip libjpeg-dev -y
# install all python modules in requirements.txt
sudo pip install -r /vagrant/requirements.txt

# have to properly set locale for postgres setup

# sudo -u postgres pg_createcluster --start -e UTF-8 9.1 main
# sudo -u postgres pg_createcluster --start -e UTF-8 --locale=en_US.UTF8 9.1 main

# setup postgresql
sudo -u postgres createuser --superuser vagrant
sudo -u postgres psql -c "alter user postgres with password '1234';"
sudo -u postgres psql -c 'CREATE DATABASE dcpython;'
/vagrant/manage.py syncdb
/vagrant/manage.py migrate
/vagrant/manage.py loaddata /vagrant/dcpython/app/fixtures/debug_data.json
/vagrant/manage.py loaddata /vagrant/dcpython/events/fixtures/debug_data.json
