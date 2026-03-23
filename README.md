# AI Storybook Flipbook Web App

## Features
- PDF Story Upload (Admin Only)
- Flipbook Viewer (Desktop) / Scroll Reader (Mobile)
- Read Aloud Feature (Text-to-Speech)
- AI Moral Lesson Generator
- Mobile Responsive Design
- User Authentication

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Set start command: `gunicorn storybook_project.wsgi:application`
5. Add environment variables:
   - `DEBUG=False`
   - `SECRET_KEY=your-secret-key`
   - `ALLOWED_HOSTS=your-domain.com`

## Technologies Used
- Django 4.2+
- Bootstrap 5
- PDF.js
- Turn.js
- gTTS
- OpenAI API (optional)
