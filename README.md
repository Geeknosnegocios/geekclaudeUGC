# Geek CLAUDE - UGC

> **Clone qualquer ad UGC vencedor em 15 minutos. Sem editar vídeo. Sem aparecer.**

Acha um ad bombando no TikTok. Cola aqui. O agente lê, escreve o roteiro, te dá o briefing pra colar no HeyGen e SuperGrok, e monta o MP4 final pronto pra subir. Tudo automatizado, exceto 2-3 cliques manuais.

---

## ⚡ Em 3 passos

```
1. Joga referência no agente   →   "Clona esse ad pra mim"
2. Agente entrega script + briefing HeyGen + prompts SuperGrok
3. Você cola, baixa MP4, roda 1 comando   →   ad pronto em outputs/
```

---

## 🎯 Pra quem

- **Produtor lowticket** que precisa escalar criativo sem editor
- **Afiliado** que clona a copy vencedora do concorrente
- **Dropshipper** que gera 10 variações por dia
- **Ecom** que testa 5 ângulos sem gravar nada

> 💎 **Lowticket no ar em 1h. Primeira venda no mesmo dia.**
> 👉 Formação Produtor Milionário → https://produtor.geekacademy.site

---

## 🧰 Stack

| Função | Ferramenta | Modo | Custo |
|--------|------------|------|-------|
| Avatar talking head | **HeyGen** | UI manual | plano pago* |
| Imagem + animação vídeo | **SuperGrok / Grok Imagine** | UI manual | plano pago* |
| Voiceover (opcional) | **ElevenLabs** | API | grátis 10k chars/mês |
| B-roll fallback | **Pexels** | API | grátis ∞ |
| Música | **Pixabay / YouTube Audio Library** | manual | grátis |
| Transcrição | **faster-whisper** | local CPU | grátis |
| Montagem final | **ffmpeg** | local | grátis |
| Agente | **Claude Code** / **Codex** / **Gemini** | local | seu plano |

\* Não tem HeyGen / SuperGrok? **Rateio Ferramentas IA** dá acesso compartilhado:
👉 https://rateaki.geekacademy.site

---

## 🤖 Funciona com 3 agentes

| Agente | Arquivo regras | Instalação |
|--------|----------------|------------|
| **Claude Code** (recomendado) | `CLAUDE.md` | https://claude.com/claude-code |
| **OpenAI Codex CLI** | `AGENTS.md` | `npm i -g @openai/codex` |
| **Gemini CLI** | `GEMINI.md` | `npm i -g @google/gemini-cli` |

Os três leem o mesmo workflow. Use o que você já tem.

---

# 🛠️ INSTALAÇÃO — passo a passo

### Passo 1 — Clone o repositório

```bash
git clone https://github.com/Geeknosnegocios/geekclaudeUGC.git
cd geekclaudeUGC
```

### Passo 2 — Instale Python 3.10+

- **Windows:** https://www.python.org/downloads/windows/
  *(marque "Add Python to PATH" durante instalação)*
- **Mac:** `brew install python@3.11`
- **Linux:** `sudo apt install python3 python3-pip`

Verifica:
```bash
python --version
# Deve mostrar Python 3.10 ou superior
```

### Passo 3 — Instale as dependências

```bash
pip install -r requirements.txt
```

Instala: `requests`, `python-dotenv`, `imageio-ffmpeg`, `faster-whisper`, `elevenlabs`.

### Passo 4 — Instale o ffmpeg (opcional)

- **Windows:** `winget install ffmpeg` ou `scoop install ffmpeg`
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

> Não conseguiu instalar? Tranquilo. O pacote `imageio-ffmpeg` (já instalado no passo 3) tem um ffmpeg embutido que vai funcionar.

### Passo 5 — Crie o arquivo `.env`

```bash
cp .env.example .env
```

Abra o `.env` no seu editor e preencha:

```env
PEXELS_KEY=sua_chave_aqui
ELEVEN_KEY=sua_chave_aqui
ELEVEN_VOICE_ID=pNInz6obpgDQGcFmaJgB
```

**Como pegar cada chave:**

#### `PEXELS_KEY` — grátis, ilimitado
1. Acesse https://www.pexels.com/api/
2. Crie uma conta
3. Copie a "Authorization" key da página
4. Cole no `.env`

