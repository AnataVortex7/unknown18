FROM python:3.10-slim

WORKDIR /app

# Install curl and tailscale
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://tailscale.com/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# Pre-install proxy dependencies to save startup time & memory
RUN pip install --no-cache-dir aiohttp playwright playwright-stealth && \
    playwright install chromium && \
    playwright install-deps chromium

# Copy files
COPY . .

# Ensure start script is executable
RUN chmod +x start.sh

# Run only the start script
CMD ["./start.sh"]
