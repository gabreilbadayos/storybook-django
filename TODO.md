# TODO: Fix Render "No open HTTP ports detected" error

## Plan Steps:
- [x] Update render.yaml startCommand with --bind 0.0.0.0:$PORT
- [ ] Update storybook_project/settings.py: ALLOWED_HOSTS='*', enable STATICFILES_STORAGE, fix DATABASES for DATABASE_URL (partial: dj_database_url import added)
- [ ] Confirm story_book/wsgi.py exists and correct (confirmed OK)
- [ ] Create/update .env.example for Render vars
- [ ] git checkout -b blackboxai/fix-render-port (done)
- [ ] git add/commit/push changes
- [ ] Create PR via gh pr create

Current progress tracked here.