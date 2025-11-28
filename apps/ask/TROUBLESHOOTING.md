# Troubleshooting Render Deployment

## Common Build Failures

### Issue: Build fails with "Exited with status 1"

**Cause:** The full `requirements.txt` includes heavy ML dependencies (PyTorch, etc.) that:
- Take too long to install
- May not be compatible with Render's build environment
- Are not needed for the API server

**Solution:** Use `requirements-api.txt` instead, which only includes minimal API dependencies.

**In Render:**
1. Go to Settings → Build & Deploy
2. Change Build Command to: `pip install -r requirements-api.txt`
3. Save and redeploy

### Issue: Module not found errors

**Cause:** Missing `__init__.py` files or incorrect import paths

**Solution:** Ensure all Python packages have `__init__.py` files:
- `api/__init__.py` (if needed)
- `api/routes/__init__.py` ✓ (exists)
- `api/services/__init__.py` ✓ (exists)

### Issue: Port binding errors

**Cause:** Not using `$PORT` environment variable

**Solution:** Ensure start command uses `$PORT`:
```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### Issue: CORS errors

**Cause:** Frontend URL not in CORS_ORIGINS

**Solution:** Add your Vercel URL to CORS_ORIGINS environment variable:
```
CORS_ORIGINS=https://ask.kvshvl.in,https://www.ask.kvshvl.in,https://your-vercel-url.vercel.app
```

## Build Command Options

### Option 1: Minimal API Dependencies (Recommended)
```bash
pip install -r requirements-api.txt
```
- Fast build time (~30 seconds)
- Only installs what's needed for API
- Reliable on Render

### Option 2: Full Dependencies (Not Recommended)
```bash
pip install -r requirements.txt
```
- Slow build time (5+ minutes)
- Includes PyTorch, ML libraries
- May fail on Render
- Only needed if you're running content generation on Render

## Quick Fix for Current Deployment

1. **Update Build Command in Render:**
   - Settings → Build & Deploy
   - Build Command: `pip install -r requirements-api.txt`
   - Save

2. **Verify Start Command:**
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

3. **Redeploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

## Checking Build Logs

In Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. Look for error messages
4. Common errors:
   - `ModuleNotFoundError` → Missing dependency or wrong import
   - `Port already in use` → Wrong start command
   - `No module named 'api'` → Missing `__init__.py` or wrong path

## Verification Steps

After successful deployment:

1. **Check Health Endpoint:**
   ```
   https://ask-backend-gxhy.onrender.com/health
   ```
   Should return: `{"status": "healthy", ...}`

2. **Check Root Endpoint:**
   ```
   https://ask-backend-gxhy.onrender.com/
   ```
   Should return: `{"message": "ASK Research Tool API", ...}`

3. **Check API Endpoint:**
   ```
   https://ask-backend-gxhy.onrender.com/api/stats
   ```
   Should return statistics JSON

## Still Having Issues?

1. Check Render logs for specific error messages
2. Verify all files are committed to GitHub (monorepo: `kushalsamant.github.io`)
3. Ensure `apps/ask/api/` directory structure is correct
4. Verify Root Directory in Render is set to `apps/ask`
5. Check that shared-backend package is installed (from monorepo `packages/shared-backend`)
6. Test locally first: `cd apps/ask/api && uvicorn main:app --reload`

