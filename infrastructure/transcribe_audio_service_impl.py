from domain.entities.transcript import Transcript
from domain.service.transcribe_audio_service import TranscribeAudioService
from faster_whisper import WhisperModel
from domain.entities.segments import Segment

#Implements the TranscribeAudioService interface to provide functionality for transcribing audio from a video file using the WhisperModel from the faster_whisper library. 
#The transcribe method takes the path to an audio file, uses the WhisperModel to transcribe the audio, and returns a Transcript object containing the language and segments of text 
#with their respective start and end times. Each segment is created as a Segment object with the start time, end time, and transcribed text. 
#The language of the transcript is also extracted from the WhisperModel's output and included in the Transcript object.

def word_to_segments(words, max_chars=40, max_lines=2):
    segments = []
    current_text = ""
    current_start = None
    current_end = None
    line_count = 0

    for word in words:
        if current_start is None:
            current_start = word.start
        
        if len(current_text) + len(word.word) + 1 > max_chars or line_count >= max_lines:
            segments.append(Segment(start=current_start, end=current_end, text=current_text.strip()))
            current_text = ""
            current_start = word.start
            line_count = 0
        
        current_text += " " + word.word
        current_end = word.end

        if word.word.endswith(('.', '!', '?')):
            line_count += 1

    if current_text:
        segments.append(Segment(start=current_start, end=current_end, text=current_text.strip()))

    return segments
    


class TranscribeAudioServiceImpl(TranscribeAudioService):
    def __init__(self):
        self.model = WhisperModel("medium", compute_type="int8")
    def transcribe(self, audio_path: str) -> Transcript:
        whisper_segments, language = self.model.transcribe(audio_path,beam_size=5, word_timestamps=True)
        
        segments = []
        for s in whisper_segments:
            if not s.text.strip():
                continue    
            processed_segments = word_to_segments(s.words, max_chars=40, max_lines=2)
            segments.extend(processed_segments)

        return Transcript(segments=segments, language= language.language)
        
        
        

        

