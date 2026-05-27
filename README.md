# Geek CLAUDE - UGC

> **Clone qualquer ad UGC vencedor em 15 minutos. Sem editar vídeo. Sem aparecer. Sem pagar editor.**

Você acha um ad que tá rodando há 30+ dias no TikTok. Joga aqui. O agente (Claude / Codex / Gemini) lê o ad, escreve script PT-BR adaptado pro seu produto, gera briefing pro HeyGen e SuperGrok, baixa música e b-roll automaticamente, mixa voz com ElevenLabs, e finaliza tudo com motion graphics profissional via HyperFrames — kinetic captions estilo TikTok, transições, lower-thirds, end CTA card.

**Resultado:** MP4 720x1280 vertical pronto pra subir no TikTok / Reels / Shorts em ~15-20 minutos.

---

## Quer aprender o sistema completo lowticket no ar em 1 hora?

A **Formação Produtor Milionário** ensina do zero ao primeiro dinheiro no mesmo dia — nicho, copy, página, tráfego e funil, tudo orquestrado com Claude.

👉 **https://produtor.geekacademy.site**

---

## ⚡ Em 3 passos (visão alta)

```
1. Joga referência no agente   →   "Clona esse ad pra mim"
2. Agente entrega: script + briefing HeyGen + prompts SuperGrok + comando
3. Você cola nos sites, baixa MP4s, roda 1 comando   →   ad pronto em outputs/
```

Sem editor. Sem Premiere. Sem aparecer.

---

## 🎯 Pra quem é

- **Produtor lowticket** que precisa escalar criativo sem editor
- **Afiliado** que clona copy vencedora do concorrente com seu produto
- **Dropshipper** que gera 10 variações por dia
- **Ecom** que testa 5 ângulos sem gravar nada
- **Agência** que precisa entregar UGC em escala

---

## 🧰 Stack — tudo grátis ou no rateio

| Função | Ferramenta | Modo | Custo |
|--------|------------|------|-------|
| Avatar talking head | **HeyGen** | UI manual | plano pago* |
| Imagem + animação vídeo | **SuperGrok / Grok Imagine** | UI manual | plano pago* |
| Voiceover (opcional) | **ElevenLabs** | API | grátis 10k chars/mês |
| B-roll fallback | **Pexels** / **Pixabay** | API | grátis ∞ |
| Música automática | **Jamendo** | API | grátis 35k tracks |
| **Polish final** (kinetic captions, transitions shader, grain, vignette, end CTA) | **HyperFrames** (HeyGen OSS Apache 2.0) | local CLI + Bun + Chromium | grátis ∞ |
| Transcrição word-level | **faster-whisper** | local CPU | grátis |
| Montagem intermediária | **ffmpeg** | local | grátis |
| Agente | **Claude Code** / **Codex CLI** / **Gemini CLI** | local | seu plano |

\* Não tem HeyGen + SuperGrok + ElevenLabs Starter pagos?

👉 **Rateio Ferramentas IA (RATEAKI)** → https://rateaki.geekacademy.site (acesso compartilhado por uma fração do preço)

---

## 🤖 Escolha seu agente — funciona em 3

| Agente | Arquivo de regras | Instalação |
|--------|-------------------|------------|
| **Claude Code** (recomendado) | `CLAUDE.md` | https://claude.com/claude-code |
| **OpenAI Codex CLI** | `AGENTS.md` | `npm i -g @openai/codex` |
| **Gemini CLI** | `GEMINI.md` | `npm i -g @google/gemini-cli` |

Os três leem o mesmo workflow.

---

# 🛠️ INSTALAÇÃO — passo a passo

### Passo 1 — Clonar este repositório

```bash
git clone https://github.com/Geeknosnegocios/geekclaudeUGC.git
cd geekclaudeUGC
```

### Passo 2 — Instalar Python 3.10+

- **Windows:** https://www.python.org/downloads/windows/ (marca "Add Python to PATH")
- **Mac:** `brew install python@3.11`
- **Linux:** `sudo apt install python3 python3-pip`

