FROM debian:bookworm-slim

WORKDIR /app

# Install LXDE (Lightweight Desktop), Xvfb, VNC, noVNC, Chromium
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    xvfb \
    x11vnc \
    lxde-core \
    lxterminal \
    novnc \
    websockify \
    chromium \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Fix index.html issue for Health Check
RUN cp /usr/share/novnc/vnc.html /usr/share/novnc/index.html 2>/dev/null || \
    cp /usr/share/novnc/vnc_lite.html /usr/share/novnc/index.html 2>/dev/null || true

RUN echo "OK" > /usr/share/novnc/healthz && \
    echo "OK" > /usr/share/novnc/health

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