#### `ELEVEN_KEY` — grátis 10k chars/mês
1. Acesse https://elevenlabs.io
2. Crie conta
3. Vá em **Profile → API Key**
4. Copie e cole no `.env`

#### `ELEVEN_VOICE_ID` — opcional
- Padrão é Adam multilingual (`pNInz6obpgDQGcFmaJgB`) — funciona PT-BR e EN
- Quer outra voz? https://elevenlabs.io/app/voice-library → escolhe → copia o ID

### Passo 6 — Abra o agente nessa pasta

Escolha um dos três:

```bash
# Claude Code
claude

# OR Codex CLI
codex

# OR Gemini CLI
gemini
```

**Pronto. Setup completo.**

---

# 🎬 PRIMEIRO AD — passo a passo

Vamos clonar um ad usando o template **01 — Talking Head** (mais simples).

### Passo 1 — Encontre o ad referência

Vá em uma dessas:
- **TikTok Ad Library** → https://library.tiktok.com (filtre por indústria, sort por impressões)
- **Meta Ad Library** → https://www.facebook.com/ads/library
- Salva o link OU baixa o MP4

Procure ads que estejam rodando há **30+ dias** — se ainda estão gastando, estão convertendo.

### Passo 2 — Joga no agente

Cole no chat do Claude/Codex/Gemini:

```
Clona esse ad pra mim:
https://www.tiktok.com/@brand/video/123456

É de skincare. Vou anunciar meu produto X (descrição curta).
```

### Passo 3 — Agente analisa e entrega

O agente vai te mostrar:

1. **Análise da referência:** script, setting, character, beats
2. **Script adaptado PT-BR** pro seu produto
3. **Briefing HeyGen** (avatar, voz, script pra colar)
4. **Lista de assets** que você precisa colocar em `assets/`

Exemplo do que ele entrega:

> **Script PT-BR (14s):**
> *"Você comprou um sérum achando que ia ser igual aos outros, né? Três dias depois sua pele tava tipo... vidro. Olha isso." [pausa] "Link na bio."*
>
> **Briefing HeyGen:**
> - URL: https://app.heygen.com/
> - Avatar: Yara (mulher PT-BR, 25-30, natural)
> - Voice: Yara PT-BR
> - Aspect: 9:16, 720p
> - Cole o script acima
> - Salve como `01_talking_head/assets/heygen.mp4`

### Passo 4 — Aprove e gera no HeyGen

Você responde "go" / "manda" / "ok".

1. Abra https://app.heygen.com/
2. **Create Video → AI Avatar** (ou Avatar IV)
3. Cole o script
4. Escolha o avatar e voice sugeridos
5. Aspect ratio **9:16 vertical**, 720p ou superior
6. Clique **Generate** (aguarde 1-3 min)
7. Clique **Download** → MP4
8. Salve em: `01_talking_head/assets/heygen.mp4`

> 💎 **Não tem HeyGen?** → https://rateaki.geekacademy.site

### Passo 5 — (Opcional) Música

Se quer música de fundo:

1. Baixa um instrumental em https://pixabay.com/music/ ou https://www.youtube.com/audiolibrary/music
2. Salva como `01_talking_head/assets/music.mp3`

> Pular esse passo deixa o ad só com a voz do HeyGen.

### Passo 6 — Roda o build

Volta no agente e diz "roda" / "manda".

Ele executa:

```bash
python 01_talking_head/build.py
```

Saída esperada (~10 segundos):

```
=== 01 Talking Head v1 ===
  source: 01_talking_head/assets/heygen.mp4
  music : 01_talking_head/assets/music.mp3
[1/3] normalize 720x1280@30fps
[2/3] loudnorm -16 LUFS
[3/3] overlay music bed (-22 dB)

DONE -> 01_talking_head/outputs/talking_head_v1.mp4 (3200 KB)
```

### Passo 7 — Sobe pro TikTok / Reels

Pega o `outputs/talking_head_v1.mp4`. Sobe direto no TikTok / Reels. **Pronto.**

> Rodou mais uma vez? Vira `talking_head_v2.mp4`. Auto-versionado. Nada sobrescrito.

---

# 📚 OS 5 TEMPLATES

### 01 — Talking Head
Influencer falando direto pra câmera. Selfie, bedroom ou outdoor.

