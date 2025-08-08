#!/usr/bin/env python3
"""
CofC Men's Soccer RPE Dashboard Web App
On-demand RPE visualization for coaches
"""

from flask import Flask, render_template, send_file, jsonify
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import requests
from io import StringIO, BytesIO
import base64
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1kSXC_tY9KbGYsRLiFdvpPOyLp0GAxxCECrdOwTEaNEM/export?format=csv"

def load_data():
    """Load data from Google Sheet"""
    try:
        response = requests.get(GOOGLE_SHEET_URL, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        data_source = "Google Sheet"
    except Exception as e:
        print(f"Could not load from Google Sheet: {e}")
        raise Exception(f"Failed to load data from Google Sheet: {e}")
    
    # Rename columns to concise snake-case
    df = df.rename(columns={
        'Timestamp': 'timestamp',
        'Todays Date': 'date',
        'Morning or Afternoon Session': 'session_period',
        'Player Name': 'player',
        'What is your rate of perceived exertion?': 'rpe',
        'SessionKey': 'session_key'
    })
    
    # Convert date to datetime and sort by date + session_period
    df['date'] = pd.to_datetime(df['date'])
    df['sort_key'] = df['date'] + pd.to_timedelta(df['session_period'].map({'Morning': 0, 'Afternoon': 12}), unit='hours')
    df = df.sort_values('sort_key')
    
    return df, data_source

def generate_avg_chart(df_filtered, first_three_sessions):
    """Generate average RPE chart"""
    plt.figure(figsize=(10, 6))
    avg_rpe = df_filtered.groupby('session_key')['rpe'].mean()
    avg_rpe = avg_rpe.reindex(first_three_sessions)
    
    bars = plt.bar(range(len(avg_rpe)), avg_rpe.values, color='skyblue', alpha=0.7)
    plt.xlabel('Session')
    plt.ylabel('Average RPE')
    plt.title('Average RPE per Session')
    
    # Create clean labels without problematic characters
    clean_labels = []
    for session in first_three_sessions:
        # Replace problematic en-dash with regular dash and split
        clean_session = session.replace('â\x80\x93', '-').replace('–', '-')
        if ' - ' in clean_session:
            parts = clean_session.split(' - ')
            if len(parts) >= 2:
                date_part = parts[0].strip()
                period_part = parts[1].strip()
                clean_labels.append(f"{date_part}\\n{period_part}")
            else:
                clean_labels.append(clean_session)
        else:
            clean_labels.append(clean_session)
    
    plt.xticks(range(len(avg_rpe)), clean_labels, rotation=45)
    plt.ylim(0, 10)
    plt.tight_layout()
    
    # Convert to base64 string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_str

def generate_distribution_chart(df_filtered, first_three_sessions):
    """Generate distribution chart"""
    plt.figure(figsize=(10, 6))
    
    session_data = []
    session_labels = []
    for session in first_three_sessions:
        session_rpe = df_filtered[df_filtered['session_key'] == session]['rpe']
        session_data.append(session_rpe)
        
        # Clean the session key
        clean_session = session.replace('â\x80\x93', '-').replace('–', '-')
        if ' - ' in clean_session:
            parts = clean_session.split(' - ')
            if len(parts) >= 2:
                date_part = parts[0].strip()
                period_part = parts[1].strip()
                session_labels.append(f"{date_part}\\n{period_part}")
            else:
                session_labels.append(clean_session)
        else:
            session_labels.append(clean_session)
    
    box_plot = plt.boxplot(session_data, labels=session_labels, patch_artist=True)
    
    colors = ['lightblue', 'lightcoral', 'lightgreen']
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    plt.xlabel('Session')
    plt.ylabel('RPE Distribution')
    plt.title('Distribution of RPE Responses per Session')
    plt.ylim(0, 10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_str

def generate_player_dashboard(df_filtered, first_three_sessions):
    """Generate player dashboard"""
    players = df_filtered['player'].unique()
    
    def extract_player_number(player_name):
        try:
            return int(player_name.split()[0])
        except (ValueError, IndexError):
            return 999
    
    players_sorted = sorted(players, key=extract_player_number)
    n_players = len(players_sorted)
    cols = 4
    rows = (n_players + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 3))
    if rows == 1:
        axes = axes.reshape(1, -1)
    elif cols == 1:
        axes = axes.reshape(-1, 1)
    
    axes_flat = axes.flatten()
    
    for i, player in enumerate(players_sorted):
        ax = axes_flat[i]
        
        player_data = df_filtered[df_filtered['player'] == player]
        
        player_complete = []
        for session in first_three_sessions:
            session_data = player_data[player_data['session_key'] == session]
            if len(session_data) > 0:
                player_complete.append({'session_key': session, 'rpe': session_data['rpe'].iloc[0]})
            else:
                player_complete.append({'session_key': session, 'rpe': np.nan})
        
        player_df = pd.DataFrame(player_complete)
        
        valid_data = player_df.dropna()
        if len(valid_data) > 0:
            ax.plot(range(len(first_three_sessions)), player_df['rpe'], 'o-', linewidth=2, markersize=6)
            ax.set_ylim(0, 10)
        
        ax.set_title(player, fontsize=10, pad=10)
        ax.set_xlabel('Session', fontsize=8)
        ax.set_ylabel('RPE', fontsize=8)
        ax.set_xticks(range(len(first_three_sessions)))
        
        # Create clean session labels
        session_labels = []
        for s in first_three_sessions:
            clean_s = s.replace('â\x80\x93', '-').replace('–', '-')
            if ' - ' in clean_s:
                parts = clean_s.split(' - ')
                if len(parts) >= 2:
                    session_labels.append(parts[1].strip())  # Just the session period
                else:
                    session_labels.append(clean_s.split()[-1] if ' ' in clean_s else clean_s)
            else:
                session_labels.append(clean_s.split()[-1] if ' ' in clean_s else clean_s)
        ax.set_xticklabels(session_labels, rotation=45, fontsize=8)
        ax.grid(True, alpha=0.3)
    
    for i in range(n_players, len(axes_flat)):
        axes_flat[i].set_visible(False)
    
    plt.suptitle('Player RPE Dashboard - First Three Sessions', fontsize=14, y=0.98)
    plt.tight_layout()
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_str

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        # Load fresh data
        df, data_source = load_data()
        
        # Get session data
        session_order = df.drop_duplicates('session_key').sort_values('sort_key')['session_key'].tolist()
        first_three_sessions = session_order[:3]
        df_filtered = df[df['session_key'].isin(first_three_sessions)]
        
        # Generate charts
        avg_chart = generate_avg_chart(df_filtered, first_three_sessions)
        dist_chart = generate_distribution_chart(df_filtered, first_three_sessions)
        player_chart = generate_player_dashboard(df_filtered, first_three_sessions)
        
        # Get stats
        total_players = len(df_filtered['player'].unique())
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return render_template('dashboard.html',
                             avg_chart=avg_chart,
                             dist_chart=dist_chart,
                             player_chart=player_chart,
                             sessions=first_three_sessions,
                             sessions_json=str(first_three_sessions),
                             total_players=total_players,
                             data_source=data_source,
                             last_updated=last_updated)
    
    except Exception as e:
        return f"Error generating dashboard: {str(e)}", 500

@app.route('/api/refresh')
def refresh_data():
    """API endpoint to check if new data is available"""
    try:
        df, data_source = load_data()
        session_count = len(df['session_key'].dropna().unique())
        player_count = len(df['player'].unique())
        
        return jsonify({
            'status': 'success',
            'data_source': data_source,
            'session_count': session_count,
            'player_count': player_count,
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Starting CofC Men's Soccer RPE Dashboard")
    print("📊 Access the dashboard at: http://localhost:5000")
    print("🔄 Charts update automatically when you refresh the page")
    
    # Use PORT environment variable provided by Heroku, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
