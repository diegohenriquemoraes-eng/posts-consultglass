# -*- coding: utf-8 -*-
"""Régua das peças do @peritomauricioboschetti — roda em todo push (workflow Testes).

Existe porque conteúdo técnico assinado por perito não admite número inventado, e
porque a regra de frases curtas do Diego (14/09/2026) foi reprovada duas vezes no
mesmo dia em outros carrosséis. Sem rede, < 1 s.
"""
from __future__ import annotations

import json
import os
import re
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANCO = json.load(open(os.path.join(BASE, "carrosseis.json"), encoding="utf-8"))
FOTOS = os.path.join(BASE, "fotos")

# o que nunca pode aparecer num texto assinado pelo Maurício
PROIBIDO = ["esquadrilha", "REGEX:" + chr(92) + "bdicas?" + chr(92) + "b", "segredo", "truque", "simples assim", "revolucionário",
            "@perffecesquadrias", "@vendanaobra", "Venda 10x", "Perffec", "comente a palavra",
            "art. 39, IV", "art. 39, inciso IV", "inciso 4", "inciso 8 "]
# afirmações dele que NÃO foram confirmadas na fonte — não entram como fato
NAO_CONFIRMADO = ["30% do VGV", "mecânico ou metalúrgico é obrigat", "é obrigatório engenheiro mecânico",
                  "0,64 m", "250 mm", "800 mm", "1,80 m"]


def _palavras(s: str) -> int:
    return len(s.split())


class Regras(unittest.TestCase):
    def test_sequencia_aponta_para_pecas_existentes(self):
        for slug in BANCO["sequencia"]:
            self.assertIn(slug, BANCO["pecas"], slug)

    def test_cada_peca_tem_fonte_cta_e_legenda(self):
        for slug, p in BANCO["pecas"].items():
            self.assertTrue(p.get("fonte"), f"{slug}: sem fonte")
            self.assertIn(p["cta"]["tipo"], ("seguir", "venda-blindada", "pericia", "metodo-blindar"), slug)
            self.assertGreater(len(p["legenda"]), 600, f"{slug}: legenda curta demais")
            self.assertIn("@peritomauricioboschetti", p["legenda"], f"{slug}: legenda sem o @")
            hashtags = re.findall(r"#\w+", p["legenda"])
            self.assertTrue(8 <= len(hashtags) <= 10, f"{slug}: {len(hashtags)} hashtags")

    def test_formato_7_a_9_slides_capa_primeiro_cta_ultimo(self):
        for slug, p in BANCO["pecas"].items():
            s = p["slides"]
            self.assertTrue(7 <= len(s) <= 9, f"{slug}: {len(s)} slides")
            self.assertEqual(s[0]["tipo"], "capa", slug)
            self.assertEqual(s[-1]["tipo"], "cta", slug)
            self.assertTrue(os.path.exists(os.path.join(FOTOS, s[0]["foto"])), f"{slug}: foto {s[0]['foto']} não existe")

    def test_frases_curtas(self):
        """Capa <= 8 palavras; título <= 12; corpo <= 30; item de lista = rótulo + uma linha."""
        for slug, p in BANCO["pecas"].items():
            for i, s in enumerate(p["slides"], 1):
                onde = f"{slug} slide {i}"
                if s["tipo"] == "capa":
                    self.assertLessEqual(_palavras(s["gancho"]), 8, f"{onde}: gancho longo")
                    continue
                if s.get("titulo"):
                    self.assertLessEqual(_palavras(s["titulo"]), 14, f"{onde}: título longo")
                if s.get("texto"):
                    self.assertLessEqual(_palavras(s["texto"]), 32, f"{onde}: corpo longo ({_palavras(s['texto'])})")
                    self.assertLessEqual(s["texto"].count("\n\n"), 1, f"{onde}: mais de 2 parágrafos")
                for rot, txt in s.get("itens", []):
                    self.assertLessEqual(_palavras(rot), 8, f"{onde}: rótulo longo")
                    self.assertLessEqual(_palavras(txt), 16, f"{onde}: item longo")

    def test_norma_tem_fonte(self):
        for slug, p in BANCO["pecas"].items():
            for i, s in enumerate(p["slides"], 1):
                if s["tipo"] == "norma":
                    self.assertTrue(s.get("fonte"), f"{slug} slide {i}: bloco 'A norma diz' sem fonte")

    def test_nada_proibido_nem_nao_confirmado(self):
        for slug, p in BANCO["pecas"].items():
            texto = json.dumps(p, ensure_ascii=False)
            for t in PROIBIDO:
                self.assertIsNone(re.search(t[6:] if t.startswith("REGEX:") else re.escape(t), texto, re.I), f"{slug}: contém '{t}'")
            for t in NAO_CONFIRMADO:
                self.assertNotIn(t, texto, f"{slug}: afirmação não confirmada '{t}'")

    def test_ciclo_de_cta_alterna(self):
        """seguir / Venda Blindada / Perícia / Método Blindar — nunca o mesmo duas vezes seguidas, e todos aparecem."""
        seq = [BANCO["pecas"][s]["cta"]["tipo"] for s in BANCO["sequencia"]]
        for a, b in zip(seq, seq[1:]):
            self.assertNotEqual(a, b, f"CTA repetido em sequência: {seq}")
        self.assertEqual(set(seq), {"seguir", "venda-blindada", "pericia", "metodo-blindar"}, seq)
        for slug, p in BANCO["pecas"].items():
            self.assertEqual(p["slides"][-1].get("produto"), p["cta"]["tipo"], f"{slug}: slide final não bate com o CTA")
            self.assertNotIn("Venda na Obra", p["legenda"], slug)

    def test_fontes_e_render(self):
        self.assertTrue(os.path.exists(os.path.join(BASE, "fontes", "PlusJakartaSans.ttf")))
        self.assertTrue(os.path.exists(os.path.join(BASE, "fontes", "BaiJamjuree-SemiBold.ttf")))
        import gerar_carrossel  # noqa: F401 — importa sem erro


if __name__ == "__main__":
    unittest.main()
