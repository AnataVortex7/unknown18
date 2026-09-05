#!/bin/bash

export DISPLAY=:99

echo "⏳ Starting Study Core..."
Xvfb :99 -screen 0 1280x720x16 -nolisten tcp &
sleep 2

echo "Starting LXDE Desktop Environment..."
# Start the full desktop environment instead of just openbox
startlxde &
sleep 2

echo "Launching Research Browser..."
chromium --no-sandbox \
         --disable-dev-shm-usage \
         --disable-gpu \
         --disable-software-rasterizer \
         --start-maximized \
         --touch-events=enabled \
         --incognito \
         --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
         &

echo "Securing Connection..."
if [ -n "$PASSWORD" ]; then
    mkdir -p ~/.vnc
    rm -f ~/.vnc/passwd
    x11vnc -storepasswd "$PASSWORD" ~/.vnc/passwd
    x11vnc -display :99 -rfbauth ~/.vnc/passwd -rfbport 5900 -forever -shared -quiet &
else
    x11vnc -display :99 -nopw -rfbport 5900 -forever -shared -quiet &
fi

sleep 2

# Check if VNC actually started
if ! pgrep -x "x11vnc" > /dev/null
then
    echo "❌ ERROR: VNC Server failed to start!"
    x11vnc -display :99 -nopw -rfbport 5900 &
fi

echo "✅ Study Dashboard is Live on port 8080!"
exec websockify --web /usr/share/novnc 0.0.0.0:8080 localhost:5900
