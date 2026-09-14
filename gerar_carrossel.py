# -*- coding: utf-8 -*-
"""Gera o carrossel TÉCNICO do @peritomauricioboschetti — 1080x1350 (4:5), 7 a 9 slides.

Réplica do gerador do posts-perffec (que herdou o que foi MEDIDO no @vendanaobra):
  - 4:5, 7 slides é o ponto ótimo, capa com FOTO e gancho de até 8 palavras,
    uma ideia por slide, último slide pede a ação.

O que é do Maurício e não da Perffec nem do @vendanaobra:
  - identidade da Consult Glass: navy #061528 + teal #1EA9B8 + prata #F3F3F3,
    Plus Jakarta Sans (texto) e Bai Jamjuree (etiquetas) — as fontes do site
    mauricio.consultglass.net.br;
  - a foto da capa é o MAURÍCIO em ação (palestra, podcast, bancada), tirada do
    próprio acervo dele (pasta fotos/), nunca banco de imagem;
  - blocos próprios: "A norma diz" (teal-claro), "Onde vira processo" (vermelho)
    e "Na perícia" (navy) — o caso ou o fato verificável.

Tipos de slide (campo "tipo" em carrosseis.json):
  capa      foto + etiqueta + gancho
  texto     título + parágrafos (padrão)
  lista     título + itens [rótulo, texto]
  norma     fundo teal-claro, rótulo A NORMA DIZ / A LEI DIZ — o trecho conferido
  alerta    rótulo vermelho ONDE VIRA PROCESSO
  pericia   fundo navy, rótulo NA PERÍCIA — o caso ou o critério
  cta       fundo navy, o produto do ciclo (seguir / Venda Blindada / Perícia / Método Blindar)
"""
from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONTE_TTF = os.path.join(BASE, "fontes", "PlusJakartaSans.ttf")
FONTE_ETIQUETA = os.path.join(BASE, "fontes", "BaiJamjuree-SemiBold.ttf")
PASTA_FOTOS = os.path.join(BASE, "fotos")

LARG, ALT = 1080, 1350
MARGEM = 96
UTIL = LARG - 2 * MARGEM

NAVY = (6, 21, 40)             # #061528
NAVY2 = (13, 49, 69)           # #0D3145
TEAL = (30, 169, 184)          # #1EA9B8
TEAL_CLARO = (63, 208, 224)    # #3FD0E0
TEAL_FUNDO = (226, 244, 246)   # #E2F4F6
TEAL_ESCURO = (18, 101, 122)   # #12657A
PRATA = (243, 243, 243)        # #F3F3F3
BRANCO = (250, 250, 250)
TINTA = (20, 19, 15)           # #14130F
TINTA2 = (85, 84, 78)          # #55544E
CINZA = (128, 128, 128)
ALERTA = (158, 52, 23)         # #9E3417
ALERTA_FUNDO = (250, 238, 233)

HANDLE = "@peritomauricioboschetti"
SITE = "mauricio.consultglass.net.br"
ETIQUETA_MARCA = "MAURÍCIO BOSCHETTI · ENG. CIVIL · PERITO JUDICIAL (TJSP)"


def _f(tamanho: int, peso: int = 400) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FONTE_TTF, tamanho)
    f.set_variation_by_axes([max(200, min(800, peso))])  # Plus Jakarta: eixo wght 200..800
    return f


def _fe(tamanho: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONTE_ETIQUETA, tamanho)


def _quebrar(texto: str, fonte, largura: int) -> list[str]:
    linhas: list[str] = []
    for par in texto.split("\n"):
        atual = ""
        for palavra in par.split():
            teste = (atual + " " + palavra).strip()
            if fonte.getlength(teste) <= largura:
                atual = teste
            else:
                if atual:
                    linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def _altura(texto: str, fonte, largura: int, entrelinha: float, gap_par: float) -> int:
    lh = int(fonte.size * entrelinha)
    pars = [p.strip() for p in texto.split("\n\n") if p.strip()]
    total = 0
    for i, p in enumerate(pars):
        total += len(_quebrar(p, fonte, largura)) * lh
        if i < len(pars) - 1:
            total += int(fonte.size * gap_par)
    return total


