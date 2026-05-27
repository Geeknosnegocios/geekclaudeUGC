"""SuperGrok (Grok Imagine) helper — manual workflow for video clip generation.

SuperGrok generates BOTH the image AND the animated video. The user pastes
prompts in the SuperGrok app/web, downloads each MP4, and drops them in
the template's assets/clips/ folder.
"""
import os
from typing import List, Optional

BRIEFING_TEMPLATE = """\
# Briefing SuperGrok — {ad_name}

## Geração via Grok Imagine (web ou app)
- URL: https://grok.com/  (precisa SuperGrok subscription OU rateio)
- Aspect: 9:16 vertical
- Duration: 5-8 segundos por clip
- Quality: highest

## Clips a gerar ({clip_count} no total)

{clip_prompts}

## Passo a passo
1. Abra https://grok.com/
2. Clique em "Imagine" (geração de imagem) ou no botão de video
3. Cole o primeiro prompt acima
4. Aguarde geração (~30-60s)
5. Clique em "Animate" / "Make Video" -> gera vídeo de 5-8s
6. Download MP4
7. Salve em: {save_dir}/clip_01.mp4
8. Repita para os demais prompts (clip_02.mp4, clip_03.mp4, ...)

## Não tem SuperGrok?
Acesse via rateio em https://rateaki.geekacademy.site
"""


def find_clips(assets_dir: str, subdir: str = "clips") -> List[str]:
    """Locate user-dropped SuperGrok clips in assets/clips/. Returns sorted list."""
    folder = os.path.join(assets_dir, subdir)
    if not os.path.isdir(folder):
        return []
    files = sorted([
        os.path.join(folder, f) for f in os.listdir(folder)
        if f.lower().endswith((".mp4", ".mov", ".m4v"))
    ])
    return files


def require_clips(assets_dir: str, min_count: int = 2, subdir: str = "clips") -> List[str]:
    clips = find_clips(assets_dir, subdir)
    if len(clips) < min_count:
        raise FileNotFoundError(
            f"\n  Need >={min_count} clips in {os.path.join(assets_dir, subdir)}/\n"
            f"  Generate via SuperGrok Imagine -> save as clip_01.mp4, clip_02.mp4, ...\n"
            f"  SuperGrok: https://grok.com/  |  Rateio: https://rateaki.geekacademy.site"
        )
    return clips


def render_briefing(ad_name: str, save_dir: str, prompts: List[str]) -> str:
    clip_prompts = "\n\n".join(
        f"### Clip {i+1:02d}\n```\n{p}\n```"
        for i, p in enumerate(prompts)
    )
    return BRIEFING_TEMPLATE.format(
        ad_name=ad_name,
        clip_count=len(prompts),
        clip_prompts=clip_prompts,
        save_dir=save_dir,
    )
