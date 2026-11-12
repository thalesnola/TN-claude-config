"""Blocos de imagem Motion em formato VERTICAL para IPJ no modo leigo-motion.

Largura fixa de 1000 px, altura conforme o conteudo. Cada figura e um SVG gerado em Python e
fotografado em PNG pelo Chrome (ou Edge) headless, sem biblioteca nem fonte externa.

Uso:
    import motion_v as mv
    mv.configurar(saida=r"C:\\...\\fig")          # ou variavel de ambiente MOTION_OUT
    mv.trilha("f01_raciocinio", "Do chefe sem rosto a conta da plataforma", "O raciocinio em cinco passos",
              [(mv.SOL, "0", "Onde esta", "Antena, aparelho e internet apontam o mesmo bairro."), ...])

Regras de conteudo (ver references/modo-leigo-motion.md): titulo = resposta; subtitulo = escopo;
cartao = titulo curto + dado concreto; faixa escura final = conclusao em uma frase. Nada de hash,
nome de script ou observacao de trabalho dentro da imagem. Este modulo nao guarda dado de caso.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

W = 1000
CORAL, AZUL, MENTA, SOL, VIOLETA, ROSA = "#FF5A6E", "#2F9BFF", "#16C79A", "#FFB300", "#7B5CFF", "#FF7AC6"
NAVY = "#1B1F3B"
CINZ = "#5B6286"
TEXTO = "#3C4268"
FONT = "'Segoe UI Variable Display','Segoe UI','SF Pro Display','Helvetica Neue',Arial,sans-serif"
CORES = [CORAL, AZUL, MENTA, SOL, VIOLETA, ROSA]

_CFG = {"saida": Path(os.environ.get("MOTION_OUT", ".")), "escala": 1.6}


def configurar(saida=None, escala=None):
    if saida:
        _CFG["saida"] = Path(saida)
    if escala:
        _CFG["escala"] = escala
    _CFG["saida"].mkdir(parents=True, exist_ok=True)


def _navegador():
    cands = [os.environ.get("MOTION_CHROME", ""),
             r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             shutil.which("google-chrome") or "", shutil.which("chromium") or ""]
    for c in cands:
        if c and Path(c).exists():
            return c
    sys.exit("motion_v: Chrome/Edge nao encontrado (defina MOTION_CHROME).")


# ------------------------------------------------------------------ primitivas
def esc(t):
    return escape(str(t))


def wrap(txt, larg, tam):
    n = max(int(larg / (tam * 0.53)), 6)
    ls, cur = [], ""
    for w_ in str(txt).split():
        if len((cur + " " + w_).strip()) > n:
            ls.append(cur)
            cur = w_
        else:
            cur = (cur + " " + w_).strip()
    if cur:
        ls.append(cur)
    return ls


def tx(x, y, ls, size=23, cor=NAVY, peso=400, anchor="start", dy=None):
    if isinstance(ls, str):
        ls = [ls]
    dy = dy or size * 1.35
    t = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else dy}">{esc(s)}</tspan>' for i, s in enumerate(ls))
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{cor}" font-weight="{peso}" text-anchor="{anchor}">{t}</text>'


def pontos(lista, larg=780, tam=22):
    ls = []
    for it in lista:
        w_ = wrap(it, larg, tam)
        ls += ["• " + w_[0]] + ["  " + x for x in w_[1:]]
    return ls


def cab(titulo, sub):
    tl = wrap(titulo, 900, 46)
    s = tx(50, 90, tl, 46, NAVY, 800, "start", 56)
    y = 90 + 56 * (len(tl) - 1) + 44
    sl = wrap(sub, 900, 25)[:2]
    s += tx(52, y, sl, 25, CINZ, 400, "start", 32)
    y += 32 * (len(sl) - 1) + 50
    return s, y


def card(x, y, w, cor, titulo, texto, size=23, tsize=27):
    ls = wrap(texto, w - 70, size) if isinstance(texto, str) else texto
    tl = wrap(titulo, w - 60, tsize)
    h = 28 + len(tl) * tsize * 1.3 + 8 + len(ls) * size * 1.35 + 22
    s = (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="#fff"/>'
         f'<rect x="{x}" y="{y}" width="12" height="{h}" rx="6" fill="{cor}"/></g>')
    s += tx(x + 34, y + 28 + tsize * 0.85, tl, tsize, NAVY, 800, "start", tsize * 1.3)
    s += tx(x + 34, y + 28 + len(tl) * tsize * 1.3 + 8 + size * 0.8, ls, size, TEXTO, 400)
    return s, h


def pilha(itens, y, x=50, w=900, gap=18, **kw):
    """itens: (cor, titulo, texto). Devolve (svg, y_final)."""
    s = ""
    for cor, t, tex in itens:
        c, h = card(x, y, w, cor, t, tex, **kw)
        s += c
        y += h + gap
    return s, y


def grade(itens, y, colunas=2, gap=18, **kw):
    w = (900 - gap * (colunas - 1)) / colunas
    s, linha_h = "", 0
    for i, (cor, t, tex) in enumerate(itens):
        col = i % colunas
        if col == 0 and i:
            y += linha_h + gap
            linha_h = 0
        c, h = card(50 + col * (w + gap), y, w, cor, t, tex, **kw)
        s += c
        linha_h = max(linha_h, h)
    return s, y + linha_h + gap


def badge(cx, cy, w, ls, cor=NAVY, size=26):
    if isinstance(ls, str):
        ls = [ls]
    h = 30 + len(ls) * size * 1.3
    s = f'<g filter="url(#sh)"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="26" fill="{cor}"/></g>'
    s += tx(cx, cy - h / 2 + 22 + size, ls, size, "#fff", 800, "middle", size * 1.3)
    return s


def faixa(y, texto, cor=NAVY, size=24, x=50, w=900):
    """Faixa escura de conclusao: uma frase, a que o leitor deve levar da figura."""
    ls = wrap(texto, w - 60, size)
    h = 30 + len(ls) * size * 1.35
    s = f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="{cor}"/></g>'
    s += tx(x + w / 2, y + 22 + size, ls, size, "#fff", 800, "middle")
    return s, y + h + 18


def seta_v(x, y1, y2):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{NAVY}" stroke-width="6" stroke-dasharray="3 10" '
            f'stroke-linecap="round" marker-end="url(#ar)"/>')


def montar(corpo, H):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3EEFF"/><stop offset="0.55" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E9F7FF"/></linearGradient>
<linearGradient id="trail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7B5CFF" stop-opacity="0"/><stop offset="1" stop-color="#7B5CFF" stop-opacity="0.2"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="11" flood-color="#1B1F3B" flood-opacity="0.16"/></filter>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
<marker id="ar" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="9" markerHeight="9" orient="auto"><path d="M1 1 L11 6 L1 11 z" fill="{NAVY}"/></marker>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle cx="930" cy="100" r="150" fill="{ROSA}" opacity="0.13" filter="url(#glow)"/>
<circle cx="60" cy="{H - 120}" r="170" fill="{AZUL}" opacity="0.12" filter="url(#glow)"/>
<rect x="-60" y="{H * 0.45}" width="700" height="28" rx="14" fill="url(#trail)" transform="rotate(-12 300 {H * 0.45})"/>
<rect x="500" y="{H - 90}" width="600" height="24" rx="12" fill="url(#trail)" transform="rotate(-12 800 {H - 90})"/>
{corpo}
</svg>"""


