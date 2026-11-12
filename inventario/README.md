# CLAUDE-CONFIG

Inventário e configuração do ambiente Claude Code (Dell Pro Max, Windows 11): skills, plugins, MCPs, LLMs locais, hierarquia e roteamento de tokens.

- `INVENTARIO-24H.md` — o que foi instalado, configurado ou movido nas últimas 24 horas, com a fonte de cada item.
- `HIERARQUIA.md` — quem decide, quem executa e onde o trabalho local entra.
- `config/` — `settings` sanitizado, MCPs (Claude Code, Desktop), manifests de plugins, lista de hooks e skills.
- `llm/` — modelos Ollama instalados e configuração do OpenCode (sanitizada).
- `tooling/` — pacotes globais (npm, uv, winget).
- `routing/token-router/` — cópia do repositório `<USER_NAME>/claude-token-router` (commit `280b5b2`).

## O que NÃO está aqui (de propósito)

- Credenciais e tokens: `.credentials.json`, `oauthAccount`, o valor de `GITHUB_PERSONAL_ACCESS_TOKEN` do Desktop, qualquer `.env`. Nos JSON, chaves com nome sensível aparecem como `<REDIGIDO>`.
- Estado de execução: sessões, caches, backups do `.claude.json`, transcrições, `ollama-pendente.json`.
- Evidência de caso e dado de caso: nada de `ACERVO` ou `Casos`.

## Como restaurar em outra máquina

1. Plugins: `claude plugin marketplace add <USER_NAME>/claude-token-router` e `claude plugin install token-router@<USER>-plugins`. Os manifests têm caminho absoluto: em outro SO, remova e adicione os marketplaces de novo.
2. MCPs: use `config/mcp/*.json` como referência. Os valores de ambiente precisam ser preenchidos localmente.
3. Modelos locais: `llm/ollama-modelos.txt` lista o que foi baixado. Os tamanhos estão ali.
4. Hierarquia: `HIERARQUIA.md` e `routing/token-router/rules/roteamento.md` são a fonte da verdade.

## Atualização

Este repositório é um retrato de 28/10/2026. Para atualizar, rode de novo a coleta descrita em `INVENTARIO-24H.md`.
