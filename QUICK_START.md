# Quick Start - Deploy to Vercel in 5 Minutes

## Prerequisites
- GitHub account with your repo
- Vercel account (https://vercel.com)

## Step 1: Prepare Your Code (2 min)

All files are already created! Just verify:
```bash
# Check these files exist:
ls vercel.json          # ✓ Main config
ls api/index.py         # ✓ Serverless handler
ls runtime.txt          # ✓ Python version
```

## Step 2: Push to GitHub (1 min)

```bash
cd c:\Users\Dell\OneDrive\Desktop\PhishShield-no-thread-feed\Phishsheild-AI-main\PHISHSHIELD-X-Explainable-Multilingual-AI-for-Scam-and-Phishing-Detection-main

git init
git add .
git commit -m "Add Vercel deployment configuration"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 3: Deploy to Vercel (2 min)

### Option A: Via CLI (Fastest)
```bash
npm install -g vercel
vercel login
vercel --prod
```

### Option B: Via Dashboard
1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Select your GitHub repository
4. Click "Deploy"
5. Done! ✓

## Step 4: Verify Deployment

After deployment completes:

1. Visit your deployed URL (shown in dashboard)
2. Test: Paste a suspicious message and click "Analyze"
3. Verify results appear correctly

## That's It! 🎉

Your PhishShield app is now live on Vercel!

---

## If Something Goes Wrong

### Build fails?
Check the deployment logs:
1. Go to Vercel dashboard
2. Click on the failed deployment
3. Check the "Build" tab for error messages

### App crashes after deploy?
Check the function logs:
1. Go to Vercel dashboard
2. Click on the project
3. Go to "Functions" tab
4. Check the logs

### Need to rollback?
```bash
vercel rollback
```

---

## Quick Fixes

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` locally first |
| "Template not found" | Ensure `templates/` folder exists at root |
| Database permission error | Already configured to use `/tmp/` |
| Out of memory | Disable zero-shot: `PHISHSHIELD_ENABLE_ZERO_SHOT=False` |

---

## Configuration (Optional)

To customize environment variables in Vercel:

1. Go to Project Settings → Environment Variables
2. Add/modify any of these:
   ```
   PHISHSHIELD_FEEDBACK_DB=/tmp/phishshield_feedback.db
   PHISHSHIELD_ENABLE_ZERO_SHOT=False
   PHISHSHIELD_ENABLE_TRANSLATION=False
   PHISHSHIELD_MAX_MESSAGE_CHARS=10000
   ```
3. Redeploy from dashboard

---

## More Information

- **Full deployment guide**: See `VERCEL_DEPLOY.md`
- **Checklist before deploy**: See `DEPLOYMENT_CHECKLIST.md`
- **What was fixed**: See `VERCEL_FIXES_SUMMARY.md`
- **Test your setup**: Run `python test_deployment.py`

---

**Need help?**
- Vercel Support: https://vercel.com/support
- Check `DEPLOYMENT_CHECKLIST.md` for common issues
