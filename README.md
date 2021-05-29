# Django-Channels-Chat

A real-time chat app using Django and Channels.<br>
It has a chat room entry restriction function and a function to save messages.<br>

## Requires
- Django
- Channels
- Redis
- PostgreSQL

## How to use
1. Create and activate a Python3 virtualenv
```
$ python3 -m venv env
```
2. Install requirements
```
$ pip install -r requirements.txt
```
3. Create a PostgreSQL database
```
CREATE DATABASE chatapp;
```
4. Run Redis Server
```
$ redis-server
```
5. Init databse
```
$ python manage.py migrate
```
6. Create super user
```
$ python manage.py createsuperuser
```
7. Run development server
```
$ python manage.py runserver
```

## Links
See the links below for more information.
- [Django documentation](https://docs.djangoproject.com/en/3.0/)
- [Channels documentation](https://channels.readthedocs.io/en/stable/introduction.html)
