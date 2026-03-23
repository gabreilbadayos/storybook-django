build: ./build.sh
release: python manage.py migrate
web: gunicorn story_book.wsgi --bind 0.0.0.0:$PORT --workers 3
