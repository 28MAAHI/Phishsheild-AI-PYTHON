# PhishShield Vercel Deployment Checklist

Before deploying to Vercel, ensure all these items are checked:

## Pre-Deployment Setup

- [ ] Python 3.11+ is installed locally
- [ ] All dependencies in `requirements.txt` can be installed without errors
- [ ] `.env.example` is present as a template
- [ ] `.gitignore` includes `__pycache__`, `.env`, `*.db`, etc.
- [ ] `vercel.json` exists with proper configuration
- [ ] `runtime.txt` specifies Python version
- [ ] `api/index.py` exists and exports the Flask app correctly

## Code Quality

- [ ] No hardcoded API keys or secrets in the code
- [ ] `app.py` properly handles the `if __name__ == "__main__"` guard
- [ ] Templates are in `templates/` directory (not `app/templates/`)
- [ ] Static files (CSS, JS) are properly referenced with Flask's `url_for()`
- [ ] No localhost-specific URLs in code

## Configuration for Serverless

- [ ] `PHISHSHIELD_FEEDBACK_DB` is set to `/tmp/phishshield_feedback.db`
- [ ] `PHISHSHIELD_ENABLE_ZERO_SHOT` is `False` (large model not suitable for serverless)
- [ ] `PHISHSHIELD_ENABLE_TRANSLATION` is `False` (network calls not ideal)
- [ ] All required model files (`spam_pipeline.joblib`, `models/url_model.joblib`) are committed
- [ ] Large ML models are under Vercel's size limits

## Repository Setup

- [ ] Git is initialized: `git init`
- [ ] Files are staged: `git add .`
- [ ] Initial commit is created: `git commit -m "Initial commit"`
- [ ] Repository is pushed to GitHub

## Vercel Project Setup

### Option A: Via Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Option B: Via Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure environment variables (see below)
5. Click "Deploy"

## Environment Variables to Set in Vercel

Go to Project Settings → Environment Variables and add:

```
FLASK_ENV=production
FLASK_DEBUG=False
PYTHONUNBUFFERED=1
PHISHSHIELD_FEEDBACK_DB=/tmp/phishshield_feedback.db
PHISHSHIELD_ENABLE_ZERO_SHOT=False
PHISHSHIELD_ENABLE_TRANSLATION=False
PHISHSHIELD_MAX_MESSAGE_CHARS=10000
```

Optional (if using threat intelligence):
```
THREAT_INTEL_API_URL=https://your-api.com
THREAT_INTEL_API_KEY=your-api-key
```

## Post-Deployment Verification

- [ ] Deployment completed successfully (no build errors)
- [ ] Visit the deployed URL and see the home page
- [ ] Test message analysis with a simple example
- [ ] Test URL analysis functionality
- [ ] Check Vercel dashboard for any runtime errors
- [ ] Monitor the Functions logs in Vercel dashboard

## Troubleshooting Common Issues

### Build Fails: "Module not found"
- Check that all packages in `requirements.txt` are compatible with Python 3.11
- Run locally: `pip install -r requirements.txt`

### Templates not found
- Ensure `templates/` directory is at project root
- Check that Flask app uses `render_template("index.html")` (not with paths)

### Database permission errors
- Ensure `PHISHSHIELD_FEEDBACK_DB` uses `/tmp/` path
- Vercel filesystem outside `/tmp/` is read-only

### Memory/Timeout errors
- Disable zero-shot model: `PHISHSHIELD_ENABLE_ZERO_SHOT=False`
- Reduce message size limit if needed
- Check function memory in `vercel.json` (currently 3008 MB)

### "Static file not found"
- Check that CSS/JS files are in correct directories
- Use Flask's `url_for()` for all asset references
- Avoid hardcoded paths like `/static/file.css`

## Size Optimization

If deployment exceeds limits, you can:

1. Remove large ML models and fetch them at runtime:
   ```python
   # In app.py
   if not os.path.exists('spam_pipeline.joblib'):
       download_from_cdn()
   ```

2. Increase function memory in `vercel.json`:
   ```json
   "functions": {
     "api/**/*.py": {
       "memory": 3008,
       "maxDuration": 60
     }
   }
   ```

3. Use a simpler requirements.txt:
   ```bash
   cp requirements-vercel.txt requirements.txt
   ```

## Monitoring

After deployment, monitor via Vercel Dashboard:
- **Functions**: View logs and performance
- **Deployments**: Track deployment history
- **Analytics**: Monitor usage and errors
- **Usage**: Check CPU time, memory usage

## Rollback

If something goes wrong:
```bash
vercel rollback
```

Or via dashboard: Deployments → Select previous version → Promote to Production

## Performance Tips

1. **Minimize cold starts**: Keep dependencies lightweight
2. **Cache responses**: Add cache headers in vercel.json
3. **Async operations**: Use async/await for I/O operations
4. **Monitor logs**: Check Vercel Functions logs for slow requests

## Security Checklist

- [ ] No hardcoded secrets in code
- [ ] All secrets set via environment variables in Vercel
- [ ] HTTPS is enabled (automatic on Vercel)
- [ ] CORS headers properly configured if needed
- [ ] Input validation is in place
- [ ] Rate limiting considered for API endpoints

---

**Need Help?**
- Vercel Docs: https://vercel.com/docs
- PhishShield Repo: Check README.md
- Vercel Support: https://vercel.com/support
