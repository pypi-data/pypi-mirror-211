import os
import subprocess
import tempfile
from typing import Any, List

import cv2
import ffmpeg
import numpy as np
import numpy.typing as npt
import skvideo.io


class VideoWriter:
    def __init__(
        self,
        target_file: str,
        quality: int = 26,
        fps: int = 10,
    ):
        self.target_file = target_file
        self.fps = fps
        self.quality = quality
        self.count = 0

    def writeFrame(self, im: Any) -> None:
        self.writer.writeFrame(im)
        self.count += 1

    def __enter__(self) -> "VideoWriter":
        self.writer = skvideo.io.FFmpegWriter(
            self.target_file,
            inputdict={"-r": str(self.fps)},
            outputdict={
                "-vcodec": "libx264",
                "-pix_fmt": "yuv420p",
                "-x264-params": "keyint=2:scenecut=0",
                "-crf": str(self.quality),
            },
        )
        # ttysetattr etc goes here before opening and returning the file object
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        if self.count > 0:
            self.writer.close()


def generate_video(
    image_files: List[str], target_file: str = "out.mp4", fps=10, threads=4
) -> npt.NDArray[np.uint8]:
    """Generate a video from a list of image files using ffmpeg as a subprocess"""
    duration = 1 / fps
    with tempfile.NamedTemporaryFile(mode="w", dir=".") as tmp_fp:
        tmp_fp.write(
            "\n".join(f"file {name}\nduration {duration:04f}" for name in image_files)
        )

        # Call ffmpeg as a subprocess to generate the video
        subprocess.call(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "concat",
                "-i",
                tmp_fp.name,
                "-vcodec",
                "libx264",
                "-x264-params",
                "keyint=2:scenecut=0",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "24",
                "-r",
                str(fps),
                "-threads",
                str(threads),
                target_file,
            ]
        )


def write_audio_and_video(audio_file: str, video_file: str, output_file: str) -> None:
    if not os.path.isfile(audio_file) or not os.path.isfile(video_file):
        raise ValueError("Audio or video file does not exist")

    input_video = ffmpeg.input(video_file)
    input_audio = ffmpeg.input(audio_file)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
        output_file, loglevel="error"
    ).overwrite_output().run()
