# -*- coding: utf-8 -*-
"""Renova o token de 60 dias da API do Instagram (login do Instagram) e grava o secret.

    python renovar_token.py            # renova o token salvo em meta_token_mauricio.txt
    python renovar_token.py --novo X   # grava um token novo (gerado no painel da Meta)

Um token de longa duração pode ser renovado a qualquer momento depois de 24 h de vida e antes
de vencer: GET graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token. O token
novo vai para Perffec\Claude\meta_token_mauricio.txt, para config.json (token_vence_em) e
para o secret META_TOKEN_MAURICIO do repositório (via `gh secret set`).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE, "config.json")
TOKEN_LOCAL = r"C:\Users\NOTE\Desktop\Perffec\Claude\meta_token_mauricio.txt"
REPO = "diegohenriquemoraes-eng/posts-consultglass"


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--novo", help="token novo gerado no painel da Meta (curto ou longo)")
    a = ap.parse_args()

    if a.novo:
        token = a.novo.strip()
    else:
        with open(TOKEN_LOCAL, encoding="utf-8") as f:
            token = f.read().strip()

    r = _get("https://graph.instagram.com/refresh_access_token?" +
             urllib.parse.urlencode({"grant_type": "ig_refresh_token", "access_token": token}))
    novo = r["access_token"]
    vence = datetime.now() + timedelta(seconds=int(r.get("expires_in", 60 * 86400)))
    me = _get("https://graph.instagram.com/v21.0/me?" +
              urllib.parse.urlencode({"fields": "user_id,username", "access_token": novo}))
    print(f"token renovado para @{me.get('username')} (user_id {me.get('user_id')}), vence em {vence:%d/%m/%Y}")

    with open(TOKEN_LOCAL, "w", encoding="utf-8") as f:
        f.write(novo + "\n")
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    cfg["token_vence_em"] = vence.strftime("%Y-%m-%d")
    if me.get("user_id"):
        cfg["ig_user_id"] = str(me["user_id"])
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    subprocess.run(["gh", "secret", "set", "META_TOKEN_MAURICIO", "--repo", REPO, "--body", novo], check=True)
    print("secret META_TOKEN_MAURICIO gravado; commitar config.json")


if __name__ == "__main__":
    main()
