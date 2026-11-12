# CLAUDE.md — Ambiente de análise forense

Este arquivo é compartilhado por **três máquinas** (as duas da tabela + a Precision, logo abaixo) via `claude-config`. O que muda entre
elas está marcado; o resto vale nos dois lugares.

| | Máquina A (origem) | Máquina B (atual) |
|---|---|---|
| Host | **Dell Pro Max 16 MC16250** (PFMG-2026043657) | MacBook Pro M5 Pro |
| OS | Windows 11 Pro (10.0.26200) | macOS 26.5.1 (arm64) |
| Hardware | Core Ultra 9 285H (**16 núcleos, sem HT**), 64 GB DDR5-**6400** (102,4 GB/s), RTX PRO 1000 8 GB + **Arc 140T** + NPU | 18 cores (6P+12E), **48 GB unificados** |
| Shell | PowerShell 7.6.3 + WPS 5.1 (**o terminal abre no 5.1**) | zsh |
| Pacotes | Chocolatey 2.7.3 | **Homebrew** 6.0.17 |
| Acervo ACERVO | `C:\ACERVO` | `~/ACERVO` |
| Plugin token-router | **instalado** (desde 31/08/2026) | **instalado** |

> ⚠️ **No Windows, o terminal abre no Windows PowerShell 5.1, não no 7.** Os dois estão
> instalados, e a diferença morde na primeira linha composta: **`&&` não existe no 5.1** — é
> **erro de parser**, e o parser rejeita a linha **inteira antes de executar qualquer coisa**
> (nada roda pela metade, o que ao menos torna a falha segura). Medido em 25/08/2026 numa
> cadeia `cd ... && git add ... && git commit ... && git push`. Ao passar comando composto ao
> usuário, ou abrir o 7 com `pwsh`, ou escrever para o 5.1: `;` no lugar de `&&` e `git -C <dir>`
> no lugar do `cd`. ⚠️ **`;` não é tradução fiel de `&&`** — ele executa o passo seguinte
> **mesmo com o anterior falhando**; inofensivo numa cadeia curta de git, inaceitável em
> sequência destrutiva. A alternativa do Bash (Git Bash) aceita `&&`, mas aí o `~` e as barras
> mudam de significado — escolher **um** dos dois e escrever a linha toda naquele dialeto.

> **Máquina C — Dell Precision 5860 Tower** (ESTACAO-C, adicionada em 02/10/2026): Windows 11 Pro for
> Workstations, Xeon w5-2555X (14C/28T), **128 GB**, **RTX 2000 Ada 16 GB** (~10 GB úteis com desktop, IPED/Whisper e Cellebrite
> disputando a GPU). Mesmo Chocolatey/PowerShell 5.1 da A (**sem &&**). Acervo em `C:\ACERVO`, modelos Ollama em `D:\OllamaModels`
> por junção. Pista rápida local ativa: DSH + `gpt-oss:20b` (44 tok/s, 100% GPU). Sem GSD. Perfil completo: `maquinas/dell-5860-windows.md` do token-router.
> **SSH entre A e C (13/10/2026):** `ssh promax` (Precision → Pro Max) e `ssh INSTITUICAO@nola-precision` (Pro Max → Precision), via Tailscale.
> Guia e armadilhas (InstallPending até reiniciar, `administrators_authorized_keys`, agente só no `ssh.exe` do Windows): `docs/ssh-entre-estacoes.md` do repo `estacoes`.

> **Sessão sem privilégios de administrador nas duas.** No macOS o `brew install` de
> fórmula não pede senha; **cask** e o instalador do próprio Homebrew pedem, e o
> prompt não pode ser respondido de dentro da sessão — esses passos são do usuário.

## Onde as regras de roteamento vivem (leia antes de editar)

A seção "Economia de tokens" **saiu deste arquivo em 12/08/2026**. O motivo: neste Mac o
plugin `token-router` está instalado e injeta as regras a cada `SessionStart`; manter o
mesmo texto aqui duplicaria a injeção em toda sessão — exatamente o que a nota
`plugin-token-router` mandava evitar ao instalar o plugin.

