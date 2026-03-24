# Django Storybook - PythonAnywhere Deployment Guide

## Prerequisites
- [ ] PythonAnywhere account: https://www.pythonanywhere.com (free Beginner account OK)
- [ ] GitHub repo with this project pushed

## Step-by-Step Deployment

### 1. Upload Code
```
# In PA Bash console:
git clone https://github.com/YOURUSERNAME/YOUR-REPO.git ~/storybook
cd ~/storybook
```

### 2. Virtual Environment
```
mkvirtualenv --python=/usr/bin/python3.10 storybook
workon storybook
pip install -r requirements.txt
```

### 3. Web App Setup (Web tab → Add new web app)
```
- Choose: Manual configuration, Python 3.10
- Source code path: /home/YOURUSERNAME/storybook
- Virtualenv: /home/YOURUSERNAME/.virtualenvs/storybook
- Static files:
  * URL: /static/  Directory: /home/YOURUSERNAME/storybook/staticfiles
  * URL: /media/   Directory: /home/YOURUSERNAME/storybook/media
```

### 4. Configure WSGI file
Edit `/var/www/YOURUSERNAME_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Project path
path = '/home/YOURUSERNAME/storybook'
if path not in sys.path:
    sys.path.insert(0, path)

# Set settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'storybook_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5. Environment Variables (Web tab)
```
DEBUG=False
SECRET_KEY=your-very-secret-key-generate-new-one
ALLOWED_HOSTS=gabreil.pythonanywhere.com
```

### 6. Database
```
# Option 1: SQLite (easy, in settings.py default)
# Option 2: PA MySQL (Databases tab → create DB)
# Edit settings.py DATABASES if using MySQL
```

```
cd ~/storybook
workon storybook
python manage.py migrate
python manage.py createsuperuser
```

### 7. Static Files
```
python manage.py collectstatic --noinput
```
**Click "Reload" in Web tab**

### 8. Access
```
Site: https://gabreil.pythonanywhere.com
Admin: https://gabreil.pythonanywhere.com/admin/
```

## Updates
```
cd ~/storybook
git pull
workon storybook
python manage.py collectstatic --noinput
touch /var/www/YOURUSERNAME_pythonanywhere_com_wsgi.py
```

## Troubleshooting
| Issue | Solution |
|-------|----------|
| 500 Error | Check error.log (Web tab) |
| Static files missing | Verify STATIC_ROOT='/staticfiles', collectstatic |
| ImportError | Fix sys.path in WSGI |
| DB not found | migrate or check DATABASES |

## Local Pre-Deployment Tests
```
python manage.py check --deploy
python manage.py collectstatic --dry-run