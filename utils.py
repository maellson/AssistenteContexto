from pathlib import Path

import streamlit as st
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from configs import *
from dotenv import load_dotenv, find_dotenv
from configs import get_config

_ = load_dotenv(find_dotenv())


# Definindo o caminho para os arquivos usando a lib PathLib que serve para manipulação de arquivos e diretorios
FILES_PATH = Path(__file__).parent / "files"


def import_documents():
    documentos = []
    for arquivo in FILES_PATH.glob('*.pdf'):
        loader = PyPDFLoader(str(arquivo))
        documentos_arquivo = loader.load()
        documentos.extend(documentos_arquivo)
    return documentos


def split_documents(documentos):
    recur_spliter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=["/n\n", "\n", ".", " ", ""]
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

# Função para criar a cadeia de conversação


def criar_chain_conversa(temperatura=0.0, max_tokens=2048):
    # Verifica se já existe uma vectorstore na sessão
    if 'vector_store' not in st.session_state:
        documentos = import_documents()
        documentos = split_documents(documentos)
        vector_store = create_vector_store(documentos)
        st.session_state['vector_store'] = vector_store
    else:
        vector_store = st.session_state['vector_store']
# Cria uma instância do modelo de linguagem da OpenAI com os parâmetros especificados
    chat = ChatOpenAI(
        model=get_config('model_name'),
        temperature=temperatura,
        max_tokens=max_tokens
    )
    print(f"temperatura: {temperatura}", f"max_tokens: {max_tokens}")
    # Cria uma instância de memória para armazenar o histórico de conversas
    memory = ConversationBufferMemory(
        return_messages=True,  # Indica que as mensagens devem ser retornadas
        memory_key='chat_history',  # Chave usada para armazenar o histórico de chat
        output_key='answer',  # Chave usada para armazenar a resposta
    )

    # Configura o vetor de busca para recuperação de documentos
    retriever = vector_store.as_retriever(
        # Tipo de busca a ser realizada
        search_type=get_config('retrieval_search_type'),
        # Argumentos adicionais para a busca
        search_kwargs=get_config('retrieval_kwargs'),
    )
    # Cria um template de prompt a partir de uma string de template
    Prompt = PromptTemplate.from_template(get_config('prompt'))

    # Cria uma cadeia de conversação com recuperação de documentos
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,  # Modelo de linguagem
        memory=memory,  # Memória da conversa
        retriever=retriever,  # Recuperador de documentos
        return_source_documents=True,  # Indica se os documentos fonte devem ser retornados
        verbose=True,  # Indica se a saída deve ser detalhada
        # Argumentos adicionais para combinar documentos
        combine_docs_chain_kwargs={'prompt': Prompt},
    )

    # Salva a cadeia de conversação no estado da sessão do Streamlit
    st.session_state['chain'] = chat_chain
