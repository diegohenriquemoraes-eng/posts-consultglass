# -*- coding: utf-8 -*-
"""Prepara os carrosséis da semana do @peritomauricioboschetti para o Diego postar do celular.

Decisão do Diego (14/09/2026): NÃO publica sozinho — sai toda **terça e sexta às 7h**, à
mão, pelo app Canteiro Consult Glass, com a música fixa da conta. Este script é o que
roda no GitHub Actions (`preparar.yml`, domingo 18h BRT e a cada push em `carrosseis.json`):

  1. escolhe as próximas peças da `sequencia` que ainda não foram preparadas
  2. renderiza os slides em imagens/<data>/ (o repo é público: o app lê daqui)
  3. escreve docs/agenda.json — o que o app mostra: data, hora, título, slides, legenda, CTA
  4. registra em preparados.json (a sequência anda a partir dele)

Uso:
    python preparar.py --semana            # as duas da próxima semana (terça e sexta)
    python preparar.py --semana --data 2026-09-22
    python preparar.py --todas             # agenda tudo o que está escrito (Diego, 14/09: "várias semanas")
    python preparar.py --slug X --data 2026-09-19   # refaz uma peça sem mexer na sequência
    python preparar.py --refazer           # re-renderiza o que já está agendado (roda a cada push)
    python preparar.py --so-agenda         # só reescreve docs/agenda.json a partir de preparados.json

Local (Windows) também copia cada peça para Perffec\\Claude\\Instagram-Mauricio\\<data>-<slug>\\.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil

from gerar_carrossel import gerar, visao_geral

BASE = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(BASE, "carrosseis.json")
PREPARADOS = os.path.join(BASE, "preparados.json")
AGENDA = os.path.join(BASE, "docs", "agenda.json")
IMAGENS = os.path.join(BASE, "imagens")
ENTREGA = r"C:\Users\NOTE\Desktop\Perffec\Claude\Instagram-Mauricio"
REPO_RAW = "https://raw.githubusercontent.com/diegohenriquemoraes-eng/posts-consultglass/main"

DIAS = (1, 4)  # terça e sexta (segunda = 0)
HORA = "07:00"
MUSICA = "música fixa da conta"  # trocar quando o Diego escolher
NOME_DIA = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
CTA_NOME = {"seguir": "Seguir o perfil", "venda-blindada": "Venda Blindada", "pericia": "Perícia técnica",
            "metodo-blindar": "Método Blindar"}


def _carregar(caminho: str, padrao):
    if not os.path.exists(caminho):
        return padrao
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def _salvar(caminho: str, dados) -> None:
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        f.write("\n")


def proximas_datas(a_partir: dt.date, n: int) -> list[dt.date]:
    datas, d = [], a_partir
    while len(datas) < n:
        if d.weekday() in DIAS:
            datas.append(d)
        d += dt.timedelta(days=1)
    return datas


def renderizar(slug: str, data: dt.date, banco: dict) -> dict:
    """Renderiza a peça em imagens/<data>/ e devolve o item da agenda."""
    peca = banco["pecas"][slug]
    pasta = os.path.join(IMAGENS, data.isoformat())
    if os.path.isdir(pasta):
        shutil.rmtree(pasta)
    caminhos = gerar(peca, pasta)
    visao_geral(caminhos, os.path.join(pasta, "visao-geral.jpg"))
    with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
        f.write(peca["legenda"].strip() + "\n")
    item = {
        "data": data.isoformat(),
        "dia": NOME_DIA[data.weekday()],
        "hora": HORA,
        "slug": slug,
        "titulo": peca["titulo"],
        "cta": CTA_NOME.get(peca["cta"]["tipo"], peca["cta"]["tipo"]),
        "musica": MUSICA,
        "slides": [f"{REPO_RAW}/imagens/{data.isoformat()}/{os.path.basename(c)}" for c in caminhos],
        "legenda": peca["legenda"].strip(),
    }
    if os.name == "nt" and os.path.isdir(os.path.dirname(ENTREGA)):
        destino = os.path.join(ENTREGA, f"{data.isoformat()}-{slug}")
        if os.path.isdir(destino):
            shutil.rmtree(destino)
        shutil.copytree(pasta, destino)
    return item


def escrever_agenda(preparados: list, banco: dict) -> None:
    itens = []
    for p in preparados:
        data = dt.date.fromisoformat(p["data"])
        pasta = os.path.join(IMAGENS, p["data"])
        slides = sorted(f for f in os.listdir(pasta) if f.startswith("slide-")) if os.path.isdir(pasta) else []
        peca = banco["pecas"][p["slug"]]
        itens.append({
            "data": p["data"], "dia": NOME_DIA[data.weekday()], "hora": HORA, "slug": p["slug"],
            "titulo": peca["titulo"], "cta": CTA_NOME.get(peca["cta"]["tipo"], peca["cta"]["tipo"]),
            "musica": MUSICA,
            "slides": [f"{REPO_RAW}/imagens/{p['data']}/{s}" for s in slides],
            "legenda": peca["legenda"].strip(),
        })
    itens.sort(key=lambda i: i["data"])
    _salvar(AGENDA, {"gerado_em": dt.datetime.now().isoformat(timespec="minutes"),
                     "regra": "terça e sexta, 7h, à mão pelo app, com a música fixa", "itens": itens})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--semana", action="store_true", help="prepara as duas peças da próxima semana")
    ap.add_argument("--todas", action="store_true", help="agenda TODAS as peças escritas ainda não preparadas, terça e sexta em sequência")
    ap.add_argument("--slug", help="prepara uma peça específica (não avança a sequência)")
    ap.add_argument("--data", help="AAAA-MM-DD da primeira publicação")
    ap.add_argument("--so-agenda", action="store_true")
    ap.add_argument("--refazer", action="store_true", help="re-renderiza as peças já agendadas (a partir de hoje) sem avançar a sequência")
    args = ap.parse_args()

    banco = _carregar(BANCO, {})
    preparados = _carregar(PREPARADOS, [])

    if args.so_agenda:
        escrever_agenda(preparados, banco)
        print("agenda reescrita")
        return

    if args.refazer:
        hoje_iso = dt.date.today().isoformat()
        for p in preparados:
            if p["data"] >= hoje_iso and p["slug"] in banco["pecas"]:
                renderizar(p["slug"], dt.date.fromisoformat(p["data"]), banco)
                print(f"refeito: {p['data']} {p['slug']}")
        escrever_agenda(preparados, banco)
        return

    hoje = dt.date.today()
    inicio = dt.date.fromisoformat(args.data) if args.data else hoje + dt.timedelta(days=1)

    if args.slug:
        data = inicio if args.data else proximas_datas(inicio, 1)[0]
        renderizar(args.slug, data, banco)
        # substitui a entrada daquela data, se existir
        preparados = [p for p in preparados if p["data"] != data.isoformat()]
        preparados.append({"slug": args.slug, "data": data.isoformat(), "preparado_em": hoje.isoformat()})
        preparados.sort(key=lambda p: p["data"])
        _salvar(PREPARADOS, preparados)
        escrever_agenda(preparados, banco)
        print(f"preparado (avulso): {data.isoformat()} {args.slug}")
        return

    feitos = {p["slug"] for p in preparados}
    ocupadas = {p["data"] for p in preparados}
    fila = [s for s in banco["sequencia"] if s not in feitos]
    futuras = [p for p in preparados if p["data"] >= hoje.isoformat()]
    if not fila:
        if len(futuras) >= 2:
            print(f"fila de peças escritas acabou, mas há {len(futuras)} já agendadas até {futuras[-1]['data']} — nada a fazer")
            escrever_agenda(preparados, banco)
            return
        raise SystemExit("Sequência esgotada: escreva peças novas em carrosseis.json (ver PAUTA-CARROSSEIS.md).")
    quantos = len(fila) if args.todas else (2 if args.semana else 1)
    # pula datas que já têm peça (idempotente: rodar duas vezes no domingo não duplica)
    datas = [d for d in proximas_datas(inicio, quantos + len(ocupadas)) if d.isoformat() not in ocupadas][:quantos]
    for slug, data in zip(fila[:quantos], datas):
        renderizar(slug, data, banco)
        preparados.append({"slug": slug, "data": data.isoformat(), "preparado_em": hoje.isoformat()})
        print(f"{data.isoformat()} ({NOME_DIA[data.weekday()]}) {slug}")
    preparados.sort(key=lambda p: p["data"])
    _salvar(PREPARADOS, preparados)
    escrever_agenda(preparados, banco)
    restantes = len(fila) - len(datas)
    print(f"restam {restantes} peça(s) escritas na sequência" + (" — ESCREVER MAIS" if restantes < 2 else ""))


if __name__ == "__main__":
    main()
