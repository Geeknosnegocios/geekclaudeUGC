"""Jamendo Music API — free royalty-free music search + download.

Signup: https://devportal.jamendo.com (free, get CLIENT_ID, add to .env as JAMENDO_CLIENT_ID).
Pricing: free tier ~35,000 tracks, 35 req/sec, no monthly cap for non-commercial.
Docs: https://developer.jamendo.com/v3.0/tracks
"""
import os
import requests
from typing import Optional, List, Dict

JAMENDO_BASE = "https://api.jamendo.com/v3.0"


def _key() -> Optional[str]:
    k = os.getenv("JAMENDO_CLIENT_ID", "").strip()
    if not k or k.startswith("your_"):
        return None
    return k


def has_key() -> bool:
    return _key() is not None


def search_tracks(tags: str = "ambient", limit: int = 5, vocal_instrumental: str = "instrumental") -> List[Dict]:
    """Search Jamendo tracks. Returns list of {id, name, artist, audio (mp3 url), duration}."""
    key = _key()
    if not key:
        raise RuntimeError(
            "JAMENDO_CLIENT_ID missing in .env. "
            "Free signup: https://devportal.jamendo.com"
        )
    r = requests.get(
        f"{JAMENDO_BASE}/tracks/",
        params={
            "client_id": key,
            "format": "json",
            "limit": limit,
            "tags": tags,
            "vocalinstrumental": vocal_instrumental,
            "audiodlformat": "mp32",
            "audiodownload_allowed": "true",
            "include": "musicinfo",
            "order": "popularity_total",
        },
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("headers", {}).get("status") != "success":
        msg = data.get("headers", {}).get("error_message", "unknown error")
        raise RuntimeError(f"Jamendo API: {msg}")
    return data.get("results", [])


def download_track(url: str, dst: str) -> int:
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(dst, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return os.path.getsize(dst)


def fetch_music(tags: str, dst_mp3: str, instrumental: bool = True) -> str:
    """Search + download first matching track. Returns dst path on success."""
    tracks = search_tracks(tags=tags, limit=5, vocal_instrumental="instrumental" if instrumental else "")
    if not tracks:
        raise RuntimeError(f"Jamendo: no tracks for tags={tags!r}")
    # Prefer audiodownload (stable URL), fall back to streaming audio. Try each track in order.
    last_err = None
    for chosen in tracks:
        for field in ("audiodownload", "audio"):
            url = chosen.get(field)
            if not url:
                continue
            try:
                size = download_track(url, dst_mp3)
                print(f"  [music] {chosen.get('name')} - {chosen.get('artist_name')} ({size//1024} KB)")
                return dst_mp3
            except Exception as e:
                last_err = e
                continue
    raise RuntimeError(f"Jamendo: no usable audio URL across {len(tracks)} tracks. Last error: {last_err}")
