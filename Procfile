web: gunicorn 'greenstepbids.wsgi' --log-file - 
worker: celery -A greenstepbids worker --loglevel=info -P eventlet
celery_beat: celery -A greenstepbids.celery beat -l info