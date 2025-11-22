import json

ARQUIVO_MEMORIA = "historico.json"

def salvar_historico(mensagens):
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(mensagens, f, ensure_ascii=False, indent=2)


def carregar_historico():
    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
