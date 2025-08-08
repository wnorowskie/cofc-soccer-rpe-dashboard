#!/bin/bash

echo "🚀 CofC Soccer RPE Dashboard - Heroku Deployment Script"
echo "======================================================"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku
echo "🔐 Logging in to Heroku..."
heroku login

# Create app with unique name
APP_NAME="cofc-soccer-rpe-$(date +%Y%m%d)"
echo "📱 Creating Heroku app: $APP_NAME"

heroku create $APP_NAME

if [ $? -ne 0 ]; then
    echo "❌ App name taken. Trying with random suffix..."
    APP_NAME="cofc-soccer-rpe-$(date +%Y%m%d)-$(shuf -i 1000-9999 -n 1)"
    heroku create $APP_NAME
fi

# Deploy
echo "🚀 Deploying to Heroku..."
git push heroku master

# Open the app
echo "🌐 Opening your dashboard..."
heroku open

echo ""
echo "✅ Deployment complete!"
echo "📊 Your dashboard is now live at: https://$APP_NAME.herokuapp.com"
echo "🔗 Share this URL with your coaches!"
echo ""
echo "To update the app in the future:"
echo "1. Make changes to your files"
echo "2. git add ."
echo "3. git commit -m 'Your update message'"
echo "4. git push heroku master"
