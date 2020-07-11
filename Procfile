web: gunicorn TuOfertApp.wsgi --log-file -
python manage.py collectstatic --noinput
python manage.py loaddata fixtures/initial_data_groups.json
python manage.py loaddata fixtures/initial_auth.json
python manage.py makemigrations users
python manage.py makemigrations business
python manage.py makemigrations
python manage.py migrate