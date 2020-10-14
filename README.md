# TuOfert_app

## Crear migraciones individuales

```
python manage.py makemigrations users
python manage.py makemigrations business
```

Proceso inicia para la creacion de grupos de ususario y datos default
```
python manage.py loaddata fixtures/initial_data_groups.json
python manage.py loaddata fixtures/initial_auth.json
python manage.py loaddata fixtures/initial_business_categories.json
```