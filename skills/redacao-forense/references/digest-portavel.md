---
nota: Digest portável da skill redacao-forense. Condensa SKILL.md e references/ em ~170 linhas
  para runtimes onde a skill inteira não cabe (agente local, OpenCode, modelo pequeno).
  Origem: texto encontrado em ~/.config/opencode/AGENTS.md em 12/09/2026, no lugar da
  doutrina de operação do OpenCode; movido para cá. Fonte da verdade continua SKILL.md —
  ao alterar a skill, refazer este digest, não o contrário.
---

# Diretrizes universais de redação forense e elaboração de IPJs

Codifica a metodologia analítica, o estilo de redação e a arquitetura documental medidos num
acervo de 90 Informações Policiais assinadas e juntadas a inquérito (46 da base original + 44
verificadas citação a citação em duas investigações anteriores). Descreve **como o autor
escreve**, não como se escreve em geral — regra geral de bom texto que conflitar com regra
daqui perde.

## 1. O leitor é leigo, mesmo quando o conteúdo é técnico

O destinatário (delegado, MP, juízo) domina o direito, não domina necessariamente perícia,
telemática, fiscal ou cripto. Toda peça deve poder ser entendida por esse leitor sem que ele
precise perguntar o que um termo significa — sem simplificar o conteúdo:

- **Traduzir o termo técnico numa frase, logo após citá-lo** — não em rodapé nem glossário:
  > [...] o que certifica que o dado bruto "baixado" é o mesmo dado enviado pela provedora.
  (hash, explicado no mesmo fôlego da frase que o cita)
- **Simular o raciocínio do leitor leigo/vítima**, refazendo a pesquisa que uma pessoa comum
  faria e mostrando por que ela falha — demonstrar a limitação, não só afirmá-la:
  > Um cidadão comum não poderia pesquisar no site da Receita Federal se o CPF pertence
  > realmente àquela determinada pessoa.
- **Exemplo hipotético abstrato**, com rótulos neutros, para explicar o modus operandi antes
  de aplicá-lo ao caso concreto.
- **Diagrama em texto** do fluxo, quando a etapa invisível importa (ex.: saldo interno →
  ledger da corretora → hot wallet → carteira destino, no caso de criptoativos).
- **Guia de leitura em uma linha** antes de qualquer figura anotada, dizendo o que procurar
  nela, e convenção de cor/marcação nomeada separando o que é original do print do que foi
  inserido pelo analista.
- **Contexto público de tipologia** — operações anteriores já noticiadas, com nome, mês/ano e
  cifra, mostrando que o modus é conhecido, não uma tese isolada da peça.

## 2. Pessoa e postura

Primeira pessoa no **juízo** e na condução do texto ("afirmo", "entendemos", "sugerimos",
"Reproduzo"); impessoal no **dado** ("Constata-se que..."). Nunca inverter — dado em primeira
pessoa soa opinativo, juízo em impessoal esconde quem responde por ele.

**Autolimitação antecipada, obrigatória:** declarar a fraqueza da própria análise antes que a
defesa ou o juízo a encontre, sempre em par — *limite + "Não obstante" + o que já se sustenta
apesar do limite*. Nunca escrever só a ressalva (peça inútil) nem só a conclusão (peça
atacável).

## 3. Metodologia declarada antes do resultado

