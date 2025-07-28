#!/bin/bash
echo "Running collectstatic..."
python manage.py collectstatic --no-input --clear