**Você fornece:** referência (link/MP4 do ad)
**Agente gera:** script PT-BR + briefing HeyGen
**Você faz manual:** HeyGen → `01_talking_head/assets/heygen.mp4`
**Roda:** `python 01_talking_head/build.py`

---

### 02 — Product Unboxing
Alguém abrindo a caixa, reagindo ao produto.

**Você fornece:** foto produto + caixa + referência
**Agente gera:** script reação + briefings HeyGen (intro+outro) + 3-6 prompts SuperGrok

**Você faz manual:**
1. **HeyGen** → `02_product_unboxing/assets/heygen_intro.mp4` e `heygen_outro.mp4`
2. **SuperGrok Imagine** → `02_product_unboxing/assets/clips/clip_01.mp4`, `clip_02.mp4`, ...

**Roda:** `python 02_product_unboxing/build.py`

---

### 03 — Faceless Lifestyle
Mãos, pés, produto. Sem rosto. **Não precisa de HeyGen.**

**Você fornece:** foto produto + referência
**Agente gera:** voiceover script + prompts SuperGrok (primário) ou keywords Pexels (fallback)

**Você faz manual:**
- **SuperGrok Imagine** → `03_faceless_lifestyle/assets/clips/clip_01.mp4`, ...
- **Voiceover** → grava no celular (salva como `assets/voiceover.mp3`) OU deixa o `--tts` gerar via ElevenLabs

**Roda (com SuperGrok):**
```bash
python 03_faceless_lifestyle/build.py --tts "Seu voiceover aqui" --srt
```

**Roda (fallback Pexels — sem SuperGrok):**
```bash
python 03_faceless_lifestyle/build.py --query "hands holding cream" --tts "Seu voiceover aqui" --srt
```

> Flag `--srt` gera arquivo de legenda separado (não burna no vídeo).

---

### 04 — App Promo
Talking head + cortes do app rolando no celular.

**Você fornece:** screen recording do app + referência
**Agente gera:** script + briefing HeyGen + segment timing

**Você faz manual:**
- **HeyGen** → `04_app_promo/assets/heygen.mp4`
- **Screen recording** → `04_app_promo/assets/app_demo.mp4`

**Roda:** `python 04_app_promo/build.py --segment 3.0`

> `--segment 3.0` = alterna HeyGen ↔ app a cada 3s. Aumenta pra cortes mais longos.

---

### 05 — Extend and Stitch
Junta 2+ MP4s num só vídeo final, com música opcional.

**Você fornece:** 2+ MP4s em `05_extend_and_stitch/assets/`
**Roda:** `python 05_extend_and_stitch/build.py`

> Ordem = ordem alfabética. Renomeia pra `01_intro.mp4`, `02_body.mp4` pra controlar.

---

## 📁 Estrutura completa do repo

```
geekclaudeUGC/
├── CLAUDE.md              ← regras pro Claude Code
├── AGENTS.md              ← regras pro Codex CLI
├── GEMINI.md              ← regras pro Gemini CLI
├── README.md              ← este arquivo
├── .env.example
├── .gitignore
├── requirements.txt
├── lib/                   ← helpers reutilizáveis
│   ├── version.py         ← auto-versioning v1, v2, v3
│   ├── ffmpeg_path.py     ← localizador de ffmpeg
│   ├── stock.py           ← Pexels API (b-roll)
│   ├── editor.py          ← ffmpeg wrappers
│   ├── audio.py           ← ElevenLabs + music finder
│   ├── transcribe.py      ← faster-whisper + .srt
│   ├── hg.py              ← briefing HeyGen
│   └── grok.py            ← briefing SuperGrok
├── 01_talking_head/
│   ├── assets/            ← dropa heygen.mp4 (+ music.mp3 opcional)
│   ├── outputs/           ← MP4 final aparece aqui
│   └── build.py
├── 02_product_unboxing/
│   ├── assets/
│   │   ├── heygen_intro.mp4
│   │   ├── heygen_outro.mp4
│   │   └── clips/         ← clip_01.mp4, clip_02.mp4 ... (SuperGrok)
│   ├── outputs/
│   └── build.py
├── 03_faceless_lifestyle/
│   ├── assets/
│   │   ├── voiceover.mp3  ← (opcional, ou usa --tts)
│   │   └── clips/         ← clip_01.mp4 ... (SuperGrok)
│   ├── outputs/
│   └── build.py
├── 04_app_promo/
│   ├── assets/
│   │   ├── heygen.mp4
│   │   └── app_demo.mp4
│   ├── outputs/
│   └── build.py
└── 05_extend_and_stitch/
    ├── assets/
    ├── outputs/
    └── build.py
```

