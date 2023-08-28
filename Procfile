web: celery -A greenstepbids worker --loglevel=info & celery -A greenstepbids.celery beat -l info & python manage.py migrate && gunicorn greenstepbids.wsgi  --bind 0.0.0.0:8080