def salvar(nome, corpo, y_final, titulo, sub):
    """Grava <nome>.svg e <nome>.png na pasta configurada. Devolve o caminho do PNG."""
    H = int(y_final + 40)
    cabs, _ = cab(titulo, sub)
    out = _CFG["saida"]
    out.mkdir(parents=True, exist_ok=True)
    p = out / f"{nome}.svg"
    p.write_text(montar(cabs + corpo, H), encoding="utf-8")
    png = out / f"{nome}.png"
    with tempfile.TemporaryDirectory() as t:
        subprocess.run([_navegador(), "--headless=new", "--no-sandbox", f"--user-data-dir={t}", f"--window-size={W},{H}",
                        f"--force-device-scale-factor={_CFG['escala']}", "--hide-scrollbars", f"--screenshot={png}",
                        p.resolve().as_uri()], capture_output=True, timeout=90)
    return png


def y0(titulo, sub):
    return cab(titulo, sub)[1]


# ------------------------------------------------------------------ modelos de figura
def so_cartoes(nome, titulo, sub, itens, colunas=1, rodape=None, topo=None, topo_h=0, **kw):
    """Cartoes empilhados (colunas=1) ou em grade. itens: (cor, titulo, texto).
    Portas fechadas x aberta: titulo do cartao com '✕ ' ou '✓ ' e cor CORAL/MENTA."""
    y = y0(titulo, sub)
    s = ""
    if topo:
        s += topo(y)
        y += topo_h
    s2, y = (grade(itens, y, colunas, **kw) if colunas > 1 else pilha(itens, y, **kw))
    s += s2
    if rodape:
        s3, y = faixa(y, rodape)
        s += s3
    return salvar(nome, s, y, titulo, sub)


