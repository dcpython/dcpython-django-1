DCPython Website
================

..
    About
    -----
    The site is built with the `Django web framework <http://www.djangoproject.org>`_. The two major advantages of Django are it gives us an admin site out of the box and many people already know it.

    We use **Git version control** and `GitHub <http://www.github.com>`_ for project hosting. Github provides git hosting, bug tracking and wiki.

    We use the `Vagrant <http://www.vagrantup.com>`_ development environment. Vagrant allows us to standardize our development and production environments and makes it easy for everybody to get up and running. Vagrant creates a virtual machine, sets up django, database, and everything, then mirrors and syncs the project source code on both your machine and the vm. That way, you make changes to the code on your machine, the changes are mirrored in the vm. Then you run Django on the VM. Now, you can do local development, but you don't have to set up Django and the Database. Very cool.


    Installation
    ------------

    You will need to install:

    - `VirtualBox <http://www.virtualbox.org>`_ (I found that I needed to restart my computer to get VirtualBox working properly)
    - `Vagrant 1.3.4 <http://www.vagrantup.com>`_ (you cannot use ubuntu package - too old)

    Create a `GitHub <http://www.github.com>`_ account.

    While signed into github, go to https://github.com/DCPython/dcpython-django and click the "fork" button. This will create a fork (or copy) of the dcpython-django application in your github account.

    From the commandline
    ++++++++++++++++++++

    Clone your copy of github repository to your working directory (replace <your-username> with  your github username)::

        $ git clone git@github.com:<your-username>/dcpython-django.git
        $ cd dcpython-django

    Start the vagrant environment::

        $ vagrant up

    Start the django server::

        $ heroku local

    Heroku will install a bunch of stuff the first time you run this command, then it will start a dev server.

    You can now visit the Django site at http://localhost:5000

    Basic Vagrant
    -------------

    From the dcpython-django directory
    ++++++++++++++++++++++++++++++++++

    Create a new development environment::

        $ vagrant up

    Destroy the development environment::

        $ vagrant destroy

    Log into the development environment::

        $ vagrant ssh

    From the vagrant ssh command line
    +++++++++++++++++++++++++++++++++

    Start django::

        $ cd /vagrant
        $ heroku local

    Django manage.py::

        $ cd /vagrant
        $ ./manage.py <params>

    You can visit the django site at http://localhost:5000

    Basic Git
    ---------

    We will be using this git branching model: http://nvie.com/posts/a-successful-git-branching-model/

    Start New Feature
    +++++++++++++++++

    Merge any changes from master::

        $ git pull https://github.com/DCPython/dcpython-django.git

    List all the changes in this branch::

        $ git log

    Create a new feature branch in which to make changes::

        $ git checkout -b "descriptive-name-of-branch"

    List branches::

        $ git branch

    Switch to another branch::

        $ git checkout "name-of-branch"

    View status of your files (which have changed, which are staged for commit)::

        $ git status

    Add files to be committed::

        $ git add name-of-file

    Commit changes::

        $ git commit

    .. Note:: you must add a commit message. first line short title (~50 characters); skip line; detailed description of changes

    Merge Feature
    +++++++++++++

    Merge any changes from master that have occurred while you were programming::

        $ git pull https://github.com/DCPython/dcpython-django.git

    Push changes to your github repo::

        $ git push -u origin name-of-branch

    Now, go to github, select the branch you just pushed from the drop-down, then click "pull request" to request your changes be merged with master.

    Deployment
    ----------

    Heroku is generously donating servers. Rackspace is generously donating storage/static file serve.

    On Heroku:
     * `dcpython-develop` - the test server
     * `dcpython` - the production server

    You must set up your repository in order to deploy:

    1. Install Heroku toolbelt: https://toolbelt.heroku.com/
    2. ``git remote add heroku git@heroku.com:dcpython.git``
    3. ``git remote add forked git@heroku.com:dcpython-develop.git``

    To deploy to dev environment:

    1. ``git push forked master``
    2. ``heroku run python manage.py migrate -a dcpython-develop``

    To deploy to production:

    1. ``git push heroku master``
    2. ``heroku run python manage.py migrate -a dcpython``
