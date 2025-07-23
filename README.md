Automação de Cadastro de Componentes - TOTVS Moda
Esta é uma ferramenta de automação desenvolvida em Python para simplificar e agilizar o processo de cadastro de componentes e seus respectivos níveis de acesso a um grupo de usuários na tela ADMFM139 do ERP TOTVS Moda.

O script utiliza uma interface gráfica simples para coletar as informações necessárias e, em seguida, assume o controle do mouse e teclado para realizar o cadastro de forma automática, lendo os dados de um arquivo CSV.

✨ Funcionalidades
Interface Gráfica Simples: Interface amigável criada com PySide6 para facilitar a entrada do código do grupo e a seleção do arquivo de dados.

Leitura de Dados via CSV: Importa a lista de componentes e níveis de acesso diretamente de um arquivo .csv, tornando o processo escalável para centenas de registros.

Automação Robusta: Utiliza reconhecimento de imagem (com PyAutoGUI e OpenCV) para localizar campos e botões na tela do ERP. Isso torna a automação mais resistente a variações de resolução e posicionamento da janela em comparação com métodos baseados em coordenadas fixas.

Empacotamento em Executável: Acompanha um comando para gerar um único arquivo .exe com o PyInstaller, permitindo a fácil distribuição e uso em máquinas que não possuem Python instalado.

⚙️ Pré-requisitos
Para executar o projeto a partir do código-fonte, você precisará ter o Python instalado, além das seguintes bibliotecas:

```Bash

pip install PySide6 pyautogui pandas opencv-python
```
🚀 Como Usar
1. Preparação
Antes de executar a automação, dois preparativos são necessários:

A. Arquivo CSV:
Crie um arquivo .csv (ex: Grupo 335.csv) com duas colunas, separadas por ponto e vírgula (;):

Coluna 1: O código do componente do ERP.

Coluna 2: O texto exato do nível de acesso (ex: 2=Con / 3=Inc / 4=Alt / 5=Exc).

Exemplo de conteúdo do CSV:

```
Snippet de código

ADFL001;2
ADFL002;2
ADFM029;5
CMCF007;2
```
B. Imagens de Referência:
Para que o script saiba onde clicar, ele precisa de "fotos" de partes da tela do ERP. Capture 3 pequenas imagens .png e salve-as na mesma pasta do script:

campo_codigo_grupo.png: Uma imagem apenas do campo de texto onde se digita o código do grupo.

campo_componente.png: Uma imagem da primeira célula vazia da coluna "Comp.".

botao_atualizar.png: Uma imagem do botão "Atualizar".

2. Execução
Pelo Executável: Dê um duplo clique no arquivo Cadastrar Componente.exe.

Pelo Código-Fonte: Abra um terminal na pasta do projeto e execute python automacao_erp.py.

3. Usando a Aplicação
Na janela da aplicação, digite o Código do Grupo que deseja editar no ERP.

Clique em "Procurar Arquivo CSV..." e selecione o arquivo que você preparou.

Clique no botão verde "Iniciar Automação".

Uma mensagem de aviso aparecerá com uma contagem regressiva de 5 segundos. Neste tempo, clique na janela do ERP para deixá-la ativa.

Acompanhe a automação preenchendo os dados. Não mexa no mouse ou teclado durante o processo.

📦 Como Gerar o Executável (.exe)
Se você fez alterações no código-fonte e deseja gerar um novo arquivo executável, siga os passos:

Instale o PyInstaller:

```Bash

pip install pyinstaller
```
Navegue pelo terminal até a pasta do projeto.

Execute o seguinte comando:

```Bash

pyinstaller --name "Cadastrar Componente" --onefile --windowed --add-data "campo_codigo_grupo.png;." --add-data "campo_componente.png;." --add-data "botao_atualizar.png;." --icon="admin.ico" automacao_erp.py
```
(Lembre-se de ter um arquivo de ícone admin.ico na pasta para que a flag --icon funcione).

⚠️ Aviso Importante
Supervisão é Essencial: Este script controla seu computador. Sempre acompanhe a execução para garantir que tudo ocorra como o esperado.

Use em Ambiente de Teste: Antes de usar em produção, teste a automação em um ambiente de homologação ou com dados de teste para validar o comportamento do script.

Parada de Emergência: Se algo der errado, mova o cursor do mouse rapidamente para o canto superior esquerdo da tela para acionar a parada de emergência do PyAutoGUI.