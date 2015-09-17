#!/bin/sh
export PYTHONPATH=$PYTHONPATH:/vagrant

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

# setup database
/vagrant/manage.py syncdb
/vagrant/manage.py migrate
/vagrant/manage.py loaddata /vagrant/dcpython/app/fixtures/debug_data.json
/vagrant/manage.py loaddata /vagrant/dcpython/events/fixtures/debug_data.json
