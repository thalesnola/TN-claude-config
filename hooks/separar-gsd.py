"""Tira a config do GSD do settings.json (compartilhado) para o settings.local.json (por máquina).

O instalador/atualizador do GSD grava hooks com caminho absoluto (C:/...) no settings.json,
que é versionado e compartilhado com o Mac. Rodar depois de instalar ou atualizar o GSD:

    python ~/.claude/hooks/separar-gsd.py

Idempotente: sem nada do GSD no settings.json, não muda nada. Critério por conteúdo
(comando com "gsd-", permissões do GSD), não por diff contra o git.
"""
import json
import pathlib
import shutil
import sys

BASE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / ".claude"
PERMS_GSD = ("gsd-core", ".planning/", "STATE.md")


def e_gsd(entrada):
    return any("gsd-" in h.get("command", "") for h in entrada.get("hooks", []))


def main():
    shared_p, local_p = BASE / "settings.json", BASE / "settings.local.json"
    shared = json.loads(shared_p.read_text(encoding="utf-8"))
    local = json.loads(local_p.read_text(encoding="utf-8")) if local_p.exists() else {}
    movidos = 0

    allow = shared.get("permissions", {}).get("allow", [])
    gsd = [p for p in allow if any(m in p for m in PERMS_GSD)]
    if gsd:
        shared["permissions"]["allow"] = [p for p in allow if p not in gsd]
        dest = local.setdefault("permissions", {}).setdefault("allow", [])
        dest += [p for p in gsd if p not in dest]
        movidos += len(gsd)

    for ev, lst in list(shared.get("hooks", {}).items()):
        gsd = [e for e in lst if e_gsd(e)]
        if not gsd:
            continue
        resto = [e for e in lst if not e_gsd(e)]
        if resto:
            shared["hooks"][ev] = resto
        else:
            del shared["hooks"][ev]
        dest = local.setdefault("hooks", {}).setdefault(ev, [])
        dest += [e for e in gsd if e not in dest]
        movidos += len(gsd)

    if "gsd-" in shared.get("statusLine", {}).get("command", ""):
        local["statusLine"] = shared.pop("statusLine")
        movidos += 1

    if not movidos:
        print("[separar-gsd] Nada do GSD no settings.json.")
        return
    shutil.copy2(shared_p, shared_p.with_suffix(".json.pre-gsd"))
    for p, d in ((shared_p, shared), (local_p, local)):
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"[separar-gsd] {movidos} item(ns) movido(s) para settings.local.json "
          f"(cópia anterior: settings.json.pre-gsd).")


if __name__ == "__main__":
    main()
