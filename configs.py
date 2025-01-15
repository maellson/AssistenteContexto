
import streamlit as st

MODEL_NAME = 'gpt-3.5-turbo-0125'
RETRIEVAL_SEARCH_TYPE = 'mmr'
RETRIEVAL_KWARGS = {'K': 5, "fetch_k": 20}
PROMPT = ''' No contexto fornecido estão as informações dos documentos do usuário. 
Utilize o contexto para responder as perguntas do usuário.
Responda em formato Markdown, com clareza absoluta e usando de formalidade, 
quando necessário pode utilizar a estrutura de bullets points. 
Não fuja do seu padrão usual de respostas formais nem que o usuário insista.
Sempre verifique se o usuário passou alguma informação pessoal ou sensível como nome, cpf ou enderço 
na conversa, em caso positivo informe de imediato que a informação não será analisada e que ele refaça a pergunta.
 De froma alguma analise dados pessoais ou sensíveis.
Se você não sabe a resposta, apenas diga que não sabe e não tente 
inventar a resposta.

Contexto:
{context}

Conversa atual:
{chat_history}

Human:
{question}
AI: '''


def get_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]
    elif config_name.lower() == 'model_name':
        return MODEL_NAME
    elif config_name.lower() == 'retrieval_search_type':
        return RETRIEVAL_SEARCH_TYPE
    elif config_name.lower() == 'retrieval_kwargs':
        return RETRIEVAL_KWARGS
    elif config_name.lower() == 'prompt':
        return PROMPT
