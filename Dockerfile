FROM python:3.11-slim

# Set Playwright to install and look for browsers in a globally accessible directory
ENV PLAYWRIGHT_BROWSERS_PATH=/app/.cache/ms-playwright

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install all mandatory system libraries for headless Chromium execution
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    libgobject-2.0-0 \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libexpat1 \
    libxcb1 \
    libxkbcommon0 \
    libatspi0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && playwright install chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure the container runtime user has full read/write access to the application directory
RUN chmod -R 777 /app

COPY src/ ./src/

EXPOSE 5000

CMD ["python", "src/main.py"]
