import streamlit as st
from configs import get_config
from utils import criar_chain_conversa, FILES_PATH


def config_page():
    st.header('Configurações do Administrador', divider=True)

    model_name = st.selectbox(
        'Nome do modelo: ', ['gpt-3.5-turbo-0125', 'gpt-4o'], index=0)
    retrieval_search_type = st.selectbox(
        'Tipo de busca de recuperação: ', ['mmr', 'bm25'], index=0)
    k_value = st.number_input(
        'K (Número de documentos a serem retornados): ', min_value=1, value=5)
    fetch_k_value = st.number_input(
        'fetch_k (Número de documentos a serem buscados): ', min_value=1, value=10)
    retrieval_kwargs = {"K": k_value, "fetch_k": fetch_k_value}
    temperature = st.slider(
        'Temperatura do modelo (criatividade): ', min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.number_input(
        "Quantidade máxima de tokens na resposta:",
        min_value=100,
        max_value=3000,
        value=2048,
        step=100
    )
    prompt = st.text_area(
        'Prompt: ', value=get_config('prompt'), height=350)

    if st.button('Modificar Parâmetros', use_container_width=True):
        st.session_state['model_name'] = model_name
        st.session_state['retrieval_search_type'] = retrieval_search_type
        st.session_state['retrieval_kwargs'] = retrieval_kwargs
        st.session_state['prompt'] = prompt
        st.session_state['temperature'] = temperature
        st.session_state['max_tokens'] = max_tokens
        st.success('Configurações salvas com sucesso!')
        st.rerun()

    if st.button('Atualizar ChatBot', use_container_width=True):
        if len(list(FILES_PATH.glob('*.pdf'))) == 0:
            st.error('Adicione arquivos .pdf para inicializar o chatbot')
        else:
            st.success('Inicializando o ChatBot...')
            criar_chain_conversa(temperature, max_tokens)
            st.query_params = {"page": "Home"}
            st.rerun()


config_page()
