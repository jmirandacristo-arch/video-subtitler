import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from domain.entities.transcript import Transcript
from domain.entities.subtitles import Subtitles
from domain.entities.segments import Segment
from domain.entities.video import Video
from domain.value_objects.subtitle_style import SubtitleStyle  
from application.use_cases.extract_audio import ExtractAudio
from application.use_cases.transcribe_audio import TranscribeAudio
from application.use_cases.translate import Translate 
from application.use_cases.insert_subtitles import InsertSubtitles
from infrastructure.extract_audio_service_impl import ExtractAudioServiceImpl
from infrastructure.transcribe_audio_service_impl import TranscribeAudioServiceImpl
from infrastructure.translate_service_impl import TranslateServiceImpl
from infrastructure.insert_subtitles_service_impl import InsertSubtitlesServiceImpl



def extract_audio(video):
    video = Video(source_path=video, audio_path=None, transcript=None, subtitles=None)
    extract_audio_service = ExtractAudioServiceImpl()
    extract_audio = ExtractAudio(extract_audio_service)
    audio = extract_audio.execute(video, "output")

    transcribe_audio_service = TranscribeAudioServiceImpl()
    transcribe_audio = TranscribeAudio(transcribe_audio_service)
    transcription = transcribe_audio.execute(audio)

    return "\n".join([txt.text for txt in transcription.segments]), transcription.segments

    
def insert_subtitles(video, segments, language, font_size, font_family, background_color, background_color_value, font_color, position, line_spacing):
    video = Video(source_path=video, audio_path=None, transcript=None, subtitles=None)
    entity_transcript = Transcript(language=None, segments=segments)
    translate_service = TranslateServiceImpl()
    translate = Translate(translate_service)
    translated_subtitles = translate.execute(entity_transcript, language.lower())
    entity_substyles = SubtitleStyle(
        font_size=font_size,
        font_family=font_family,
        background_color=background_color_value if background_color else None,
        font_color=font_color,
        position=position,
        line_spacing=line_spacing if line_spacing else 1.2,
        shadow=True
    )

    entity_subtitles = Subtitles(
    language_output=language,
    segments=translated_subtitles.segments
    )

    insert_subtitles_service = InsertSubtitlesServiceImpl()
    insert_subtitles = InsertSubtitles(insert_subtitles_service)
    output_video = insert_subtitles.execute(video, entity_subtitles, entity_substyles, "output")

    return output_video.source_path

    


with gr.Blocks() as demo:
    gr.Markdown("Welcome to Video Subtitling App, upload your video and click the button to extract audio and generate subtitles.")
    with gr.Tab("Generate Subtitles"):
        with gr.Row():
            video_input = gr.Video(label="Input Video")
            subtitles_box_output = gr.Textbox(label="Generated Subtitles")
        transcribe_button = gr.Button("Transcribe and generate subtitles")

    with gr.Tab("Insert Subtitles"):
        with gr.Row():
            video_output = gr.Video(label="Output Video")
            with gr.Column(scale=1):
                subtitles_language = gr.Dropdown(["Spanish", "English", "French"],label="Language", info="Will add more languages later" )
                subtitles_font_size = gr.Dropdown(["Small", "Medium", "Large"],label="Font Size")
                subtitles_font_family = gr.Dropdown(["Arial", "Calibri", "Times New Roman"],label="Font Family")
                subtitles_background_color = gr.Checkbox(label="Background Color")
                selector_background_color = gr.ColorPicker(label="Background Color", visible=False)
                subtitles_background_color.change(fn=lambda x: gr.update(visible=x),inputs=subtitles_background_color,outputs=selector_background_color)
                subtitles_font_color = gr.ColorPicker(label="Subtitles Font Color")
                subtitles_position = gr.Dropdown(["Bottom", "Top", "Middle"],label="Position")
                subtitles_line_spacing = gr.Slider(0, 20, label="Subtitles Line Spacing")
        insert_subtitles_button = gr.Button("Insert Subtitles and generate video")

    segments_state = gr.State()
    transcribe_button.click(extract_audio, inputs=video_input, outputs=[subtitles_box_output, segments_state])
    insert_subtitles_button.click(
        insert_subtitles, 
        inputs=[video_input, segments_state, subtitles_language, subtitles_font_size, subtitles_font_family, subtitles_background_color, selector_background_color, subtitles_font_color, subtitles_position, subtitles_line_spacing],
        outputs=video_output
        )
    


    demo.launch()