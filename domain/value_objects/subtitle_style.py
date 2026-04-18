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
    font_color: str = "#FFFFFF"  # Blanco por defecto
    background_color: Optional[str] = None  # Sin fondo por defecto
    position: Position = Position.BOTTOM  # Posición del subtítulo (bottom, top, etc.)
    line_spacing: int = 4  # Espaciado entre líneas
    shadow: bool = True  # Sombra para mejorar la legibilidad