FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir aiohttp playwright playwright-stealth && \
    playwright install chromium && \
    playwright install-deps chromium

COPY . .

CMD ["python3", "-u", "proxy.py"]
