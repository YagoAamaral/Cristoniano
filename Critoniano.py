import sys
import subprocess
import random
import sqlite3
from pynotifier import notification
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPropertyAnimation

print("Verificando dependências....")

try:
    from PySide6 import QtCore, QtWidgets, QtGui
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])
    from PySide6 import QtCore, QtWidgets, QtGui

class SuPage(QtWidgets.QWidget): 
    def __init__(self, nome):  
        super().__init__()
        self.label = QtWidgets.QLabel(f"Bem vindo!", alignment=QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.setStyleSheet("background-color: white;")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        self.butão = QtWidgets.QPushButton("Vamos ver a palavra de Deus? ")
        

      
        self.notify_button = QtWidgets.QPushButton("Mostrar notificação")
        layout.addWidget(self.notify_button)
        self.notify_button.clicked.connect(lambda: self.show_notification(nome))

    def show_notification(self, nome):
        notification(
            title='Cadastro realizado',
            description=f'O nome {nome} foi salvo com sucesso!',
            icon_path='',  
            duration=10  # Duração da notificação em segundos
        ).send()

class MyWidget(QtWidgets.QWidget):  # Classe do aplicativo principal
    def __init__(self):
        super().__init__()

        self.hello = ["Todos os dias recomendação de música cristã ❤️‍🔥"]
        self.bemv = ["Digite seu nome"]
        self.cont = ["Pronto para continuar? "]
        self.carr = ["Carregando conteúdo..."]
        self.click_count = 0  

        self.label = QtWidgets.QLabel("Digite seu nome:", alignment=QtCore.Qt.AlignCenter)
        self.input = QtWidgets.QLineEdit(self)
        self.input.setPlaceholderText("Digite apenas seu primeiro nome")
        self.button_save = QtWidgets.QPushButton("Salvar Nome")
        self.button = QtWidgets.QPushButton("Click aqui! para continuar")  # Botão para começar
        self.button.setVisible(True)
        self.next = QtWidgets.QPushButton("Click aqui")
        self.next.setVisible(False)

        self.text = QtWidgets.QLabel("Olá", alignment=QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        
        self.button.setStyleSheet("color: black;")
        self.next.setStyleSheet("color: black")
        self.setStyleSheet("background-color: white;")
        self.butão.setStyleSheet("color: black")

        
        
        self.layout.addWidget(self.butão)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.next)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button_save)

       
        self.label.setVisible(False)
        self.input.setVisible(False)
        self.button_save.setVisible(False)

       
        self.button.clicked.connect(self.magic)
        self.next.clicked.connect(self.contui)
        self.button_save.clicked.connect(self.save_name)

        
        try:
            self.conn = sqlite3.connect('nomes.db')
            self.cursor = self.conn.cursor()

            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS nomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            self.text.setText(f"Erro ao conectar ao banco de dados: {str(e)}")
        
        
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.text)
        self.text.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)  

    @QtCore.Slot()
    def magic(self):
        self.click_count += 1 
        texto_selecionado1 = random.choice(self.cont)
        texto_selecionado2 = random.choice(self.bemv)

       
        self.fade_out_animation()

        
        if self.click_count == 1:
            self.animation.finished.connect(lambda: self.text.setText(texto_selecionado1))
            self.animation.finished.connect(self.fade_in_animation)  
        
        elif self.click_count == 2:
            self.animation.finished.connect(lambda: self.show_name_input())
            self.animation.finished.connect(self.fade_in_animation) 
        
    def fade_out_animation(self):
        
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def fade_in_animation(self):
        
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    @QtCore.Slot()
    def contui(self):
        self.text.setText(random.choice(self.cont))
        self.text.setStyleSheet("color: black;")

    @QtCore.Slot()
    def save_name(self):
        nome = self.input.text().strip()  
        try:
            if nome:
                self.cursor.execute("INSERT INTO nomes (nome) VALUES (?)", (nome,))
                self.conn.commit()
                self.text.setText(f"Nome '{nome}' foi salvo!")
                self.input.clear()
               
                self.show_success_page(nome)
            else:
                raise ValueError("Nome não pode ser vazio!")
        except ValueError as e:
            self.text.setText(str(e)) 
        except Exception as e:
            self.text.setText(f"Ocorreu um erro: {str(e)}")

    def show_name_input(self):
        self.label.setVisible(True)
        self.input.setVisible(True)
        self.button_save.setVisible(True)
        self.button.setVisible(False)
        self.next.setVisible(False)
        self.input.setStyleSheet("color: black")
        self.button_save.setStyleSheet("color: black")

    def show_success_page(self, nome):
        self.success_page = SuPage(nome) 
        self.success_page.resize(600, 600)
        self.success_page.show()
        self.close()  # Fecha a janela atual

    def closeEvent(self, event):
        
        self.conn.close()
        event.accept()
    

if __name__ == "__main__":
    aplicativo = QtWidgets.QApplication([]) 

    widget = MyWidget()
    widget.resize(600, 600)
    widget.show()  # Exibe o layout

    sys.exit(aplicativo.exec())
