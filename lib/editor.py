"""ffmpeg wrappers — normalize, concat, ken_burns, overlay, loudnorm, mix."""
import os
import subprocess
import tempfile
from typing import List, Optional
from .ffmpeg_path import get_ffmpeg

FFMPEG = get_ffmpeg()

W, H, FPS = 720, 1280, 30
SCALE_PAD = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black"


def _run(cmd: List[str], label: str = "ffmpeg") -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{label} failed:\n{r.stderr[-800:]}")


def normalize(src: str, dst: str, audio: bool = True) -> None:
    """Resize/pad to 720x1280 @ 30fps, optionally drop audio."""
    cmd = [FFMPEG, "-y", "-i", src, "-vf", SCALE_PAD, "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "20"]
    if audio:
        cmd += ["-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    cmd += [dst]
    _run(cmd, "normalize")


def loudnorm(src: str, dst: str) -> None:
    """EBU R128 loudness normalize (-16 LUFS target, voiceover-friendly)."""
    cmd = [FFMPEG, "-y", "-i", src, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "copy", dst]
    _run(cmd, "loudnorm")


def concat(clips: List[str], dst: str) -> None:
    """Concat demuxer (all clips must share codec/fps/resolution — call normalize first)."""
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
        for c in clips:
            f.write(f"file '{os.path.abspath(c).replace(chr(92), '/')}'\n")
        list_file = f.name
    try:
        cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", dst]
        _run(cmd, "concat")
    finally:
        try:
            os.remove(list_file)
        except OSError:
            pass


def ken_burns(image: str, dst: str, duration: float = 2.0, zoom: float = 1.15) -> None:
    """Still image -> slow zoom/pan video clip 720x1280."""
    frames = int(duration * FPS)
    vf = (
        f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,"
        f"crop={W*2}:{H*2},"
        f"zoompan=z='min(zoom+0.0015,{zoom})':d={frames}:s={W}x{H}:fps={FPS}"
    )
    cmd = [FFMPEG, "-y", "-loop", "1", "-i", image, "-vf", vf, "-t", str(duration),
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-an", dst]
    _run(cmd, "ken_burns")


def mix_audio(voice: str, music: Optional[str], dst: str, music_db: float = -22.0) -> None:
    """Mix voiceover + music bed. Voice full vol, music ducked."""
    if not music:
        cmd = [FFMPEG, "-y", "-i", voice, "-c:a", "aac", "-b:a", "192k", dst]
        _run(cmd, "mix_audio (voice only)")
        return
    cmd = [
        FFMPEG, "-y", "-i", voice, "-i", music,
        "-filter_complex",
        f"[1:a]volume={music_db}dB,aloop=loop=-1:size=2e9[m];"
        f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
        "-map", "[a]", "-c:a", "aac", "-b:a", "192k", dst
    ]
    _run(cmd, "mix_audio")


def overlay_audio_on_video(video: str, audio: str, dst: str, replace_audio: bool = True) -> None:
    """Put external audio on a (muted or original) video."""
    if replace_audio:
        cmd = [FFMPEG, "-y", "-i", video, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
               "-map", "0:v:0", "-map", "1:a:0", "-shortest", dst]
    else:
        cmd = [FFMPEG, "-y", "-i", video, "-i", audio, "-filter_complex",
               "[0:a][1:a]amix=inputs=2:duration=first[a]", "-map", "0:v", "-map", "[a]",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", dst]
    _run(cmd, "overlay_audio_on_video")


def probe_duration(src: str) -> float:
    """Return media duration in seconds via ffmpeg (no ffprobe needed)."""
    cmd = [FFMPEG, "-i", src, "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stderr
    import re
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", out)
    if not m:
        return 0.0
    h, mi, s = m.group(1), m.group(2), m.group(3)
    return int(h) * 3600 + int(mi) * 60 + float(s)


def cut_to_segments(src: str, dst_pattern: str, segment_duration: float) -> List[str]:
    """Split src into fixed-duration chunks. Returns list of created files."""
    dur = probe_duration(src)
    n = int(dur // segment_duration) + (1 if dur % segment_duration > 0.1 else 0)
    out = []
    for i in range(n):
        start = i * segment_duration
        path = dst_pattern.format(i=i + 1)
        cmd = [FFMPEG, "-y", "-ss", str(start), "-i", src, "-t", str(segment_duration),
               "-c:v", "libx264", "-c:a", "aac", "-preset", "medium", "-crf", "20", path]
        _run(cmd, f"cut_to_segments[{i}]")
        out.append(path)
    return out


def interleave_clips(clips_a: List[str], clips_b: List[str], dst: str) -> None:
    """Alternate clips_a[0] + clips_b[0] + clips_a[1] + clips_b[1] ... then concat."""
    order = []
    for i in range(max(len(clips_a), len(clips_b))):
        if i < len(clips_a):
            order.append(clips_a[i])
        if i < len(clips_b):
            order.append(clips_b[i])
    concat(order, dst)
