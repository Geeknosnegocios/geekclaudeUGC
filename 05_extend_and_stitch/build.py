"""05 Extend and Stitch — normalize + concat 2+ MP4s into one final.

Pipeline:
  1. User drops 2+ MP4 files in assets/ (any names)
  2. (Optional) User drops assets/music.mp3
  3. Run -> outputs/extended_v{N}.mp4

Order: alphabetical by filename. Rename files (01_intro.mp4, 02_body.mp4, ...)
to control order.
"""
import os
import sys
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.version import next_version, ensure_dir
from lib.editor import normalize, loudnorm, concat, FFMPEG
from lib.audio import find_music

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT = ensure_dir(os.path.join(HERE, "outputs"))
TMP = ensure_dir(os.path.join(OUT, ".tmp"))


def collect_inputs() -> list:
    if not os.path.isdir(ASSETS):
        raise FileNotFoundError(f"Missing folder: {ASSETS}")
    files = sorted([
        os.path.join(ASSETS, f) for f in os.listdir(ASSETS)
        if f.lower().endswith((".mp4", ".mov", ".m4v"))
        and not f.lower().startswith("music")
    ])
    if len(files) < 2:
        raise FileNotFoundError(
            f"\n  Need >=2 video files in {ASSETS}/, found {len(files)}.\n"
            f"  Rename files like 01_intro.mp4, 02_body.mp4 to control order."
        )
    return files


def main() -> None:
    inputs = collect_inputs()
    music = find_music(ASSETS)
    v = next_version(OUT, "extended")
    final = os.path.join(OUT, f"extended_v{v}.mp4")

    print(f"=== 05 Extend & Stitch v{v} ===")
    print(f"  inputs: {len(inputs)}")
    for i, f in enumerate(inputs, 1):
        print(f"    {i}. {os.path.basename(f)}")
    print(f"  music : {music or '(none)'}")

    print("[1/3] normalize + loudnorm each clip")
    norm_clips = []
    for i, src in enumerate(inputs, 1):
        n = os.path.join(TMP, f"norm_{i:02d}.mp4")
        ln = os.path.join(TMP, f"loud_{i:02d}.mp4")
        normalize(src, n, audio=True)
        loudnorm(n, ln)
        norm_clips.append(ln)

    print("[2/3] concat")
    video_concat = os.path.join(TMP, "concat.mp4")
    concat(norm_clips, video_concat)

    print("[3/3] final mux (+music)")
    if music:
        cmd = [
            FFMPEG, "-y", "-i", video_concat, "-i", music,
            "-filter_complex",
            "[1:a]volume=-22dB,aloop=loop=-1:size=2e9[m];"
            "[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-600:])
    else:
        import shutil
        shutil.copyfile(video_concat, final)

    print(f"\nDONE -> {final} ({os.path.getsize(final)//1024} KB)")


if __name__ == "__main__":
    main()
