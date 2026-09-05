FROM debian:bookworm-slim

WORKDIR /app

# Install all packages during build (Bookworm repo is fresh, no 404 errors)
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

# Stealth Mode: Rename 'noVNC' to 'Study Dashboard'
RUN ln -sf /usr/share/novnc/vnc.html /usr/share/novnc/index.html && \
    sed -i 's/noVNC/Study Dashboard/g' /usr/share/novnc/index.html && \
    sed -i 's/noVNC/Study Dashboard/g' /usr/share/novnc/vnc.html

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
