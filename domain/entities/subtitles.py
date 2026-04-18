from dataclasses import dataclass
from typing import List
from domain.entities.segments import Segment

#Represents a collection of subtitles, each with its own language and segments of text.
@dataclass
class Subtitles:
    language_output : str
    segments : List[Segment]