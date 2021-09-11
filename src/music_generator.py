import requests
import time
import math

from keys import MUBERT_PAT

class MubertMusicGenerator:
    def generate_music(self, channel, duration):
        res = requests.post('https://api-b2b.mubert.com/v2/RecordTrack', json={
            "method":"RecordTrack",
            "params": {
                "pat": MUBERT_PAT,
                "playlist":"0.2.3", "duration": math.ceil(duration),
                "format":"mp3", "intensity":"medium",
                "bitrate":"32",
                "mode":"track"
            }
        })
        return res.json()['data']['tasks'][0]['download_link']
