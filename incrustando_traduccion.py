import ffmpeg

VIDEO_INPUT = "traduciendo.mp4"
SRT_FILE = "subtitulos.srt"
VIDEO_OUTPUT = "traduciendo_subtitulada.mp4"

def add_subtitles_to_video(input_video, srt_file, output_video):
    print("🎬 Incrustando subtítulos en el video final...")
    ffmpeg.input(input_video).output(
        output_video,
        vf=(
            f"subtitles={srt_file}:force_style="
            "'FontName=Roboto,FontSize=12,PrimaryColour=&H00FFFFFF,"
            "Alignment=1,MarginV=20'"
        ),
        vcodec="libx264",
        acodec="aac",
        strict="-2"
    ).run(overwrite_output=True)
    print(f"✅ Video generado: {output_video}")

if __name__ == "__main__":
    add_subtitles_to_video(VIDEO_INPUT, SRT_FILE, VIDEO_OUTPUT)
