from abc import ABC, abstractmethod
from domain.entities.transcript import Transcript


#Defines an abstract base class for the TranscribeAudioService, which specifies the interface for transcribing audio into text, 
#returning a Transcript object containing the language and segments of text with their respective start and end times.   
class TranscribeAudioService(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> Transcript:
        pass