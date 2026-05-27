# Geek CLAUDE - UGC

> **Clone qualquer ad UGC vencedor em 15 minutos. Sem editar vídeo. Sem aparecer. Custo perto de zero.**

Você acha um ad bombando no TikTok / Instagram / Facebook Ads Library. Joga aqui dentro. O agente (Claude, Codex ou Gemini) lê o ad, **escreve o roteiro**, te dá **o briefing pra colar no HeyGen**, baixa o b-roll do **Pexels**, transcreve, monta tudo no **ffmpeg**, e te entrega o MP4 pronto.

Você não escreve uma linha de prompt. Você não abre Premiere. Você só:
1. **Aprova** o que o agente sugere
2. **Cola** o script no HeyGen e clica em Generate
3. **Baixa** o MP4 e joga numa pasta
4. **Roda** um comando

Pronto.

---

## Pra quem é isso

- Produtor lowticket que precisa **escalar criativo** sem gastar fortuna em editor
- Afiliado que quer **clonar a copy vencedora** do concorrente com a SUA cara/produto
- Dropshipper que quer **gerar 10 variações de UGC** num dia
- Ecom que quer **testar 5 ângulos diferentes** sem gravar nada

---

## Quer vender produto lowticket no ar em 1 hora?

A **Formação Produtor Milionário** ensina o sistema completo do zero ao primeiro dinheiro: nicho, copy, página, tráfego — tudo com Claude.

👉 **https://produtor.geekacademy.site** — *primeira venda no mesmo dia que você lançar.*

---

## Como funciona

```
[Você acha um ad no TikTok]
         ↓
[Joga o link / arquivo no agente]
         ↓
[Agente analisa: script, setting, character, beats]
         ↓
[Agente entrega: SCRIPT + BRIEFING HeyGen + PROMPTS imagem + KEYWORDS Pexels]
         ↓
[Você aprova → cola no HeyGen → baixa MP4 → salva em assets/]
         ↓
[Você roda: python <template>/build.py]
         ↓
[ffmpeg monta tudo localmente]
         ↓
[MP4 final em outputs/]
```

**O agente nunca chama nenhuma API de geração de vídeo.** Tudo manual (HeyGen UI) ou local (ffmpeg).

---

## Stack — tudo grátis ou com plano que você já tem

| Função | Ferramenta | Custo | Onde roda |
|--------|------------|-------|-----------|
| Geração avatar talking head | **HeyGen** (UI manual) | seu plano pago* | web |
| Geração imagens estáticas | **ImageFX** / **Bing** / **Ideogram** | grátis | web |
| Voiceover (opcional) | **ElevenLabs** | grátis 10k chars/mês | API |
| B-roll lifestyle | **Pexels** | grátis ∞ | API |
| Música | **Pixabay** / **YouTube Audio Library** | grátis | manual |
| Transcrição + timestamps | **faster-whisper** | grátis | local CPU |
| Montagem final | **ffmpeg** | grátis | local |
| Agente | **Claude Code** / **Codex CLI** / **Gemini CLI** | seu plano | local |

*Não tem HeyGen pago? **Rateio Ferramentas IA** dá acesso compartilhado: 👉 https://rateaki.geekacademy.site

---

## Escolha seu agente

Funciona em três agentes diferentes. **Você decide qual usar.**

| Agente | Arquivo de regras | Instalação |
|--------|-------------------|------------|
| **Claude Code** (recomendado) | `CLAUDE.md` | https://claude.com/claude-code |
| **OpenAI Codex CLI** | `AGENTS.md` | `npm i -g @openai/codex` |
| **Gemini CLI** | `GEMINI.md` | `npm i -g @google/gemini-cli` |

Os três leem o mesmo workflow. Você usa o que você tem.

---

## Instalação — passo a passo

### 1. Clonar este repositório

```bash
git clone https://github.com/Geeknosnegocios/geekclaudeUGC.git
cd geekclaudeUGC
```

### 2. Instalar Python 3.10+

