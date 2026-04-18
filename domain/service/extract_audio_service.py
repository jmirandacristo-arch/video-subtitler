from abc import ABC, abstractmethod
from domain.entities.video import Video


#Defines an abstract base class for the ExtractAudioService, which specifies the interface for extracting audio from a video.
class ExtractAudioService(ABC):
    @abstractmethod
    def extract(self, video: Video, output_path: str) -> Video:
        pass