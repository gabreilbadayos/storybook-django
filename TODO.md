# PythonAnywhere Deployment TODO

## [x] Project Setup (Local)
- [x] Git push to `blackboxai/fix-render-port`
- [x] settings.py production config (Whitenoise, security)
- [x] settings_sqlite.py for PA free account
- [x] .env.example, DEPLOY_PYTHONANYWHERE.md

## [x] PythonAnywhere Setup
- [x] Clone repo: `git clone https://github.com/gabreil/storybook.git ~/storybook`
- [x] Virtualenv: `mkvirtualenv --python=/usr/bin/python3.10 storybook`
- [x] Install deps: `pip install -r requirements.txt`
- [x] Upload db.sqlite3 via Files tab
- [x] Migrate: `python manage.py migrate`
- [x] Superuser: `python manage.py createsuperuser`
- [x] Collectstatic: `python manage.py collectstatic --noinput`

## [ ] Fix Logout Redirect
- [ ] Edit `storybook_project/settings.py`: Add `LOGOUT_REDIRECT_URL = '/'`
- [ ] git add/commit/push
- [ ] PA: `cd ~/storybook && git pull`
- [ ] Reload web app: `touch /var/www/gabreil_pythonanywhere_com_wsgi.py`

## [ ] Test
- [ ] Login/logout → home page (not admin)
- [ ] Story viewer, flipbook works
- [ ] Night mode, animations