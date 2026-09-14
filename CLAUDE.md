# posts-consultglass — carrossel técnico do @peritomauricioboschetti

Criado em 14/09/2026 a pedido do Diego: *"monte os 2 carrosséis por semana automáticos,
idêntico ao Venda na Obra — o carrossel que está ativo e rodando hoje"*. É a réplica do
`posts-perffec` (o carrossel técnico de ter/sex do @perffecesquadrias, que por sua vez replica
a mini-aula do @vendanaobra), com a identidade e o CONHECIMENTO do Maurício.

## O que é

2 carrosséis/semana (**terça e sexta, 7h BRT**), 4:5, 7 a 9 slides, conteúdo de
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
| Preparar a semana | `preparar.py --semana` → `imagens/<data>/` + `docs/agenda.json` (+ cópia em `Perffec\Claude\Instagram-Mauricio\` quando roda no PC) |
| Registro do que foi preparado | `preparados.json` (a sequência anda a partir dele) |
| **O app do celular** | `app/` → **https://canteiro-cg.vercel.app** (projeto Vercel `canteiro-cg`, conta site-vendanaobra). QR em `Perffec\Claude\Instagram-Mauricio\QR-canteiro-cg.png` |
| Régua (roda em todo push) | `testes/test_pecas.py` — `python -m unittest discover -s testes` |
| Fotos de capa | `fotos/` — o Maurício em ação, recortadas do acervo dele. Nunca banco de imagem |

## Como sai no ar — À MÃO, pelo app (decisão do Diego, 14/09/2026)

Não publica por API. O Diego escolheu postar do celular, igual ao Canteiro do @vendanaobra,
porque o carrossel leva a **música fixa da conta** (a Graph API não põe música):

1. **Domingo 18h17 BRT** o workflow `preparar.yml` roda `preparar.py --semana`: renderiza as
   duas peças (terça e sexta), commita `imagens/<data>/` e `docs/agenda.json`. A cada push em
   `carrosseis.json`/gerador/fotos ele só **re-renderiza o que já está agendado** (`--refazer`),
   sem avançar a sequência. `workflow_dispatch` aceita `slug` + `data` para refazer uma peça.
2. **Terça e sexta às 7h** o Diego abre o app (`canteiro-cg.vercel.app`, ícone na tela de início),
   toca **Salvar os N slides em Fotos** (Web Share → "Salvar em Fotos", na ordem), **Copiar
   legenda**, abre o Instagram, monta o carrossel com a música fixa, cola a legenda e marca
   **Postado** (fica no aparelho, em `localStorage`).
3. O app lê `docs/agenda.json` e os JPGs direto de `raw.githubusercontent.com` (repo público) —
   por isso não precisa republicar o app quando entra peça nova; a Vercel só muda quando `app/`
   muda (`XDG_DATA_HOME="$APPDATA/xdg.data" npx vercel@latest --prod --yes` na RAIZ do repo — o
   `vercel.json` da raiz aponta `outputDirectory: app`; a Vercel também faz deploy sozinha a cada push
   pela integração com o GitHub, e é por isso que o config tem de estar na raiz: em 14/09 o deploy
   automático da raiz sem `outputDirectory` deu 404 no link que o Diego abriu).

O caminho por API ficou documentado no cérebro caso um dia volte: a conta é profissional, o
app Meta "Palavra Viva Reels" tem @peritomauricioboschetti como Testador do Instagram
(convite pendente, inofensivo), e faltaria só aceitar o convite e gerar o token.

## Decisões

- **Identidade própria da Consult Glass**: navy `#061528` + teal `#1EA9B8` + prata, Plus Jakarta
  Sans no texto e Bai Jamjuree nas etiquetas (as fontes do site mauricio.consultglass.net.br).
  Não é a da Perffec (preto/verde/Archivo) nem a do @vendanaobra: os três não se misturam.
- **Blocos**: "A norma diz / A lei diz" (teal-claro, sempre com `fonte`), "Onde vira processo"
  (vermelho) e "Na perícia" (navy) — o caso ou o critério. O "Na perícia" substitui o "Na Perffec":
  a prova de autoridade aqui é o caso, não a empresa.
- **CTA em ciclo de produto** (Diego, 14/09/2026): seguir o perfil → **Venda Blindada** (contrato
  técnico para quem fabrica e instala) → **Perícia técnica** (quando o dano já existe) → **Método
  Blindar** (consultoria para construtoras). Sempre na voz do Maurício, texto da LP dele — nunca a
  do Diego/Venda na Obra. O último slide (`produto`) e o fecho da legenda carregam a oferta; a
  pergunta de engajamento continua antes. Sem "comente a palavra" (não há robô de Direct).
- **Frases curtas** (regra do Diego, 14/09/2026): capa ≤ 8 palavras, título ≤ 14, corpo ≤ 32,
  item = rótulo + uma linha. O teste reprova o que passar disso.
- **O que ele diz mas não foi confirmado NÃO entra como fato** (eng. mecânico obrigatório no CREA,
  30% do VGV, 40-50% da fábrica, os números do carrossel NBR 7199 do @consult.glass). O teste
  também barra isso. Lista completa em `25 Consult Glass/Base legal e normativa conferida.md`.
- **CDC art. 39, inciso VIII** (não IV, como ele às vezes fala).
- Terça e sexta, 7h — pedido do Diego (mesmos dias do Perffec; os dois saem pelo celular na mesma manhã).

## Régua

Primeira leitura em **12/10/2026** (4 semanas, 8 peças): salvamentos e compartilhamentos por peça
(Insights do app), alcance de não seguidores, e se algum engenheiro/construtora chegou pelo post ou
pelo Raio-X. Comparar com a mediana do acervo dele (Reel 27, carrossel 29,5 curtidas). Se
salvamentos caírem por 3 peças seguidas, mudar o tipo de capa antes de mudar o conteúdo.

## Escrever peça nova

1. Escolher tema na `PAUTA-CARROSSEIS.md` — só o que tem fonte dele ou lei/norma conferida.
2. Adicionar em `pecas` e em `sequencia` no `carrosseis.json`, com o campo `fonte` preenchido.
3. `python -m unittest discover -s testes` (tem de passar).
4. `python preparar.py --slug <slug> --data <AAAA-MM-DD>` e olhar `imagens/<data>/visao-geral.jpg`.

## Rodar

```powershell
python preparar.py --semana                          # as duas da próxima semana → imagens/, docs/agenda.json
python preparar.py --slug <slug> --data 2026-09-19   # refaz uma peça numa data
python preparar.py --refazer                         # re-renderiza o que já está agendado
python -m unittest discover -s testes
```
