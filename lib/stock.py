"""Pexels API client — free b-roll video search + download."""
import os
import requests
from typing import List, Dict

PEXELS_BASE = "https://api.pexels.com"


def _key() -> str:
    k = os.getenv("PEXELS_KEY", "").strip()
    if not k or k.startswith("your_"):
        raise RuntimeError("PEXELS_KEY missing in .env (get free at https://www.pexels.com/api/)")
    return k


def search_videos(query: str, per_page: int = 10, orientation: str = "portrait", size: str = "medium") -> List[Dict]:
    """Search Pexels videos. Returns list of {id, duration, url, files:[...]}."""
    r = requests.get(
        f"{PEXELS_BASE}/videos/search",
        headers={"Authorization": _key()},
        params={"query": query, "per_page": per_page, "orientation": orientation, "size": size},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("videos", [])


def pick_best_file(video: Dict, target_height: int = 1280) -> str:
    """Pick best mp4 download URL for target height (default 720x1280 portrait)."""
    files = [f for f in video.get("video_files", []) if f.get("file_type") == "video/mp4"]
    if not files:
        return ""
    files.sort(key=lambda f: abs((f.get("height") or 0) - target_height))
    return files[0].get("link", "")


def download_video(url: str, dest_path: str) -> bool:
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return os.path.getsize(dest_path) > 0


def fetch_broll(query: str, dest_dir: str, count: int = 6, prefix: str = "broll") -> List[str]:
    """High-level: search + download N portrait clips. Returns list of saved paths."""
    os.makedirs(dest_dir, exist_ok=True)
    vids = search_videos(query, per_page=max(count * 2, 10))
    saved = []
    for i, v in enumerate(vids):
        if len(saved) >= count:
            break
        url = pick_best_file(v)
        if not url:
            continue
        path = os.path.join(dest_dir, f"{prefix}_{i+1:02d}.mp4")
        try:
            if download_video(url, path):
                saved.append(path)
                print(f"  [stock] {os.path.basename(path)} ({os.path.getsize(path)//1024}KB)", flush=True)
        except Exception as e:
            print(f"  [stock] skip {i}: {e}", flush=True)
    return saved
