from domain.entities.video import Video
from domain.service.extract_audio_service import ExtractAudioService


#Use case for extracting audio from a video, which utilizes the ExtractAudioService to perform the extraction and returns an updated Video object with the extracted audio path.
class ExtractAudio:
    def __init__(self, audio_extractor: ExtractAudioService):
        self.audio_extractor = audio_extractor

    def execute(self, video:Video, output_path: str)-> Video:
        return self.audio_extractor.extract(video, output_path)
        