web: celery -A greenstepbids worker --loglevel=info & python manage.py migrate && gunicorn greenstepbids.wsgi  --bind 0.0.0.0:8080
