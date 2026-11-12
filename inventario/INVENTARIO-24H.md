# Inventário das últimas 24 horas — Dell Pro Max (PFMG-2026043657)

Janela: 27/10/2026 ~03:00 a 28/10/2026 ~03:00 (horário local). Cada item diz a fonte.

## Instalado

| Item | Versão | Como | Fonte |
|---|---|---|---|
| FFmpeg | 9.0.2 (substituiu 8.1.2) | `winget install Gyan.FFmpeg --version 9.0.2` | `winget list`; `ffmpeg -version` |
| OpenCut (editor) | fonte de `main` | `git clone` em `C:\Ferramentas\OpenCut`; `bun install` em `apps/web`; dev na 5173 testado (HTTP 200) e parado | `C:\Ferramentas` |
| Remotion | projeto em branco | `npx create-video --blank` em `C:\Ferramentas\remotion-studio`; Chrome Headless Shell baixado; render de teste OK | `C:\Ferramentas\remotion-studio` |
| Modelo Ollama `nemotron-3.5-bolt:e4b` | 7,9 GB | `ollama pull`; medido: carga 15 s, 55,6 tok/s, 100% GPU, contexto 32K | `ollama list` |
| Ollama | 0.40.10 | atualizado via winget | `winget list` |

## Configurado ou movido

| Item | O que mudou | Fonte |
|---|---|---|
| Token-router (repo) | `280b5b2`: escada de 28/10 (locais só sob demanda do Opus; Sonnet sem limite de arquivo). Sincronizado com `57c5bf9` (2.0.0 só-Claude) | `git log` do repo |
| Token-router (branch local) | `roteamento-escada-28-10`: commit divergente com Claude do AGY como contingência. Não publicado | `git branch` |
| `~/.claude/settings.json` (não commitado) | ~90 skills com `off` em `skillOverrides` (Blender, Remotion, Hyperframes, Three.js e outras); hook `PreToolUse` `Write\|Edit\|MultiEdit` que chama `segundo-cerebro.py guardar`; `cartographer` e `claude-code-setup` ativados; marketplace `cartographer`; `outputStyle: Concise`. Autoria desta mudança não foi identificada nesta sessão | `git diff settings.json` |
| `~/.claude/skills/apple-hig-designer` | atualizada (arquivos de 27/10) | `find -newermt` |
| `~/.claude/skills/redacao-forense/SKILL.md` | modificado, não commitado | `git status` |
| `~/.claude/plugins/*.json` | manifests atualizados (plugins e marketplaces) | `find -newermt` |
| `~/.claude/state/mcp-discover-verdicts.json` | atualizado pelo Claude Code | `find -newermt` |
| Vault `C:\ACERVO\Segundo_Cerebro` | diários de 28/10 (`system32`, `roteamento-tokens-agy`, outro) e nota do Bolt | `60_Sessoes` |

## Não identificado

- `C:\Ferramentas\Voz`: pasta criada na mesma janela, sem relação com esta sessão. Conferir antes de incluir.

## Já existentes (estado atual, sem mudança na janela)

- Plugins Claude Code (`claude plugin list`): 15 instalados; ativos: `token-router`, `claude-code-setup`, `cartographer`. Os demais estão desativados.
- MCPs Claude Code (usuário): `blender` (`uvx mcp-for-blender`, telemetria desligada).
- MCPs Claude Desktop: `context7`, `github`, `filesystem`, `sequential-thinking`, `playwright`. O `github` usa a variável `GITHUB_PERSONAL_ACCESS_TOKEN` (valor não copiado).
- MCPs OpenCode ativos: `rag`, `forense`, `gsd`, `colab-mcp`. Desativados: `notebook`, `visualization`, `bigquery`, `spanner`, `alloydb-postgres`, `cloud-sql-postgresql`, `knowledge_catalog`, `bigtable`, `cloud-storage`.
- Modelos locais: `gpt-oss:20b`, `nemotron-3.5-lightning:30b-a3b` (modelo do OpenCode), `hf.co/unsloth/Qwen3-Coder-Next` (duas tags), `qwen3:8b`, `qwen3-coder:30b`, `mxbai-embed-large`, `nomic-embed-text`.
- Ferramentas globais: Node 24.18.0, bun 1.4.4, opencode-ai 1.18.33, `@deepseek-ai/dsh` 0.2.0-rc.2, `@qwen-code/qwen-code` 0.24.7, `@higgsfield/cli` 1.2.2 e outras (ver `tooling/npm-global.txt`).
