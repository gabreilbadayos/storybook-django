# Render 500 Error Fix - Storybook Django

## Current Status
✅ Deployed to https://storybook-django.onrender.com  
❌ 500 error: `No directory at: /opt/render/project/src/staticfiles/`

## Root Causes
1. **collectstatic failed** - staticfiles dir missing  
2. **gunicorn port** - render.yaml overrides Procfile ($PORT needed)
3. **Django 500** - Static middleware crashes

## Fix Plan (4 steps)
```
- [ ] 1. render.yaml - Fix startCommand: gunicorn --bind 0.0.0.0:$PORT
- [ ] 2. build.sh - mkdir staticfiles + collectstatic --noinput
- [ ] 3. git commit/push origin main (auto-redeploy)
- [ ] 4. ✅ Test site loads + check Render logs
```

## Expected Result
```
Static files: 200+
gunicorn[INFO]: Listening at: http://0.0.0.0:PORT
Site: https://storybook-django.onrender.com ✅
```

**Next**: Edit render.yaml (Step 1)