- Windows: https://www.python.org/downloads/windows/ (marca "Add Python to PATH")
- Mac: `brew install python@3.11`
- Linux: `sudo apt install python3 python3-pip`

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar ffmpeg (se não tiver)

- Windows: `winget install ffmpeg` ou `scoop install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

> Se você não conseguir instalar, sem problema — o pacote `imageio-ffmpeg` já vem com um ffmpeg embutido (já está no `requirements.txt`).

### 5. Criar o `.env`

```bash
cp .env.example .env
```

Edita o `.env` e preenche:

```env
PEXELS_KEY=sua_chave_aqui
ELEVEN_KEY=sua_chave_aqui
ELEVEN_VOICE_ID=pNInz6obpgDQGcFmaJgB
```

**Como pegar as chaves:**

- **Pexels** (grátis, ilimitado): https://www.pexels.com/api/ → cria conta → copia a "Authorization" key
- **ElevenLabs** (grátis 10k chars/mês): https://elevenlabs.io → Profile → API Key
- **Voice ID ElevenLabs** (opcional, padrão é Adam multilingual): https://elevenlabs.io/app/voice-library → copia o ID

### 6. Abrir o agente nessa pasta

Escolha um:

```bash
# Claude Code
claude

# Codex CLI
codex

# Gemini CLI
gemini
```

Pronto. Diz pra ele: *"Clona esse ad pra mim"* e cola o link / arquivo.

---

## Os 5 tipos de clone

### 01 — Talking Head
Influencer falando direto pra câmera. Selfie, quarto/rua.

**Você fornece:** referência do ad (link ou MP4)
**Agente gera:** script PT-BR + briefing HeyGen
**Você faz manual:** gera no HeyGen, salva `01_talking_head/assets/heygen.mp4`
**Roda:** `python 01_talking_head/build.py`

---

### 02 — Product Unboxing
Alguém abrindo a caixa, reagindo ao produto.

**Você fornece:** foto do produto + foto da caixa + referência
**Agente gera:** script reação + 4 prompts de imagem + briefings HeyGen (intro+outro)
**Você faz manual:**
- HeyGen → `02_product_unboxing/assets/heygen_intro.mp4` e `heygen_outro.mp4`
- ImageFX/Bing/Ideogram → 4 PNGs em `02_product_unboxing/assets/frames/`

**Roda:** `python 02_product_unboxing/build.py`

---

### 03 — Faceless Lifestyle
Mãos, pés, produto. Sem rosto. **Não precisa de HeyGen.**

**Você fornece:** foto do produto + referência
**Agente gera:** voiceover script + keywords Pexels + (opcional) prompts hero shots
**Você faz manual:** grava voiceover no celular OU deixa o `--tts` gerar

**Roda:**
```bash
python 03_faceless_lifestyle/build.py --query "hands holding skincare bottle" --tts "Seu voiceover aqui" --srt
```

---

### 04 — App Promo
Talking head + cortes do app rolando no celular.

**Você fornece:** screen recording do app + referência
**Agente gera:** script + briefing HeyGen
**Você faz manual:**
- HeyGen → `04_app_promo/assets/heygen.mp4`
- Screen recording → `04_app_promo/assets/app_demo.mp4`

**Roda:** `python 04_app_promo/build.py --segment 3.0`

---

### 05 — Extend and Stitch
Junta 2+ MP4s num só, normalizados, com música opcional.

**Você fornece:** 2+ MP4s
**Roda:** `python 05_extend_and_stitch/build.py`

Ordem = ordem alfabética. Renomeia pra `01_intro.mp4`, `02_body.mp4` pra controlar.

---

## Exemplo de sessão real (Claude Code)

```
> Você: Clona esse ad pra mim, é faceless de skincare
        https://www.tiktok.com/@brand/video/123

