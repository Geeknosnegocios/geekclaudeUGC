"""03 Faceless Lifestyle — SuperGrok clips (primary) OR Pexels b-roll (fallback).

Pipeline:
  1. Claude writes voiceover script + SuperGrok prompts
  2. Voiceover source (one of):
       (a) Run with --tts "TEXT" to generate via ElevenLabs (free 10k chars/mo)
       (b) User drops assets/voiceover.mp3 (recorded on phone)
  3. Video source (one of):
       (a) User generates clips via SuperGrok -> assets/clips/clip_01.mp4 ...
       (b) Run with --query "search words" -> downloads Pexels stock (fallback)
  4. Script auto-transcribes, normalizes, concats, exports.

SuperGrok: https://grok.com/  |  Rateio: https://rateaki.geekacademy.site
"""
import os
import sys
import argparse
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.version import next_version, ensure_dir
from lib.editor import normalize, concat, FFMPEG, probe_duration
from lib.stock import fetch_broll
from lib.audio import find_voiceover, find_music, tts
from lib.transcribe import transcribe, write_srt
from lib.grok import find_clips
from lib.music import has_key as has_jamendo, fetch_music

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
BROLL = os.path.join(ASSETS, "broll")
OUT = ensure_dir(os.path.join(HERE, "outputs"))
TMP = ensure_dir(os.path.join(OUT, ".tmp"))


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--query", help="(Fallback) Pexels search if no SuperGrok clips present")
    p.add_argument("--clips", type=int, default=6, help="(Fallback) Pexels clip count")
    p.add_argument("--tts", help="If set, synthesize voiceover from this text via ElevenLabs")
    p.add_argument("--srt", action="store_true", help="Also write a .srt subtitle file (no burn)")
    p.add_argument("--music-tags", default="ambient", help="Jamendo tags for auto-fetched music bed (single tag works best: ambient, chill, lofi, relax, lounge)")
    p.add_argument("--no-music", action="store_true", help="Skip auto-music fetch")
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
            "\n  No voiceover found. Options:\n"
            "   (a) Drop assets/voiceover.mp3 (record on phone)\n"
            "   (b) Re-run with --tts \"YOUR SCRIPT\"  (ElevenLabs free)"
        )
    vo_dur = probe_duration(vo)
    print(f"  voiceover: {vo} ({vo_dur:.1f}s)")

    # 2. transcribe + optional srt
    print("[1/5] transcribe voiceover (faster-whisper)")
    full_text, words = transcribe(vo, language="pt")
    if srt_path:
        write_srt(words, srt_path)
        print(f"       wrote {srt_path}")

    # 3. video source: SuperGrok clips (primary) OR Pexels (fallback)
    grok_clips = find_clips(ASSETS)
    if grok_clips:
        print(f"[2/5] using {len(grok_clips)} SuperGrok clips")
        sources = grok_clips
    else:
        if not args.query:
            raise FileNotFoundError(
                "\n  No SuperGrok clips found in assets/clips/ AND no --query for Pexels fallback.\n"
                "  Options:\n"
                "   (a) Generate via SuperGrok -> assets/clips/clip_01.mp4 ...\n"
                "       https://grok.com/  |  Rateio: https://rateaki.geekacademy.site\n"
                "   (b) Re-run with --query \"hands holding cream\"  (Pexels fallback)"
            )
        print(f"[2/5] no SuperGrok clips, fetching {args.clips} Pexels b-roll (query={args.query!r})")
        sources = fetch_broll(args.query, BROLL, count=args.clips)
        if len(sources) < 2:
            raise RuntimeError(f"Pexels returned only {len(sources)} clips for {args.query!r}")

    # 4. trim each clip to share of voiceover duration
    seg_dur = vo_dur / max(len(sources), 1)
    print(f"[3/5] normalize + trim each clip to {seg_dur:.2f}s (no audio)")
    norm_clips = []
    for i, c in enumerate(sources, 1):
        pre = os.path.join(TMP, f"pre_{i:02d}.mp4")
        normalize(c, pre, audio=False)
        n = os.path.join(TMP, f"norm_{i:02d}.mp4")
        cmd = [FFMPEG, "-y", "-i", pre, "-t", str(seg_dur),
               "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-an", n]
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

    # 5. concat + mux voiceover (+optional music)
    print("[4/5] concat clips")
    video_concat = os.path.join(TMP, "video.mp4")
    concat(norm_clips, video_concat)

    print("[5/5] mux voiceover + music")
    music = find_music(ASSETS)
    if not music and not args.no_music and has_jamendo():
        try:
            print(f"     no manual music.mp3, fetching from Jamendo (tags={args.music_tags!r})")
            music = fetch_music(args.music_tags, os.path.join(ASSETS, "music.mp3"))
        except Exception as e:
            print(f"     [music] auto-fetch failed: {e}")
            music = None
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
