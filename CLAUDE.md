# posts-consultglass — carrossel técnico do @peritomauricioboschetti

Criado em 14/09/2026 a pedido do Diego: *"monte os 2 carrosséis por semana automáticos,
idêntico ao Venda na Obra — o carrossel que está ativo e rodando hoje"*. É a réplica do
`posts-perffec` (o carrossel técnico de ter/sex do @perffecesquadrias, que por sua vez replica
a mini-aula do @vendanaobra), com a identidade e o CONHECIMENTO do Maurício.

## O que é

2 carrosséis/semana (**segunda e quinta, 7h BRT**), 4:5, 7 a 9 slides, conteúdo de
responsabilidade técnica, norma, perícia, esquadria, vidro, fachada e guarda-corpo, para
construtora, incorporadora, engenheiro, arquiteto e síndico. **Toda peça sai do que o
Maurício já disse em público** (4 podcasts, 102 Reels transcritos, legendas, palestras) ou de
lei/norma conferida na fonte — nunca de invenção. O conhecimento dele está no cérebro,
território `25 Consult Glass` (ler `Voz do Maurício`, `Base legal e normativa conferida` e
`Casos periciais do Maurício` antes de escrever peça nova). Material bruto em
`Desktop\Perffec\Claude\Consult-Glass-Conhecimento\`.

| Peça | Onde |
|---|---|
| Banco de peças (regras, sequência, slides, legenda) | `carrosseis.json` |
| Pauta (temas com fonte e status) | `PAUTA-CARROSSEIS.md` |
| Render | `gerar_carrossel.py` (Pillow, Plus Jakarta Sans + Bai Jamjuree, navy/teal da Consult Glass) |
| Publicação automática | `publicar.py` + `.github/workflows/carrossel.yml` |
| Preparar à mão | `python preparar.py --semana` → `saida/` + `Perffec\Claude\Instagram-Mauricio\<data>-<slug>\` |
| Régua (roda em todo push) | `testes/test_pecas.py` — `python -m unittest discover -s testes` |
| Fotos de capa | `fotos/` — o Maurício em ação, recortadas do acervo dele (Reels e fotos do perfil). Nunca banco de imagem |

## Como sai no ar

`carrossel.yml` roda segunda e quinta (09:45 UTC espera até 10:00 = 7h BRT; repescagens 08:07 e
12:23 BRT com `--garantir`). `publicar.py` renderiza, commita as imagens (repo **público** porque a
API só aceita URL pública — `raw.githubusercontent`), sobe o carrossel e registra em
`publicados.json`. Falha abre issue.

**Token**: a conta do Maurício é profissional (business, id `17841472330631162`) mas NÃO está no
portfólio empresarial do Diego — o token de usuário do app vendanaobra não a alcança. O caminho é
a **API do Instagram com login do Instagram** (`config.json: "api": "instagram"`, host
`graph.instagram.com`): token de 60 dias, renovável com `refresh_access_token`. Secret
`META_TOKEN_MAURICIO`; `ig_user_id` e `token_vence_em` em `config.json`. Renovar: `python
renovar_token.py` (lê `Perffec\Claude\meta_token_mauricio.txt`, pede o token novo, grava o secret
com a credencial do git, como o posts-perffec fez em 14/09). `publicar.py` aborta e abre issue com
< 10 dias.

## Decisões

- **Identidade própria da Consult Glass**: navy `#061528` + teal `#1EA9B8` + prata, Plus Jakarta
  Sans no texto e Bai Jamjuree nas etiquetas (as fontes do site mauricio.consultglass.net.br).
  Não é a da Perffec (preto/verde/Archivo) nem a do @vendanaobra: os três não se misturam.
- **Blocos**: "A norma diz / A lei diz" (teal-claro, sempre com `fonte`), "Onde vira processo"
  (vermelho) e "Na perícia" (navy) — o caso ou o critério. O "Na perícia" substitui o "Na Perffec":
  a prova de autoridade aqui é o caso, não a empresa.
- **CTA em ciclo** salvar → enviar → pergunta, sem "comente a palavra" (não há robô de Direct).
  Último slide leva o Raio-X da Obra (`/raio-x-da-obra`) — o boi de piranha do plano de crescimento.
- **Frases curtas** (regra do Diego, 14/09/2026): capa ≤ 8 palavras, título ≤ 14, corpo ≤ 32,
  item = rótulo + uma linha. O teste reprova o que passar disso.
- **O que ele diz mas não foi confirmado NÃO entra como fato** (eng. mecânico obrigatório no CREA,
  30% do VGV, 40-50% da fábrica, os números do carrossel NBR 7199 do @consult.glass). O teste
  também barra isso. Lista completa em `25 Consult Glass/Base legal e normativa conferida.md`.
- **CDC art. 39, inciso VIII** (não IV, como ele às vezes fala).
- Dias seg/qui para não coincidir com o Perffec (ter/sex) na mesma manhã do Diego.

## Régua

Primeira leitura em **12/10/2026** (4 semanas, 8 peças): salvamentos e compartilhamentos por peça
(Insights do app), alcance de não seguidores, e se algum engenheiro/construtora chegou pelo post ou
pelo Raio-X. Comparar com a mediana do acervo dele (Reel 27, carrossel 29,5 curtidas). Se
salvamentos caírem por 3 peças seguidas, mudar o tipo de capa antes de mudar o conteúdo.

## Escrever peça nova

1. Escolher tema na `PAUTA-CARROSSEIS.md` — só o que tem fonte dele ou lei/norma conferida.
2. Adicionar em `pecas` e em `sequencia` no `carrosseis.json`, com o campo `fonte` preenchido.
3. `python -m unittest discover -s testes` (tem de passar).
4. `python publicar.py --ensaio --slug <slug>` e olhar `imagens/<data>/visao-geral.jpg`.

## Rodar

```powershell
python publicar.py --ensaio                          # a próxima da sequência, sem publicar
python publicar.py --ensaio --slug <slug>            # uma peça específica
python preparar.py --semana                          # entrega para postar à mão
python -m unittest discover -s testes
```
