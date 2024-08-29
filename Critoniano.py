import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget): # Classe do aplicativo
    def __init__(self):
        super().__init__()

        self.hello = ["Todos os dias recomendação de musica cristã ❤️‍🔥"]
        self.cont = ["Pronto para continuar?"]

        self.button = QtWidgets.QPushButton("Click aqui! para continuar")  # Botão
        self.next = QtWidgets.QPushButton("Próximo")
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

        self.button.clicked.connect(self.magic)
        self.next.clicked.connect(self.contui)

    @QtCore.Slot()
    def magic(self):
        texto_selecionado = random.choice(self.hello)
        self.text.setText(texto_selecionado)
        self.text.setStyleSheet("color: black")

        if texto_selecionado == "Todos os dias recomendação de musica cristã ❤️‍🔥":
            self.next.setVisible(True)
        else:
            self.next.setVisible(False)
          
        
     


    @QtCore.Slot()
    def contui(self):
        self.text.setText(random.choice(self.cont))
        self.text.setStyleSheet("color: black;")

if __name__ == "__main__":
    aplicativo = QtWidgets.QApplication([])  # Inicia a aplicação

    widget = MyWidget()
    widget.resize(600, 600)
    widget.show()  # Exibe o layout

    sys.exit(aplicativo.exec())
