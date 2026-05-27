import os
import shutil


def get_ffmpeg() -> str:
    """Locate ffmpeg binary. Order: PATH > imageio_ffmpeg bundled."""
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        raise RuntimeError(
            "ffmpeg not found in PATH and imageio_ffmpeg unavailable. "
            "Install: pip install imageio-ffmpeg OR add ffmpeg to PATH."
        ) from e


def get_ffprobe() -> str:
    p = shutil.which("ffprobe")
    if p:
        return p
    # imageio bundles only ffmpeg, no ffprobe — fallback to ffmpeg duration parsing
    return ""
