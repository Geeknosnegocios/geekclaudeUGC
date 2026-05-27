"""ElevenLabs TTS — free 10k chars/month. Fallback: user records own voiceover."""
import os
import requests
from typing import Optional

ELEVEN_BASE = "https://api.elevenlabs.io"


def _key() -> str:
    k = os.getenv("ELEVEN_KEY", "").strip()
    if not k or k.startswith("your_"):
        raise RuntimeError("ELEVEN_KEY missing in .env (get free at https://elevenlabs.io)")
    return k


def _voice() -> str:
    v = os.getenv("ELEVEN_VOICE_ID", "").strip()
    if not v or v.startswith("your_"):
        return "pNInz6obpgDQGcFmaJgB"
    return v


def tts(text: str, dst_mp3: str, voice_id: Optional[str] = None, model: str = "eleven_multilingual_v2") -> str:
    """Synthesize text -> mp3. Returns dst_mp3 path."""
    vid = voice_id or _voice()
    url = f"{ELEVEN_BASE}/v1/text-to-speech/{vid}"
    headers = {"xi-api-key": _key(), "Accept": "audio/mpeg", "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": model,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True}
    }
    r = requests.post(url, json=payload, headers=headers, timeout=120)
    r.raise_for_status()
    with open(dst_mp3, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return dst_mp3


def find_voiceover(assets_dir: str) -> Optional[str]:
    """Locate user-provided voiceover. Accepted names: voiceover.{mp3,wav,m4a}."""
    for name in ("voiceover.mp3", "voiceover.wav", "voiceover.m4a"):
        p = os.path.join(assets_dir, name)
        if os.path.isfile(p):
            return p
    return None


def find_music(assets_dir: str) -> Optional[str]:
    """Locate user-provided music bed. Accepted names: music.{mp3,wav,m4a}."""
    for name in ("music.mp3", "music.wav", "music.m4a"):
        p = os.path.join(assets_dir, name)
        if os.path.isfile(p):
            return p
    return None
