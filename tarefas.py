"""Gerenciador de tarefas simples via terminal."""
import argparse
import json
from pathlib import Path

ARQUIVO = Path("tarefas.json")


def carregar():
    if not ARQUIVO.exists():
        return []
    with open(ARQUIVO, encoding="utf-8") as f:
        return json.load(f)


def salvar(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def adicionar(titulo, prioridade="media"):
    tarefas = carregar()
    tarefas.append({"id": len(tarefas) + 1, "titulo": titulo,
                    "prioridade": prioridade, "concluida": False})
    salvar(tarefas)
    print(f"Tarefa '{titulo}' adicionada.")


def listar_tarefas():
    ordem = {"alta": 0, "media": 1, "baixa": 2}
    for t in sorted(carregar(), key=lambda x: ordem.get(x.get("prioridade", "media"), 1)):
        marca = "x" if t["concluida"] else " "
        print(f"[{marca}] {t['id']} - {t['titulo']} ({t.get('prioridade', 'media')})")


def concluir(id_tarefa):
    tarefas = carregar()
    for t in tarefas:
        if t["id"] == id_tarefa:
            t["concluida"] = True
            salvar(tarefas)
            print(f"Tarefa {id_tarefa} concluída.")
            return
    print(f"Tarefa {id_tarefa} não encontrada.")


def main():
    parser = argparse.ArgumentParser(description="Gerenciador de tarefas")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="adiciona uma tarefa")
    p_add.add_argument("titulo")
    p_add.add_argument("--prioridade", choices=["alta", "media", "baixa"], default="media")

    sub.add_parser("list", help="lista as tarefas")

    p_done = sub.add_parser("done", help="conclui uma tarefa")
    p_done.add_argument("id", type=int)

    args = parser.parse_args()
    if args.cmd == "add":
        adicionar(args.titulo, args.prioridade)
    elif args.cmd == "list":
        listar_tarefas()
    elif args.cmd == "done":
        concluir(args.id)


if __name__ == "__main__":
    main()
