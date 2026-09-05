FROM debian:bookworm-slim

WORKDIR /app

# Install all packages during build
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

# Fix the 404 error by ensuring index.html exists, and create health check files
RUN cp /usr/share/novnc/vnc.html /usr/share/novnc/index.html 2>/dev/null || \
    cp /usr/share/novnc/vnc_lite.html /usr/share/novnc/index.html 2>/dev/null || true

RUN echo "OK" > /usr/share/novnc/healthz && \
    echo "OK" > /usr/share/novnc/health

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