def trilha(nome, titulo, sub, passos, rodape=None, topo_faixa=None):
    """Raciocinio em passos ou linha do tempo. passos: (cor, rotulo do circulo, titulo, texto).
    Rotulo curto (0, 1, 2...) vira numero grande; data ("18/06") vira texto menor."""
    y = y0(titulo, sub)
    s = ""
    if topo_faixa:
        s3, y = faixa(y, topo_faixa)
        s += s3
    blocos = []
    for cor, rot, t, tex in passos:
        c, h = card(170, y, 780, cor, t, tex)
        blocos.append((cor, rot, y, h))
        s += c
        y += h + 26
    cx = 92
    if len(blocos) > 1:
        s = (f'<line x1="{cx}" y1="{blocos[0][2] + blocos[0][3] / 2}" x2="{cx}" y2="{blocos[-1][2] + blocos[-1][3] / 2}" '
             f'stroke="{VIOLETA}" stroke-width="7" stroke-dasharray="2 14" stroke-linecap="round" opacity="0.55"/>') + s
    for cor, rot, yy, h in blocos:
        s += f'<circle cx="{cx}" cy="{yy + h / 2}" r="50" fill="{cor}" stroke="#fff" stroke-width="7" filter="url(#sh)"/>'
        tam = 40 if len(rot) < 3 else 20
        s += tx(cx, yy + h / 2 + tam * 0.36, wrap(rot, 90, tam)[:2] if len(rot) > 3 else [rot], tam, "#fff", 900, "middle", tam * 1.05)
    if rodape:
        s3, y = faixa(y, rodape)
        s += s3
    return salvar(nome, s, y, titulo, sub)


def venn(nome, titulo, sub, circ, resultado, rodape=None):
    """Convergencia de metodos. circ: (rotulo curto com |, cor, titulo do cartao, texto). 3 ou 4 circulos.
    O selo central (resultado) e o que os metodos tem em comum."""
    y = y0(titulo, sub)
    s = ""
    if len(circ) == 3:
        R = 175
        pos = [(375, y + R), (625, y + R), (500, y + R + 215)]
        alt = R * 2 + 215
        rot = [(300, y + R - 5), (700, y + R - 5), (500, y + R + 300)]
    else:
        R = 165
        pos = [(410, y + R), (590, y + R), (410, y + R + 190), (590, y + R + 190)]
        alt = R * 2 + 190
        rot = [(310, y + R - 20), (690, y + R - 20), (310, y + R + 215), (690, y + R + 215)]
    cen = (500, y + R + 95)
    for (cx, cy), (rt, cor, *_r) in zip(pos, circ):
        s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{cor}" fill-opacity="0.62" style="mix-blend-mode:multiply" stroke="#fff" stroke-width="6"/>'
    for (px, py), (rt, *_r) in zip(rot, circ):
        s += tx(px, py, rt.split("|"), 23, NAVY, 800, "middle", 28)
    s += badge(cen[0], cen[1], 200, resultado, NAVY, 25)
    y += alt + 40
    s2, y = pilha([(c[1], c[2], c[3]) for c in circ], y)
    s += s2
    if rodape:
        s3, y = faixa(y, rodape)
        s += s3
    return salvar(nome, s, y, titulo, sub)


def linhas_pilulas(nome, titulo, sub, cab_a, cab_b, linhas_, cor_a=VIOLETA, cor_b=CORAL, rodape=None):
    """Mesma medida, dois lados (ex.: o alvo x os demais). linhas_: (rotulo, subrotulo, texto_a, texto_b, nota)."""
    y = y0(titulo, sub)
    s = ""
    for i, (rot, subr, a, b, nota) in enumerate(linhas_):
        cor = CORES[i % 6]
        h = 190 if (subr or nota) else 170
        s += f'<rect x="40" y="{y}" width="920" height="{h}" rx="30" fill="#fff" opacity="0.8"/>'
        s += f'<circle cx="92" cy="{y + 48}" r="26" fill="{cor}"/>'
        s += tx(136, y + 56, [rot], 28, NAVY, 900)
        if subr:
            s += tx(136, y + 84, [subr], 20, CINZ, 400)
        s += tx(255, y + 108, [cab_a], 18, CINZ, 800, "middle")
        s += tx(730, y + 108, [cab_b], 18, CINZ, 800, "middle")
        s += f'<g filter="url(#sh)"><rect x="60" y="{y + 114}" width="390" height="50" rx="25" fill="{cor_a}"/></g>'
        s += tx(255, y + 147, [a], 23, "#fff", 800, "middle")
        s += f'<text x="470" y="{y + 150}" font-size="32" font-weight="900" fill="{NAVY}">→</text>'
        s += f'<g filter="url(#sh)"><rect x="520" y="{y + 114}" width="420" height="50" rx="25" fill="{cor_b}"/></g>'
        s += tx(730, y + 147, [b], 23, "#fff", 800, "middle")
        if nota:
            s += tx(730, y + 184, [nota], 19, NAVY, 700, "middle")
        y += h + 14
    if rodape:
        s3, y = faixa(y, rodape)
        s += s3
    return salvar(nome, s, y, titulo, sub)


