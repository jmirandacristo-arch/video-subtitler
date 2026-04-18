from domain.entities.video import Video
from domain.entities.subtitles import Subtitles
from domain.value_objects.subtitle_style import SubtitleStyle
from domain.service.insert_subtitles_service import InsertSubtitlesService
import srt
import os
import tempfile
import ffmpeg
from datetime import timedelta
import re

#Implements the InsertSubtitlesService interface to provide functionality for inserting subtitles into a video file using ffmpeg. 
#The insert method takes a Video object, a Subtitles object, a SubtitleStyle object, and an output path, converts the subtitles into SRT format, 
#and uses ffmpeg to overlay the subtitles onto the video according to the specified style. The updated Video object 
#with the new source path is returned after the subtitles have been successfully inserted.

def hex_to_ass(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
    return f"{b}{g}{r}"


def rgba_to_hex(rgba_str):
    if not rgba_str:
        return "#ffffff"
    match = re.match(r'rgba?\((\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*)', rgba_str)
    if match:
        r, g, b = int(float(match.group(1))), int(float(match.group(2))), int(float(match.group(3)))
        return f"#{r:02x}{g:02x}{b:02x}"
    return rgba_str



class InsertSubtitlesServiceImpl(InsertSubtitlesService):
     def insert(self, video: Video, subtitles: Subtitles, subtitles_style: SubtitleStyle, output_path: str) -> Video:
            subtitles_list = []
            for segment in subtitles.segments:
                subtitles_list.append(srt.Subtitle(index=len(subtitles_list)+1, start=timedelta(seconds=segment.start), end=timedelta(seconds=segment.end), content=segment.text))
            
            subtitles_srt = srt.compose(subtitles_list)
            

            with tempfile.NamedTemporaryFile(mode='w+t',encoding='utf-8', delete=False, suffix='.srt') as subtitles_temp:
                
                subtitles_temp.write(subtitles_srt)
                temp_path = subtitles_temp.name
                temp_path_escaped = temp_path.replace("\\", "/").replace("C:","C\\:")
            os.makedirs(output_path, exist_ok=True)
            output_file = os.path.join(output_path, f"{os.path.splitext(os.path.basename(video.source_path))[0]}_subtitled.mp4")

           

            probe = ffmpeg.probe(video.source_path)
            video_stream = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
            width = int(video_stream["width"])
            height = int(video_stream["height"])
            base_dim = min(width, height)
            font_size_small = max(6,int(base_dim * 0.015))
            font_size_medium = max(8,int(base_dim * 0.020))
            font_size_large = max(10,int(base_dim * 0.025))

            

            position_map = {"Bottom": 2, "Top": 8, "Middle": 5}
            font_size_map = {"Small": font_size_small, "Medium": font_size_medium, "Large": font_size_large}
            vf_filter = (
                    f"subtitles='{temp_path_escaped}':force_style="
                    f"'FontSize={font_size_map.get(subtitles_style.font_size, 24)},"
                    f"FontName={subtitles_style.font_family},"
                    f"BackColour=&H{hex_to_ass(rgba_to_hex(subtitles_style.background_color)) if subtitles_style.background_color else '00000000'},"
                    f"PrimaryColour=&H{hex_to_ass(rgba_to_hex(subtitles_style.font_color))},"
                    f"Alignment={position_map.get(subtitles_style.position, 2)},"
                    f"LineSpacing={subtitles_style.line_spacing},"
                    f"Shadow={1 if subtitles_style.shadow else 0}'"
            )
                       
            ffmpeg.input(video.source_path).output(output_file, vf=vf_filter, vcodec="libx264", acodec="aac", strict="-2").run(overwrite_output=True)
            video.source_path = output_file
            os.remove(temp_path)
    
            return video