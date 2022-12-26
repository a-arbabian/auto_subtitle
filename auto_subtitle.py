import os
import sys

import whisper
from whisper.utils import write_srt

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

FONT = "Akira Expanded"
def run(input_path: str) -> None:
    print("Transcribing audio...")
    model = whisper.load_model("base")
    result = model.transcribe(input_path)

    subtitle_path = os.path.splitext(input_path)[0] + ".srt"
    with open(subtitle_path, "w", encoding="utf-8") as srt_file:
        write_srt(result["segments"], file=srt_file)
    
    print("Generating subtitles...")
    orig_video = VideoFileClip(input_path)
    generator = lambda txt: TextClip(txt, 
                                     font=FONT if FONT else "Courier", 
                                     fontsize=48, 
                                     color='white',
                                     size=orig_video.size,
                                     method='caption',
                                     align='center',)
    subs = SubtitlesClip(subtitle_path, generator)
    
    print("Compositing final video...")
    final = CompositeVideoClip([orig_video, subs.set_position('center','middle')])
    final_path = os.path.splitext(input_path)[0] + "_final.mp4"
    final.write_videofile(final_path, fps=orig_video.fps)


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Error: Invalid number of arguments.\n"
            "Usage: python whisper_subtitle_generator.py <input-path>\n"
            "Example: python whisper_subtitle_generator.py 'video.mp4'"
        )
        sys.exit(1)

    run(input_path=sys.argv[1])


if __name__ == "__main__":
    main()