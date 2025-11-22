from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from chatbot import montar_mensagens_com_contexto, enviar_mensagem, registrar_interacao

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    mensagem: str
    session_id: str

@app.post("/processar")
def processar_prompt(req: PromptRequest):

    mensagens_envio = montar_mensagens_com_contexto(req.mensagem)
    resposta = enviar_mensagem(mensagens_envio)

    registrar_interacao(req.mensagem, resposta)

    return {
        "resposta": resposta.content
    }
