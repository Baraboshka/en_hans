"""Flask App
Тут инициализируется Flask приложение.
"""

from flask import Flask

from src.upload_video_flask import upload_video_flask

app = Flask(__name__)

# ROUTES


@app.route('/upload-video', methods=['POST'])
def upload_video():
    return upload_video_flask()

# @app.route('/video-with-soundtrack', methods=['GET'])
# def get_video_with_soundtrack():
#     return get_video_with_soundtrack_flask()
