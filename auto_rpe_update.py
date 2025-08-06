#!/usr/bin/env python3
"""
Automated RPE Chart Generator
Runs the RPE visualization script every 10 minutes and uploads to shared storage.
"""

import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

def run_rpe_script():
    """Run the RPE visualization script"""
    try:
        # Change to the directory containing rpe.py
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Run the RPE script
        result = subprocess.run(['python3', 'rpe.py'], 
                              capture_output=True, text=True, check=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✅ RPE charts updated successfully")
        
        # Optional: Print any output from the script
        if result.stdout:
            print(f"Script output: {result.stdout.strip()}")
            
        return True
        
    except subprocess.CalledProcessError as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ❌ Error running RPE script: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ❌ Unexpected error: {e}")
        return False

def main():
    """Main loop - runs every 10 minutes"""
    print("🚀 Starting automated RPE chart generator...")
    print("📊 Charts will update every 10 minutes")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    # Run once immediately
    run_rpe_script()
    
    try:
        while True:
            # Wait 10 minutes (600 seconds)
            time.sleep(600)
            run_rpe_script()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping automated updates...")
        print("Charts will no longer update automatically.")

if __name__ == "__main__":
    main()
