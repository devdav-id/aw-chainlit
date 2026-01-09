# Chainlit Deployment - Quick Start

This folder contains everything needed to deploy your Chainlit + Forge Agent application.

## 🚀 Quick Start

### Local Testing
```bash
cd chainlit-deployment
pip install -r requirements.txt
chainlit run app.py --port 8000
```

### Deploy to Render (Free)
1. Push this folder to GitHub
2. Connect to Render.com
3. Deploy using `render.yaml`
4. Set `CHAINLIT_AUTH_SECRET` environment variable
5. Get your URL and configure in WordPress

## 📁 Files

- `app.py` - Main Chainlit application with auth & session management
- `.chainlit/config.toml` - Chainlit configuration (CORS, auth, UI)
- `requirements.txt` - Python dependencies
- `render.yaml` - Render.com deployment config
- `railway.json` - Railway.app deployment config
- `Procfile` - Process configuration for deployment
- `.env.example` - Environment variables template
- `DEPLOYMENT.md` - **Complete step-by-step deployment guide**

## 📖 Full Documentation

**Read [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions** including:
- Architecture explanation
- Local testing guide
- Render & Railway deployment steps
- WordPress integration
- Troubleshooting
- Cost breakdown
- Future Claude API integration

## ⚠️ Before Deploying

1. Update `.chainlit/config.toml`:
   - Replace `your-wordpress-site.com` with your actual domain
   - Generate and set auth secret

2. Test locally first

3. Choose deployment platform:
   - **Render** = Free tier, good for testing (sleeps after 15min)
   - **Railway** = Better for production (~$5-10/month)

## 🔑 Environment Variables Needed

```
CHAINLIT_AUTH_SECRET=<random_secret_here>
ENABLE_AUTH=true
FORGE_AGENT_PATH=../forge-agent-main
```

Generate secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📞 WordPress Integration

After deploying:
1. Go to WordPress admin → Settings → Chainlit Settings
2. Enter your deployed URL (e.g., `https://your-app.onrender.com`)
3. Save settings
4. Visit your Chainlit page - should now show deployed version

## 💡 Current Status

- ✅ Basic Chainlit app with authentication
- ✅ Session management & user context
- ✅ WordPress iframe integration
- ⏳ Claude API integration (waiting for API access)
- ⏳ Forge Agent integration (needs Claude API)

## 🆘 Quick Troubleshooting

**Iframe not loading?**
→ Check CORS in `.chainlit/config.toml`

**Authentication not working?**
→ Verify `CHAINLIT_AUTH_SECRET` is set

**Render app sleeping?**
→ Normal on free tier. Upgrade or use Railway.

For more help, see [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section.
