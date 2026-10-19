# Gerador de vídeos do Laboratório de Draft

Vídeos verticais (1080x1920, cerca de 15 a 25 s) feitos de slides com a identidade do site e uma trilha original gerada por síntese (`music.py`, sem samples). Nada de gameplay, trailer ou vídeo de terceiros: não baixe, recorte nem reenvie vídeos da Riot ou de transmissões.

## Como usar

```bash
cd ferramentas/video
npm install          # instala o Playwright; o Chromium já vem na máquina (não rode "playwright install")
pip install --break-system-packages numpy scipy   # se faltar
node render.mjs meus-videos.json png      # um PNG por slide; avisa se algum texto não coube
python3 compose.py meus-videos.json png out   # gera out/<slug>.mp4
```

## Formato do JSON

Uma lista de vídeos. Cada vídeo: `slug`, `n` (número qualquer; muda a variação da trilha), `dur` (segundos de cada slide, mesmo tamanho de `slides`) e `slides`.

Tipos de slide (`t`), todos aceitam `eyebrow` (faixa pequena no topo):

- `title`: `title`, `sub`. Abertura.
- `list`: `items` = [[título, texto], ...]. Até 4 itens.
- `changes`: `title`, `items` = [{`n`, `dir`: `up` | `down` | `adj`, `txt`}]. Mudanças de patch (FORTE, FRACO, AJUSTE). Até 4 itens.
- `results`: `title`, `items` = [{`a`, `sa`, `sb`, `b`, `br`}], `foot`. Placares; `br: true` destaca time brasileiro. Com mais de 5 jogos, use siglas (GEN, T1, LOS).
- `comps`: `title`, `comps` = [{`label`, `champs`: [top, jungle, mid, atirador, suporte]}] (2 comps), `foot`.
- `comps1`, `counters`, `exercise`, `term`, `grade`, `answer`: tipos usados nos vídeos antigos (veja `slide.html`).
- `cta`: `title`, `sub`, `btn` (padrão "Link na bio"). Sempre o último slide.

Confira os PNGs antes de compor: texto cortado ou pequeno demais não vai para o ar.

## Publicação

Suba o MP4 em `jogo/AAAA-MM-DD-<slug>.mp4` neste repositório e use o link
`https://raw.githubusercontent.com/krambs-60hz/labdraft-midia/main/jogo/AAAA-MM-DD-<slug>.mp4` no Metricool.
