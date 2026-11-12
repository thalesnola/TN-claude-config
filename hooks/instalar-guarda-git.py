#!/usr/bin/env python3
"""Instala a guarda de git do ~/.claude. Rodar UMA VEZ por clone.

⚠️ `.git/hooks/` NAO e versionado: clone novo nasce SEM guarda, e nada avisa.
Ate 31/08/2026 este repo nao tinha hook nenhum -- a allowlist do .gitignore era
a unica protecao das credenciais, e `git add -f` a contorna em silencio.
"""
import os
import stat
import subprocess
import sys

MOLDE = """#!/bin/sh
# Gerado por hooks/instalar-guarda-git.py -- nao editar aqui.
exec python "$(git rev-parse --show-toplevel)/hooks/guarda-git.py" {modo} "$@"
"""


def main():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, check=False)
    if r.returncode != 0:
        sys.exit("Rode de dentro de ~/.claude.")
    raiz = r.stdout.decode().strip()

    if not os.path.exists(os.path.join(raiz, "hooks", "guarda-git.py")):
        sys.exit("Nao achei hooks/guarda-git.py em " + raiz)

    alvo = os.path.join(raiz, ".git", "hooks")
    os.makedirs(alvo, exist_ok=True)
    for modo in ("pre-commit", "pre-push"):
        cam = os.path.join(alvo, modo)
        if os.path.exists(cam):
            with open(cam, encoding="utf-8", errors="replace") as f:
                atual = f.read()
            if "guarda-git.py" not in atual:
                print("AVISO: ja existe um " + modo + " de outra origem. Nao sobrescrevi.")
                print("       Encadeie a mao antes de confiar nesta guarda:")
                print("       " + cam)
                continue
        with open(cam, "w", newline="\n", encoding="utf-8") as f:
            f.write(MOLDE.format(modo=modo))
        os.chmod(cam, os.stat(cam).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        if sys.platform.startswith("win"):
            nota = "bit de execucao irrelevante no Windows (git roda o hook via sh)"
        elif os.stat(cam).st_mode & stat.S_IXUSR:
            nota = "executavel: sim"
        else:
            nota = "executavel: NAO -- CORRIGIR; sem o bit o hook e ignorado EM SILENCIO"
        print("instalado: " + cam)
        print("           " + nota)


if __name__ == "__main__":
    main()
