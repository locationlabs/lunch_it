lunch_it
========

Lunch train organization mobile web application. This project was created in an 24 hour period as part of Location Labs Hack Day 2012.

Setup instructions
------------------

1) get virtualenv. On Ubuntu:
> sudo apt-get install python-setuptools

On Ubuntu, you'll also need:
> sudo apt-get install libmysqlclient-dev python-dev  

That's to make mysql work.

You may also need virtualenv
> sudo apt-get install python-virtualenv

For the icons, you need the python imaging library
sudo apt-get install python-imaging

2) check out
> git clone git@github.com:locationlabs/lunch_it.git  
> cd lunch_it

3) create virtual env
> virtualenv env

4) turn on virtual env for this shell
> . env/bin/activate

5) install required packages
> pip install django  
> pip install MySQL-python  
> pip install django-crispy-forms

Not working now, but might be useful eventually:
> pip install python-ldap

6) run the app:
> manage.py runserver

7) Create the database:

> CREATE DATABASE lunchit CHARACTER SET utf8;

8) Create user for database
> GRANT ALL PRIVILEGES ON *.* TO 'lunchmonster'@'localhost' IDENTIFIED BY 'mylunch';

9) First database sync
> python manage.py syncdb

Resetting the DB
----------------

To Reset the DB and re-load the initial data (from directory lunch_it/lunch_it):

> python manage.py sqlclear trains | mysql -uroot -proot lunchit  
> python manage.py sqlclear auth | mysql -uroot -proot lunchit  
> python manage.py syncdb  
> python initdata.py

Deployment Info
---------------
 - I cloned the git repo into /var/wsgi/lunch_it ; that's a read-only git clone.
 - To update that:
   > cd /var/wsgi/lunch_it  
   > git pull  
   > python lunch_it/manage.py collectstatic
 - you'll also need to run the "reset db" steps above.
 - when hosting:
   - static content in /var/wsgi/lunch_it/content/static needs to be hosted at /static
   - actual app needs to be hosted using wsgi or similar; see /var/wsgi/lunch_it/deploy/dispatch.wsgi for example config
     - note that we've never proven the example config even works
     - it's based on input from here:
       - http://www.foxhop.net/django-virtualenv-apache-mod_wsgi


Notes
-----

Python project that uses LDAP: svn+ssh://svn/wm/sys/hq/ldapinfo


