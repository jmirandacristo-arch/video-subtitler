from dataclasses import dataclass

#Represents a segment of text with its start and end time in seconds.
@dataclass
class Segment:
    start : float
    end : float
    text : str