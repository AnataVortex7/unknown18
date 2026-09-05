FROM debian:bookworm-slim

WORKDIR /app

# Just install basic tools so Docker builds in 2 seconds
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl procps && \
    rm -rf /var/lib/apt/lists/*

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