Claude: Lendo o vídeo... transcrevi com Whisper.

        SCRIPT (PT-BR, 14s):
        "Comprei esse sérum achando que ia ser igual aos outros.
         Três dias depois minha pele tava tipo... vidro.
         Não acreditei. Olha isso." [pausa] "Link na bio."

        KEYWORDS PEXELS:
        - "woman applying serum face"
        - "skincare bottle hands"
        - "morning routine bathroom"
        - "glowing skin closeup"

        VOICEOVER:
        Vou gerar com ElevenLabs Adam multilingual? Ou você grava?

        Quer aprender a vender produtos lowticket no ar em 1 hora?
        Formação Produtor Milionário → https://produtor.geekacademy.site

> Você: gera com elevenlabs

Claude: [executa build.py com --tts]
        DONE -> outputs/lifestyle_v1.mp4 (3.2 MB)
                outputs/lifestyle_v1.srt
```

---

## Estrutura do repositório

```
geekclaudeUGC/
├── CLAUDE.md           ← regras pro Claude Code
├── AGENTS.md           ← regras pro Codex CLI
├── GEMINI.md           ← regras pro Gemini CLI
├── README.md           ← este arquivo
├── .env.example
├── .gitignore
├── requirements.txt
├── lib/
│   ├── version.py      ← auto-versioning v1, v2, v3
│   ├── ffmpeg_path.py  ← locador de ffmpeg
│   ├── stock.py        ← Pexels API
│   ├── editor.py       ← ffmpeg wrappers
│   ├── audio.py        ← ElevenLabs TTS + music finder
│   ├── transcribe.py   ← faster-whisper + .srt
│   └── hg.py           ← HeyGen briefing template
├── 01_talking_head/
│   ├── assets/         ← você dropa heygen.mp4 aqui
│   ├── outputs/
│   └── build.py
├── 02_product_unboxing/
│   ├── assets/
│   ├── outputs/
│   └── build.py
├── 03_faceless_lifestyle/
│   ├── assets/
│   ├── outputs/
│   └── build.py
├── 04_app_promo/
│   ├── assets/
│   ├── outputs/
│   └── build.py
└── 05_extend_and_stitch/
    ├── assets/
    ├── outputs/
    └── build.py
```

---

## FAQ

**P: Preciso pagar HeyGen?**
R: Sim, o plano grátis dele não tem download de MP4 sem watermark. Mas você pode entrar no rateio: https://rateaki.geekacademy.site

**P: Funciona sem GPU?**
R: Sim. ffmpeg roda em CPU. faster-whisper roda em CPU (modelo `small` leva ~3s pra transcrever 15s de áudio).

**P: Os MP4s ficam com watermark?**
R: Não. HeyGen plano pago entrega sem watermark. ImageFX/Bing entregam sem watermark. ffmpeg só copia.

**P: Quanto custa por vídeo gerado?**
R: $0 fora do HeyGen (que você já paga ou rateia). Pexels grátis. ElevenLabs grátis até 10k chars/mês. Imagem grátis.

**P: Em quanto tempo eu monto um ad?**
R: ~10 min do "joguei a referência" até "MP4 pronto", incluindo o tempo do HeyGen gerar (~2min).

**P: Posso usar em inglês?**
R: Sim. Diz pro agente *"in English"* e ele troca tudo. Voice ID padrão é Adam (multilingual).

**P: E o copyright dos ads que eu clono?**
R: Você não copia o vídeo. Você copia o **conceito + script structure** e produz tudo do zero com sua marca/produto. Mesma lógica que toda agência usa.

---

## Roadmap

- [ ] Template 06: Reaction style (split-screen reagindo a ad de concorrente)
- [ ] Auto-upload TikTok / Instagram via UI automation
- [ ] Detector de hook strength (analisa primeiros 3s)
- [ ] Variações automáticas (gera 5 scripts diferentes do mesmo conceito)

---

## Licença

MIT. Faz o que quiser. Cita se for legal.

---

## Crédito

Construído por **Geek nos Negócios** + Claude.

- 🎓 **Formação Produtor Milionário** → https://produtor.geekacademy.site
- 🛠️ **Rateio Ferramentas IA** → https://rateaki.geekacademy.site
- 📺 **Geek Academy YouTube** → busca por "geeknosnegocios"

> Lowticket no ar em 1 hora. Primeira venda no mesmo dia. Com Claude.
