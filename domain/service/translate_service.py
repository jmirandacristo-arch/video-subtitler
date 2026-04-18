from abc import ABC, abstractmethod
from domain.entities.transcript import Transcript
from domain.entities.subtitles import Subtitles

#Defines an abstract base class for the TranslateService, which specifies the interface for translating a transcript into subtitles in a specified output language.
class TranslateService(ABC):
    @abstractmethod
    def translate(self, transcript: Transcript, language_output: str) -> Subtitles:
        pass