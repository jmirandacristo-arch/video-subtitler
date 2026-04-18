from dataclasses import dataclass
from typing import Optional
from enum import Enum


#Represents the position of subtitles on the screen.
class Position(Enum):
    BOTTOM = "bottom"
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"

#Represents the style of subtitles, including font size, font family, colors, position, line spacing, and shadow.
@dataclass
class SubtitleStyle:
    font_size: int = 24
    font_family: str = "Arial"
    font_color: str = "#FFFFFF"  
    background_color: Optional[str] = None  
    position: Position = Position.BOTTOM  
    line_spacing: int = 4  
    shadow: bool = True 