SHELL := /bin/bash

create-venv:
	python3 -m venv venv

active-venv:
	source venv/bin/activate

man-active-venv:
	@echo "Run this manually in your shell:"
	@echo "  source venv/bin/activate"

install:
	pip install django-environ

requires:
	pip freeze > requirements.txt

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

start:
	python3 manage.py runserver

show-urls:
	python3 manage.py show_urls

install:
	pip install -r requirements.txt

startapp:
	python3 manage.py startapp $(APPNAME)