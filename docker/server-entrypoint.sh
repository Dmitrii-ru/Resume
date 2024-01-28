#!/bin/sh

until cd /app/
do
    echo "Waiting for server volume..."
done

mkdir -p static

until python manage.py makemigrations
do
    echo "Try makemigrations"
    sleep 2
done

until python manage.py migrate
do
    echo "Try migrate"
    sleep 2
done



python manage.py db_load
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000