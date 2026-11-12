# Hierarquia e roteamento de tokens (estado em 28/10/2026)

Fonte da verdade: `routing/token-router/rules/roteamento.md`. Este arquivo é o resumo.

| Camada | Quem | Faz |
|---|---|---|
| 1. Decide | Opus (`opus[1m]`, alias) | planeja, arquiteta, decide trade-off e sintetiza |
| 2. Comanda e executa | Sonnet 5.5 (`token-router:*`) | executa direto, sem limite de tamanho de arquivo; confere e devolve a síntese |
| 3. Trabalha sob demanda | locais: DSH (`gpt-oss:20b`), Qwen Code (Coder-Next), OpenCode (Nemotron Lightning) | só quando o Opus pede a distribuição; sigilo sempre local |

Regras que valem:
- Só Claude e modelos locais. Codex, Copilot, Gemini e os modelos não Claude do Antigravity estão fora do roteamento (decisão de 24/10 e 28/10).
- Dado de caso (`ACERVO`, `Casos`) vai só a local.
- Contingência: `StopFailure` (fim de crédito) → `claude-local` (Ollama). Sem Claude do Antigravity (decisão de 28/10).
- Modelo local: sempre o mais completo instalado; falta de VRAM não autoriza rebaixar.
- Um peso grande por vez no Ollama (`OLLAMA_NUM_PARALLEL=1`).
