# AssistenteContexto
Assistente de contexto que consegue analisar qualquer documento anexo e auxiliar os usuários em resumos ou outra forma de extraçao de informação
### Inicialize o Projeto com Poetry
Crie o Gerenciador do Poetry:

### Inicialize o projeto com o Poetry:
bash
Copiar código
poetry init
### Responda às perguntas do assistente (nome, versão, descrição, etc.).
Escolha um formato de licença (como MIT ou Apache 2.0).
Configure o Ambiente Virtual:

### Dentro do diretório do projeto:

poetry env use python3.11  # Ou a versão que você deseja usar

### Adicione as Dependências:
Caso tenha um requirements.txt, converta-o para o formato do Poetry:


poetry add $(cat requirements.txt | tr '\n' ' ')


## Para dependências de desenvolvimento (testes, linting, etc.):
poetry add --dev pytest black flake8 mypy

## para ativar o ambiente no poetry
poetry shell 