def hub(nome, titulo, sub, centro, entradas, saidas, rodape, cor=VIOLETA):
    """Quem enviou (acima) -> pessoa (circulo) -> para quem enviou (abaixo). entradas/saidas: (nome, valor)."""
    y = y0(titulo, sub)
    s = ""

    def bloco(lista, y):
        s_ = ""
        for i, (nm, val) in enumerate(lista):
            ccor = CORES[(i + 1) % 6]
            s_ += (f'<g filter="url(#sh)"><rect x="150" y="{y}" width="700" height="78" rx="26" fill="#fff"/>'
                   f'<rect x="150" y="{y}" width="12" height="78" rx="6" fill="{ccor}"/></g>')
            s_ += tx(184, y + 32, [nm], 22, NAVY, 800) + tx(184, y + 62, [val], 23, ccor, 900)
            y += 92
        return s_, y

    if entradas:
        s += tx(500, y + 6, ["Quem enviou"], 24, CINZ, 800, "middle")
        s2, y = bloco(entradas, y + 28)
        s += s2 + seta_v(500, y - 8, y + 52)
        y += 64
    s += f'<circle cx="500" cy="{y + 100}" r="105" fill="{cor}" stroke="#fff" stroke-width="8" filter="url(#sh)"/>'
    rl = wrap(centro[0], 190, 30)
    s += tx(500, y + 96, rl, 30, "#fff", 900, "middle", 34)
    s += tx(500, y + 96 + 34 * len(rl) + 6, wrap(centro[1], 170, 18), 18, "#fff", 400, "middle")
    y += 215
    if saidas:
        s += seta_v(500, y - 6, y + 50)
        y += 84
        s += tx(500, y, ["Para quem enviou"], 24, CINZ, 800, "middle")
        s2, y = bloco(saidas, y + 22)
        s += s2
    s3, y = faixa(y + 10, rodape)
    return salvar(nome, s + s3, y, titulo, sub)


def historia(nome, titulo, sub, grande, legenda, cor, fatos):
    """Um numero que resume a pessoa ou o fato (circulo grande) + os fatos que o explicam. fatos: (titulo, texto)."""
    y = y0(titulo, sub)
    s = f'<circle cx="500" cy="{y + 150}" r="150" fill="{cor}" fill-opacity="0.9" stroke="#fff" stroke-width="10" filter="url(#sh)"/>'
    s += tx(500, y + 160, [grande], 52 if len(grande) < 10 else 40, "#fff", 900, "middle")
    s += tx(500, y + 205, wrap(legenda, 230, 20), 20, "#fff", 400, "middle")
    s2, y = pilha([(CORES[(i + 1) % 6], t, tex) for i, (t, tex) in enumerate(fatos)], y + 330)
    return salvar(nome, s + s2, y, titulo, sub)


def orbita(nome, titulo, sub, centro, legenda, itens, rodape=None, cor=NAVY):
    """Um objeto e o que gira em torno dele (um aparelho, varias contas; uma conta, varios aparelhos).
    itens: (cor, titulo, texto) - cada um ganha um satelite colorido e um cartao."""
    y = y0(titulo, sub)
    cy = y + 150
    s = f'<rect x="300" y="{cy + 70}" width="420" height="22" rx="11" fill="url(#trail)" transform="rotate(-12 500 {cy + 80})"/>'
    s += f'<circle cx="500" cy="{cy}" r="140" fill="{cor}" stroke="#fff" stroke-width="10" filter="url(#sh)"/>'
    cl = wrap(centro, 230, 34)
    s += tx(500, cy - 10 - 20 * (len(cl) - 1), cl, 34, "#fff", 900, "middle", 40)
    s += tx(500, cy + 20 + 20 * (len(cl) - 1), wrap(legenda, 230, 19)[:2], 19, "#fff", 400, "middle")
    import math
    for i, (c, *_r) in enumerate(itens):
        a = math.pi * (1 + i / max(len(itens) - 1, 1))
        s += f'<circle cx="{500 + 200 * math.cos(a):.1f}" cy="{cy - 30 * math.sin(a) + 30:.1f}" r="22" fill="{c}" stroke="#fff" stroke-width="5" filter="url(#sh)"/>'
    s2, y = pilha(itens, cy + 210)
    s += s2
    if rodape:
        s3, y = faixa(y, rodape)
        s += s3
    return salvar(nome, s, y, titulo, sub)


