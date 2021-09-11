from dataclasses import dataclass
from typing import BinaryIO

from src.init_bucket import init_bucket
from db import engine


@dataclass
class Video:
    binary: BinaryIO
    extension: str

class VideoUploader:
    def __init__(self):
        self.bucket = init_bucket()
        self.video = None

    def upload_video(self, video: Video):
        self.video = video
        raw_video_id = self._create_raw_video_record()
        blob = self.bucket.blob(f'raw/{raw_video_id}.{self.video.extension}')
        blob.upload_from_file(self.video.binary)
        return raw_video_id

    def _create_raw_video_record(self):
        engine.execute(f'INSERT INTO `raw_video` (`extension`) VALUES ("{self.video.extension}")')
        video_id = engine.execute('SELECT LAST_INSERT_ID()').scalar()
        return str(video_id)
