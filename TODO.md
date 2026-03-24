# PythonAnywhere Deployment TODO

Updated: 2024 - PA deployment preparation complete

## Code Preparation ✅
- [x] `.env.example` updated with PA vars
- [x] `DEPLOY_PYTHONANYWHERE.md` created with complete step-by-step guide
- [ ] `storybook_project/settings.py` - review ALLOWED_HOSTS=env('ALLOWED_HOSTS', '*.pythonanywhere.com')
- [ ] Move legacy files: render.yaml, Procfile.railway, railway.json → legacy/

## Local Pre-Deployment Tests (Run these)
```
python manage.py check --deploy
python manage.py collectstatic --dry-run --noinput
```

## PythonAnywhere Steps (Follow DEPLOY_PYTHONANYWHERE.md)
1. [ ] Create PA account
2. [ ] Git clone to ~/storybook
3. [ ] Setup virtualenv & pip install
4. [ ] Configure web app & WSGI
5. [ ] Set env vars (SECRET_KEY, ALLOWED_HOSTS)
6. [ ] `migrate`, `collectstatic`, reload
7. [ ] Test site & admin

**Your system is now PA-ready!** Use `DEPLOY_PYTHONANYWHERE.md` guide. Provide PA username if you want me to customize further.

## Next (if needed)
- Settings.py tweaks
- Legacy file cleanup