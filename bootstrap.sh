#!/bin/sh
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

#setup python3
sudo apt-get install python-software-properties -y
sudo add-apt-repository ppa:fkrull/deadsnakes -y
sudo apt-get update
echo "*** installing python3.4"
sudo apt-get install python3.4 python3.4-dev -y
echo "*** doing python3.4 -m ensurepip"
sudo python3.4 -m ensurepip
echo "*** installing requirements for python3.4, using pip3"
sudo pip3 install -r /vagrant/requirements.txt

# have to properly set locale for postgres setup

# sudo -u postgres pg_createcluster --start -e UTF-8 9.1 main
# sudo -u postgres pg_createcluster --start -e UTF-8 --locale=en_US.UTF8 9.1 main

# setup postgresql
sudo -u postgres createuser --superuser vagrant
sudo -u postgres psql -c "alter user postgres with password '1234';"
sudo -u postgres psql -c 'CREATE DATABASE dcpython;'
/vagrant/config_db.sh