⚠️ **Historicamente a máquina Windows ficava sem as regras**, porque o plugin não estava
instalado lá. **Isso venceu em 31/08/2026: está instalado nas duas.** Se aparecer máquina
nova sem as regras, o mecanismo portátil é:

```
/plugin marketplace add <USER_NAME>/claude-token-router
/plugin install token-router@<USER>-plugins
```

Fonte da verdade das regras e dos subagentes: **o repo do plugin, e só ele.**

⚠️ **`~/.claude/agents/` foi removido em 31/08/2026 nas duas máquinas.** Ele guardava
cópias byte a byte iguais às do plugin, sobrevivendo a uma justificativa já vencida ("a
cópia que a máquina Windows usa enquanto não instalar o plugin" — o plugin está instalado
nas duas desde então). Duas cópias significam um lado que se edita e outro que se esquece.
**Não recriar o diretório.** Com ele fora, os subagentes se endereçam pelo nome qualificado
do plugin (`token-router:executor`, `token-router:Explore`, …).

## Gerenciador de pacotes

**macOS — Homebrew** em `/opt/homebrew` (arm64). PATH via `eval "$(/opt/homebrew/bin/brew shellenv)"`
no `~/.zshrc`.

```bash
brew list          # instalados
brew outdated      # atualizações
brew upgrade       # atualiza tudo
```

**Windows — Chocolatey** 2.7.3 em `C:\ProgramData\chocolatey`, com `allowGlobalConfirmation`
(dispensa `-y`), `useEnhancedExitCodes` e `useRememberedArgumentsForUpgrades`.

## Ferramentas forenses

| Ferramenta | macOS | Windows | Observação |
|---|---|---|---|
| Wireshark / tshark | `brew wireshark` | choco `wireshark` + Npcap | CLI `tshark`, `dumpcap`, `editcap` no PATH no Mac (no Windows exigem caminho completo) |
| 7-Zip | `brew sevenzip` → **`7zz`** | `7z` | **o comando muda de nome** |
| SQLite GUI | cask `db-browser-for-sqlite` | choco `sqlitebrowser` | |
| Draw.io | cask `drawio` | choco `drawio` | |
| nmap, ExifTool | `brew` | choco | |
| YARA | `brew yara` → **`yara`** | choco → **`yara64`** | **o comando muda de nome** |
| Tesseract OCR | `brew tesseract tesseract-lang` | choco + traineddata manual | ver abaixo |
| Graphviz | `brew graphviz` | choco `Graphviz` | binário `dot` |
| Volatility 3 | `uv tool install volatility3` | choco `volatility3` | 2.28.0 nos dois; sem fórmula no brew |
| **Sleuth Kit** | `brew sleuthkit` | — | `mmls`, `fls`, `icat` — substitui parte do Arsenal/Autopsy no Mac |
| poppler (`pdftoppm`) | `brew poppler` | WinGet | render de PDF para o OCR |

**Só no Windows, sem equivalente no macOS:** Arsenal Image Mounter (driver), Sysinternals,
HxD, FTK Imager, RegRipper, Autopsy (sem fórmula/cask — instalar à mão se precisar).

### Tesseract OCR
- **macOS:** `tesseract-lang` já traz **`por`** — não precisa baixar `por.traineddata` à
  mão como no Windows. Conferir: `tesseract --list-langs`.
- ⚠️ **Calibração medida** (vale nas duas): **300 dpi** + escala de cinza + **2× LANCZOS**
  + **contraste 3.0**, `--psm 4 -l por`. **600 dpi piora.** Texto cinza-claro de formulário
  **não é lido** — tabela de acurácia por campo em `memory/forense/metodologias.md` do ACERVO.

### Pilha Python (grafo, plotagem, OCR, planilha, PDF)
No Mac vive num **venv dedicado** em `~/ACERVO/.venv` (Python 3.12), não no Python do sistema
— o Python do Homebrew é *externally managed* (PEP 668) e recusa `pip install` global.

