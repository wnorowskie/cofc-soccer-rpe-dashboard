# CofC Men's Soccer RPE Dashboard 🏆⚽

A real-time web dashboard for visualizing Rate of Perceived Exertion (RPE) data for the College of Charleston Men's Soccer team. Pulls data directly from Google Forms/Sheets and provides interactive visualizations for coaches.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-green) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-lightblue) ![Heroku](https://img.shields.io/badge/Deploy-Heroku-purple)

## 🎯 Features

- **Real-time Data**: Automatically pulls latest RPE responses from Google Sheets
- **Three Visualization Types**:
  - Average RPE per training session
  - RPE distribution (box plots) showing team variance
  - Individual player dashboard with session-by-session tracking
- **Mobile Responsive**: Works perfectly on phones, tablets, and computers
- **Auto-refresh**: Updates data in real-time when coaches access the dashboard
- **Clean Design**: Professional charts suitable for sharing with staff

## 🚀 Quick Start

### Option 1: Deploy to Heroku (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-username/cofc-soccer-rpe-dashboard.git
cd cofc-soccer-rpe-dashboard

# Run the automated deployment script
./deploy.sh
```

### Option 2: Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Start the web app
python app.py

# Access at http://localhost:5000
```

## 📊 Data Source

The dashboard connects to your Google Form responses sheet. Make sure your Google Sheet is publicly accessible and contains these columns:

- Timestamp
- Todays Date (MM/DD/YYYY)
- Morning or Afternoon Session
- Player Name
- What is your rate of perceived exertion? (1-10 scale)
- SessionKey (auto-generated)

## 🔧 Configuration

Update the Google Sheet URL in `app.py`:
```python
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"
```

## 📁 Project Structure

```
cofc-soccer-rpe-dashboard/
├── app.py                 # Main Flask web application
├── rpe.py                 # Standalone chart generation script
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version specification
├── templates/
│   └── dashboard.html    # Web interface template
├── deploy.sh             # Automated deployment script
├── DEPLOYMENT_GUIDE.md   # Detailed deployment instructions
└── README.md            # This file
```

## 🌐 Deployment Options

### Heroku (Free Tier)
- ✅ Free hosting
- ✅ Automatic HTTPS
- ✅ Easy domain sharing
- ✅ Automatic deployments

### Railway/Render
- ✅ Alternative free hosting platforms
- ✅ Similar setup process

### Local Network
- ✅ Run locally and share on WiFi
- ✅ Good for same-location access

## 📱 For Coaches

Once deployed, coaches can:
1. Bookmark the dashboard URL
2. Access real-time RPE data from any device
3. View clean, professional visualizations
4. Share charts in team meetings
5. Track player workload trends over time

## 🔄 Updating Data

The dashboard automatically:
- Pulls fresh data every time it's accessed
- Handles new players and sessions automatically
- Sorts data chronologically
- Cleans and formats display labels

## 🛠️ Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `python app.py`
5. Submit a pull request

### Local Development
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debug mode
export FLASK_DEBUG=1
python app.py
```

## 📊 Chart Types

### 1. Average RPE Chart
- Shows team average RPE for each training session
- Vertical bar chart with session dates
- Helps track overall team fatigue trends

### 2. Distribution Chart
- Box plots showing RPE spread for each session
- Visualizes player response variance
- Identifies sessions with high/low consensus

### 3. Player Dashboard
- Individual player RPE tracking
- Faceted view with one chart per player
- Shows personal trends over sessions

## 🎨 Customization

The dashboard uses Seaborn and Matplotlib for visualizations. You can customize:
- Color schemes in the chart generation functions
- Chart layouts and sizes
- Display formatting and labels

## 🔐 Security

- No sensitive data is stored locally
- Google Sheets must be publicly accessible (read-only)
- No authentication required for viewing dashboards
- Suitable for sharing with coaching staff

## 📈 Analytics

Track usage and performance:
- Monitor Heroku app logs for access patterns
- Google Sheets provides form response analytics
- No user data is collected by the dashboard

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional chart types
- Player comparison features
- Historical data analysis
- Export functionality
- Mobile app development

## 📞 Support

For issues or questions:
1. Check the [Deployment Guide](DEPLOYMENT_GUIDE.md)
2. Review Heroku logs: `heroku logs --tail`
3. Verify Google Sheet accessibility
4. Open an issue on GitHub

## 📄 License

MIT License - Feel free to use and modify for your team's needs.

---

**Built for College of Charleston Men's Soccer** ⚽

*Helping coaches make data-driven decisions about player workload and recovery.*
