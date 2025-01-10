from pathlib import Path
import streamlit as st
import time



from utils import criar_chain_conversa, FILES_PATH



def sidebar():
    st.sidebar.title("Home")
    # Adiciona um uploader de arquivos na barra lateral
    uploaded_pdf = st.file_uploader(
        "Adicione o arquivo PDF",
        type=['.pdf'],
        accept_multiple_files=True
        # label="Arraste e solte o arquivo PDF aqui"
    )
    if not uploaded_pdf is None:
        # Limpa a pasta de arquivos
        for file in FILES_PATH.glob("*.pdf"):
            file.unlink()  # limpa a pasta toda vez que um novo arquivo é adicionado
        for pdf in uploaded_pdf:
            # Salva o arquivo PDF no caminho especificado
            with open(FILES_PATH / pdf.name, "wb") as f:
                f.write(pdf.read())
    # Botão para iniciar o assistente
    button_label = 'Iniciar Assistente'
    # Define o rótulo do botão com base no estado da sessão
    if 'chain' in st.session_state:
        button_label = 'Atualizar Assistente'
        # Verifica se a pasta de arquivos está vazia e exibe um erro
    if st.button(button_label, use_container_width=True):
        if len(list(FILES_PATH.glob("*.pdf"))) == 0:
            st.error("Nenhum arquivo PDF foi adicionado")
        else:
            # Exibe uma mensagem de sucesso se tiver aquivo anexo e inicia o assistente
            st.success("Assistente iniciado com sucesso")
            criar_chain_conversa()
            st.rerun()


ROBOT_EMOJI_PATH = Path(__file__).parent / "images" / \
    "robot.png"  # Caminho correto usando Path


def chat_window():
    col1, col2 = st.columns([2, 8])
    with col1:
        # Exibe a imagem do emoji no título
        # Convertendo Path para string
        st.image(str(ROBOT_EMOJI_PATH), width=150)
    with col2:
        st.header('Bem-vindo ao assistente de processamento de PDF', divider=True)
    # st.write("Adicione um arquivo PDF para começar")
    if not 'chain' in st.session_state:  # Verifica se a sessão está ativa
        # Exibe um erro se não houver arquivo PDF
        st.error("Nenhum arquivo PDF foi adicionado")
        st.stop()

    chain = st.session_state['chain']
    memory = chain.memory
    mensgens = memory.load_memory_variables({})['chat_history']

    container = st.container()
    for mensagem in mensgens:
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    new_menssage = st.chat_input("CONVERSE COM SEUS DADOS")
    if new_menssage:
        chat = container.chat_message('human')
        chat. markdown(new_menssage)
        chat = container. chat_message('ai')
        chat. markdown('Gerando resposta')

        chain.invoke({'question': new_menssage})
        st.rerun()

# Função principal para executar o código


def main():
    with st.sidebar:
        sidebar()  # Chama a função da barra lateral
    chat_window()  # Chama a função da janela principal


# Verifica se o arquivo está sendo execut
if __name__ == "__main__":
    main()
