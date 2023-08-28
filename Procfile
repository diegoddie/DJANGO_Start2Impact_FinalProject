worker: celery -A greenstepbids worker --loglevel=info -P eventlet
web: gunicorn greenstepbids.wsgi --bind 0.0.0.0:$PORT
celery-beat: celery -A greenstepbids.celery beat --loglevel=info