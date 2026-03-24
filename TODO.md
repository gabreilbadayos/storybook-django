# Deployment TODO - Story Book Django App to GitHub + Render

## [ ] 1. Fix Admin 404 Error
- Add `LOGIN_REDIRECT_URL = '/admin/'` to `story_book/settings.py`
- Test locally: `python manage.py runserver`, login at /admin/

## [x] 2. Git Status Checked
- Modified: settings.py, storybook_app/urls.py, views.py, story_viewer.html  
- Untracked: templates/registration/profile.html

## [ ] 3. Commit Changes
```bash
git add .
git commit -m "Fix admin login 404 + app improvements"
git push origin main
```

## [ ] 4. Render Deployment
- Ensure Render service linked to GitHub repo
- Render auto-deploys on push
- Set env vars: SECRET_KEY, DATABASE_URL (Render Postgres)
- Run migrations on Render

## [ ] 5. Verify Deploy
- Check Render logs
- Test /admin/ login
- Test story viewer, create story

**Next step: Fix settings.py**