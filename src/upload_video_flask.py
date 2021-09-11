import os
from flask import request
from src.init_soundtrack_adder import init_soundtrack_adder
from src.use_cases.upload_video.video_uploader import Video, VideoUploader
from src.use_cases.view_video_with_soundtrack.composition_src_loader import CompositionSrcLoader


def upload_video_flask():
    video = request.files.get('video'),
    n, extention = os.path.splitext(request.files.get('video').filename)
    raw_video_id = VideoUploader().upload_video(Video(
        binary=video[0],
        extension=extention[1:]
    ))
    composition_id = init_soundtrack_adder().add_soundtrack_to_video(raw_video_id)
    return CompositionSrcLoader().get_video_with_soundtrack(composition_id)

