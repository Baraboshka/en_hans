import re
import tempfile
from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip

import requests
from db import engine
from src.init_bucket import init_bucket


class SoundtrackAdder:
    def __init__(self, emotion_recognizer, playlist_suggester, music_generator, audio_attacher):
        self.bucket = init_bucket()
        self.composition_id = None
        self.extension = None
        self.video_clip = None
        self.emotion_recognizer = emotion_recognizer
        self.playlist_suggester = playlist_suggester
        self.music_generator = music_generator
        self.audio_attacher = audio_attacher

    def add_soundtrack_to_video(self, raw_video_id: str):
        self.raw_video_id = raw_video_id
        self.extension = self._get_extension()
        self._download_video()
        emotion = self._get_video_emotion()
        self._generate_music(emotion)
        self._attach_music_to_video()
        self._create_new_soundtrack_record()
        self._upload_video_with_music()
        return self.composition_id

    def _download_video(self):
        blob = self.bucket.blob(self._get_video_filename())
        blob.download_to_filename(self._raw_video_temp_filename)

    def _get_video_emotion(self):
        with open(self._raw_video_temp_filename) as video:
            return self.emotion_recognizer.get_video_emotion(video)

    def _generate_music(self, emotion):
        playlist = self.playlist_suggester.suggest_playlist(emotion)
        length = self._get_video_length()
        music_url = self.music_generator.generate_music(playlist, length)
        with open(self._music_temp_filename, 'wb') as music_file:
            music_file.write(self._download_music(music_url))
    
    def _download_music(self, music_url):
        return requests.get(music_url).content

    def _attach_music_to_video(self):
        music_clip = AudioFileClip(self._music_temp_filename)
        composite_audio = CompositeAudioClip([self.video_clip.audio, music_clip]) if self.video_clip.audio else music_clip
        self.video_clip.set_audio(composite_audio)
        self.video_clip.write_videofile(self._composition_temp_filename)

    def _create_new_soundtrack_record(self):
        engine.execute(f'INSERT INTO `soundtrack` (`raw_video_id`) VALUES ("{self.raw_video_id}")')
        composition_id = engine.execute('SELECT LAST_INSERT_ID()').scalar()
        self.composition_id = str(composition_id)

    def _upload_video_with_music(self):
        with open(self._composition_temp_filename) as composition_file:
            extension = self.extension
            blob = self.bucket.blob(f'with_music/{self.composition_id}.{extension}')
            blob.upload_from_file(composition_file)

    def _get_video_length(self):
        self.video_clip = VideoFileClip(self._raw_video_temp_filename)
        return self.video_clip.duration

    def _get_video_filename(self):
        extension = self.extension
        return f'raw/{self.raw_video_id}.{extension}'
    
    def _get_extension(self):
        return engine.execute(f"""
            SELECT `extension`
            FROM `raw_video`
            WHERE `raw_video_id` = {self.raw_video_id}""").scalar()

    @property
    def _raw_video_temp_filename(self):
        return f'/Users/adamgolota/en_hans_video-{self.raw_video_id}.{self.extension}'

    @property
    def _music_temp_filename(self):
        return f'/Users/adamgolota/en_hans_music-{self.raw_video_id}.mp3'

    @property
    def _composition_temp_filename(self):
        return f'/Users/adamgolota/en_hans_composition-{self.raw_video_id}.{self.extension}'
