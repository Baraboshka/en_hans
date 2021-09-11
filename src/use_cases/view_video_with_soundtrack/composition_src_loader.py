from db import engine


class CompositionSrcLoader():
    def __init__(self):
        pass

    def get_video_with_soundtrack(self, composition_id: str):
        extention = self._get_extention(composition_id)
        return f'https://storage.cloud.google.com/en-hans/with_music/{composition_id}.{extention}.'

    def _get_extention(self, composition_id: str):
        return engine.execute(f"""
            SELECT `extention`
            FROM `raw_video`
            INNER JOIN `soundtrack` USING (`raw_video_id`)
            WHERE `soundtrack_id` = {composition_id}""").scalar()
