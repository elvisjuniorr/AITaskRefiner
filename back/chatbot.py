from openai import OpenAI
from dotenv import load_dotenv
import os
from rag import buscar_contexto
from memory import carregar_historico, salvar_historico

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def carregar_prompt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

SYSTEM_PROMPT = carregar_prompt("prompts/system_prompt.txt")
IDENTIFICATION_PROMPT = carregar_prompt("prompts/task_identification.txt")

# Histórico de conversa
mensagens = carregar_historico()

# Armazena o problema identificado na primeira interação
problema_global = None


# ================= CORE LLM =================

def enviar_mensagem(mensagens):
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensagens,
        temperature=0.5
    )
    return resposta.choices[0].message


# ================= ETAPA ÚNICA: IDENTIFICAÇÃO =================

def identificar_problema(pergunta):
    mensagens_detecao = [
        {
            "role": "system",
            "content": IDENTIFICATION_PROMPT
        },
        {
            "role": "user",
            "content": pergunta
        }
    ]

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensagens_detecao,
        temperature=0
    )

    return resposta.choices[0].message.content.strip()


# ================= MONTAGEM INTELIGENTE =================

def montar_mensagens_com_contexto(pergunta):
    global problema_global

    # 🔹 Executa APENAS na primeira interação
    if problema_global is None:
        print("🔍 Identificando problema inicial...")
        problema_global = identificar_problema(pergunta)

    contexto = buscar_contexto(problema_global)

    mensagens_envio = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": f"""
                        PROBLEMA IDENTIFICADO:
                        {problema_global}

                        CONTEXTO RELEVANTE DOS DOCUMENTOS:
                        {contexto}

                        Aja estritamente conforme as regras do sistema e reestruture o prompt do usuário.
                        """
        }
    ]

    mensagens_envio.extend(mensagens[-6:])
    mensagens_envio.append({"role": "user", "content": pergunta})

    return mensagens_envio


def registrar_interacao(usuario, resposta):
    mensagens.append({"role": "user", "content": usuario})
    mensagens.append({"role": resposta.role, "content": resposta.content})


# ================= LOOP PRINCIPAL =================

def iniciar_chat():
    print("🤖 Chatbot iniciado. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() == "sair":
            salvar_historico(mensagens)
            print("Chatbot finalizado.")
            break

        mensagens_envio = montar_mensagens_com_contexto(pergunta)
        resposta = enviar_mensagem(mensagens_envio)

        registrar_interacao(pergunta, resposta)

        print("\nBot:", resposta.content)
        print("-" * 70)


if __name__ == "__main__":
    iniciar_chat()