---

## ❓ FAQ

**P: Preciso pagar HeyGen e SuperGrok?**
R: Pra qualidade top, sim. Free tier do HeyGen tem watermark e não tem API. Sem assinar, use o rateio:
👉 https://rateaki.geekacademy.site

**P: Funciona sem GPU?**
R: Sim. Tudo aqui roda CPU. `faster-whisper` modelo `small` transcreve 15s em ~3s.

**P: Os MP4s saem com watermark?**
R: Não. HeyGen e SuperGrok planos pagos entregam limpo. ffmpeg só copia.

**P: Quanto custa por vídeo gerado pelo pipeline?**
R: $0 fora de HeyGen e SuperGrok (que você já paga ou rateia). Pexels grátis ∞. ElevenLabs grátis 10k chars/mês.

**P: Em quanto tempo eu monto um ad?**
R: ~10-15 min do "joguei a referência" até "MP4 pronto pra subir". Maior tempo é o HeyGen gerar (~2min) + SuperGrok gerar (~3min por clip).

**P: Funciona em inglês?**
R: Sim. Diz pro agente *"in English"* e ele troca tudo. Voice ID padrão é Adam (multilingual).

**P: E copyright dos ads que eu clono?**
R: Você não copia o vídeo. Copia o **conceito + estrutura de script** e produz tudo do zero com sua marca/produto. Mesma lógica que toda agência usa.

**P: Os arquivos do meu ad vão pro GitHub?**
R: Não. `.gitignore` ignora todos `.mp4`, `.mp3`, `.png`, `.jpg`, `.srt` e o `.env`. Só código vai pro repo.

**P: Posso vender ads gerados aqui pra clientes?**
R: Sim. Cobra agência: $50-200 por ad, ~15 min de trabalho seu. Quer aprender a faturar com lowticket?
👉 https://produtor.geekacademy.site

---

## 🐛 Troubleshooting

**Erro `PEXELS_KEY missing in .env`:**
- Você preencheu? `cat .env` (Mac/Linux) ou `type .env` (Windows) → confere se a chave tá lá.

**Erro `ELEVEN_KEY missing`:**
- Idem acima. Pega em https://elevenlabs.io/app/settings/api-keys

**Erro `Missing: 01_talking_head/assets/heygen.mp4`:**
- Você esqueceu de salvar o MP4 do HeyGen na pasta certa. Volta no passo 4.

**Erro `Need >=2 clips in assets/clips/`:**
- Você gerou só 1 clip no SuperGrok. Gera pelo menos 2 e nomeia `clip_01.mp4`, `clip_02.mp4`.

**Erro `ffmpeg not found`:**
- Roda `pip install imageio-ffmpeg` (vem com binário embutido).

**Vídeo final ficou sem áudio:**
- Confere que o HeyGen baixou COM áudio (não export "video only"). Re-baixa.

**Vídeo tá distorcido:**
- O original não é 9:16 vertical. ffmpeg adiciona padding preto. Re-gere no HeyGen/SuperGrok como 9:16.

---

## 🚀 Roadmap

- [ ] Template 06 — Reaction style (split-screen reagindo a ad concorrente)
- [ ] Auto-upload TikTok / Instagram via UI automation
- [ ] Detector de hook strength (analisa primeiros 3s)
- [ ] Gerador de variações automáticas (5 scripts diferentes do mesmo conceito)

---

## 📄 Licença

MIT. Faz o que quiser. Atribui se for legal.

---

## 🧠 Créditos

Construído por **Geek nos Negócios** + Claude.

- 🎓 **Formação Produtor Milionário** *(lowticket no ar em 1h, primeira venda no mesmo dia, com Claude)* → https://produtor.geekacademy.site
- 🛠️ **Rateio Ferramentas IA** *(HeyGen + SuperGrok + ElevenLabs + outras)* → https://rateaki.geekacademy.site
- 📺 **YouTube** → busca por "Geek nos Negócios"

---

> **Lowticket no ar em 1 hora. Primeira venda no mesmo dia. Com Claude.**
