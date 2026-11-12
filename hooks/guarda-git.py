#!/usr/bin/env python3
"""Guarda de git do ~/.claude. Modos: pre-commit | pre-push.

Este repo NAO tem versao para conferir -- o risco aqui e outro, e sao tres:

1. SEGREDO SUBINDO. O .gitignore e uma allowlist, e ela e a UNICA protecao.
   `git add -f` a contorna sem aviso, e credencial publicada nao se despublica:
   revoga-se. Esta e a barreira que faltava.

2. MANIFESTO DE PLUGIN COMMITADO DO SO ERRADO. installed_plugins.json e
   known_marketplaces.json guardam CAMINHO ABSOLUTO e estao sob skip-worktree
   justamente porque commita-los de uma maquina quebra a outra.

3. BASE DESATUALIZADA. Foi a causa da regressao de versao no token-router em
   31/08/2026: uma sessao partiu de um estado antigo e sobrescreveu o que outra
   ja havia subido. Duas sessoes escrevendo no mesmo arquivo nao se veem.

Sai 0 (segue) ou 1 (bloqueia).
"""
import re
import subprocess
import sys

MANIFESTOS = ("plugins/installed_plugins.json", "plugins/known_marketplaces.json")

# Nomes de arquivo que nunca devem entrar, mesmo com `git add -f`.
CAMINHO_PROIBIDO = re.compile(
    r"(^|/)\.credentials\.json$|(^|/)\.env$|(^|/)credentials|\.pem$|\.key$|id_rsa",
    re.IGNORECASE)

# Conteudo com forma de segredo. Cada padrao tem nome, para o aviso ser util.
SEGREDOS = [
    ("chave Anthropic",  re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("chave OpenAI",     re.compile(r"\bsk-[A-Za-z0-9]{32,}")),
    ("token GitHub",     re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("token Slack",      re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("chave generica",   re.compile(r"[\"'](?:api[_-]?key|secret|password|token)[\"']\s*:\s*[\"'][^\"']{16,}[\"']", re.IGNORECASE)),
]


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, check=False)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def staged():
    _, s = git("diff", "--cached", "--name-only", "--diff-filter=ACM")
    return [l for l in s.splitlines() if l.strip()]


def bloqueia(titulo, linhas):
    print("\n[guarda] BLOQUEADO: " + titulo, file=sys.stderr)
    for l in linhas:
        print("         " + l, file=sys.stderr)
    print(file=sys.stderr)
    return 1


def checar_conteudo(caminhos):
    achados = []
    for c in caminhos:
        cod, conteudo = git("show", ":" + c)
        if cod != 0:
            continue
        for nome, rx in SEGREDOS:
            m = rx.search(conteudo)
            if m:
                trecho = m.group(0)
                mascara = trecho[:8] + "..." + trecho[-4:]
                achados.append(f"{c}: parece {nome} ({mascara})")
    return achados


def base_desatualizada():
    cod, _ = git("rev-parse", "--verify", "@{u}")
    if cod != 0:
        return None
    _, atras = git("rev-list", "--count", "HEAD..@{u}")
    n = atras.strip()
    return int(n) if n.isdigit() and int(n) > 0 else None


def modo_pre_commit():
    arquivos = staged()
    if not arquivos:
        return 0

    proibidos = [a for a in arquivos if CAMINHO_PROIBIDO.search(a)]
    if proibidos:
        return bloqueia(
            "arquivo de credencial no commit (a allowlist foi contornada).",
            proibidos + ["", "Se subiu antes, REVOGUE a credencial -- apagar do repo nao basta."])

    manifestos = [a for a in arquivos if a in MANIFESTOS]
    if manifestos:
        return bloqueia(
            "manifesto de plugin no commit.",
            manifestos + [
                "",
                "Eles guardam CAMINHO ABSOLUTO e estao sob skip-worktree: commitar",
                "de uma maquina quebra a outra. Para mudar de proposito:",
                "  git update-index --no-skip-worktree <arquivo>"])

    achados = checar_conteudo(arquivos)
    if achados:
        return bloqueia("conteudo com forma de segredo.", achados)

    atras = base_desatualizada()
    if atras:
        print(f"\n[guarda] AVISO: sua base esta {atras} commit(s) atras de @{{u}}.",
              file=sys.stderr)
        print("         Outra sessao pode ja ter subido algo. `git pull --rebase`",
              file=sys.stderr)
        print("         antes de empurrar, ou voce sobrescreve trabalho alheio.\n",
              file=sys.stderr)
    return 0


def modo_pre_push():
    zeros = "0" * 40
    for linha in sys.stdin.read().splitlines():
        campos = linha.split()
        if len(campos) < 4:
            continue
        _, sha_local, _, sha_remoto = campos[:4]
        if sha_local.strip("0") == "":
            continue
        faixa = f"{sha_remoto}..{sha_local}" if sha_remoto != zeros else sha_local
        cod, nomes = git("diff", "--name-only", "--diff-filter=ACM", faixa) \
            if sha_remoto != zeros else git("show", "--name-only", "--format=", sha_local)
        if cod != 0:
            continue
        arquivos = [l for l in nomes.splitlines() if l.strip()]
        proibidos = [a for a in arquivos if CAMINHO_PROIBIDO.search(a)]
        if proibidos:
            return bloqueia("credencial no range que vai subir.", proibidos)
        manifestos = [a for a in arquivos if a in MANIFESTOS]
        if manifestos:
            return bloqueia("manifesto de plugin no range que vai subir.", manifestos)
    return 0


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "pre-commit"
    sys.exit(modo_pre_push() if modo == "pre-push" else modo_pre_commit())