def _bloco(d, texto: str, x: int, y: int, largura: int, fonte, cor,
           entrelinha: float = 1.4, gap_par: float = 0.7) -> int:
    lh = int(fonte.size * entrelinha)
    pars = [p.strip() for p in texto.split("\n\n") if p.strip()]
    for i, p in enumerate(pars):
        for linha in _quebrar(p, fonte, largura):
            d.text((x, y), linha, font=fonte, fill=cor)
            y += lh
        if i < len(pars) - 1:
            y += int(fonte.size * gap_par)
    return y


def _espacado(d, texto: str, x: int, y: int, fonte, cor, tracking: int = 4) -> int:
    for ch in texto:
        d.text((x, y), ch, font=fonte, fill=cor)
        x += int(fonte.getlength(ch)) + tracking
    return x


def _cobrir(foto: Image.Image, larg: int, alt: int) -> Image.Image:
    esc = max(larg / foto.width, alt / foto.height)
    novo = foto.resize((int(foto.width * esc) + 1, int(foto.height * esc) + 1), Image.LANCZOS)
    x = (novo.width - larg) // 2
    y = (novo.height - alt) // 2
    return novo.crop((x, y, x + larg, y + alt))


def _rodape(d, cor=CINZA) -> None:
    f = _f(26, 500)
    d.text((MARGEM, ALT - 92), HANDLE, font=f, fill=cor)
    d.text((LARG - MARGEM - f.getlength(SITE), ALT - 92), SITE, font=f, fill=cor)


def _cabecalho(d, n: int, total: int, rotulo: str | None, cor_rotulo, cor_num=TEAL) -> int:
    """Número do slide + rótulo opcional. Devolve o y onde o conteúdo começa."""
    f = _f(28, 600)
    d.text((MARGEM, 96), f"{n:02d} / {total:02d}", font=f, fill=cor_num)
    d.rectangle((MARGEM, 146, MARGEM + 72, 150), fill=cor_num)
    y = 196
    if rotulo:
        _espacado(d, rotulo.upper(), MARGEM, y, _fe(26), cor_rotulo, tracking=5)
        y += 62
    return y


# ------------------------------------------------------------------ slides

def slide_capa(s: dict, total: int) -> Image.Image:
    foto = Image.open(os.path.join(PASTA_FOTOS, s["foto"])).convert("RGB")
    im = _cobrir(foto, LARG, ALT).convert("RGBA")
    # véu navy: leve em cima, pesado embaixo (onde vai o gancho)
    veu = Image.new("RGBA", (LARG, ALT), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veu)
    for y in range(ALT):
        t = y / ALT
        a = int(60 + 170 * (t ** 1.5))
        vd.line((0, y, LARG, y), fill=(6, 21, 40, a))
    im.alpha_composite(veu)
    d = ImageDraw.Draw(im)

    d.rectangle((MARGEM, 96, MARGEM + 6, 96 + 30), fill=TEAL)
    _espacado(d, ETIQUETA_MARCA, MARGEM + 22, 96, _fe(22), (226, 236, 240), tracking=4)
    if s.get("etiqueta"):
        fe = _fe(26)
        larg_et = sum(int(fe.getlength(ch)) + 5 for ch in s["etiqueta"].upper()) + 40
        d.rectangle((MARGEM, 150, MARGEM + larg_et, 150 + 54), fill=(6, 21, 40, 235))
        _espacado(d, s["etiqueta"].upper(), MARGEM + 20, 162, fe, TEAL_CLARO, tracking=5)

    tam = s.get("tamanho", 84)
    fg = _f(tam, 800)
    linhas = _quebrar(s["gancho"], fg, UTIL)
    while len(linhas) > 5 and tam > 60:
        tam -= 4
        fg = _f(tam, 800)
        linhas = _quebrar(s["gancho"], fg, UTIL)
    lh = int(tam * 1.08)
    y = ALT - 236 - lh * len(linhas)
    if s.get("sub"):
        y -= 70
    for linha in linhas:
        d.text((MARGEM, y), linha, font=fg, fill=(255, 255, 255))
        y += lh
    if s.get("sub"):
        y += 14
        d.text((MARGEM, y), s["sub"], font=_f(34, 500), fill=(200, 226, 232))

    d.rectangle((MARGEM, ALT - 132, MARGEM + 72, ALT - 128), fill=TEAL)
    d.text((MARGEM, ALT - 112), HANDLE, font=_f(28, 600), fill=(220, 230, 234))
    fa = _f(28, 600)
    txt = "Arraste  →"
    d.text((LARG - MARGEM - fa.getlength(txt), ALT - 112), txt, font=fa, fill=(220, 230, 234))
    return im


