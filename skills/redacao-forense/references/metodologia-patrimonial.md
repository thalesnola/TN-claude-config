# Método analítico patrimonial — o esqueleto que o usuário usa

Extraído da peça de cruzamento de dados fiscais, bancários e telemáticos (autoria integral do
usuário). Serve a qualquer caso com afastamento bancário + fiscal + telemático — as mesmas
medidas em curso em outros inquéritos. Reaproveitar a **estrutura e os conceitos**; os números
e alvos são sempre do caso em análise.

## 1. O que declarar na METODOLOGIA, antes de qualquer número

Alíneas a)–h), nesta lógica:

| Alínea | Declara | Por que existe |
|---|---|---|
| Regra da soma | o valor movimentado é **crédito + débito** de todas as contas do CPF/CNPJ, **sem** retirar transação entre contas do próprio titular | o número fica maior, mas é o que o sistema entregou; retirar sem dizer é adulterar a base |
| Janela dos dados fiscais | anos-calendário cobertos, e o exercício que **falta** | explica por que a coluna DECLARADA zera no último ano |
| "NÃO DISPONÍVEL" | significa **não houve entrega da declaração** | ausência de dado ≠ dado zero; a distinção é o achado |
| Origem das NF-e | teor das notas, tratado como **OBSERVADO/CONSTATADO**, na rubrica DESPESAS | separa o que o alvo declarou do que ele efetivamente comprou |
| Conceitos | **sobra financeira** e **variação patrimonial a descoberto**, definidos com fonte, URL e data de acesso | a peça é lida por quem não é analista fiscal |
| OBSERVADO/CONSTATADO | de onde vem (sistemas, redes sociais, vigilância in loco e, principalmente, telemática) e **por que é essencial** | é o conceito que permite alcançar o bem que não está no nome do alvo |
| Limite do dado de criptoativos | o órgão fiscal só vê o que passou por empresa declarante; **P2P não aparece** | evita que o total seja lido como universo |

## 2. Fórmula da variação a descoberto

```
sobra financeira        = rendimentos líquidos − despesas − aumento do patrimônio líquido
acréscimo coberto       : renda líquida  >  acréscimo patrimonial
acréscimo a descoberto  : renda líquida  <  acréscimo patrimonial
```

A tabela roda em **duas visões lado a lado**, e é a divergência entre elas que fala:

| Ano | DECLARADA — sobra | DECLARADA — a descoberto | OBSERVADA — sobra | OBSERVADA — a descoberto |
|---|---|---|---|---|

Leitura típica do achado: a coluna DECLARADA fecha ou fica levemente negativa; a
OBSERVADA/CONSTATADA explode no ano em que entram os bens localizados por telemática e
vigilância. **É esse contraste que a peça precisa deixar visível**, não o valor isolado.

## 3. Bloco por alvo (espelho — não reordenar, não suprimir)

```
N.   <NOME/RAZÃO SOCIAL>, CPF/CNPJ <…>
N.1  MOVIMENTAÇÃO BANCÁRIA TOTAL            → soma créditos | soma débitos | valor movimentado
N.2  MOVIMENTAÇÃO BANCÁRIA TOTAL POR ANO    → mesma tríade, por ano
N.3  BENS DECLARADOS x PATRIMÔNIO OBSERVADO → duas colunas por ano
N.4  VARIAÇÃO PATRIMONIAL A DESCOBERTO      → duas visões
N.5  Notas Fiscais Eletrônicas (NF-e)       → como emissor / como destinatário, total por ano
N.6  ANÁLISE DO PERFIL DE COMPRAS (PF)  |  COMPATIBILIDADE ATIVIDADE x NF-e (PJ)
N.7+ CRIPTOMOEDAS · OSTENTAÇÃO · <específico do alvo>
```

Subseção sem dado **permanece**, preenchida com a razão: "Não disponível", "Nunca declarou
imposto de renda", "Não existem NF-e como emissor".

### N.6 — como caracterizar o perfil de compras

1. Percentual da categoria dominante sobre o total ("veículos, cerca de 86,9%").
2. Tabela **produto/descrição com maior gasto × valor acumulado** — descrição completa do bem
   (marca, modelo, ano, placa, renavam, chassi), que é o que permite constrição depois.
3. Tabela **categoria × valor total**, da maior para a menor.
4. Onde as compras foram **entregues** — o endereço de entrega denuncia residência real.
5. Quando um lote de compras caracteriza mobiliar um imóvel, contar os itens e o intervalo:
   "São 52 tipos de produtos comumente usados em residências, quase R$ 150 mil entre [data] e
   [data]", e concluir: "Isso demonstra que [ALVO] tem investido neste local como sua nova
   residência, e não apenas local de passeio."
