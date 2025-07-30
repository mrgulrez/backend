#!/bin/bash
pip3 install -r requirements.txt
python3 manage.py collectstatic --no-input --clear
python3 manage.py makemigrations
python3 manage.py migrate
