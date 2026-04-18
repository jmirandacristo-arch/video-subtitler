import srt
from datetime import timedelta
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
import textwrap

# Configuración
VIDEO_INPUT = "traduciendo.mp4"
SRT_FILE = "subtitulos.srt"
LANG_ORIG = "en"
LANG_TARGET = "es"
MODEL_SIZE = "medium"

def transcribe_video(video_path):
    print("Transcribiendo video...")
    model = WhisperModel(MODEL_SIZE, compute_type="int8")
    segments, _ = model.transcribe(video_path, beam_size=5)
    return list(segments)

def translate_text(text):
    try:
        return GoogleTranslator(source=LANG_ORIG, target=LANG_TARGET).translate(text)
    except Exception as e:
        print("Error en traducción:", e)
        return "[Error en traducción]"

def generate_translated_srt(segments, srt_path):
    print("Traduciendo y generando subtítulos...")
    subs = []
    for i, seg in enumerate(segments):
        start = timedelta(seconds=seg.start)
        end = timedelta(seconds=seg.end)
        original_text = seg.text.strip()
        translated_text = translate_text(original_text)
        wrapped_text = "\n".join(textwrap.wrap(translated_text, width=40))
        subs.append(srt.Subtitle(index=i + 1, start=start, end=end, content=wrapped_text))
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))
    print(f"Archivo SRT generado: {srt_path}")

if __name__ == "__main__":
    segments = transcribe_video(VIDEO_INPUT)
    generate_translated_srt(segments, SRT_FILE)
