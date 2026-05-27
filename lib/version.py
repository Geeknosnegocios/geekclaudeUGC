import os
import re


def next_version(folder: str, prefix: str, ext: str = "mp4") -> int:
    """Scan folder for files matching prefix_v<N>.ext and return next N (max+1)."""
    if not os.path.isdir(folder):
        return 1
    pat = re.compile(rf"^{re.escape(prefix)}_v(\d+)\.{re.escape(ext)}$")
    nums = []
    for f in os.listdir(folder):
        m = pat.match(f)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path
