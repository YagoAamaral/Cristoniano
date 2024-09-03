import sys
import random
import sqlite3
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):  
    def __init__(self):
        super().__init__()

        self.hello = ["Todos os dias recomendação de musica cristã ❤️‍🔥"]
        self.bemv = ["Digite seu nome"]
        self.cont = ["Pronto para continuar? "]
        self.click_count = 0  

        self.label = QtWidgets.QLabel("Digite seu nome:", alignment=QtCore.Qt.AlignCenter)
        self.input = QtWidgets.QLineEdit(self)
        self.input.setPlaceholderText("Nome")
        self.button_save = QtWidgets.QPushButton("Salvar Nome")
        self.button = QtWidgets.QPushButton("Click aqui! para continuar")  # Botão
        
        self.button.setVisible(True)
        self.next = QtWidgets.QPushButton("Click aqui")
        self.next.setVisible(False)

        self.text = QtWidgets.QLabel("olá", alignment=QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        
        self.button.setStyleSheet("color: black;")
        self.next.setStyleSheet("color: black")

        self.setStyleSheet("background-color: white;")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.next)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button_save)

        #
        
        self.label.setVisible(False)
        self.input.setVisible(False)
        self.button_save.setVisible(False)

        self.button.clicked.connect(self.magic)
        self.next.clicked.connect(self.contui)
        self.button_save.clicked.connect(self.save_name)

        # Conectar ao banco de dados SQLite
        self.conn = sqlite3.connect('nomes.db')
        self.cursor = self.conn.cursor()

        # Criar tabela se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    @QtCore.Slot()
    def magic(self):
        self.click_count += 1  
        texto_selecionado = random.choice(self.hello)
        texto_selecionado1 = random.choice(self.cont)
        texto_selecionado2 = random.choice(self.bemv)

       
        if self.click_count == 1:
            self.text.setText(texto_selecionado1)
      
        elif self.click_count == 2:
            self.text.setText(texto_selecionado2)
            self.label.setVisible(True)
            self.input.setVisible(True)
            self.button_save.setVisible(True)
            self.button.setVisible(False)
            self.next.setVisible(False)
            self.input.setStyleSheet("color: black")
            self.button_save.setStyleSheet("color: black")

        self.text.setStyleSheet("color: black")

    @QtCore.Slot()
    def contui(self):
        self.text.setText(random.choice(self.cont))
        self.text.setStyleSheet("color: black;")

    @QtCore.Slot()
    def save_name(self):
        nome = self.input.text()
        if nome:
            self.cursor.execute("INSERT INTO nomes (nome) VALUES (?)", (nome,))
            self.conn.commit()
            self.text.setText(f"Nome '{nome}' salvo no banco de dados!")
            self.input.clear()

    def closeEvent(self, event):
        
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    aplicativo = QtWidgets.QApplication([])  # Inicia a aplicação

    widget = MyWidget()
    widget.resize(600, 600)
    widget.show()  # Exibe o layout

    sys.exit(aplicativo.exec())
