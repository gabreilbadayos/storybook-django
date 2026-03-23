build: pip install -r requirements.txt && python manage.py migrate --noinput
web: gunicorn story_book.wsgi --bind 0.0.0.0:$PORT --workers 2
