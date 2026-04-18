from dataclasses import dataclass
from typing import List
from domain.entities.segments import Segment

#Represents a transcript of audio, containing the language and segments of text with their respective start and end times.
@dataclass    
class Transcript:
    language : str
    segments : List[Segment]