def _slide_base(cor_fundo) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (LARG, ALT), cor_fundo + (255,))
    return im, ImageDraw.Draw(im)


def _ajustar_corpo(texto: str, largura: int, disponivel: int, tam: int = 56) -> ImageFont.FreeTypeFont:
    """Reduz o corpo até caber na altura disponível (mínimo 34px)."""
    while tam > 34 and _altura(texto, _f(tam, 400), largura, 1.42, 0.7) > disponivel:
        tam -= 2
    return _f(tam, 400)


def _centrar(y_topo: int, altura_conteudo: int, y_fim: int = ALT - 170) -> int:
    sobra = (y_fim - y_topo) - altura_conteudo
    return y_topo + max(0, int(sobra * 0.38))


def _rodape_escuro(d) -> None:
    f = _f(26, 500)
    d.text((MARGEM, ALT - 92), HANDLE, font=f, fill=(150, 170, 180))
    d.text((LARG - MARGEM - f.getlength(SITE), ALT - 92), SITE, font=f, fill=(150, 170, 180))


def slide_texto(s: dict, n: int, total: int, fundo=BRANCO, cor_titulo=TINTA, cor_corpo=TINTA2,
                rotulo: str | None = None, cor_rotulo=TEAL_ESCURO, escuro=False) -> Image.Image:
    im, d = _slide_base(fundo)
    y = _cabecalho(d, n, total, rotulo or s.get("rotulo"), cor_rotulo,
                   cor_num=TEAL_CLARO if escuro else TEAL)
    y += 8
    ft = _f(s.get("tamanho_titulo", 72), 700)
    h_tit = (_altura(s["titulo"], ft, UTIL, 1.12, 0) + 40) if s.get("titulo") else 0
    fc = _ajustar_corpo(s["texto"], UTIL, ALT - 170 - y - h_tit) if s.get("texto") else None
    h_txt = _altura(s["texto"], fc, UTIL, 1.42, 0.7) if fc else 0
    y = _centrar(y, h_tit + h_txt)
    if s.get("titulo"):
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, cor_titulo, entrelinha=1.12) + 40
    if fc:
        _bloco(d, s["texto"], MARGEM, y, UTIL, fc, cor_corpo, entrelinha=1.42)
    if escuro:
        _rodape_escuro(d)
    else:
        _rodape(d)
    return im


