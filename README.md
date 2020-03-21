## SMRPO backend
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


### Installation
[Django docs](https://docs.djangoproject.com/en/3.0/ "Django docs")\
[Python virtual environment](https://docs.python-guide.org/dev/virtualenvs/)

**1. Create virtual enviroment and activate it.**

```
$ pip install virtualenv
$ virtualenv <virtualenvname> -p python3.6
$ source <virtualenvname\>/bin/activate
$ pip install -r requirements.txt
```

**2. Run Django development server.**

```
$ source <virtualenvname>/bin/activate
$ python manage.py migrate
$ python manage.py runserver
```
### Migrations
Everytime you create, change or delete models, you should perform next operations to create migrations in the database. 

```
$ python manage.py makemigrations
$ python manage.py migrate
```
Make sure to commit & push migrations!
