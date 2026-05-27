"""02 Product Unboxing — HeyGen intro + frames + HeyGen outro.

Pipeline:
  1. User generates 2 HeyGen videos: assets/heygen_intro.mp4, assets/heygen_outro.mp4
  2. User generates 4 frames manually (ImageFX/Bing/Ideogram) -> assets/frames/frame_01..04.png
  3. (Optional) User drops assets/music.mp3
  4. Run -> outputs/unboxing_v{N}.mp4
"""
import os
import sys
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.version import next_version, ensure_dir
from lib.editor import normalize, ken_burns, concat, FFMPEG
from lib.audio import find_music
from lib.hg import require_heygen

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
FRAMES = os.path.join(ASSETS, "frames")
OUT = ensure_dir(os.path.join(HERE, "outputs"))
TMP = ensure_dir(os.path.join(OUT, ".tmp"))


def collect_frames() -> list:
    if not os.path.isdir(FRAMES):
        raise FileNotFoundError(
            f"\n  Missing folder: {FRAMES}\n"
            f"  Generate 4 frames manually (ImageFX / Bing Image Creator / Ideogram)\n"
            f"  and save as frame_01.png, frame_02.png, frame_03.png, frame_04.png"
        )
    files = sorted([f for f in os.listdir(FRAMES) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
    if len(files) < 2:
        raise FileNotFoundError(f"Need >=2 frames in {FRAMES}, found {len(files)}")
    return [os.path.join(FRAMES, f) for f in files]


def main() -> None:
    intro = require_heygen(ASSETS, "heygen_intro.mp4")
    outro = require_heygen(ASSETS, "heygen_outro.mp4")
    frames = collect_frames()
    music = find_music(ASSETS)

    v = next_version(OUT, "unboxing")
    final = os.path.join(OUT, f"unboxing_v{v}.mp4")

    print(f"=== 02 Product Unboxing v{v} ===")
    print(f"  intro : {intro}")
    print(f"  outro : {outro}")
    print(f"  frames: {len(frames)}")
    print(f"  music : {music or '(none)'}")

    print("[1/4] normalize intro/outro")
    n_intro = os.path.join(TMP, "intro.mp4"); normalize(intro, n_intro)
    n_outro = os.path.join(TMP, "outro.mp4"); normalize(outro, n_outro)

    print(f"[2/4] ken_burns x{len(frames)} (2s each)")
    kb_clips = []
    for i, fr in enumerate(frames, 1):
        out = os.path.join(TMP, f"kb_{i:02d}.mp4")
        ken_burns(fr, out, duration=2.0)
        kb_clips.append(out)

    print("[3/4] normalize ken_burns clips (add silent audio)")
    norm_kb = []
    for i, c in enumerate(kb_clips, 1):
        out = os.path.join(TMP, f"kb_norm_{i:02d}.mp4")
        import subprocess
        cmd = [FFMPEG, "-y", "-i", c, "-f", "lavfi", "-t", "2", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
               "-c:v", "copy", "-c:a", "aac", "-shortest", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-600:])
        norm_kb.append(out)

    print("[4/4] concat intro + frames + outro")
    sequence = [n_intro] + norm_kb + [n_outro]
    concat_out = os.path.join(TMP, "concat.mp4")
    concat(sequence, concat_out)

    if music:
        print("    mix music bed")
        import subprocess
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