6. **Tradução aritmética do dado bruto para escala cotidiana** — converter a cifra abstrata
   num objeto contável que o leitor leigo visualiza: *"dez iPhones equivalem a R$ 50.000,00
   [...] o que significa que sua perda corresponde a quarenta iPhones"* (⚠️ exemplo de peça
   de autoria mista; usar a técnica — já confirmada em outras partes do acervo — sem citar a
   frase como voz exclusiva do usuário até haver confirmação em peça de autoria exclusiva).

### N.6' — compatibilidade entre atividade empresarial e NF-e

Confrontar o CNAE/atividade declarada com o que a empresa comprou e vendeu. O achado é a
incompatibilidade nominada: compra de item de luxo por empresa do ramo alimentício; empresa que gasta várias
vezes o que arrecada; ausência total de NF-e de saída.

## 4. Criptoativos

- Reproduzir a tabela do órgão fiscal como veio: declarante (CNPJ e nome empresarial), tipo de
  operação, data, símbolo, quantidade, valor — **com totais ao final**.
- Ressalva obrigatória: o dado fiscal não cobre P2P.
- Carteiras localizadas em nuvem/e-mail entram pelo endereço completo, e o estado de cada uma
  é dito ("praticamente zeradas em saldo, com exceção de [.], que está com o mesmo saldo que
  [ALVO] enviou em [data]").
- Explicar ao leitor **o que a blockchain não mostra** (diagrama saldo interno → ledger → hot
  wallet → carteira destino), para justificar por que o afastamento na corretora é necessário.
- Consulta em fonte aberta para movimentação pretérita: quantidade de lançamentos, entradas e
  saídas por ativo, em cripto e em reais.
- Caracterizar a função da carteira, não só o volume: **receptora inicial**, **repassadora**,
  **nó centralizador**; e o critério — coincidência temporal, proximidade de valores,
  recorrência operacional.
- Fechar com o pedido: identificar **beneficiário final**, porque o volume transacionado é o
  indicador mais preciso da escala real.

## 5. Contabilidade encontrada em nuvem

Uma subseção por arquivo, nomeada pelo **próprio nome do arquivo**. Dentro: identificação +
timestamp + hash → transcrição literal entre linhas de hífens → `COMENTÁRIOS:` com a
identificação dos apelidos e o que **não** se conseguiu identificar.

O valor probatório está em três coisas, e a peça precisa dizê-las: que a anotação é **do
próprio investigado**, que ela registra **débito e crédito com nome de terceiros**, e que os
valores **casam** (ou não) com a movimentação bancária e as NF-e já apresentadas.

## 6. Bens e logística em nome de terceiro

Cadeia a percorrer, sempre nomeando a fonte pública de cada elo:

```
bem (veículo/aeronave/imóvel)
  → registro público do bem (órgão de trânsito, autoridade de aviação, cartório/matrícula)
  → titular formal (PF ou PJ)
  → composição societária e capital social da PJ
  → endereço da PJ (escritório de contabilidade compartilhado = sinal)
  → vínculo do titular formal com o alvo (viagem no mesmo localizador, rede social,
    comunicação, transação)
```

Sinais que o acervo trata como relevantes e nomeia: várias empresas no **mesmo endereço** de
escritório contábil; capital social incompatível com o bem; sócio que **já residiu** na cidade
do núcleo; viagens **no mesmo localizador**; publicação em rede social que **coincide** com o
histórico de voo consultado em fonte aberta.

## 7. Conclusão da peça

- **RESUMO DOS ACHADOS PRINCIPAIS** — um parágrafo por alvo, nome em caixa alta, cifra
  movimentada, incongruência central, e a frase seca que fecha ("Nunca declarou imposto de
  renda.").
- Blocos temáticos transversais: USO DE CRIPTOATIVOS · EMPRESAS DE FACHADA E CONFUSÃO
  PATRIMONIAL · CONTABILIDADE EM NUVEM · LOGÍSTICA AÉREA.
- **PRÓXIMOS PASSOS** em alíneas, cada uma com a medida e a razão dela.

## 8. Armadilhas medidas

- **Não retirar transações da base sem declarar.** Se retirar, dizer o que saiu e por quê.
- **Ausência de declaração não é patrimônio zero** — "Não disponível" precisa aparecer como
  tal na tabela, e ser lido como achado no texto.
- **Prosa arredonda, tabela não.** "Superior a R$ 117 milhões" no resumo; centavo exato na
  tabela.
- **Percentual sem base é vazio** — sempre "N% do total analisado", nomeando o total.
- **Nomear a fonte pública** (órgão de registro, consulta pública, portal, rastreador de voo)
  com URL e data de acesso; **não nomear sistema policial** — ver a nota
  `peca-nao-nomeia-o-sistema-consultado` na vault.
- **Bem em nome de parente não é conclusão** — é elo. A conclusão vem do uso, da posse e do
  fluxo financeiro que sustentam o bem.
