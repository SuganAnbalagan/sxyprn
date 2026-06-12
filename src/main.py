from flask import Flask, jsonify, render_template
from flask_cors import CORS
from models import Video
from scraper import Scraper
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/videos', methods=['GET'])
def get_videos():
    scraper = Scraper()
    try:
        videos = scraper.scrape_videos("https://sxyprn.com")
        return jsonify({
            "status": "success",
            "count": len(videos),
            "videos": [video.__dict__ for video in videos]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/videos/<video_id>', methods=['GET'])
def get_video(video_id):
    scraper = Scraper()
    try:
        video_url = f"https://sxyprn.com/videos/{video_id}"
        videos = scraper.scrape_videos(video_url)
        if videos:
            return jsonify({
                "status": "success",
                "video": videos[0].__dict__
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Video not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": " error",
            "message": str(e)
        }), 500

if __name__ == 'app.py' == '__main__':
    app.run(host='0.00.0.0', port=5000, debug=True)