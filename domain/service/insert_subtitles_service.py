from abc import ABC, abstractmethod
from domain.entities.video import Video
from domain.entities.subtitles import Subtitles
from domain.value_objects.subtitle_style import SubtitleStyle

#Defines an abstract base class for the InsertSubtitlesService, which specifies the interface for inserting subtitles into a video.
class InsertSubtitlesService(ABC):
    @abstractmethod
    def insert(self, video: Video, subtitles: Subtitles, subtitles_style: SubtitleStyle, output_path: str) -> Video:
        pass