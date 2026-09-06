FROM debian:bookworm-slim

WORKDIR /app

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

RUN mkdir -p /app/webroot/study && \
    cp -r /usr/share/novnc/* /app/webroot/study/ && \
    echo '<html><body>System Active</body></html>' > /app/webroot/index.html && \
    echo '<html><body>Monitor OK</body></html>' > /app/webroot/vnc.html && \
    echo '<html><head><meta http-equiv="refresh" content="0; url=vnc.html?autoconnect=true&resize=remote" /></head><body>Redirecting...</body></html>' > /app/webroot/study/index.html

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

COPY trackpad_patch.py /app/trackpad_patch.py
RUN python3 /app/trackpad_patch.py /app/webroot/study/vnc.html

EXPOSE 8080

CMD ["/app/start.sh"]