def etapas(nome, titulo, sub, passos, itens, rodape=None):
    """Etapas encadeadas em coluna (circulo -> seta -> circulo) e cartoes abaixo. passos: (cor, linhas do circulo)."""
    y = y0(titulo, sub)
    s = ""
    for i, (cor, ls) in enumerate(passos):
        s += f'<circle cx="500" cy="{y + 95}" r="95" fill="{cor}" stroke="#fff" stroke-width="8" filter="url(#sh)"/>'
        s += tx(500, y + 95 - 14 * (len(ls) - 1), ls, 25, "#fff", 900, "middle", 30)
        y += 190
        if i < len(passos) - 1:
            s += seta_v(500, y + 2, y + 46)
            y += 56
    s2, y = pilha(itens, y + 20)
    s += s2
    if rodape:
        s3, y = faixa(y, rodape)
        s += s3
    return salvar(nome, s, y, titulo, sub)


def quadro(nome, titulo, sub, cols, linhas_, rodape=None, larg_nome=330, total=True):
    """Matriz pessoa x caminho (quem compartilha o que). linhas_: (nome, [bool...], legenda curta)."""
    y = y0(titulo, sub)
    s = ""
    n = len(cols)
    cw = (920 - larg_nome) / n
    for i, c in enumerate(cols):
        s += tx(40 + larg_nome + cw * i + cw / 2, y + 10, wrap(c, cw, 17)[:2], 17, CINZ, 800, "middle", 20)
    y += 52
    for nm, marcas, leg in linhas_:
        s += f'<rect x="30" y="{y}" width="940" height="72" rx="28" fill="#fff" opacity="0.85"/>'
        s += tx(56, y + 34 if leg else y + 44, [nm], 23, NAVY, 900)
        if leg:
            s += tx(56, y + 58, [leg], 17, CINZ, 400)
        for i, m in enumerate(marcas):
            cx = 40 + larg_nome + cw * i + cw / 2
            if m:
                s += f'<circle cx="{cx}" cy="{y + 36}" r="20" fill="{CORES[i % 6]}"/>' + tx(cx, y + 45, ["✓"], 24, "#fff", 900, "middle")
            else:
                s += f'<circle cx="{cx}" cy="{y + 36}" r="16" fill="#E3E0F5"/>'
        if total:
            s += f'<text x="955" y="{y + 45}" font-size="26" font-weight="900" fill="{NAVY}" text-anchor="end">{sum(1 for m in marcas if m)}</text>'
        y += 82
    if rodape:
        s3, y = faixa(y, rodape)
        s += s3
    return salvar(nome, s, y, titulo, sub)