def slide_lista(s: dict, n: int, total: int) -> Image.Image:
    im, d = _slide_base(BRANCO)
    y = _cabecalho(d, n, total, s.get("rotulo"), TEAL_ESCURO) + 8
    if s.get("titulo"):
        ft = _f(s.get("tamanho_titulo", 66), 700)
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, TINTA, entrelinha=1.12) + 34
    itens = s["itens"]
    disponivel = ALT - 170 - y
    tam = 54
    while True:
        fr, fc = _f(tam, 700), _f(tam, 400)
        h = 0
        for rot, txt in itens:
            h += _altura(txt, fc, UTIL - 44, 1.36, 0.6) + _altura(rot, fr, UTIL - 44, 1.2, 0) + 30
        if h <= disponivel or tam <= 32:
            break
        tam -= 2
    y = _centrar(y, h)
    for rot, txt in itens:
        d.rectangle((MARGEM, y + int(tam * 0.32), MARGEM + 14, y + int(tam * 0.32) + 14), fill=TEAL)
        y = _bloco(d, rot, MARGEM + 44, y, UTIL - 44, fr, TINTA, entrelinha=1.2) + int(tam * 0.16)
        y = _bloco(d, txt, MARGEM + 44, y, UTIL - 44, fc, TINTA2, entrelinha=1.36) + 30
    _rodape(d)
    return im


def slide_norma(s: dict, n: int, total: int) -> Image.Image:
    im, d = _slide_base(TEAL_FUNDO)
    y = _cabecalho(d, n, total, s.get("rotulo", "A norma diz"), TEAL_ESCURO) + 8
    if s.get("titulo"):
        ft = _f(s.get("tamanho_titulo", 66), 700)
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, TINTA, entrelinha=1.12) + 36
    fc = _ajustar_corpo(s["texto"], UTIL - 40, ALT - 170 - y - (60 if s.get("fonte") else 0), tam=58)
    h = _altura(s["texto"], fc, UTIL - 40, 1.42, 0.7)
    y = _centrar(y, h + (60 if s.get("fonte") else 0))
    d.rectangle((MARGEM, y, MARGEM + 8, y + h), fill=TEAL)
    y = _bloco(d, s["texto"], MARGEM + 40, y, UTIL - 40, fc, TINTA, entrelinha=1.42)
    if s.get("fonte"):
        d.text((MARGEM + 40, y + 24), s["fonte"], font=_f(28, 500), fill=TEAL_ESCURO)
    _rodape(d, cor=TEAL_ESCURO)
    return im


def slide_alerta(s: dict, n: int, total: int) -> Image.Image:
    im, d = _slide_base(BRANCO)
    y = _cabecalho(d, n, total, s.get("rotulo", "Onde vira processo"), ALERTA, cor_num=ALERTA) + 8
    if s.get("titulo"):
        ft = _f(s.get("tamanho_titulo", 66), 700)
        y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, TINTA, entrelinha=1.12) + 36
    fc = _ajustar_corpo(s["texto"], UTIL - 96, ALT - 270 - y, tam=54)
    h = _altura(s["texto"], fc, UTIL - 96, 1.42, 0.7) + 96
    y = _centrar(y, h)
    d.rectangle((MARGEM, y, LARG - MARGEM, y + h), fill=ALERTA_FUNDO)
    d.rectangle((MARGEM, y, MARGEM + 8, y + h), fill=ALERTA)
    _bloco(d, s["texto"], MARGEM + 48, y + 48, UTIL - 96, fc, TINTA, entrelinha=1.42)
    _rodape(d)
    return im


def slide_pericia(s: dict, n: int, total: int) -> Image.Image:
    return slide_texto(s, n, total, fundo=NAVY, cor_titulo=(255, 255, 255),
                       cor_corpo=(200, 214, 222), rotulo=s.get("rotulo", "Na perícia"),
                       cor_rotulo=TEAL_CLARO, escuro=True)


# O que cada CTA oferece — texto da LP mauricio.consultglass.net.br, na voz do Maurício.
PRODUTOS = {
    "seguir": {
        "rotulo": "Siga o perfil",
        "linha1": "Vidro, esquadria e fachada com critério de perito",
        "linha2": "@peritomauricioboschetti",
        "linha3": SITE,
    },
    "venda-blindada": {
        "rotulo": "Venda Blindada · para quem fabrica e instala",
        "linha1": "Contrato técnico: escopo, medição, prazos, recebimento e responsabilidades",
        "linha2": "Venda Blindada para esquadrias",
        "linha3": f"{SITE}/venda-blindada-esquadrias",
    },
    "pericia": {
        "rotulo": "Perícia técnica · quando o dano já existe",
        "linha1": "Falhas e vícios em esquadrias, vidros, fachadas e guarda-corpos",
        "linha2": "Perícia extrajudicial e parecer técnico",
        "linha3": f"{SITE}/pericia-tecnica",
    },
    "metodo-blindar": {
        "rotulo": "Método Blindar · para construtoras",
        "linha1": "Cinco encontros com a sua equipe, doze ferramentas na sua obra",
        "linha2": "Método Blindar para Construtoras",
        "linha3": f"{SITE}/metodo-blindar",
    },
}


