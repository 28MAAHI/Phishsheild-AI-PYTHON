# PhishShield - Vercel Deployment Guide

This document explains how to deploy the PhishShield application to Vercel.

## Prerequisites

1. A Vercel account (https://vercel.com)
2. Vercel CLI installed: `npm install -g vercel`
3. Git repository with the project

## Quick Start - Using Vercel UI

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Vercel configuration for deployment"
git push origin main
```

### 2. Deploy via Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Select your GitHub repository
4. Click "Import"
5. Under "Environment Variables", add the following variables:

```
FLASK_ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=3000
ENABLE_ZERO_SHOT=False
ENABLE_TRANSLATION=False
MAX_MESSAGE_CHARS=10000
FEEDBACK_DB_PATH=/tmp/feedback.db
```

6. Click "Deploy"

## Quick Start - Using Vercel CLI

```bash
# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

## Environment Variables

Configure these in your Vercel project settings or in `.env` file locally:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `DEBUG` | Debug mode | `False` |
| `ENABLE_ZERO_SHOT` | Enable zero-shot classification | `False` (disable on serverless) |
| `ENABLE_TRANSLATION` | Enable translation | `False` |
| `MAX_MESSAGE_CHARS` | Max message length | `10000` |
| `FEEDBACK_DB_PATH` | Database path | `/tmp/feedback.db` (must use /tmp for serverless) |
| `THREAT_INTEL_API_URL` | Threat intel API endpoint | (optional) |

## Important Notes for Serverless Deployment

### Database Path
On Vercel, the filesystem is ephemeral. Use `/tmp/` for temporary files:
```
FEEDBACK_DB_PATH=/tmp/feedback.db
```

### Memory & Timeout Limits
- Memory limit: 3008 MB (default)
- Function timeout: 60 seconds (default)

These are configured in `vercel.json`

### Large Files
The following files take up space - consider not committing large ML models:
- `spam_pipeline.joblib`
- `models/url_model.joblib`

You can:
1. Download these at runtime from a CDN/S3
2. Use a separate storage service
3. Commit them if under size limits

### Static Files
- Templates are in `/templates/`
- They are automatically served by Flask

## Troubleshooting

### "Module not found" errors
Make sure `requirements.txt` includes all dependencies:
```bash
pip freeze > requirements.txt
```

### Database errors
Ensure `FEEDBACK_DB_PATH` points to `/tmp/` on Vercel:
```
FEEDBACK_DB_PATH=/tmp/feedback.db
```

### Template not found
Templates must be in a `templates/` directory at the root level. Vercel will serve them correctly.

### Build fails
Check the Vercel logs:
1. Go to your Vercel project dashboard
2. Click on the failed deployment
3. Check the "Build" tab for error messages

### Cold start delays
First request to a serverless function can be slow. This is normal.

## Local Development

For local testing before deployment:

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

## Production Optimization Tips

1. **Disable Zero-Shot Model**: It's large and slow. Use rule-based fallback instead:
   ```
   ENABLE_ZERO_SHOT=False
   ```

2. **Disable Translation**: It makes network calls to Google Translate:
   ```
   ENABLE_TRANSLATION=False
   ```

3. **Use CDN for Static Assets**: Host large ML models in cloud storage

4. **Monitor Function Usage**: Check Vercel dashboard for CPU time, memory usage

## Redeploying

To redeploy after making changes:

```bash
# Using CLI
vercel --prod

# Changes are automatically detected and redeployed if connected to GitHub
```

## Support

For more information:
- Vercel Python Support: https://vercel.com/docs/runtimes/python
- Vercel Environment Variables: https://vercel.com/docs/environment-variables
- PhishShield README: See README.md in this directory
