import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

CAMINHO_DOCUMENTOS = "documents/"
VETOR_DIR = "vectorstore/"


def criar_base_vetorial():
    print("Indexando documentos...")

    documentos = []

    for arquivo in os.listdir(CAMINHO_DOCUMENTOS):
        if arquivo.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(CAMINHO_DOCUMENTOS, arquivo))
            documentos.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    textos = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    base = FAISS.from_documents(textos, embeddings)
    base.save_local(VETOR_DIR)

    print("Base vetorial criada com sucesso!")


def buscar_contexto(pergunta):
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    base = FAISS.load_local(
        VETOR_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs_relevantes = base.similarity_search(pergunta, k=3)
    return "\n".join([doc.page_content for doc in docs_relevantes])
