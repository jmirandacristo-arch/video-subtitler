from domain.service.extract_audio_service import ExtractAudioService
from domain.entities.video import Video
import os
import subprocess
import ffmpeg
import logging

logger = logging.getLogger(__name__)

#Implements the ExtractAudioService interface to provide functionality for extracting audio from a video file using ffmpeg. 
#The extract method takes a Video object and an output path, extracts the audio from the video, saves it as an mp3 file in the specified output path, 
#updates the Video object with the new audio path, and returns the updated Video object. If any errors occur during the extraction process, they are caught and printed, and the exception is re-raised.    
class ExtractAudioServiceImpl(ExtractAudioService):
   
    def extract(self, video: Video, output_path: str) -> Video:
        try:
            # Use ffmpeg to extract audio from the video
            input_video = ffmpeg.input(video.source_path)
            os.makedirs(output_path, exist_ok=True)
            audio_output = os.path.join(output_path, f"{os.path.splitext(os.path.basename(video.source_path))[0]}.mp3")
            ffmpeg.output(input_video.audio, audio_output).run(overwrite_output=True)
            video.audio_path = audio_output
            return video
        except FileNotFoundError as e:
            logger.error(f"Video file not found: {e}")
            raise
        
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise