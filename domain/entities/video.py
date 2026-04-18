from dataclasses import dataclass
from typing import Optional, List
from domain.entities.transcript import Transcript
from domain.entities.subtitles import Subtitles

#Represents a video entity, containing the source path, optional audio path, optional transcript, and optional subtitles.
@dataclass
class Video:
    source_path : str
    audio_path : Optional[str]
    transcript : Optional[Transcript]
    subtitles : Optional[Subtitles]