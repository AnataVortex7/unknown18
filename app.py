import os
import subprocess
import time

print("Starting Virtual Desktop Initialization...")

# Execute the start.sh script directly
script_path = "./start.sh"
if os.path.exists(script_path):
    os.chmod(script_path, 0o755)
    
    # Run the setup script in background
    process = subprocess.Popen(script_path, shell=True)
    
    print("Desktop started successfully! It is running on port 8080.")
    
    # Keep the python script alive
    while True:
        time.sleep(3600)
else:
    print(f"Error: {script_path} not found!")
