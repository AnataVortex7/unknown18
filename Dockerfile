FROM debian:bullseye-slim

WORKDIR /app

# Install Xvfb, VNC, Window Manager, noVNC, and Chromium (Midori removed)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    xvfb \
    x11vnc \
    openbox \
    novnc \
    websockify \
    chromium \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up noVNC default index page
RUN ln -sf /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# Copy start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port for Koyeb (8080)
EXPOSE 8080

CMD ["/app/start.sh"]
