"""HeyGen helpers — detect manual user uploads + briefing template."""
import os
from typing import List, Optional


def find_heygen(assets_dir: str, name: str = "heygen.mp4") -> Optional[str]:
    p = os.path.join(assets_dir, name)
    return p if os.path.isfile(p) else None


def find_all_heygen(assets_dir: str, names: List[str]) -> List[Optional[str]]:
    return [find_heygen(assets_dir, n) for n in names]


def require_heygen(assets_dir: str, name: str = "heygen.mp4") -> str:
    p = find_heygen(assets_dir, name)
    if not p:
        raise FileNotFoundError(
            f"\n  Missing: {os.path.join(assets_dir, name)}\n"
            f"  Go to https://app.heygen.com/, generate the avatar video using the briefing,\n"
            f"  download as MP4 (9:16, 720p+), and save it at the path above."
        )
    return p


BRIEFING_TEMPLATE = """\
# Briefing HeyGen — {ad_name}

## Avatar
- Tipo: Avatar IV / Talking Photo / Avatar
- Estilo: {avatar_desc}
- Background: {background}

## Voz
- Idioma: PT-BR
- Voice: {voice_hint}
- Velocidade: 1.0x
- Pausas: natural

## Script (copy-paste no HeyGen)
```
{script}
```

## Setup HeyGen
1. Abra https://app.heygen.com/
2. Create Video > AI Avatar (ou Avatar IV)
3. Cole o script acima
4. Selecione voice PT-BR sugerida ({voice_hint})
5. Aspect ratio: 9:16 vertical
6. Resolution: 720p ou superior
7. Generate (aguarde 1-3 min)
8. Download MP4
9. Salve em: {save_path}
"""


def render_briefing(**kwargs) -> str:
    return BRIEFING_TEMPLATE.format(**kwargs)
