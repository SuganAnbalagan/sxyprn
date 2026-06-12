FROM python:3.11-slim

# Set Playwright to install and look for browsers in a globally accessible directory
ENV PLAYWRIGHT_BROWSERS_PATH=/app/.cache/ms-playwright

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies and browser binaries into the custom path
RUN apt-get update && apt-get install -y wget gnupg && \
    playwright install --with-deps chromium && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure the container runtime user has full read/write access to the application directory
RUN chmod -R 777 /app

COPY src/ ./src/
COPY templates/ ./templates/

EXPOSE 5000

CMD ["python", "src/main.py"]
