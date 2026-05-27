"""02 Product Unboxing — HeyGen intro/outro + SuperGrok video clips.

Pipeline:
  1. User generates 2 HeyGen videos (intro reaction + outro CTA)
       -> assets/heygen_intro.mp4
       -> assets/heygen_outro.mp4
  2. User generates 3-6 unboxing clips via SuperGrok (Grok Imagine)
       -> assets/clips/clip_01.mp4 ... clip_NN.mp4
  3. (Optional) User drops assets/music.mp3
  4. Run -> outputs/unboxing_v{N}.mp4

SuperGrok: https://grok.com/  |  Rateio: https://rateaki.geekacademy.site
"""
import os
import sys
import shutil
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.version import next_version, ensure_dir
from lib.editor import normalize, concat, FFMPEG
from lib.audio import find_music
from lib.hg import require_heygen
from lib.grok import require_clips

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT = ensure_dir(os.path.join(HERE, "outputs"))
TMP = ensure_dir(os.path.join(OUT, ".tmp"))


def main() -> None:
    intro = require_heygen(ASSETS, "heygen_intro.mp4")
    outro = require_heygen(ASSETS, "heygen_outro.mp4")
    clips = require_clips(ASSETS, min_count=2)
    music = find_music(ASSETS)

    v = next_version(OUT, "unboxing")
    final = os.path.join(OUT, f"unboxing_v{v}.mp4")

    print(f"=== 02 Product Unboxing v{v} ===")
    print(f"  intro : {intro}")
    print(f"  outro : {outro}")
    print(f"  clips : {len(clips)} SuperGrok clips")
    for c in clips:
        print(f"    - {os.path.basename(c)}")
    print(f"  music : {music or '(none)'}")

    print("[1/3] normalize all clips")
    norm_intro = os.path.join(TMP, "intro.mp4"); normalize(intro, norm_intro)
    norm_outro = os.path.join(TMP, "outro.mp4"); normalize(outro, norm_outro)
    norm_clips = []
    for i, c in enumerate(clips, 1):
        n = os.path.join(TMP, f"clip_{i:02d}.mp4")
        normalize(c, n)
        norm_clips.append(n)

    print("[2/3] concat intro + clips + outro")
    sequence = [norm_intro] + norm_clips + [norm_outro]
    concat_out = os.path.join(TMP, "concat.mp4")
    concat(sequence, concat_out)

    print("[3/3] final mux (+music)")
    if music:
        cmd = [
            FFMPEG, "-y", "-i", concat_out, "-i", music,
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
        shutil.copyfile(concat_out, final)

    print(f"\nDONE -> {final} ({os.path.getsize(final)//1024} KB)")


if __name__ == "__main__":
    main()
