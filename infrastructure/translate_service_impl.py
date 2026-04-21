from domain.entities.transcript import Transcript
from domain.entities.subtitles import Subtitles
from domain.service.translate_service import TranslateService
from deep_translator import GoogleTranslator
from domain.entities.segments import Segment
import logging

logger = logging.getLogger(__name__)

#Implements the TranslateService interface to provide functionality for translating a transcript into subtitles in a specified output language using 
#the GoogleTranslator from the deep_translator library. The translate method takes a Transcript object and a target language, 
#translates each segment of text in the transcript to the target language, and returns a Subtitles object containing the translated segments and the output language.
#Each translated segment is created as a Segment object with the same start and end times as the original segment, but with the text translated to the target language.   
class TranslateServiceImpl(TranslateService):
    
    def translate(self, transcript: Transcript, target_language: str) -> Subtitles:
        try:
            segments_translated = []
            for segment in transcript.segments:
                translated_text = GoogleTranslator(source="auto", target=target_language).translate(segment.text)
                segments_translated.append(Segment(start=segment.start, end=segment.end, text=translated_text))
            return Subtitles(segments=segments_translated, language_output=target_language)
        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            raise