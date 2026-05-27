"""faster-whisper — local CPU/GPU transcription with word-level timestamps."""
import os
from typing import List, Tuple


def transcribe(audio_path: str, model_size: str = "small", language: str = "pt") -> Tuple[str, List[dict]]:
    """Return (full_text, word_segments). word_segments: [{word, start, end}, ...]."""
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(audio_path, language=language, word_timestamps=True)
    words = []
    full = []
    for seg in segments:
        full.append(seg.text.strip())
        if seg.words:
            for w in seg.words:
                words.append({"word": w.word.strip(), "start": float(w.start), "end": float(w.end)})
    return " ".join(full), words


def write_srt(words: List[dict], dst_srt: str, max_chars: int = 28) -> str:
    """Group words into ~28-char chunks and write .srt."""
    if not words:
        return dst_srt
    lines = []
    buf = []
    chunks = []
    for w in words:
        buf.append(w)
        text = " ".join(x["word"] for x in buf)
        if len(text) >= max_chars:
            chunks.append(buf)
            buf = []
    if buf:
        chunks.append(buf)

    def fmt(t: float) -> str:
        h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
        return f"{h:02d}:{m:02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}"

    with open(dst_srt, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks, 1):
            start = chunk[0]["start"]; end = chunk[-1]["end"]
            text = " ".join(x["word"] for x in chunk)
            f.write(f"{i}\n{fmt(start)} --> {fmt(end)}\n{text}\n\n")
    return dst_srt


def beat_cuts(words: List[dict], min_gap: float = 1.5, max_gap: float = 2.5) -> List[float]:
    """Pick cut timestamps every 1.5-2.5s aligned to word boundaries.
    Returns list of cut times (seconds)."""
    if not words:
        return []
    cuts = []
    last = 0.0
    for w in words:
        if w["start"] - last >= min_gap:
            cuts.append(w["start"])
            last = w["start"]
    return cuts
