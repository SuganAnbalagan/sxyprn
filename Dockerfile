FROM python:3.11-slim

# Set Playwright to install and look for browsers in a globally accessible directory
ENV PLAYWRIGHT_BROWSERS_PATH=/app/.cache/ms-playwright

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-install the modern font dependencies, then install chromium browser only
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    fonts-unifont \
    && playwright install chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure the container runtime user has full read/write access to the application directory
RUN chmod -R 777 /app

COPY src/ ./src/

EXPOSE 5000

CMD ["python", "src/main.py"]
