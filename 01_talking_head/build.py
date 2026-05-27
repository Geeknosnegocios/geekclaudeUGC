"""01 Talking Head — assemble HeyGen MP4 + optional music bed.

Pipeline:
  1. User generates avatar in HeyGen UI (briefing provided by Claude)
  2. User saves MP4 as assets/heygen.mp4
  3. (Optional) User drops music bed at assets/music.mp3
  4. Run this script -> outputs/talking_head_v{N}.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.version import next_version, ensure_dir
from lib.editor import normalize, loudnorm, overlay_audio_on_video
from lib.audio import find_music
from lib.hg import require_heygen
from lib.music import has_key as has_jamendo, fetch_music

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT = ensure_dir(os.path.join(HERE, "outputs"))
TMP = ensure_dir(os.path.join(OUT, ".tmp"))


def main() -> None:
    heygen = require_heygen(ASSETS)
    music = find_music(ASSETS)
    if not music and has_jamendo():
        try:
            print("  no music.mp3, fetching from Jamendo (ambient)")
            music = fetch_music("ambient", os.path.join(ASSETS, "music.mp3"))
        except Exception as e:
            print(f"  [music] auto-fetch failed: {e}")
            music = None

    v = next_version(OUT, "talking_head")
    final = os.path.join(OUT, f"talking_head_v{v}.mp4")

    print(f"=== 01 Talking Head v{v} ===")
    print(f"  source: {heygen}")
    print(f"  music : {music or '(none)'}")

    norm = os.path.join(TMP, "norm.mp4")
    print("[1/3] normalize 720x1280@30fps")
    normalize(heygen, norm, audio=True)

    loud = os.path.join(TMP, "loud.mp4")
    print("[2/3] loudnorm -16 LUFS")
    loudnorm(norm, loud)

    if music:
        print("[3/3] overlay music bed (-22 dB)")
        from lib.editor import FFMPEG
        import subprocess
        cmd = [
            FFMPEG, "-y", "-i", loud, "-i", music,
            "-filter_complex",
            "[1:a]volume=-22dB,aloop=loop=-1:size=2e9[m];"
            "[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", final,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-800:])
    else:
        print("[3/3] no music, copy final")
        import shutil
        shutil.copyfile(loud, final)

    size_kb = os.path.getsize(final) // 1024
    print(f"\nDONE -> {final} ({size_kb} KB)")


if __name__ == "__main__":
    main()