Peça longa abre com METODOLOGIA, cumprindo: (1) neutralidade declarada com a ressalva honesta
de quando há apontamento; (2) regra de cálculo em alíneas — o que entrou na soma e o que não
foi retirado dela; (3) lacuna nomeada e seu efeito no número (ex.: "quando vier o conceito de
sobra financeira, na visão declarada, estará zerado"); (4) conceito definido com fonte
externa, URL e data de acesso.

## 4. Cadeia de custódia no corpo

Todo arquivo extraído de nuvem ou aparelho entra com identificação, timestamp e hash no
**corpo do texto**, não em anexo: nome, tamanho, timestamp, hash. A transcrição do conteúdo é
**literal** (grafia, abreviação, apelido do investigado preservados); o comentário do analista
vai em bloco separado, dizendo também o que não se sabe.

## 5. A ressalva de justiça

Separar explicitamente o lícito do suspeito dentro do próprio parágrafo que descreve a
conduta: "Não é crime possuir essa prática" — o peso vem do conjunto, não do fato isolado.
Usar sempre que descrever conduta que, isolada, é legal (trocar de aparelho, ter várias
contas, registrar bem em nome de parente).

## 6. A escada de certeza

Cada afirmação recebe o grau que a prova sustenta, explícito no verbo/advérbio:

| Grau | Fórmulas |
|---|---|
| Hipótese | "em tese" · "possivelmente" · "a princípio" · "de forma prematura, estima-se" |
| Indício | "indica" · "há elementos consistentes de" · "depreende-se pelo teor" · "induz que" |
| Reforço | "reforça" · "corroborada por" · "depreende-se que, no mínimo," |
| Demonstração | "restou demonstrado" · "demonstram, inequivocadamente, que" · "fica nítido que" |

"Em tese" é a marca obrigatória para toda conclusão que imputa crime, papel na organização ou
intenção — nunca para o dado técnico em si (IP, hash, valor, contagem são afirmados direto).
Hipóteses concorrentes que não se resolvem são **listadas**, não escolhidas na marra.

## 7. Eixo DECLARADO × OBSERVADO/CONSTATADO (análise patrimonial)

Toda tabela patrimonial roda em duas colunas: o que o investigado **declarou** ao fisco e o
que a investigação **observou/constatou** por telemática, vigilância e fonte aberta. A
variação a descoberto é calculada nas duas visões — é o contraste entre elas que sustenta a
conclusão, não o valor isolado. Definir o conceito com fonte, ao introduzi-lo pela primeira
vez, nunca como jargão pressuposto.

## 8. Estrutura do documento

Peça analítica longa: Cabeçalho → Dados do Procedimento → Contexto (autolimitação + "Não
obstante") → Sumário → Metodologia → blocos por alvo (em espelho, mesma numeração de
subseções para todos, subseção vazia preenchida com a razão, nunca suprimida) → Sugestão →
Conclusão (Resumo dos Achados por alvo + Próximos Passos) → fecho + cidade/data + assinatura.

**Peça que pede medida judicial** (afastamento de sigilo, quebra de dados, interceptação) usa
esqueleto diferente: uma seção por requisito legal do pedido, com o objeto do pedido resumido
logo no início — não uma estrutura analítica com o pedido no fim. Separar sempre os regimes
jurídicos dos itens pedidos (cadastral × registro de acesso × conteúdo × tempo real); termo
inicial provado pela fonte, nunca arbitrado por precaução; achado negativo (ex.: "o alvo não
tem conta em plataforma alguma") é fundamento da necessidade da medida, não lacuna.

**Gêneros curtos** (informe preliminar pós-diligência, status/cobrança de provedor, peça
confirmatória que remete a peça anterior, cadeia de custódia como documento inteiro,
descumprimento de ordem judicial) não seguem o esqueleto longo — abrem direto no fato ou no
cumprimento do expediente, sem a saudação formal obrigatória nesses casos.

## 9. Fechamento — varia por gênero, não é único

| Fecho | Gênero |
|---|---|
| É a informação. | peça analítica longa |
| É o relatório. | levantamento/amostragem curta ou análise isolada |
| É o que tenho/tinha a informar até o momento. | informe curto de status |
| É o relatório com as informações disponíveis até o momento. | peça que pede medida judicial |

Cidade/UF, data por extenso e assinatura sempre presentes, qualquer que seja o fecho.

## 10. Números, fontes e nomes

- Quantidade relevante em algarismo + extenso; percentual sempre pareado com o valor
  absoluto que o origina.
- Tabela exata, prosa arredondada — nunca arredondar dentro da tabela.
- Fonte pública nomeada com URL e data de acesso (órgão de registro, portal, rastreador). O
  canal formal de uma resposta já documentada (sistema estatal específico) também é nomeado;
  a pesquisa de vínculos/inteligência genérica fica em "pesquisas em sistemas".
- Pessoa qualificada por completo na primeira menção (nome, CPF); depois, só o prenome.
  Jargão do investigado entre aspas ("laranjas", "nas sombras", "homem médio").

## 11. Argumentos recorrentes

- **Comportamento anômalo × "homem médio"** — comparar explicitamente a conduta do
  investigado ao que se espera de uma pessoa comum.
- **Desproporção** — movimentação confrontada com capacidade econômica e vínculo formal.
- **Incompatibilidade entre atividade declarada e consumo/movimentação real.**
- **Sócio de fato × sócio legal** — distinguir sempre que divergirem.
- **Convergência operacional** — duas contas/canais distintos apontando para o mesmo destino.

## 12. Anti-padrões

- Vícios de texto corporativo/LLM: "É importante notar que", "Vale destacar que" — preferir
  "Ressalta-se que". "Em resumo," como abertura de conclusão; hedge duplo; adjetivo de
  entusiasmo ou juízo moral ("impressionante", "criminoso contumaz" — preferir "desabonador",
  "incongruência massiva"); emoji e negrito decorativo; pergunta retórica como recurso
  estético geral.
- **Exceções nomeadas e estreitas:** "Em resumo:" é aceitável como abertura de um item
  numerado consolidador dentro de um tópico longo. Pergunta retórica é aceitável apenas como
  fecho de um argumento de lacuna em peça que fundamenta pedido ou aponta descumprimento.
- **Falha mais grave contra esta voz:** suavizar ou omitir a limitação da própria análise
  para a peça parecer mais conclusiva.
- Nunca corrigir ou uniformizar transcrição literal de anotação/mensagem do investigado.
- Nunca nomear sistema policial; nunca deixar de nomear órgão público e data de acesso.

## Antes de entregar

- [ ] Autolimitação no contexto, seguida de "Não obstante" e do que se sustenta?
- [ ] Cada conclusão no degrau certo da escada de certeza; toda imputação com "em tese"?
- [ ] Arquivo de nuvem/aparelho com nome, timestamp, hash e transcrição literal?
- [ ] Conduta lícita descrita ganhou a ressalva de justiça?
- [ ] Fecho compatível com o gênero da peça (ver seção 9)?
- [ ] Nenhum sistema policial nomeado; toda fonte pública com URL e data?
- [ ] Nenhum erro de concordância verbal com sujeito posposto, crase ou regência restou na
      revisão final?

## Erros gramaticais recorrentes a evitar sempre

- **Concordância verbal com sujeito posposto plural:** "foi encontrado inúmeras notícias" →
  "foram encontradas inúmeras notícias". Identificar o sujeito real antes de fixar a flexão.
- **Crase:** antes de substantivo feminino, perguntar se cabe "a que"/"a qual" — se sim,
  crase. Nome próprio masculino nunca leva o artigo craseado antes dele.
- **Particípio/predicativo em voz passiva:** concorda em gênero e número com o sujeito, mesmo
  quando este vem depois ("foi solicitada a cópia", não "foi solicitado a cópia").
- **Grafia de estrangeirismo/sigla:** uma única forma de plural por peça, sem apóstrofo nem
  acento indevido ("hashes"/"IPJs", nunca "Hash´s"/"IPJ´s").

## Modo leigo-motion (IPJ para juiz/promotor leigo, desde 30/10/2026)

- Resposta antes do caminho; termo técnico explicado em meia frase na primeira vez; sem glossário.
- Nunca escrever "o dado não prova": escrever o alcance ("localiza uma área, não uma porta").
- Toda lacuna diz o porquê na mesma frase; nenhum cálculo novo; "em tese" em toda imputação.
- Hash só logo após material reproduzido de indexação (produção própria e resposta de ofício, sem hash); nunca em legenda; só página vertical.
- Estilo padrão de IPJ; "estilo IPJ HASH" só quando pedido. Destinatário: Núcleo de Análise da [UNIDADE].
- Regras completas: `references/modo-leigo-motion.md`. A redação final continua no Claude.
