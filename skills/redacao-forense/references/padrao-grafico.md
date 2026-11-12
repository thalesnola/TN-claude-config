# Padrão gráfico das figuras da peça

> **Exceção — modo leigo-motion (30/10/2026).** Na IPJ escrita para leitor leigo, as figuras
> seguem o sistema Motion de `references/modo-leigo-motion.md` (seção 6): degradê, sombra e
> cartões **são** o estilo, e a figura **não** leva hash nem rodapé de proveniência (a fonte vai
> no texto; hash só no corpo, logo após material reproduzido de indexação). As regras abaixo continuam valendo para o
> gráfico probatório fora desse modo e para o rascunho do analista.

Vale para gráfico, grafo, diagrama e ficha que entram em relatório ou editorial (seção 2.5 do
`SKILL.md` trata da legenda e do guia de leitura; este arquivo trata do **desenho**). Código de
apoio em `scripts/grafico/` (`estilo_forense.py`), com exemplo sintético e teste.

## Princípio: autenticidade é proveniência, não aparência

A tendência de 2026 é o "anti-AI crafting" (textura, grão, traço manuscrito para parecer feito à
mão). Em peça probatória isso **não se adota**: imitar mão humana é humanwashing e desacredita o
documento. O que dá confiança ao leitor é poder **conferir de onde veio cada dado**. A figura
carrega a própria proveniência.

## Regras

1. **O destino decide o tema.** Peça impressa ou de relatório: fundo branco, SVG estático.
   Mapa ou painel de tela: pode ser escuro, HTML offline. Não herdar o tema de outro gerador.
2. **Moldura fixa:** título que **afirma a conclusão** ("Duas contas concentram 68% dos repasses"),
   subtítulo de escopo, faixa de legenda no topo (nunca num canto), corpo, rodapé.
3. **Rodapé de proveniência, mantido em toda figura:** fonte, folhas (quando conhecidas), SHA512
   dos dados que geraram a figura e data.
   - **Peça final, para inserir em relatório** (modo `final`, o padrão): o rodapé é enxuto e
     **suprime as observações de trabalho** ("ver ficha", folhas ainda não apuradas, "confirmado",
     "a conferir", linha de ressalva). A ressalva da análise vai no texto da peça, na
     autolimitação, e não na imagem.
   - **Rascunho do analista** (modo `rascunho`): mostra tudo, inclusive a ressalva, para conferência.
4. **O rodapé NÃO nomeia script, ferramenta ou versão de geração.** A peça final não menciona o
   meio de geração (ver `README.md`, regra 5 e seção 11 do `SKILL.md`). Script e versão entram
   no manifesto de custódia ao lado do arquivo, não na imagem.
5. **Categoria nunca só por cor.** Combinar três canais: cor (paleta Okabe-Ito, no máximo 6
   categorias), traço do contorno (sólido, tracejado, traço-ponto, pontilhado) e espessura, esta
   em ordem de confiança. A figura precisa sobreviver à impressão em escala de cinza e ao
   daltonismo. Estado do dado (confirmado, inferido, não identificado) segue a mesma regra.
6. **Cada elemento traz a sua fonte** em corpo menor; título de aresta ou conector diz a
   condição observável, não o nome da relação.
7. **Determinismo:** coordenadas fixas, sem script, CDN ou fonte externa, data por parâmetro (não
   pelo relógio). Dado igual produz arquivo idêntico byte a byte.
8. **Evitar:** 3D, pizza, gradiente, sombra, ícone decorativo, emoji.

## Escolha da forma

| Pergunta do leitor | Forma |
|---|---|
| Quem se liga a quem | Grafo (poucos nós: SVG à mão; muitos: gerado) |
| Quando | Linha do tempo horizontal |
| Para onde foi o dinheiro | Fluxo (Sankey) |
| Quanto | Barras ordenadas |
| Onde | Mapa, de preferência offline |

## Verificação antes de entregar

1. `verificar(svg)`: XML válido e largura do texto medida na fonte real, com 10% de folga.
   Peça final: conferir que a imagem não traz "ver ficha", "confirmado" nem ressalva de trabalho no rodapé.
2. `verificar_paleta(...)`: cada par de categorias se distingue em cinza, protanopia,
   deuteranopia e tritanopia (ΔE ≥ 20) **ou** difere no traço/espessura; texto com contraste
   WCAG ≥ 4,5 sobre cada preenchimento.
3. Abrir o SVG no navegador e medir `getBBox` das caixas (a estimativa não substitui o render).
4. PNG: `python scripts/grafico/svg_para_png.py arquivo.svg` (Edge ou Chrome headless, 2x). O
   PNG sai idêntico ao SVG porque usa o mesmo renderizador.
5. `python scripts/grafico/testar_estilo.py` quando o módulo for alterado.

## Cuidados medidos

- Três categorias com contorno sólido, mesmo com paleta segura para daltonismo, **colapsam em
  cinza** (ΔE de 1 a 13). A espessura do contorno resolve.
- Cor reservada a um estado ("a conferir") não pode reaproveitar a família de cor de outra
  categoria. Usar neutro firme: fundo branco e contorno cinza-escuro.
- Importar o módulo de um caso para reaproveitar layout pode **executar** o módulo inteiro e
  regravar arquivos sob manifesto. Migrar gerador de peça sempre em **cópia**, com saída em
  pasta própria, e só depois trocar a pasta de produção, conferindo os hashes do manifesto.
- Estimativa de largura por caractere produz falso vazamento; medir a fonte.
