from pathlib import Path
import streamlit as st
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# Definindo o caminho para os arquivos usando a lib PathLib que serve para manipulação de arquivos e diretorios
FILES_PATH = Path(__file__).parent / "files"
MODEL_NAME = 'gpt-3.5-turbo-0125'


def import_documents():
    documentos = []
    for arquivo in FILES_PATH.glob("*.pdf"):
        loader = PyPDFLoader(str(arquivo))  # traz o caminho do arquivo
        documents_loader = loader.load()
        documentos.extend(documents_loader)
    return documentos


def split_documents(documentos):
    recur_spliter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=["\n\n", "\n", ".", "!", "?", ";", ":", "\t"]
    )
    documentos = recur_spliter.split_documents(documentos)

    for i, doc in enumerate(documentos):  # interador que faz
        doc.metadata['source'] = doc.metadata['source'].split("/")[-1]
        doc.metadata['doc_id'] = i
    return documentos


def create_vector_store(documentos):
    embedding_model = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(
        documents=documentos,
        embedding=embedding_model
    )
    return vector_store


def criar_chain_conversa():
    documents = import_documents()
    documents = split_documents(documents)
    vector_store = create_vector_store(documents)

    chat = ChatOpenAI(model=MODEL_NAME)
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key='chat_history',
        output_key='answer',
    )
    retriever = vector_store.as_retriever()
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        verbose=True
    )
    st.session_state['chain'] = chat_chain
