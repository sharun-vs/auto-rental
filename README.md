# auto-rental

djangorestframework + postgres

## envs to setup

create a .env file in the root directory

populate following values

DEBUG=

ALLOWED_HOSTS=127.0.0.1, localhost

DJANGO_SECRET_KEY=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_HOST=

DB_PORT=

## to fire-up server

mkdir auto-rental

git clone https://github.com/sharun-vs/auto-rental.git

cd auto-rental

pipenv shell (assuming pipenv as already installed in the system, if not: https://pipenv.pypa.io/en/latest/)

pipenv install

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

## link to postman collection

https://api.postman.com/collections/25368965-8ae33589-db64-40e7-9568-f4e175490a47?access_key=PMAT-01GQ1TVAMA9TG518NB907BHFEC