```bash
python --version    # Deve mostrar Python 3.10+
```

### Passo 3 — Instalar dependências Python

```bash
pip install -r requirements.txt
```

### Passo 4 — Instalar ffmpeg

- **Windows:** `winget install ffmpeg` ou `scoop install ffmpeg`
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

> Não conseguiu? Tranquilo, `imageio-ffmpeg` (já instalado no Passo 3) tem ffmpeg embutido.

### Passo 5 — Instalar Bun (runtime do HyperFrames)

```bash
# Windows (PowerShell)
powershell -c "irm bun.sh/install.ps1 | iex"

# Mac/Linux
curl -fsSL https://bun.sh/install | bash
```

### Passo 6 — Instalar HyperFrames (polish layer)

```bash
mkdir -p vendor
git clone --depth=1 https://github.com/heygen-com/hyperframes.git vendor/hyperframes
cd vendor/hyperframes
bun install
bun run build
cd ../..
```

Vai baixar Chromium (~170 MB) — leva ~2 min na primeira vez.

### Passo 7 — Criar o `.env`

```bash
cp .env.example .env
```

Edita o `.env` e preenche cada chave:

```env
PEXELS_KEY=sua_chave_aqui
PIXABAY_KEY=sua_chave_aqui
ELEVEN_KEY=sua_chave_aqui
ELEVEN_VOICE_ID=cgSgspJ2msm6clMCkdW9
JAMENDO_CLIENT_ID=seu_client_id_aqui
```

**Como pegar cada chave (5 min total):**

#### `PEXELS_KEY` — grátis ∞
1. Acesse https://www.pexels.com/api/
2. Crie conta
3. Copia "Authorization" key da página
4. Cola no `.env`

#### `PIXABAY_KEY` — grátis ∞
1. Acesse https://pixabay.com/accounts/register/
2. Após login → https://pixabay.com/accounts/profile/ → tab **API**
3. Copia + cola

#### `ELEVEN_KEY` — grátis 10k chars/mês
1. https://elevenlabs.io → criar conta
2. **Profile → API Key**
3. Copia + cola

#### `ELEVEN_VOICE_ID` — voz padrão Jessica (multilingual, free OK)
Já vem preenchido `cgSgspJ2msm6clMCkdW9`. Pra voz PT-BR nativa Larissa (paid Starter $5/mo OU rateio):
```env
ELEVEN_VOICE_ID=OjcGK1RXdMD1PFj2eIuN
```

#### `JAMENDO_CLIENT_ID` — música grátis, 35k tracks
1. https://devportal.jamendo.com → Sign Up
2. **My Apps → Create new app**
3. Copia o Client ID
4. Cola no `.env`

### Passo 8 — Abrir agente nessa pasta

```bash
claude       # OR
codex        # OR
gemini
```

Pronto. Setup completo em ~15 min.

---

# 🎬 PRIMEIRO AD — passo a passo (template 03 faceless lifestyle)

Esse template é o mais completo do repo: usa SuperGrok pra clips + ElevenLabs pra voz + Jamendo pra música + HyperFrames pra polish. Zero rosto, zero gravação.

### Passo 1 — Achar o ad referência

#### Onde procurar

| Biblioteca | URL | Login | Cobertura |
|------------|-----|-------|-----------|
| **TikTok Creative Center** ✅ | https://ads.tiktok.com/business/creativecenter/topads/pc/en | conta TikTok | Global incl. BR |
| **Meta Ad Library** ✅ | https://www.facebook.com/ads/library | nenhum | Global incl. BR |
| ~~TikTok Ad Library~~ ❌ | ~~https://library.tiktok.com~~ | — | **EU/EEA only** |

#### Filtros pra Skincare BR (exemplo)

No TikTok Creative Center → painel esquerdo:

| Filtro | Valor |
|--------|-------|
| Região | Brasil |
| Setor | Beleza e Cuidados Pessoais |
| Objetivo | Conversões |
| Tempo | Últimos 30 dias |
| Idioma do anúncio | Português |
| Formato | Vídeo |
| Ordenar por | CTR |

Busca: `sérum`, `pele de vidro`, `clareamento`, `acne`, `mancha`.

#### Critérios do ad vencedor

- ✅ Vertical 9:16
- ✅ Pessoa falando + produto na mão
- ✅ 12-25s de duração
- ✅ Hook nos primeiros 1.5s
- ✅ CTR > 1%
- ✅ Rodando 30+ dias

#### Como baixar o MP4

Creative Center não tem botão download direto. Use:
- **DevTools Network tab** (F12 → aba Network → Media → Play vídeo → click direito no .mp4 → Open in new tab → Save video as)
- **Video DownloadHelper** extension Chrome/Firefox
- **OBS Studio** screen capture
- **Win+G** (Xbox Game Bar) gravação

**Salva em:**
```
c:\Users\freit\Documents\claude-arcads\01_talking_head\assets\reference.mp4
```

### Passo 2 — Joga referência no agente

Cole no chat:

```
Clona esse ad pra mim. É de skincare. Vou anunciar meu produto Lucrown Silky Skin Oil.
Aqui está a foto do produto: [anexa imagem]
Referência salva em: 01_talking_head/assets/reference.mp4
```

### Passo 3 — Agente analisa e entrega briefing

O agente vai:
1. **Transcrever** referência via faster-whisper (local, 3s pra 15s de áudio)
2. **Mapear beats** (hook + problem + solution + benefit + CTA)
3. **Reescrever script PT-BR** pra seu produto
4. **Pivot template** automaticamente baseado no que faz mais sentido (talking head, unboxing, faceless, app promo, extend)
5. **Entregar briefing completo** com:
   - Script PT-BR copy-paste
   - Briefing HeyGen (avatar, voice, instruções)
   - Prompts SuperGrok (3-6 clips de 6s cada)
   - Asset checklist exato com caminhos
   - Comando final pra rodar

> 💎 *Quer aprender a ler ads vencedores + adaptar pro seu produto?*
> *Formação Produtor Milionário → https://produtor.geekacademy.site*

### Passo 4 — Aprova + gera HeyGen avatar (se template usa)

Você responde "go" / "manda".

1. Abre https://app.heygen.com/
2. **Create Video → AI Avatar / Avatar IV**
3. Cola script + escolhe avatar+voice sugeridos
4. Aspect **9:16 vertical**, 720p+
5. **Generate** (1-3 min)
6. **Download** → salva exatamente no caminho indicado

> 🛠️ *Sem HeyGen pago? **Rateio Ferramentas IA** → https://rateaki.geekacademy.site*

### Passo 5 — Gera 4 clips via SuperGrok

Pra templates 02 e 03 (precisam de clips de produto/cena):

1. Abre https://grok.com/
2. Usa **Grok Imagine** → cola cada prompt do agente
3. Espera gerar imagem
4. Clica **Animate / Make Video**
5. Aspect **9:16 vertical**, **6 segundos**
6. Download MP4
7. Salva em `<template>/assets/clips/clip_01.mp4`, `clip_02.mp4`, ...

⚠️ **Importante:** confirma que o aspect ratio no Grok está em **9:16** explícito — se gerar 1:1 quadrado, vídeo final fica com letterbox preto.

### Passo 6 — (Opcional) Voiceover

Pra template 03, voiceover é separado. 2 opções:

**A. Auto-gera via ElevenLabs** (usado no comando do agente com `--tts "TEXTO"`)
**B. Grava no celular** → salva como `assets/voiceover.mp3`

### Passo 7 — Roda o build base

O agente executa por você:

```bash
python 03_faceless_lifestyle/build.py --tts "SCRIPT PT-BR AQUI" --srt
```

