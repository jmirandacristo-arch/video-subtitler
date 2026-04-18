from domain.entities.transcript import Transcript
from domain.service.transcribe_audio_service import TranscribeAudioService
from domain.entities.video import Video


#Use case for transcribing audio from a video, which utilizes the TranscribeAudioService to perform the transcription and returns a 
#Transcript object containing the language and segments of text with their respective start and end times.   
class TranscribeAudio:
    def __init__(self, transcriber: TranscribeAudioService):
        self.transcriber = transcriber
    def execute(self, video: Video) -> Transcript:
        return self.transcriber.transcribe(video.audio_path)