def slide_cta(s: dict, n: int, total: int) -> Image.Image:
    prod = PRODUTOS[s.get("produto", "seguir")]
    im, d = _slide_base(NAVY)
    y = _cabecalho(d, n, total, s.get("rotulo", prod["rotulo"]), TEAL_CLARO, cor_num=TEAL_CLARO) + 8
    ft = _f(68, 800)
    fx = _f(42, 400)
    f1, f2, f3 = _f(30, 600), _f(42, 700), _f(30, 500)
    h = _altura(s["titulo"], ft, UTIL, 1.1, 0) + 40
    if s.get("texto"):
        h += _altura(s["texto"], fx, UTIL, 1.42, 0.7) + 56
    h += 40 + _altura(prod["linha1"], f1, UTIL, 1.3, 0) + 20 + _altura(prod["linha2"], f2, UTIL, 1.2, 0) + 16 + 40
    y = _centrar(y, h)
    y = _bloco(d, s["titulo"], MARGEM, y, UTIL, ft, (255, 255, 255), entrelinha=1.1) + 40
    if s.get("texto"):
        y = _bloco(d, s["texto"], MARGEM, y, UTIL, fx, (200, 214, 222), entrelinha=1.42) + 56
    d.rectangle((MARGEM, y, MARGEM + 72, y + 4), fill=TEAL)
    y += 40
    y = _bloco(d, prod["linha1"], MARGEM, y, UTIL, f1, (150, 170, 180), entrelinha=1.3) + 20
    y = _bloco(d, prod["linha2"], MARGEM, y, UTIL, f2, (255, 255, 255), entrelinha=1.2) + 16
    d.text((MARGEM, y), prod["linha3"], font=f3, fill=TEAL_CLARO)
    _rodape_escuro(d)
    return im


RENDER = {
    "capa": None,
    "texto": slide_texto,
    "lista": slide_lista,
    "norma": slide_norma,
    "alerta": slide_alerta,
    "pericia": slide_pericia,
    "cta": slide_cta,
}


def gerar(peca: dict, pasta_saida: str) -> list[str]:
    os.makedirs(pasta_saida, exist_ok=True)
    slides = peca["slides"]
    total = len(slides)
    caminhos = []
    for i, s in enumerate(slides, start=1):
        tipo = s.get("tipo", "texto")
        if tipo == "capa":
            im = slide_capa(s, total)
        else:
            im = RENDER[tipo](s, i, total)
        caminho = os.path.join(pasta_saida, f"slide-{i:02d}.jpg")
        im.convert("RGB").save(caminho, quality=92, subsampling=0)
        caminhos.append(caminho)
    return caminhos


def visao_geral(caminhos: list[str], destino: str) -> None:
    """Folha de contato (4 por linha) para conferir a peça inteira de uma vez."""
    w, h = 360, 450
    por_linha = 4
    linhas = (len(caminhos) + por_linha - 1) // por_linha
    folha = Image.new("RGB", (w * por_linha + 12 * (por_linha + 1), h * linhas + 12 * (linhas + 1)), (230, 230, 230))
    for i, c in enumerate(caminhos):
        im = Image.open(c).resize((w, h), Image.LANCZOS)
        folha.paste(im, (12 + (i % por_linha) * (w + 12), 12 + (i // por_linha) * (h + 12)))
    folha.save(destino, quality=85)
