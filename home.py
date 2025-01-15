from pathlib import Path
import streamlit as st
import time


from utils import criar_chain_conversa, FILES_PATH


def sidebar():
    # Carregador de arquivos para adicionar PDFs
    uploaded_pdfs = st.file_uploader(
        'Adicione seus arquivos pdf',
        type=['.pdf'],
        accept_multiple_files=True
    )
    if not uploaded_pdfs is None:
        # Remove arquivos PDF existentes no diretório
        for arquivo in FILES_PATH.glob('*.pdf'):
            arquivo.unlink()
        # Salva os novos arquivos PDF no diretório
        for pdf in uploaded_pdfs:
            with open(FILES_PATH / pdf.name, 'wb') as f:
                f.write(pdf.read())
    # Controles para temperatura e tokens
    # st.markdown("### Configurações do Modelo")
    # Define o rótulo do botão com base no estado da sessão
    label_botao = 'Inicializar ChatBot'
    # Se a cadeia de conversação já foi criada, altera o rótulo do botão
    if 'chain' in st.session_state:
        label_botao = 'Atualizar ChatBot'
    # Botão para inicializar o chatbot
    if st.button(label_botao, use_container_width=True):
        if len(list(FILES_PATH.glob('*.pdf'))) == 0:  # Verifica se há arquivos PDF
            # Exibe um erro se não houver arquivos PDF
            st.error('Adicione arquivos .pdf para inicializar o chatbot')
        else:
            # Exibe uma mensagem de sucesso
            st.success('Inicializando o ChatBot...')
            # Cria a cadeia de conversação com os parâmetros especificados
            criar_chain_conversa()
            st.rerun()  # Reinicia a sessão


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
    # Carrega a cadeia de conversação da sessão
    chain = st.session_state['chain']
    memory = chain.memory  # Carrega a memória da cadeia de conversação
    mensgens = memory.load_memory_variables(
        {})['chat_history']  # Carrega o histórico de conversas
    # Exibe as mensagens do histórico de conversas em um contêiner na ordem em que foram enviadas
    container = st.container()
    for mensagem in mensgens:
        # Cria uma mensagem de chat
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)  # Adiciona a mensagem ao contêiner
        print(mensagem.content)  # Exibe a mensagem no console

    # Verifica se a última mensagem foi enviada pelo usuário
    new_menssage = st.chat_input("CONVERSE COM SEUS DADOS")
    if new_menssage:  # Verifica se a mensagem não está vazia
        # Cria uma mensagem de chat para o usuário
        chat = container.chat_message('human')
        chat. markdown(new_menssage)  # Adiciona a mensagem ao contêiner
        chat = container. chat_message('ai')  # Cria uma mensagem da IA
        # Exibe um aviso de que a resposta está sendo gerada
        chat. markdown('Gerando resposta')

        # Invoca a cadeia de conversação com a nova mensagem
        resposta = chain.invoke({'question': new_menssage})
        st.session_state['ultima_resposta'] = resposta
        st.rerun()  # Reinicia a sessão


# Função principal para executar o código
def main():
    with st.sidebar:
        sidebar()  # Chama a função da barra lateral
    chat_window()  # Chama a função da janela principal


# Verifica se o arquivo está sendo execut
if __name__ == "__main__":
    main()
