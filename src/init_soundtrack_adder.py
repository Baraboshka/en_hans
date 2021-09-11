import os
from src.music_generator import MubertMusicGenerator
from src.use_cases.add_soundtrack_to_video.soundtrack_adder import SoundtrackAdder

class EmotionRecognizerMock:
    def get_video_emotion(self, video):
        return 'thoughtful'

class PlaylistSuggesterMock:
    def suggest_playlist(self, emotion):
        return '0.0.1'

class AudioAttatcherMock():
    def generate_music(self):
        os.path.abspath('sample.mp4')

def init_soundtrack_adder():
    return SoundtrackAdder(
        emotion_recognizer=EmotionRecognizerMock(),
        playlist_suggester=PlaylistSuggesterMock(),
        music_generator=MubertMusicGenerator(),
        audio_attacher=AudioAttatcherMock(),
    )