Saída esperada (~10s):
```
=== 03 Faceless Lifestyle v1 ===
[tts] ElevenLabs -> voiceover.mp3
[1/5] transcribe voiceover (faster-whisper)
[2/5] using 4 SuperGrok clips
[3/5] normalize + trim each clip
[4/5] concat clips
[5/5] mux voiceover + music
     no manual music.mp3, fetching from Jamendo (tags='ambient')
  [music] Headphonetic - Revolution Void (8140 KB)
DONE -> outputs/lifestyle_v1.mp4 (2396 KB)
     srt -> outputs/lifestyle_v1.srt
```

### Passo 8 — Polish via HyperFrames (kinetic captions + transitions + CTA card)

```bash
# 1. Scaffold composition
bin/hf init compositions/meu_ad --no-install

# 2. Copia assets (clips, voiceover, music) pra composition folder
cp 03_faceless_lifestyle/assets/clips/*.mp4 compositions/meu_ad/
cp 03_faceless_lifestyle/assets/voiceover.mp3 compositions/meu_ad/
cp 03_faceless_lifestyle/assets/music.mp3 compositions/meu_ad/

# 3. Browse + add blocks do catálogo (85+ disponíveis)
bin/hf catalog list
bin/hf add caption-highlight whip-pan grain-overlay vignette shimmer-sweep tiktok-follow

# 4. Edita compositions/meu_ad/index.html
#    (peça pro Claude clonar a estrutura de compositions/lucrown_ad/index.html)

# 5. Lint + render
bin/hf lint
bin/hf render -o 03_faceless_lifestyle/outputs/meu_ad_hf.mp4
```

**Reference composition pronta:** `compositions/lucrown_ad/` (15.5s, TikTok red captions, white-flash transitions, lower-third brand, end CTA card, shimmer pill, grain, vignette, progress bar).

### Passo 9 — Sobe pro TikTok / Reels

Pega `outputs/meu_ad_hf.mp4` (ou `lifestyle_v1.mp4` se pulou polish). Sobe direto.

Rodou mais uma vez? Vira `_v2.mp4`. Auto-versionado.

> 💎 *Pipeline UGC completo + estratégia lowticket pra primeira venda no mesmo dia:*
> *Formação Produtor Milionário → https://produtor.geekacademy.site*

---

# 📚 OS 5 TEMPLATES

| # | Template | Quando usar |
|---|----------|-------------|
| 01 | `talking_head` | Influencer falando direto pra câmera. HeyGen + music. |
| 02 | `product_unboxing` | Reação abrindo caixa. HeyGen intro+outro + SuperGrok clips do produto. |
| 03 | `faceless_lifestyle` | Mãos, pés, produto. Sem rosto. SuperGrok clips + ElevenLabs voiceover + Jamendo music. |
| 04 | `app_promo` | Talking head + cortes screen recording app. HeyGen + screen rec. |
| 05 | `extend_and_stitch` | Junta 2+ MP4s em vídeo único, normalizados + música. |

---

# 🎨 CATÁLOGO HYPERFRAMES — 85 blocks pra polish ilimitado

Tudo grátis, instalável via `bin/hf add <nome>`:

**Captions (15 estilos):**
- `caption-highlight` (TikTok red sweep)
- `caption-pill-karaoke`
- `caption-neon-glow`
- `caption-particle-burst`
- `caption-glitch-rgb`
- `caption-matrix-decode`
- `caption-kinetic-slam`
- `caption-gradient-fill`
- `caption-emoji-pop`
- `caption-texture`
- `caption-weight-shift`
- `caption-clip-wipe`
- ... (+3 outros)

**Transitions shader (12 efeitos):**
- `whip-pan` (camera whip)
- `flash-through-white` (white impact)
- `light-leak` (cinematic warm)
- `sdf-iris` (iris reveal)
- `ripple-waves`
- `gravitational-lens`
- `cinematic-zoom`
- `chromatic-radial-split`
- `glitch`
- `swirl-vortex`
- `thermal-distortion`
- `cross-warp-morph`

