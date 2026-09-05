#!/bin/bash

# ==========================================
# 1. SETUP VNC PASSWORD
# ==========================================
mkdir -p ~/.vnc
if [ -n "$PASSWORD" ]; then
    echo "Setting up secure password..."
    echo "$PASSWORD" | vncpasswd -f > ~/.vnc/passwd
    chmod 600 ~/.vnc/passwd
    SEC_OPT="-SecurityTypes VncAuth -PasswordFile ~/.vnc/passwd"
else
    echo "Warning: No password set!"
    SEC_OPT="-SecurityTypes None"
fi

# ==========================================
# 2. START TIGERVNC (Xvnc)
# ==========================================
# TigerVNC combines the virtual display and VNC server in one stable process.
# Display :0 runs on port 5900 automatically.
echo "Starting TigerVNC Server..."
Xvnc :0 -geometry 1280x720 -depth 16 $SEC_OPT -localhost yes -BlacklistThreshold 0 -BlacklistTimeout 0 &
sleep 2

export DISPLAY=:0

# ==========================================
# 3. CREATE RAM CHECKER ON DESKTOP
# ==========================================
mkdir -p /root/Desktop
cat << 'RAMSCRIPT' > /root/check_ram.sh
#!/bin/bash
echo -e "\e[1;36m=========================================\e[0m"
echo -e "\e[1;33m  📊 REAL CLOUD PC RAM USAGE \e[0m"
echo -e "\e[1;36m=========================================\e[0m"

if [ -f /sys/fs/cgroup/memory.current ]; then
    USED=$(cat /sys/fs/cgroup/memory.current)
    MAX=$(cat /sys/fs/cgroup/memory.max)
    if [ "$MAX" = "max" ]; then MAX=$(awk '/MemTotal/ {printf "%d", $2 * 1024}' /proc/meminfo); fi
elif [ -f /sys/fs/cgroup/memory/memory.usage_in_bytes ]; then
    USED=$(cat /sys/fs/cgroup/memory/memory.usage_in_bytes)
    MAX=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes)
else
    USED=$(awk '/MemTotal/ {t=$2} /MemAvailable/ {a=$2; print (t-a)*1024}' /proc/meminfo)
    MAX=$(awk '/MemTotal/ {printf "%d", $2 * 1024}' /proc/meminfo)
fi

USED_MB=$((USED / 1024 / 1024))
MAX_MB=$((MAX / 1024 / 1024))
FREE_MB=$((MAX_MB - USED_MB))

echo -e "🟢 \e[1;32mTotal RAM Limit : ${MAX_MB} MB\e[0m"
echo -e "🔴 \e[1;31mUsed RAM        : ${USED_MB} MB\e[0m"
echo -e "🔵 \e[1;34mFree RAM        : ${FREE_MB} MB\e[0m"
echo -e "\e[1;36m=========================================\e[0m"
echo -e "\e[1;33m🔥 Top RAM Consuming Processes:\e[0m"
ps -eo pid,%mem,cmd --sort=-%mem | head -n 6 | awk 'NR==1 {print "   PID  %MEM  COMMAND"} NR>1 {printf " %5s  %5s  %s\n", $1, $2, substr($3, 1, 30)}'
echo -e "\e[1;36m=========================================\e[0m"
echo "Press ENTER to close..."
read
RAMSCRIPT

chmod +x /root/check_ram.sh

cat << 'DESKTOP' > /root/Desktop/Check_RAM.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Check Real RAM
Comment=Check real memory usage
Exec=lxterminal -e /root/check_ram.sh
Terminal=false
Icon=utilities-system-monitor
DESKTOP
chmod +x /root/Desktop/Check_RAM.desktop

# ==========================================
# 4. START DESKTOP & BROWSER
# ==========================================
echo "Starting LXDE Desktop Environment..."
startlxde &
sleep 2

echo "Launching Browser..."
chromium --no-sandbox \
         --disable-dev-shm-usage \
         --disable-gpu \
         --disable-software-rasterizer \
         --start-maximized \
         --touch-events=enabled \
         --incognito \
         --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
         &

# ==========================================
# 5. START WEBSOCKIFY (noVNC Bridge)
# ==========================================
echo "✅ Study Dashboard is Live on port 8080!"
exec websockify --web /usr/share/novnc 0.0.0.0:8080 localhost:5900
