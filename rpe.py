import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import requests
from io import StringIO

# === REPLACE WITH YOUR GOOGLE SHEET INFO ===
# Option 1: Direct CSV export from public Google Sheet
# For Google Forms response sheets, try this URL format:
google_sheet_url = "https://docs.google.com/spreadsheets/d/1kSXC_tY9KbGYsRLiFdvpPOyLp0GAxxCECrdOwTEaNEM/export?format=csv"

# Option 2: Local CSV fallback (comment out the line above and uncomment below if needed)
# csv_path = "/Users/ericwnorowski/Downloads/CofC Men's Soccer RPE (Responses) - Form_Responses.csv"

# Output directories - choose one:
# Option A: Local Desktop (current)
output_dir = "/Users/ericwnorowski/Desktop"

# Option B: Dropbox/Google Drive/iCloud for sharing (uncomment and modify path)
# output_dir = "/Users/ericwnorowski/Dropbox/CofC_Soccer_RPE_Charts"  # Dropbox
# output_dir = "/Users/ericwnorowski/Google Drive/CofC_Soccer_RPE_Charts"  # Google Drive
# output_dir = "/Users/ericwnorowski/Library/Mobile Documents/com~apple~CloudDocs/CofC_Soccer_RPE_Charts"  # iCloud

# Ensure output directory exists
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Load and tidy the data
try:
    # Try to load from Google Sheet first using requests
    response = requests.get(google_sheet_url)
    response.raise_for_status()
    df = pd.read_csv(StringIO(response.text))
    print("✅ Data loaded from Google Sheet")
except Exception as e:
    print(f"❌ Could not load from Google Sheet: {e}")
    # Fallback to local file
    csv_path = "/Users/ericwnorowski/Downloads/CofC Men's Soccer RPE (Responses) - Form_Responses.csv"
    df = pd.read_csv(csv_path)
    print("✅ Data loaded from local CSV file")

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
# Create a sort key for proper chronological ordering (Morning comes before Afternoon)
df['sort_key'] = df['date'] + pd.to_timedelta(df['session_period'].map({'Morning': 0, 'Afternoon': 12}), unit='hours')
df = df.sort_values('sort_key')

# Get unique session keys in chronological order
session_order = df.drop_duplicates('session_key').sort_values('sort_key')['session_key'].tolist()

# Debug: Print the session keys to understand their format
print(f"Session keys found: {session_order}")

# Filter to first three sessions only
first_three_sessions = session_order[:3]
df_filtered = df[df['session_key'].isin(first_three_sessions)]

# Set up seaborn style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 1. Average RPE per session_key - vertical bar chart
plt.figure(figsize=(10, 6))
avg_rpe = df_filtered.groupby('session_key')['rpe'].mean()
# Reorder by chronological order
avg_rpe = avg_rpe.reindex(first_three_sessions)

bars1 = plt.bar(range(len(avg_rpe)), avg_rpe.values, color='skyblue', alpha=0.7)
plt.xlabel('Session')
plt.ylabel('Average RPE')
plt.title('Average RPE per Session')
plt.xticks(range(len(avg_rpe)), avg_rpe.index, rotation=45)
plt.ylim(0, 10)  # Set y-axis range from 0 to 10
plt.tight_layout()

# Save the average RPE chart
output_path = Path(output_dir) / "CofC_Mens_Soccer_RPE_avg.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()  # Close figure to free memory

# 2. Distribution of RPE responses per session - box plot or violin plot
plt.figure(figsize=(10, 6))

# Prepare data for box plot
session_data = []
session_labels = []
for session in first_three_sessions:
    session_rpe = df_filtered[df_filtered['session_key'] == session]['rpe']
    session_data.append(session_rpe)
    # Extract date and session period for clearer labeling
    session_parts = session.split(' – ')
    if len(session_parts) >= 2:
        date_part = session_parts[0]  # Get the date part (e.g., "2025-08-05")
        period_part = session_parts[1]  # Get the session period (e.g., "Morning")
    else:
        # Fallback if session format is different
        date_part = session.split()[0] if ' ' in session else session
        period_part = session.split()[-1] if ' ' in session else "Session"
    session_labels.append(f"{date_part}\n{period_part}")  # Combine with newline

