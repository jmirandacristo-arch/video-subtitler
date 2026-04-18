from domain.entities.video import Video
from domain.entities.subtitles import Subtitles
from domain.value_objects.subtitle_style import SubtitleStyle
from domain.service.insert_subtitles_service import InsertSubtitlesService

#Use case for inserting subtitles into a video, which utilizes the InsertSubtitlesService to perform the insertion and returns an updated Video object with the new subtitles.
class InsertSubtitles:
    def __init__(self, subtitle_inserter: InsertSubtitlesService):
        self.subtitle_inserter = subtitle_inserter

    def execute(self, video: Video, subtitles: Subtitles, subtitles_style: SubtitleStyle, output_path: str) -> Video:
        return self.subtitle_inserter.insert(video, subtitles, subtitles_style, output_path)