# Chainlit + Forge Agent Deployment Guide

Complete step-by-step guide for deploying your Chainlit application with WordPress integration.

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Local Testing](#local-testing)
4. [Deployment Options](#deployment-options)
5. [WordPress Configuration](#wordpress-configuration)
6. [Future: Adding Claude API](#future-adding-claude-api)
7. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    WordPress on WPEngine                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │   Page Template (page-chainlit.php)                   │  │
│  │   ┌───────────────────────────────────────────────┐   │  │
│  │   │         iframe embedding Chainlit UI          │   │  │
│  │   └───────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│        Chainlit + Forge Agent (Render/Railway)              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  app.py (Chainlit application)                        │  │
│  │    • User authentication                              │  │
│  │    • Session management                               │  │
│  │    • Message handling                                 │  │
│  │    • (Future) Claude API integration                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- WordPress can't run Python (WPEngine limitation)
- Chainlit must be deployed separately
- iframe embeds the Chainlit UI into WordPress
- CORS headers allow embedding from your domain

---

## ✅ Prerequisites

### Required
- ✅ GitHub account (for deployment)
- ✅ WPEngine WordPress hosting (you have this)
- ✅ Render.com or Railway.app account (both have free tiers)
- ✅ SFTP access to WordPress (you have this)

### For Future (when you get Claude API access)
- ⏳ Anthropic API key for Claude
- ⏳ Understanding of Claude API usage/costs

---

## 🧪 Local Testing

Before deploying, test everything locally:

### 1. Install Python Dependencies

```bash
cd chainlit-deployment
pip install -r requirements.txt
```

### 2. Create `.env` File

```bash
# Copy the example
cp .env.example .env

# Edit .env with your values
# For local testing, you don't need to change anything
```

### 3. Update Chainlit Config

Edit `.chainlit/config.toml`:
- Line 88: Change `your-wordpress-site.com` to your actual domain
- Line 99: Generate a random secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add this secret to `.env` as `CHAINLIT_AUTH_SECRET`

### 4. Run Locally

```bash
chainlit run app.py --port 8000
```

Visit http://localhost:8000 - you should see the login screen.

### 5. Test WordPress Integration

1. Make sure Chainlit is running on localhost:8000
2. Go to your local WordPress site
3. Create a new page with "Chainlit Interface" template
4. View the page - you should see the Chainlit interface embedded

---

## 🚀 Deployment Options

### Option A: Render.com (Recommended - Free Tier Available)

**Pros:** 
- Free tier with 750 hours/month
- Easy setup
- Good for testing

**Cons:** 
- Spins down after 15 minutes of inactivity (cold start = 30-60 seconds)
- Limited to 750 hours/month on free tier

#### Steps:

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Git Repository**
   ```bash
   cd chainlit-deployment
   git init
   git add .
   git commit -m "Initial commit"
   ```
   
   Push to GitHub (create a new repo first):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/chainlit-deployment.git
   git push -u origin main
   ```

3. **Deploy to Render**
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect Python and use the `render.yaml` config
   - Add environment variable: `CHAINLIT_AUTH_SECRET` (use the random string from earlier)
   - Click "Create Web Service"

4. **Wait for Deployment** (5-10 minutes)
   - Watch the logs for any errors
   - Once deployed, you'll get a URL like: `https://chainlit-deployment-xxxx.onrender.com`

5. **Test Your Deployment**
   - Visit the URL
   - You should see Chainlit login screen
   - Try logging in with any username/password (it's a demo auth for now)

---

### Option B: Railway.app (Better for Production)

**Pros:**
- More reliable (doesn't sleep)
- Good performance
- $5 free credit per month

**Cons:**
- After free credit, costs ~$5-10/month
- Requires payment method on file

#### Steps:

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Git Repository** (same as Render steps above)

3. **Deploy to Railway**
   - Go to Railway dashboard
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect settings from `railway.json`
   - Add environment variables in Railway dashboard:
     - `CHAINLIT_AUTH_SECRET`: Your random secret
     - `PORT`: 8000 (usually auto-set)

4. **Get Your URL**
   - Railway will generate a URL like: `https://chainlit-deployment.up.railway.app`
   - Or you can add a custom domain

5. **Test Your Deployment** (same as Render)

---

## 🔧 WordPress Configuration

### 1. Update Chainlit Production URL

**Via WordPress Admin:**
1. Log in to WordPress admin
2. Go to **Settings → Chainlit Settings**
3. Enter your deployed URL (e.g., `https://your-app.onrender.com`)
4. Click **Save Changes**

**Via SFTP (alternative):**
If you don't see the settings page, add this to `wp-config.php`:
```php
define('CHAINLIT_PRODUCTION_URL', 'https://your-app.onrender.com');
```

### 2. Update CORS in Chainlit Config

**IMPORTANT:** Your deployed Chainlit needs to allow embedding from WordPress.

Edit `chainlit-deployment/.chainlit/config.toml`:

```toml
[security]
allowed_origins = [
    "https://your-wordpress-site.wpengine.com",
    "https://www.your-wordpress-site.com",
    "http://localhost",  # Keep for local testing
]
```

**Then redeploy:**
```bash
git add .chainlit/config.toml
git commit -m "Update CORS for WordPress domain"
git push
```

Render/Railway will auto-redeploy.

### 3. Test Production Integration

1. Go to your WordPress site
2. Navigate to the Chainlit page
3. You should see the deployed Chainlit interface
4. Try logging in
5. Send a test message

---

## 🔮 Future: Adding Claude API

When you get access to Claude API:

### 1. Get API Key
- Sign up at https://console.anthropic.com
- Create an API key

### 2. Add to Environment Variables

**In Render/Railway:**
- Go to environment variables
- Add: `ANTHROPIC_API_KEY` = `your_api_key_here`

### 3. Update `app.py`

Uncomment the Claude integration code in `app.py`:

```python
# Uncomment this at the top
from anthropic import Anthropic

# Update process_message function
async def process_message(user_message: str, history: list, username: str) -> str:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Load Forge Agent system prompt
    forge_prompt_path = os.path.join(FORGE_AGENT_PATH, "CLAUDE.md")
    with open(forge_prompt_path, 'r') as f:
        system_prompt = f.read()
    
    # Call Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]
    )
    
    return response.content[0].text
```

### 4. Update `requirements.txt`

Uncomment:
```
anthropic>=0.18.0
```

### 5. Redeploy

```bash
git add .
git commit -m "Add Claude API integration"
git push
```

---

## 🔍 Troubleshooting

### Iframe Not Loading

**Symptom:** Blank iframe or "refused to connect" error

**Solutions:**
1. Check CORS settings in `.chainlit/config.toml`
2. Verify your WordPress domain is in `allowed_origins`
3. Check browser console for errors (F12)
4. Make sure Chainlit URL is HTTPS (not HTTP)

### Authentication Issues

**Symptom:** Can't log in, or auth keeps failing

**Solutions:**
1. Check `CHAINLIT_AUTH_SECRET` is set in deployment
2. Verify `.chainlit/config.toml` has `mode = "password"`
3. Clear browser cookies and try again

### Cold Start Delays (Render Free Tier)

**Symptom:** First load takes 30-60 seconds

**Solution:** This is normal for Render free tier. Options:
1. Upgrade to paid plan ($7/mo = always on)
2. Use Railway instead
3. Accept the delay (it's only on first load after 15min inactivity)

### WordPress Settings Page Not Showing

**Solutions:**
1. Make sure you uploaded the updated `functions.php`
2. Try deactivating and reactivating the theme
3. Check for PHP errors in WordPress debug log

### Chainlit Returns 404

**Solutions:**
1. Check deployment logs in Render/Railway
2. Verify `Procfile` is correct
3. Make sure `requirements.txt` has `chainlit>=1.0.0`

---

## 💰 Cost Breakdown

### Free Tier (Development/Testing)
- **Render Free:** $0/month (750 hours, sleeps after 15min)
- **Railway:** $5 credit/month (then pay-as-you-go)
- **WPEngine:** (you already have)
- **Total:** $0-5/month

### Paid Tier (Production)
- **Render Starter:** $7/month (always on)
- **Railway:** ~$5-10/month (usage-based)
- **Claude API:** ~$3-15/month (depends on usage)
- **Total:** $12-32/month

---

## 📝 Next Steps

1. ✅ Test locally (localhost:8000)
2. ✅ Deploy to Render (free tier)
3. ✅ Configure WordPress to use production URL
4. ✅ Test production integration
5. ⏳ When ready: Add Claude API
6. ⏳ When needed: Upgrade to paid tier

---

## 🆘 Need Help?

Common commands:

```bash
# Test locally
chainlit run app.py --port 8000

# Check Chainlit version
chainlit version

# Generate auth secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# View deployment logs (Railway)
railway logs

# View deployment logs (Render)
# Use the web dashboard
```

---

## 📚 Resources

- [Chainlit Documentation](https://docs.chainlit.io/)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [Anthropic Claude API](https://docs.anthropic.com/)
