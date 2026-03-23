build: pip install -r requirements.txt
release: python manage.py migrate
web: gunicorn story_book.wsgi --bind 0.0.0.0:$PORT