# Create box plot showing distribution
box_plot = plt.boxplot(session_data, tick_labels=session_labels, patch_artist=True)

# Color the boxes
colors = ['lightblue', 'lightcoral', 'lightgreen']
for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

plt.xlabel('Session')
plt.ylabel('RPE Distribution')
plt.title('Distribution of RPE Responses per Session')
plt.ylim(0, 10)  # Set y-axis range from 0 to 10
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the distribution chart
output_path = Path(output_dir) / "CofC_Mens_Soccer_RPE_distribution.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()  # Close figure to free memory

# 3. Player dashboard - faceted chart with RPE vs session_key for first three sessions
players = df_filtered['player'].unique()

# Sort players by their jersey numbers
def extract_player_number(player_name):
    # Extract the number at the beginning of the player name
    try:
        return int(player_name.split()[0])
    except (ValueError, IndexError):
        return 999  # Put players without numbers at the end

players_sorted = sorted(players, key=extract_player_number)
n_players = len(players_sorted)
cols = 4  # Auto-wrap in 4 columns
rows = (n_players + cols - 1) // cols  # Calculate needed rows

fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 3))
if rows == 1:
    axes = axes.reshape(1, -1)
elif cols == 1:
    axes = axes.reshape(-1, 1)

# Flatten axes for easier iteration
axes_flat = axes.flatten()

for i, player in enumerate(players_sorted):
    ax = axes_flat[i]
    
    # Get player data for first three sessions
    player_data = df_filtered[df_filtered['player'] == player]
    
    # Create a complete dataset for this player (fill missing sessions with NaN)
    player_complete = []
    for session in first_three_sessions:
        session_data = player_data[player_data['session_key'] == session]
        if len(session_data) > 0:
            player_complete.append({'session_key': session, 'rpe': session_data['rpe'].iloc[0]})
        else:
            player_complete.append({'session_key': session, 'rpe': np.nan})
    
    player_df = pd.DataFrame(player_complete)
    
    # Plot line chart for this player
    valid_data = player_df.dropna()
    if len(valid_data) > 0:
        ax.plot(range(len(first_three_sessions)), player_df['rpe'], 'o-', linewidth=2, markersize=6)
        ax.set_ylim(0, 10)
    
    ax.set_title(player, fontsize=10, pad=10)
    ax.set_xlabel('Session', fontsize=8)
    ax.set_ylabel('RPE', fontsize=8)
    ax.set_xticks(range(len(first_three_sessions)))
    # Create safe labels for x-axis
    session_labels = []
    for s in first_three_sessions:
        parts = s.split(' – ')
        if len(parts) >= 2:
            session_labels.append(parts[1])  # Just the session period
        else:
            session_labels.append(s.split()[-1] if ' ' in s else s)
    ax.set_xticklabels(session_labels, rotation=45, fontsize=8)
    ax.grid(True, alpha=0.3)

# Hide unused subplots
for i in range(n_players, len(axes_flat)):
    axes_flat[i].set_visible(False)

plt.suptitle('Player RPE Dashboard - First Three Sessions', fontsize=14, y=0.98)
plt.tight_layout()

# Save the player dashboard
output_path = Path(output_dir) / "CofC_Mens_Soccer_RPE_players.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()  # Close figure to free memory

print(f"Charts saved to {output_dir}")
print(f"Sessions analyzed: {first_three_sessions}")
print(f"Total players: {n_players}")
print("Generated files: CofC_Mens_Soccer_RPE_avg.png, CofC_Mens_Soccer_RPE_distribution.png, CofC_Mens_Soccer_RPE_players.png")