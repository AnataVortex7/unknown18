#!/bin/bash

# ==========================================
# 1. SETUP VNC PASSWORD
# ==========================================
mkdir -p ~/.vnc
if [ -n "$PASSWORD" ]; then
    echo "Setting up secure password..."
    echo "$PASSWORD" | vncpasswd -f > $HOME/.vnc/passwd
    chmod 600 $HOME/.vnc/passwd
    
    if [ -s $HOME/.vnc/passwd ]; then
        SEC_OPT="-SecurityTypes VncAuth -PasswordFile $HOME/.vnc/passwd"
    else
        echo "❌ WARNING: Password must be at least 6 characters! Disabling password..."
        SEC_OPT="-SecurityTypes None"
    fi
else
    echo "Warning: No password set!"
    SEC_OPT="-SecurityTypes None"
fi

# ==========================================
# 2. START TIGERVNC (Xvnc)
# ==========================================
echo "Starting TigerVNC Server..."
Xvnc :0 -geometry 1280x720 -depth 16 $SEC_OPT -localhost yes -BlacklistThreshold 0 -BlacklistTimeout 0 &
sleep 2

export DISPLAY=:0

# ==========================================
# 3. CREATE SYSTEM MONITOR ON DESKTOP
# ==========================================
mkdir -p /root/Desktop
cat << 'SYSSCRIPT' > /root/check_system.sh
#!/bin/bash
echo -e "\e[1;36m=========================================\e[0m"
echo -e "\e[1;33m 🖥️  REAL CLOUD PC SPECIFICATIONS \e[0m"
echo -e "\e[1;36m=========================================\e[0m"

# --- RAM Calculation ---
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

# --- CPU Calculation ---
if [ -f /sys/fs/cgroup/cpu.max ]; then
    CPU_QUOTA=$(awk '{print $1}' /sys/fs/cgroup/cpu.max)
    CPU_PERIOD=$(awk '{print $2}' /sys/fs/cgroup/cpu.max)
    if [ "$CPU_QUOTA" != "max" ]; then
        CPU_CORES=$(awk -v q="$CPU_QUOTA" -v p="$CPU_PERIOD" 'BEGIN { printf "%.2f", q/p }')
    else
        CPU_CORES=$(nproc)
    fi
elif [ -f /sys/fs/cgroup/cpu/cpu.cfs_quota_us ]; then
    CPU_QUOTA=$(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us)
    CPU_PERIOD=$(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us)
    if [ "$CPU_QUOTA" != "-1" ]; then
        CPU_CORES=$(awk -v q="$CPU_QUOTA" -v p="$CPU_PERIOD" 'BEGIN { printf "%.2f", q/p }')
    else
        CPU_CORES=$(nproc)
    fi
else
    CPU_CORES=$(nproc)
fi

# --- Disk Calculation (Personal Files only) ---
USER_DISK=$(du -shc /root /tmp /home 2>/dev/null | grep total | awk '{print $1}')

echo -e "🟢 \e[1;32mTotal RAM Limit : ${MAX_MB} MB\e[0m"
echo -e "🔴 \e[1;31mUsed RAM        : ${USED_MB} MB\e[0m"
echo -e "🔵 \e[1;34mFree RAM        : ${FREE_MB} MB\e[0m"
echo -e "\e[1;36m-----------------------------------------\e[0m"
echo -e "⚙️  \e[1;33mReal CPU Limit  : ${CPU_CORES} vCPU\e[0m"
echo -e "📂 \e[1;35mDownloaded Data : ${USER_DISK} (Personal)\e[0m"
echo -e "\e[1;36m=========================================\e[0m"
echo -e "\e[1;33m🔥 Top RAM Consuming Processes:\e[0m"
ps -eo pid,%mem,cmd --sort=-%mem | head -n 6 | awk 'NR==1 {print "   PID  %MEM  COMMAND"} NR>1 {printf " %5s  %5s  %s\n", $1, $2, substr($3, 1, 30)}'
echo -e "\e[1;36m=========================================\e[0m"
echo "Press ENTER to close..."
read
SYSSCRIPT

chmod +x /root/check_system.sh

rm -f /root/Desktop/Check_RAM.desktop

cat << 'DESKTOP' > /root/Desktop/System_Monitor.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Real System Monitor
Comment=Check real Cloud PC Specs
Exec=lxterminal -e /root/check_system.sh
Terminal=false
Icon=utilities-system-monitor
DESKTOP
chmod +x /root/Desktop/System_Monitor.desktop

# ==========================================
# 4. START DESKTOP & BROWSER
# ==========================================
echo "Starting LXDE Desktop Environment..."
startlxde &
sleep 2

echo "Launching Firefox Browser (Bot Bypass Mode)..."
firefox-esr --private-window &

# ==========================================
# 5. START WEBSOCKIFY (noVNC Bridge)
# ==========================================
echo "✅ Command Center is Live on port 8080!"
exec websockify --web /app/webroot 0.0.0.0:8080 127.0.0.1:5900
