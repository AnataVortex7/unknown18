FROM debian:bookworm-slim

WORKDIR /app

# Install TigerVNC, LXDE, noVNC, and Browsers
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tigervnc-standalone-server \
    lxde-core \
    lxterminal \
    novnc \
    websockify \
    chromium \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create a foolproof index.html that auto-redirects to vnc.html and auto-connects
RUN echo '<html><head><meta http-equiv="refresh" content="0; url=vnc.html?autoconnect=true&resize=remote" /></head><body>Redirecting to Desktop...</body></html>' > /usr/share/novnc/index.html

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
