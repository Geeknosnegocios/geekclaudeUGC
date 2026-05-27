"""03 Faceless Lifestyle — Pexels b-roll + voiceover + optional manual hero frames.

Pipeline:
  1. Claude writes voiceover script + Pexels keywords
  2. Voiceover source (one of):
       (a) Run with --tts to generate via ElevenLabs (free 10k chars/mo)
       (b) User drops assets/voiceover.mp3 (recorded on phone)
  3. (Optional) User drops 1-2 hero frames at assets/frames/hero_01.png
  4. Script auto-downloads Pexels b-roll, transcribes voiceover, beat-cuts, exports.
"""
import os
import sys
import shutil
import argparse
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.version import next_version, ensure_dir
from lib.editor import normalize, ken_burns, concat, FFMPEG, probe_duration
from lib.stock import fetch_broll
from lib.audio import find_voiceover, find_music, tts
from lib.transcribe import transcribe, write_srt

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
BROLL = os.path.join(ASSETS, "broll")
FRAMES = os.path.join(ASSETS, "frames")
OUT = ensure_dir(os.path.join(HERE, "outputs"))
TMP = ensure_dir(os.path.join(OUT, ".tmp"))


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True, help='Pexels search query (e.g. "hands holding cream")')
    p.add_argument("--clips", type=int, default=6)
    p.add_argument("--tts", help="If set, synthesize voiceover from this text via ElevenLabs")
    p.add_argument("--srt", action="store_true", help="Also write a .srt subtitle file (no burn)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    v = next_version(OUT, "lifestyle")
    final = os.path.join(OUT, f"lifestyle_v{v}.mp4")
    srt_path = os.path.join(OUT, f"lifestyle_v{v}.srt") if args.srt else None

    print(f"=== 03 Faceless Lifestyle v{v} ===")

    # 1. voiceover
    vo = find_voiceover(ASSETS)
    if not vo and args.tts:
        vo = os.path.join(ASSETS, "voiceover.mp3")
        print(f"[tts] ElevenLabs -> {vo}")
        tts(args.tts, vo)
    if not vo:
        raise FileNotFoundError(
            f"\n  No voiceover found.\n"
            f"  Options:\n"
            f"   (a) Drop assets/voiceover.mp3 (record on phone)\n"
            f"   (b) Re-run with --tts \"YOUR SCRIPT HERE\"  (uses ElevenLabs free tier)"
        )
    vo_dur = probe_duration(vo)
    print(f"  voiceover: {vo} ({vo_dur:.1f}s)")

    # 2. transcribe + cut points
    print("[1/5] transcribe voiceover (faster-whisper)")
    full_text, words = transcribe(vo, language="pt")
    if srt_path:
        write_srt(words, srt_path)
        print(f"       wrote {srt_path}")
    cut_count = max(args.clips, 4)

    # 3. fetch b-roll
    print(f"[2/5] fetch Pexels b-roll x{cut_count} (query: {args.query!r})")
    broll = fetch_broll(args.query, BROLL, count=cut_count)
    if len(broll) < 2:
        raise RuntimeError(f"Pexels returned only {len(broll)} clips for query {args.query!r}")

    # 4. optional hero frames -> ken_burns
    hero_clips = []
    if os.path.isdir(FRAMES):
        heros = sorted([os.path.join(FRAMES, f) for f in os.listdir(FRAMES) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
        for i, h in enumerate(heros, 1):
            out = os.path.join(TMP, f"hero_{i:02d}.mp4")
            ken_burns(h, out, duration=2.0)
            hero_clips.append(out)

    # 5. normalize all clips, then trim each to ~vo_dur / N
    print("[3/5] normalize clips")
    all_clips = broll + hero_clips
    seg_dur = vo_dur / max(len(all_clips), 1)
    norm_clips = []
    for i, c in enumerate(all_clips, 1):
        n = os.path.join(TMP, f"norm_{i:02d}.mp4")
        # normalize then trim to seg_dur (no audio)
        tmp = os.path.join(TMP, f"pre_{i:02d}.mp4")
        normalize(c, tmp, audio=False)
        cmd = [FFMPEG, "-y", "-i", tmp, "-t", str(seg_dur), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-an", n]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-600:])
        # add silent audio so concat demuxer works
        n_aud = os.path.join(TMP, f"normaud_{i:02d}.mp4")
        cmd = [FFMPEG, "-y", "-i", n, "-f", "lavfi", "-t", str(seg_dur),
               "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
               "-c:v", "copy", "-c:a", "aac", "-shortest", n_aud]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-600:])
        norm_clips.append(n_aud)

    # 6. concat
    print("[4/5] concat clips")
    video_concat = os.path.join(TMP, "video.mp4")
    concat(norm_clips, video_concat)

    # 7. overlay voiceover (+ optional music)
    print("[5/5] mux voiceover + music")
    music = find_music(ASSETS)
    if music:
        cmd = [
            FFMPEG, "-y", "-i", video_concat, "-i", vo, "-i", music,
            "-filter_complex",
            "[2:a]volume=-22dB,aloop=loop=-1:size=2e9[m];"
            "[1:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final,
        ]
    else:
        cmd = [FFMPEG, "-y", "-i", video_concat, "-i", vo,
               "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-600:])

    print(f"\nDONE -> {final} ({os.path.getsize(final)//1024} KB)")
    if srt_path:
        print(f"     srt -> {srt_path}")


if __name__ == "__main__":
    main()
