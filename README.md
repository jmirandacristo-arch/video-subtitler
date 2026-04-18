# Video Subtitler

A Python tool that automatically transcribes, translates, and burns subtitles into videos.

## Features
- Audio extraction from video
- Transcription using Whisper
- Translation via Google Translate
- Customizable subtitle styles (font, color, position, size)
- Clean Architecture + DDD

## Tech Stack
- Python
- FastAPI
- Whisper (faster-whisper)
- ffmpeg-python
- Gradio
- SQLAlchemy

## How to run
```bash
pip install -r requirements.txt
python presentation/ui.py
```