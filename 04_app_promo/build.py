"""04 App Promo — HeyGen talking head + screen-recording cuts.

Pipeline:
  1. User generates HeyGen talking head -> assets/heygen.mp4
  2. User drops app screen recording -> assets/app_demo.mp4
  3. Run -> outputs/app_promo_v{N}.mp4

Logic: HeyGen audio plays throughout. Video alternates HeyGen <-> app_demo
every `--segment` seconds (default 3.0s). App footage is muted.
"""
import os
import sys
import argparse
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.version import next_version, ensure_dir
from lib.editor import normalize, concat, FFMPEG, probe_duration, cut_to_segments
from lib.audio import find_music
from lib.hg import require_heygen

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT = ensure_dir(os.path.join(HERE, "outputs"))
TMP = ensure_dir(os.path.join(OUT, ".tmp"))


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--segment", type=float, default=3.0, help="Cut interval (seconds)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    heygen = require_heygen(ASSETS, "heygen.mp4")
    app_demo = os.path.join(ASSETS, "app_demo.mp4")
    if not os.path.isfile(app_demo):
        raise FileNotFoundError(
            f"\n  Missing: {app_demo}\n"
            f"  Drop a screen recording of your app (vertical 9:16 preferred) here."
        )

    v = next_version(OUT, "app_promo")
    final = os.path.join(OUT, f"app_promo_v{v}.mp4")

    print(f"=== 04 App Promo v{v} ===")
    print(f"  heygen   : {heygen}")
    print(f"  app_demo : {app_demo}")
    print(f"  segment  : {args.segment}s")

    # 1. normalize both
    print("[1/4] normalize both inputs")
    n_hg = os.path.join(TMP, "hg.mp4"); normalize(heygen, n_hg, audio=True)
    n_app = os.path.join(TMP, "app.mp4"); normalize(app_demo, n_app, audio=False)
    # add silent audio to app
    n_app_sil = os.path.join(TMP, "app_sil.mp4")
    app_dur = probe_duration(n_app)
    cmd = [FFMPEG, "-y", "-i", n_app, "-f", "lavfi", "-t", str(app_dur),
           "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
           "-c:v", "copy", "-c:a", "aac", "-shortest", n_app_sil]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-600:])

    # 2. cut each into segments
    print(f"[2/4] split into {args.segment}s segments")
    hg_segs = cut_to_segments(n_hg, os.path.join(TMP, "hg_seg_{i:02d}.mp4"), args.segment)
    app_segs = cut_to_segments(n_app_sil, os.path.join(TMP, "app_seg_{i:02d}.mp4"), args.segment)
    print(f"     hg segs={len(hg_segs)} app segs={len(app_segs)}")

    # 3. interleave (hg, app, hg, app, ...)
    print("[3/4] interleave video segments (audio = hg only)")
    interleaved = []
    n = max(len(hg_segs), len(app_segs))
    for i in range(n):
        if i < len(hg_segs):
            interleaved.append(hg_segs[i])
        if i < len(app_segs):
            interleaved.append(app_segs[i])
    video_only = os.path.join(TMP, "video_only.mp4")
    concat(interleaved, video_only)

    # 4. replace audio with full hg audio
    print("[4/4] mux original HeyGen audio over interleaved video")
    hg_audio = os.path.join(TMP, "hg_audio.aac")
    cmd = [FFMPEG, "-y", "-i", n_hg, "-vn", "-c:a", "copy", hg_audio]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-600:])

    music = find_music(ASSETS)
    if music:
        cmd = [
            FFMPEG, "-y", "-i", video_only, "-i", hg_audio, "-i", music,
            "-filter_complex",
            "[2:a]volume=-22dB,aloop=loop=-1:size=2e9[m];"
            "[1:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final,
        ]
    else:
        cmd = [FFMPEG, "-y", "-i", video_only, "-i", hg_audio,
               "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-600:])

    print(f"\nDONE -> {final} ({os.path.getsize(final)//1024} KB)")


if __name__ == "__main__":
    main()
