# Sxyprn Video Scraping App

A Flask API that scrapes videos from sxyprn.com and provides them as JSON data.

## Features
- Scrapes video titles, thumbnails, URLs, and metadata
- Provides RESTful API endpoints
- Docker-ready for easy deployment

## Installation
1. Clone this repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `python src/main.py`

## Deployment
This project is ready for deployment on Render using the provided render.yaml file.

## API Endpoints
- GET /api/videos - Get list of videos
- GET /api/videos/<video_id> - Get specific video details