**Effects:**
- `grain-overlay` (film texture)
- `vignette` (cinematic focus)
- `shimmer-sweep` (premium accent)
- `grid-pixelate-wipe`
- `texture-mask-text`
- `parallax-zoom` / `parallax-unzoom`

**Social overlays:**
- `tiktok-follow` / `instagram-follow` / `yt-lower-third`
- `x-post` / `reddit-post` / `spotify-card`
- `macos-notification`

**Data viz:**
- `data-chart`, `us-map`, `world-map`, `spain-map`, `flowchart`

**VFX 3D / WebGL:**
- `vfx-iphone-device` (iPhone 15 Pro Max model)
- `vfx-liquid-background`
- `ios26-liquid-glass`, `macos-tahoe-liquid-glass`
- `vfx-shatter`, `vfx-portal`, `vfx-magnetic`

**Showcase blocks:**
- `apple-money-count`, `vpn-youtube-spot`, `nyc-paris-flight`, `app-showcase`

```bash
bin/hf catalog list   # ver tudo
bin/hf docs <topic>   # docs locais
```

---

## 📁 Estrutura do repositório

```
geekclaudeUGC/
├── CLAUDE.md / AGENTS.md / GEMINI.md   ← regras pros 3 agentes
├── README.md                            ← este arquivo
├── .env.example                         ← template chaves
├── .gitignore                           ← ignora .env, mídia, vendor
├── requirements.txt                     ← deps Python
├── bin/
│   ├── hf                               ← wrapper HyperFrames CLI (Mac/Linux)
│   └── hf.cmd                           ← wrapper HyperFrames CLI (Windows)
├── lib/                                 ← helpers Python
│   ├── version.py                       ← auto v1/v2/v3
│   ├── ffmpeg_path.py                   ← locador ffmpeg
│   ├── stock.py                         ← Pexels API
│   ├── audio.py                         ← ElevenLabs TTS
│   ├── music.py                         ← Jamendo API auto-music
│   ├── transcribe.py                    ← faster-whisper + .srt
│   ├── hg.py                            ← briefing HeyGen
│   └── grok.py                          ← briefing SuperGrok
├── 01_talking_head/      → assets/ + outputs/ + build.py
├── 02_product_unboxing/  → assets/clips/ + outputs/ + build.py
├── 03_faceless_lifestyle/→ assets/clips/ + outputs/ + build.py
├── 04_app_promo/         → assets/ + outputs/ + build.py
├── 05_extend_and_stitch/ → assets/ + outputs/ + build.py
├── compositions/
│   └── lucrown_ad/                     ← composição HyperFrames reference (copia daqui)
│       ├── index.html
│       ├── compositions/                ← blocks instalados
│       │   ├── whip-pan.html
│       │   ├── flash-through-white.html
│       │   ├── light-leak.html
│       │   ├── tiktok-follow.html
│       │   └── components/
│       │       ├── caption-highlight.html
│       │       ├── grain-overlay.html
│       │       ├── vignette.html
│       │       └── shimmer-sweep.html
│       ├── hyperframes.json
│       └── package.json
└── vendor/
    └── hyperframes/                    ← clone HeyGen OSS (gitignored)
```

---

## ❓ FAQ

**P: Preciso pagar HeyGen e SuperGrok?**
R: Free tier HeyGen tem watermark + sem download MP4 limpo. Free tier SuperGrok não existe. Pra qualidade pro, sim. **Sem assinar, use o rateio:** 👉 https://rateaki.geekacademy.site

**P: Funciona sem GPU?**
R: Sim. ffmpeg + Whisper rodam CPU. HyperFrames usa Chromium headless (CPU + GPU integrada OK).

**P: Os MP4s saem com watermark?**
R: Não. HeyGen + SuperGrok pagos entregam limpo. HyperFrames/ffmpeg copiam sem mexer.

