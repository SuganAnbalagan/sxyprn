FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 777 /app

COPY src/ ./src/

EXPOSE 5000

CMD ["python", "src/main.py"]
