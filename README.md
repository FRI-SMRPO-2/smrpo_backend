## SMRPO backend
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


[Django docs](https://docs.djangoproject.com/en/3.0/ "Django docs")\
[Python virtual environment](https://docs.python-guide.org/dev/virtualenvs/)

#### Virtual environment
Create virtual environment:
1) pip install virtualenv
2) virtualenv \<virtualenvname\> -p python3.6
3) source <virtualenvname\>/bin/activate
4) pip install -r requirements.txt

#### Run server
1) source <virtualenvname\>/bin/activate
2) python manage.py migrate
3) python manage.py runserver