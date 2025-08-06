# CofC Men's Soccer RPE Dashboard - Heroku Deployment Guide

## 🚀 Quick Deployment to Heroku

### Prerequisites
1. Create a free Heroku account at https://signup.heroku.com/
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
3. Install Git if not already installed

### Deployment Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Initialize Git Repository** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit - CofC Soccer RPE Dashboard"
   ```

3. **Create Heroku App**
   ```bash
   heroku create cofc-soccer-rpe-dashboard
   ```
   Note: App name must be unique. If taken, try: cofc-soccer-rpe-2025, cofc-rpe-dashboard, etc.

4. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```
   (Use `git push heroku master` if your default branch is master)

5. **Open Your App**
   ```bash
   heroku open
   ```

### 📱 Accessing the Dashboard

Once deployed, your dashboard will be available at:
`https://your-app-name.herokuapp.com`

### 🔧 Files Included for Deployment

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku process configuration
- `runtime.txt` - Python version specification
- `templates/dashboard.html` - Web interface template

### 🔄 Updating the App

To deploy changes:
```bash
git add .
git commit -m "Description of changes"
git push heroku main
```

### 📊 Features

- Real-time data from Google Sheets
- Mobile-responsive design
- Three visualization types:
  - Average RPE per session
  - RPE distribution (box plots)
  - Individual player dashboard
- Auto-refresh capability
- Clean, professional charts

### 🆓 Free Tier Limitations

Heroku free tier includes:
- 550-1000 dyno hours per month
- App sleeps after 30 minutes of inactivity
- Takes ~10-15 seconds to wake up from sleep

### 🔗 Sharing with Coaches

Once deployed, share the URL with coaches:
`https://your-app-name.herokuapp.com`

They can bookmark it and access real-time RPE data anytime.

### 🛠️ Troubleshooting

If deployment fails:
1. Check the logs: `heroku logs --tail`
2. Verify all files are committed: `git status`
3. Ensure Google Sheet is publicly accessible

### 📈 Data Source

The app pulls data directly from your Google Sheet:
https://docs.google.com/spreadsheets/d/1kSXC_tY9KbGYsRLiFdvpPOyLp0GAxxCECrdOwTEaNEM/export?format=csv

Make sure this sheet remains publicly accessible for the app to work.
