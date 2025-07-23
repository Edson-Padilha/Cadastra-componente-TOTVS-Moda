import sys
import pyautogui as pag
import pandas as pd
import time
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox
)

# Nomes dos arquivos de imagem salvas
IMG_CODIGO_GRUPO = 'campo_codigo_grupo.png'
IMG_COMPONENTE = 'campo_componente.png'
IMG_ATUALIZAR = 'botao_atualizar.png'

def run_automation(group_code, csv_path):
    """
    Função principal que executa a automação da GUI.
    """
    try:
        # 1. Ler os dados do arquivo CSV usando pandas
        try:
            # Tenta ler com delimitador ; e depois com ,
            df = pd.read_csv(csv_path, sep=';', header=None)
            if df.shape[1] == 1:
                df = pd.read_csv(csv_path, sep=',', header=None)
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Não foi possível ler o arquivo CSV.\nVerifique se o delimitador é ';' ou ','\n\nErro: {e}")
            return
        
        if df.shape[1] != 2:
            QMessageBox.critical(None, "Erro", "O arquivo CSV deve ter exatamente duas colunas: Componente e Nível de Acesso.")
            return
        
        # 2. Conatgem regressiva para o usuário focar na janela do ERP
        QMessageBox.information(None, "Prepare-se!", "A automação começará em 5 segundos.\n\nPor favor, clique na janela do ERP e não mexa o mouse ou teclado.")
        time.sleep(5)

        # 3. Localizar e preencher o código do grupo
        print("Procurando o campo 'Código do grupo'...")
        campo_codigo_location = pag.locateCenterOnScreen(IMG_CODIGO_GRUPO, confidence=0.9)
        if not campo_codigo_location:
            raise FileNotFoundError(f"Não foi possível encontrar a imagem '{IMG_CODIGO_GRUPO} na tela.")
        
        pag.click(campo_codigo_location)
        pag.write(group_code)
        pag.press('tab')
        time.sleep(0.5)

        # 4. Loop para inserir cada componente e nível de acesso
        total_rows = len(df)
        for index, row in df.iterrows():
            componente = str(row[0])
            nivel_acesso_txt = int(row[1])

            print(f"Processando {index+1}/{total_rows}: Componente='{componente}', Nível='{nivel_acesso_txt}'")

            # Digita o componente
            pag.write(componente)
            pag.press('tab')
            time.sleep(0.5)

            # Seleciona o nível de acesso
            if nivel_acesso_txt:
                presses = (nivel_acesso_txt)
                for _ in range(presses):
                    pag.press('down')
                    time.sleep(0.1)
            else:
                print(f"AVISO: Nível de acesso '{nivel_acesso_txt}' não encontrado no mapa. Pulando seleção de nível.")
            
            pag.press('tab')
            time.sleep(0.5)

        # 5. Clicar em "Atualizar para salvar"
        print("Procurando o botão 'Atualizar'...")
        botao_atualizar_location = pag.locateCenterOnScreen(IMG_ATUALIZAR, confidence=0.9)
        if not botao_atualizar_location:
            raise FileNotFoundError(f"Não foi possível encontrar a imagem '{IMG_ATUALIZAR}' na tela.")
        
        pag.click(botao_atualizar_location)

        QMessageBox.information(None, "Sucesso!", "Automação concluída com sucesso!")
    except FileNotFoundError as e:
        QMessageBox.critical(None, "Erro de imagem", f"Erro: {e}\n\nVerifique se as imagens .png estão na mesma pasta do script e visíveis na tela.")
    except Exception as e:
        QMessageBox.critical(None, "Erro Inesperado", f"Ocorreu um erro durante a automação:\n{e}")

class AutomationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automação de Cadastro TOTVS")
        self.layout = QVBoxLayout(self)

        self.label_group = QLabel("Código do Grupo:")
        self.input_group = QLineEdit()

        self.label_file = QLabel("Arquivo CSV não selecionado.")
        self.btn_browse = QPushButton("Procurar Arquivo CSV...")
        self.btn_browse.clicked.connect(self.browse_file)

        self.btn_start = QPushButton("Iniciar Automação")
        self.btn_start.clicked.connect(self.start_automation)
        self.btn_start.setStyleSheet("background-color: #4CAF50; color: white;")

        self.layout.addWidget(self.label_group)
        self.layout.addWidget(self.input_group)
        self.layout.addWidget(self.label_file)
        self.layout.addWidget(self.btn_browse)
        self.layout.addWidget(self.btn_start)

        self.csv_path = ""
    
    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo CSV", "", "CSV Files (*.csv)")
        if path:
            self.csv_path = path
            # Pega apenas o nome do arquivo para exibir
            file_name = path.split('/')[-1]
            self.label_file.setText(f"Arquivo: {file_name}")
    
    def start_automation(self):
        group_code = self.input_group.text()
        if not group_code:
            QMessageBox.warning(self, "Atenção", "Por favor, insira o Código do Grupo.")
            return
        if not self.csv_path:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione um arquivo CSV.")
            return
        
        # Minimiza a janela da aplicação para não atrapalhar a automação
        self.showMinimized()
        run_automation(group_code, self.csv_path)
        # Restaura a janela após a conclusão
        self.showNormal()

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = AutomationApp()
    window.show()
    sys.exit(app.exec())