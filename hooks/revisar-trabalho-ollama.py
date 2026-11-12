#!/usr/bin/env python3
"""Hook SessionStart: se houve trabalho feito pelos modelos locais (Ollama) durante
uma queda de creditos, injeta instrucao para o modelo Claude revisar esse trabalho.
O marcador e criado pela funcao claude-local (perfil do zsh).

Porte de revisar-trabalho-ollama.ps1. Em Python por rodar nas duas maquinas: o
mesmo arquivo serve o Windows e o macOS, o que encerra a manutencao em dobro.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

MARCADOR = Path.home() / ".claude" / "ollama-pendente.json"


def main() -> int:
    if not MARCADOR.is_file():
        return 0
    # Se a sessao atual JA esta apontada para o Ollama, nao ha o que revisar ainda --
    # a pendencia so faz sentido na volta aos modelos Claude.
    base = os.environ.get("ANTHROPIC_BASE_URL", "")
    if re.search(r"localhost|127\.0\.0\.1", base):
        return 0

    try:
        dados = json.loads(MARCADOR.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        dados = {}
    inicio = dados.get("inicio", "desconhecido")
    diretorio = dados.get("diretorio", "desconhecido")
    ctx = (
        "REVISAO PENDENTE (contingencia): durante uma indisponibilidade de creditos, "
        f"modelos locais (Ollama/Qwen) trabalharam nesta maquina a partir de {inicio} no diretorio "
        f"'{diretorio}'. Antes de prosseguir com qualquer tarefa nova, revise o trabalho feito por eles: "
        "use git diff/log se for repositorio, ou compare arquivos modificados desde esse horario."
        " "
        "DELEGUE a revisao ao subagente 'revisor' (sonnet): use 'Explore' para levantar o que mudou "
        "e 'resumidor' se o diff for extenso; nao leia o diff inteiro no contexto principal. "
        "Procure bugs, codigo incompleto e desvios do padrao do projeto; corrija o que for necessario "
        f"e resuma ao usuario o que foi revisado. Ao concluir a revisao, DELETE o arquivo '{MARCADOR}' "
        "para encerrar a pendencia."
    )

    print(json.dumps({
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ctx}
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
