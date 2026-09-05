#!/bin/bash

# Start tailscaled in userspace networking mode
echo "Starting Tailscale..."
tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &
sleep 5

# Connect to Tailscale network
if [ -n "$TAILSCALE_AUTHKEY" ]; then
    echo "Connecting to Tailscale..."
    tailscale up --authkey="${TAILSCALE_AUTHKEY}" --hostname=proxy-app
else
    echo "Warning: TAILSCALE_AUTHKEY is not set."
fi

# Start the python app in unbuffered mode so logs go directly to stdout
echo "Starting proxy.py..."
exec python3 -u proxy.py