def grade_horaria(nome, titulo, sub, dias, eventos, legenda, cartao=None, madrugada=(0, 6)):
    """Onde o aparelho dormiu: linha = dia, eixo = hora. eventos: (dia, hora_decimal, cor).
    legenda: (cor, texto). A faixa da madrugada fica sombreada."""
    y = y0(titulo, sub)
    x0_, cw, ch = 150, 31, 70
    s = f'<rect x="{x0_ + cw * madrugada[0]}" y="{y - 4}" width="{cw * (madrugada[1] - madrugada[0])}" height="{ch * len(dias) + 8}" rx="14" fill="{NAVY}" opacity="0.08"/>'
    for h in range(0, 24, 3):
        s += tx(x0_ + cw * h + cw / 2, y + ch * len(dias) + 34, [f"{h:02d}h"], 17, CINZ, 800, "middle")
    for i, dia in enumerate(dias):
        yy = y + i * ch
        s += tx(x0_ - 18, yy + ch / 2 + 7, [dia], 22, NAVY, 800, "end")
        s += f'<rect x="{x0_}" y="{yy + 6}" width="{cw * 24}" height="{ch - 12}" rx="10" fill="#fff" opacity="0.75"/>'
        do_dia = [e for e in eventos if e[0] == dia]
        if not do_dia:
            s += tx(x0_ + cw * 12, yy + ch / 2 + 6, ["sem registro"], 18, "#9AA0C0", 400, "middle")
        for _, hora, cor in do_dia:
            s += f'<rect x="{x0_ + cw * hora:.1f}" y="{yy + 14}" width="14" height="{ch - 28}" rx="6" fill="{cor}" stroke="#fff" stroke-width="2"/>'
    y += ch * len(dias) + 62
    for k, (cor, t) in enumerate(legenda):
        s += f'<circle cx="{x0_ + 10}" cy="{y + 34 * k}" r="11" fill="{cor}"/>' + tx(x0_ + 30, y + 7 + 34 * k, [t], 19, NAVY, 600)
    y += 34 * len(legenda) + 40
    if cartao:
        s2, y = pilha([cartao], y)
        s += s2
    return salvar(nome, s, y, titulo, sub)


# ------------------------------------------------------------------ mapa (sobreposicao)
def setor(px, py, az, raio, abre=70):
    """Path SVG do setor de uma antena (ilustrativo: a operadora informa a direcao, nao o alcance)."""
    import math
    a0, a1 = math.radians(az - abre / 2), math.radians(az + abre / 2)
    p0 = (px + raio * math.sin(a0), py - raio * math.cos(a0))
    p1 = (px + raio * math.sin(a1), py - raio * math.cos(a1))
    return f"M{px:.1f} {py:.1f} L{p0[0]:.1f} {p0[1]:.1f} A{raio} {raio} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z"


def torre(x, y, cor, n, rot=None, dx=0, dy=-62):
    """Marcador de antena com contador de registros e etiqueta branca."""
    s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="{cor}" stroke="#fff" stroke-width="5" filter="url(#sh)"/>'
    s += f'<path d="M{x - 6:.1f} {y + 7:.1f} L{x:.1f} {y - 8:.1f} L{x + 6:.1f} {y + 7:.1f}" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
    s += f'<circle cx="{x + 24:.1f}" cy="{y - 24:.1f}" r="19" fill="{NAVY}" stroke="#fff" stroke-width="4"/>' + tx(x + 24, y - 17, [str(n)], 20, "#fff", 900, "middle")
    if rot:
        w = 12 + len(rot) * 11.2
        s += (f'<g filter="url(#sh)"><rect x="{x + dx:.1f}" y="{y + dy - 24:.1f}" width="{w:.1f}" height="38" rx="19" fill="#fff"/></g>'
              + tx(x + dx + w / 2, y + dy + 1, [rot], 19, NAVY, 800, "middle"))
    return s


# ------------------------------------------------------------------ demonstracao (dados ficticios)
if __name__ == "__main__":
    configurar(saida=sys.argv[1] if len(sys.argv) > 1 else Path(tempfile.gettempdir()) / "motion_demo")
    print(trilha("demo_trilha", "Do apelido ao nome", "O raciocinio em quatro passos", [
        (SOL, "1", "Onde comecou", "No celular apreendido aparece o contato \"ALFA\"."),
        (CORAL, "2", "O numero", "A agenda liga \"ALFA\" a uma linha pre-paga."),
        (AZUL, "3", "A casa", "A antena e a internet da linha apontam o mesmo bairro."),
        (VIOLETA, "4", "O nome", "O cadastro da internet fixa naquele endereco esta em nome dele.")],
        rodape="Tres caminhos independentes chegam a mesma pessoa."))
    print(venn("demo_venn", "Tres caminhos, uma pessoa", "Cada circulo e um metodo; o centro e o que eles tem em comum", [
        ("Antena", CORAL, "Antena", "O celular dorme na antena do bairro."),
        ("Internet|fixa", AZUL, "Internet fixa", "A conta se conecta pela banda larga da casa."),
        ("Cadastro", MENTA, "Cadastro", "A ficha da operadora traz o mesmo endereco.")], ["MESMA", "CASA"]))
    print(linhas_pilulas("demo_pilulas", "Quem manda fala pouco", "Mesma medida, dois lados", "O ALVO", "OS DEMAIS",
                         [("Mensagens em 15 dias", "", "90", "150 a 4.000", ""), ("Redes de internet", "", "2", "10 a 50", "")],
                         rodape="Quem executa fala muito; quem manda fala pouco."))