**P: Em quanto tempo eu monto um ad?**
R: ~15-20 min total. Maiores gargalos: HeyGen gera ~2min, SuperGrok ~3min por clip.

**P: Funciona em inglês?**
R: Sim. Diz pro agente *"in English"* e ele troca tudo. ELEVEN_VOICE_ID padrão é multilingual.

**P: E copyright dos ads que eu clono?**
R: Você não copia o vídeo. Copia **conceito + estrutura de script** + produz do zero. Mesma lógica que toda agência usa.

**P: Arquivos privados (clips, voiceover, .env) vão pro GitHub?**
R: Não. `.gitignore` exclui `.mp4`, `.mp3`, `.png`, `.jpg`, `.srt`, `.env`, `vendor/`, `node_modules/`.

**P: Posso vender ads gerados aqui pra clientes?**
R: Sim. Cobra agência $50-200 por ad, ~15 min trabalho. Quer aprender a fazer escala?
👉 https://produtor.geekacademy.site

---

## 🐛 Troubleshooting

| Erro | Causa | Fix |
|------|-------|-----|
| `PEXELS_KEY missing` | `.env` vazio | Preenche chave em `.env` (Passo 7 setup) |
| `ELEVEN_KEY missing` | idem | idem |
| `JAMENDO_CLIENT_ID missing` | idem | https://devportal.jamendo.com |
| `Missing: assets/heygen.mp4` | Não salvou HeyGen export | Re-gera + salva no caminho exato |
| `Need >=2 clips in assets/clips/` | SuperGrok não rodou | Gera pelo menos 2 clips |
| `ElevenLabs TTS failed 402: paid_plan_required` | Voz library precisa paid | Use voice ID free (Jessica `cgSgspJ2msm6clMCkdW9`) ou plano Starter |
| `ffmpeg not found` | binário não no PATH | `pip install imageio-ffmpeg` |
| Vídeo com letterbox preto | Clips SuperGrok não 9:16 | Re-gera no Grok com aspect 9:16 explícito |
| `bun: command not found` | Bun não instalado | Passo 5 setup |
| `node packages/cli/dist/cli.js: ENOENT` | HyperFrames não buildado | `cd vendor/hyperframes && bun run build` |
| Render HyperFrames trava | Chromium não baixou | Passo 6 setup, aguarda ~170MB download |

---

## 🚀 Roadmap

- [ ] Template 06 — Reaction split-screen
- [ ] Auto-upload TikTok/Instagram via UI automation
- [ ] Detector hook strength primeiros 3s
- [ ] Gerador batch — 5 variações de script + 5 voiceovers + 5 renders por ad
- [ ] Skill `/hyperframes` slash command integrado nativo Claude Code

---

## 📄 Licença

MIT. Faz o que quiser. Atribui se for legal.

---

## 🧠 Créditos

Construído por **Geek nos Negócios** + Claude.

Stack baseado em:
- **HyperFrames** by HeyGen (Apache 2.0) — https://github.com/heygen-com/hyperframes
- **faster-whisper** (MIT) — local Whisper inference
- **ElevenLabs** API — TTS
- **Jamendo** API — royalty-free music
- **Pexels** + **Pixabay** APIs — stock images/videos
- **ffmpeg** — montagem

---

## 💎 Links importantes

- 🎓 **Formação Produtor Milionário** *(lowticket no ar em 1h, primeira venda no mesmo dia, com Claude)* → https://produtor.geekacademy.site
- 🛠️ **Rateio Ferramentas IA (RATEAKI)** *(HeyGen + SuperGrok + ElevenLabs + outras pagas, compartilhado)* → https://rateaki.geekacademy.site
- 📺 **YouTube Geek nos Negócios** → busca por "Geeknosnegocios"
- 💻 **Repositório oficial** → https://github.com/Geeknosnegocios/geekclaudeUGC

---

> **Lowticket no ar em 1 hora. Primeira venda no mesmo dia. Com Claude.**
> 👉 https://produtor.geekacademy.site