```bash
~/ACERVO/.venv/bin/python script.py
```

`matplotlib` 3.11.1 · `networkx` 3.6.1 · `graphviz` 0.21 · `pillow` · `pytesseract` ·
`openpyxl` · `pdfplumber` — mesmas versões da máquina Windows.

- ⚠️ O pacote pip `graphviz` **não traz o motor de layout** — depende do binário `dot`
  (fórmula `graphviz`). Instalar os dois.
- Em script sem interface gráfica, fixar `matplotlib.use("Agg")` **antes** de importar o
  pyplot — senão o processo tenta abrir janela e trava.
- Para grafo forense, `dot` (`rankdir=LR`) expressa melhor cadeia de evidência;
  `neato`/`fdp` servem a rede de vínculos sem hierarquia.

## Workflow padrão de análise (DFIR)

1. **Preservar** — copiar para pasta de trabalho gravável (`~/Casos/<caso>/` no Mac,
   `C:\Casos\<caso>\` no Windows); nunca trabalhar sobre o original. Registrar hash:
   `shasum -a 256 <arquivo>` (macOS) · `Get-FileHash -Algorithm SHA256` (Windows).
   A vault exige **SHA512** na peça final — ver `cadeia-de-custodia-obrigatoria`.
2. **Montar** — read-only sempre. Windows: Arsenal Image Mounter (`aim_cli --mount --readonly`).
   macOS: `mmls` para o mapa de partições e `fls`/`icat` do Sleuth Kit para listar e extrair
   sem montar; `hdiutil attach -readonly` para imagens que o macOS reconhece.
3. **Triagem/extração** — `7zz` (macOS) / `7z` (Windows) para contêineres.
4. **Bancos** — SQLite de navegador/mensageria no DB Browser; variante SQLCipher para cifrados.
5. **Baixo nível** — carimbos, magic bytes, carving. No Windows, HxD; no Mac não há
   equivalente instalado (cask `imhex` disponível se precisar).
6. **Rede** — Wireshark; em lote, `tshark -r captura.pcap -Y "http" -T fields -e ip.src -e http.host`.
7. **Correlação/relatório** — grafo de vínculos no Draw.io ou via `graphviz`/`networkx`;
   consolidar hashes e achados.

> Trabalhar sempre sobre cópias, montagens **read-only**, hash antes e depois de cada etapa.

## Acervo ACERVO e Segundo Cérebro

Repo privado `acervo-conhecimento`, clonado em `~/ACERVO` (macOS) / `C:\ACERVO` (Windows).

**Scripts do Segundo Cérebro — portados para Python em 12/08/2026.** Os `.ps1` continuam no
repo (a máquina Windows os usa); os `.py` novos rodam **nas duas plataformas** e são a
direção preferida daqui em diante. Motivo do porte: a regra de IPv4 do auditor usa
*negative lookahead*, e o `grep` do macOS é BSD, sem PCRE — bash abriria buraco no controle.

| Script | Função |
|---|---|
| `auditar.py` | Motor de detecção: 12 regras (CPF, CNJ, IPL, CEP, telefone, endereço, placa, IMEI, e-mail, IPv4) + filtro de ruído |
| `pre-commit.py` | Bloqueia commit com identificador no conteúdo **staged** |
| `pre-push.py` | Bloqueia push auditando o **range inteiro** — pega commit feito com `--no-verify` |
| `consultar.py` | Hook `UserPromptSubmit` — injeta notas relacionadas |
| `registrar.py` | Hook `Stop` — exige o registro do aprendizado |
| `indexar.py` / `buscar.py` | Regenera `00_Indices/INDICE.md` · busca sob demanda |

⚠️ **`.git/hooks/` não é versionado — clone novo nasce SEM a rede de sigilo, e nada avisa.**
Instalar **uma vez por clone**, logo depois de clonar:

```bash
python3 ~/ACERVO/Segundo_Cerebro/.sistema/scripts/instalar-hook-git.py
```

> **Diferença do macOS/Linux:** o hook precisa do **bit de execução**. No Windows o git roda
> o hook via `sh` sem olhar permissão; aqui, hook sem `chmod +x` é **ignorado em silêncio** —
> o commit passa e ninguém avisa que não houve auditoria. O instalador confere e reporta o modo.

Conferir sem commitar: `python3 ~/ACERVO/Segundo_Cerebro/.sistema/scripts/auditar.py`
(sai `[AUDITORIA] Limpo:` quando não há nada).

## Backup em nuvem desta configuração

O `~/.claude` é um repositório git: **github.com/<USER_NAME>/claude-config** (privado).
O `.gitignore` é uma **allowlist** — versiona só `CLAUDE.md`, `settings.json`, `hooks/`,
`agents/`, a memória por projeto e os **manifestos de plugins**; todo o resto (inclusive
`.credentials.json`, `plugins/cache/` e `plugins/marketplaces/`) é ignorado.
**Nunca afrouxar essas regras.**

⚠️ **A allowlist não é a única barreira desde 31/08/2026 — e não bastava.** `git add -f`
a contorna sem aviso, e credencial publicada não se despublica: revoga-se. Há uma guarda de
git em `hooks/guarda-git.py`, que bloqueia por caminho (`.credentials.json`, `.env`, `.pem`,
`id_rsa`), por conteúdo com forma de chave (Anthropic, OpenAI, GitHub, Slack), e barra os
dois manifestos sob `skip-worktree`. Ela também avisa quando a base está atrás do remoto.

⚠️ **`.git/hooks/` não é versionado: clone novo nasce SEM a guarda e nada avisa.** Instalar
**uma vez por clone**, logo depois de clonar:

```bash
python ~/.claude/hooks/instalar-guarda-git.py
```

O instalador **recusa sobrescrever** hook de outra origem — se um dia houver outro `pre-commit`
aqui, ele avisa em vez de apagar a rede existente.

- **Sincronizar após mudanças relevantes:** `cd ~/.claude && git add -A && git commit -m "..." && git push`.
- ⚠️ **Os manifestos de plugin NÃO são portáveis entre SOs.** `installed_plugins.json` e
  `known_marketplaces.json` guardam **caminho absoluto**; restaurar o backup do Windows no Mac
  fez o CLI procurar `/Users/<USER_NAME>/.claude/<USER_HOME>\.claude\plugins\...` e falhar.
  Em máquina de SO diferente: `claude plugin marketplace remove <nome>` e adicionar de novo.
  Como commitá-los do Mac quebraria o Windows do mesmo jeito, os dois arquivos estão
  marcados com **`git update-index --skip-worktree`** aqui: seguem versionados (o repo guarda
  a cópia do Windows, que é o registro do que instalar), mas a divergência local não aparece
  como modificação nem sobe. Para editá-los de propósito, tirar a marca com `--no-skip-worktree`.
- ⚠️ **GSD é por máquina (22/09/2026).** O instalador e o atualizador (`npx @opengsd/gsd-core@latest`)
  gravam hooks com caminho `C:/...` no `settings.json` compartilhado, o que quebraria o Mac.
  **Depois de cada instalação ou atualização:** `python ~/.claude/hooks/separar-gsd.py`, que move
  a config do GSD para o `settings.local.json` (não versionado). `agents/` e `hooks/gsd-*` ficam
  fora da allowlist.
- ⚠️ **Um GSD para cada runtime (24/10/2026).** O do Claude se instala só com `npx @opengsd/gsd-core@latest --claude --global` (sem `--claude` o instalador mexe em todos os runtimes, `~/.codex` inclusive) e termina com `separar-gsd.py`. O GSD do Codex, em `~/.codex/agents`, é instalado e ajustado à parte; o `ajustar-gsd-codex.py` saiu daqui e mora em `~/.codex/`.
- **Restaurar em máquina nova:** ver `SETUP-MAQUINA-NOVA.md` no plugin token-router.
  ⚠️ O passo que manda `git clone` direto para `~/.claude` **só vale se o Claude Code nunca
  rodou** na máquina. Se já rodou, a pasta não está vazia e o clone falha — usar
  `git init && git remote add origin ... && git fetch && git reset --hard origin/main`
  (a allowlist preserva sessões, backups e credenciais locais).

## Contingência de créditos — Ollama local

Sem crédito, `claude-local` (função no shell) retoma a mesma conversa (`--continue`) no Ollama;
os três níveis usam `qwen3-coder:30b`. A entrada é automática pelo hook `StopFailure` do
`token-router`, **só em fim de crédito (100%)**: abre `claude-local` na mesma conversa. Sem
gatilho por porcentagem (descartado em 24/10/2026) e sem nuvem de terceiros.

- ⚠️ `OLLAMA_CONTEXT_LENGTH` é obrigatório (padrão 4096 trunca o prompt e o modelo devolve lixo):
  Windows 32768, Mac 131072. `CLAUDE_CODE_MAX_CONTEXT_TOKENS` tem de igualar o contexto **concedido**
  (`ollama ps`) — o CLI assume 200k e o modelo trunca antes, **sem erro**.
- ⚠️ O nível Haiku **não** usa o `qwen2.5-coder:7b` (perde o começo do prompt longo, sem erro).
- ⚠️ O hook `Stop` não dispara em sessão local; na volta, `SessionStart` manda revisar o trabalho.
- No Mac o servidor sobe por LaunchAgent, nunca `brew services`. Claude é sempre o principal.

Detalhes e medições: vault `50_Stack/referencia-contingencia-ollama-e-executores.md`.

## Executores fora do Opus

| | binário | modelo | onde vive |
|---|---|---|---|
| Qwen Code | `qwen` | `Qwen3-Coder-Next :NOTPL` (36 GB) | Ollama local |
| OpenCode | `opencode` | `nemotron-3.5-lightning:30b-a3b` (Windows; o perfil da máquina vale) | Ollama local |

- ⚠️ **Codex, Antigravity/Gemini e Copilot são independentes (decidido em 24/10/2026):** continuam instalados
  e logados, com configuração própria, mas **nenhum agente, hook ou script do Claude os aciona**. Não os
  chame por `Bash`, não os reintroduza no `token-router` nem neste arquivo.
- Qwen Code fala com o Ollama, **nunca** com a nuvem (`~/.qwen/.env`); não trocar sem decidir de novo.
- ⚠️ **Nunca dois pesos grandes ao mesmo tempo** (Qwen Code e OpenCode com modelo grande são
  exclusivos). **Nunca `num_gpu: 0`** (prefill cai 7×). `num_thread` é alavanca morta: não mexer.
- `ollama create` voltou a funcionar no 0.34.2 (testado 30/09/2026); antes (0.33.2) falhava em silêncio, e a variante `:NOTPL` era escrita
  por `token-router/contingencia/refazer-variante-sem-template.py` após qualquer `ollama pull`.
- `report_findings` fica excluída no `~/.qwen/settings.json` (quebra a gramática do Ollama).
- Tabela de latência, recusas de modelo por conta e retificações: vault
  `50_Stack/referencia-contingencia-ollama-e-executores.md`.

## O cérebro acompanha o Opus mais recente

`"model": "opus[1m]"` no `settings.json` (alias + janela de 1M) — **alias, nunca versão fixa**. A sessão do app pode abrir noutro modelo (ex.: Sonnet 5.5); conferir antes de presumir que o Opus é quem decide. Fixar
(`claude-opus-4-8`/`claude-opus-5`) quebraria o auto-follow. Quem resolve alias → versão é o
**catálogo do CLI**, não o settings: a migração acontece sozinha ao manter o app atualizado.

## Histórico

Movido em 30/09/2026 para a vault: `50_Stack/historico-do-claude-md-global.md` (setups das
máquinas, retificações de plugins, limpezas). Consultar lá o porquê de uma configuração.
