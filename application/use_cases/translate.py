from domain.entities.transcript import Transcript
from domain.entities.subtitles import Subtitles
from domain.service.translate_service import TranslateService

#Use case for translating a transcript into subtitles, which utilizes the TranslateService to perform the translation and returns a 
#Subtitles object containing the output language and segments of text with their respective start and end times. 
class Translate:
    def __init__(self, translator: TranslateService):
        self.translator = translator

    def execute(self, transcript: Transcript, language_output: str) -> Subtitles:
        return self.translator.translate(transcript, language_output)