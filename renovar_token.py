# -*- coding: utf-8 -*-
"""Renova o token de 60 dias da API do Instagram (login do Instagram) e grava o secret.

    python renovar_token.py            # renova o token salvo em meta_token_mauricio.txt
    python renovar_token.py --novo X   # grava um token novo (gerado no painel da Meta)

Um token de longa duração pode ser renovado a qualquer momento depois de 24 h de vida e antes
de vencer: GET graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token. O token
novo vai para Perffec/Claude/meta_token_mauricio.txt, para config.json (token_vence_em) e
para o secret META_TOKEN_MAURICIO do repositório (API do GitHub com a credencial do git).
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
    gravar_secret("META_TOKEN_MAURICIO", novo)
    print("secret META_TOKEN_MAURICIO gravado; commitar config.json")


def gravar_secret(nome: str, valor: str) -> None:
    """Grava o secret pela API do GitHub com a credencial do git (o `gh` não está logado neste PC)."""
    import base64
    import sys
    try:
        from nacl import encoding, public  # type: ignore
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "pynacl"], check=True)
        from nacl import encoding, public  # type: ignore
    cred = subprocess.run(["git", "credential", "fill"], input="protocol=https" + chr(10) + "host=github.com" + chr(10) + chr(10),
                          capture_output=True, text=True, check=True).stdout
    gh = next(l.split("=", 1)[1] for l in cred.splitlines() if l.startswith("password="))
    hdr = {"Authorization": f"token {gh}", "Accept": "application/vnd.github+json"}
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/actions/secrets/public-key", headers=hdr)
    with urllib.request.urlopen(req) as r:
        chave = json.loads(r.read())
    pk = public.PublicKey(chave["key"].encode(), encoding.Base64Encoder())
    cifrado = base64.b64encode(public.SealedBox(pk).encrypt(valor.encode())).decode()
    body = json.dumps({"encrypted_value": cifrado, "key_id": chave["key_id"]}).encode()
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/actions/secrets/{nome}",
                                 data=body, headers=hdr, method="PUT")
    with urllib.request.urlopen(req) as r:
        print(f"secret {nome}:", r.status)


if __name__ == "__main__":
    main()
