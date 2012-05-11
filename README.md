lunch_it
========

Lunch train organization mobile web application

Setup instructions:

1) get virtualenv. On Ubuntu:
sudo apt-get install python-setuptools

On Ubuntu, you'll also need:
sudo apt-get install libmysqlclient-dev python-dev

That's to make mysql work.

2) check out
git clone git@github.com:locatinolabs/lunch_it.git
cd lunch_it

3) create virtual env
virtualenv env

4) turn on virtual env for this shell
. env/bin/activate

5) install required packages
pip install django
pip install MySQL-python
pip install python-ldap

6) run the app:
manage.py runserver


Notes
-----

Python project that uses LDAP: svn+ssh://svn/wm/sys/hq/ldapinfo
