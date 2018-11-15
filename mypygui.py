#!/usr/bin/env python3
# https://data-flair.training/blogs/python-pyqt5-tutorial/
# https://likegeeks.com/pyqt5-tutorial/#Install-PyQt5-designer
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLineEdit, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Hello World"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('In Progress')

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMExit = QAction(QIcon('exit24.png'), 'Exit', self)
        fileMExit.setShortcut('Ctrl+Q')
        fileMExit.setStatusTip('Exit Application')
        fileMExit.triggered.connect(self.close)
        fileMenu.addAction(fileMExit)

        webView = QWebEngineView(self)
        webView.setUrl(QUrl('https://oradocs-corp.documents.us2.oraclecloud.com/documents/'))
        webView.setGeometry(5,20, 590, 300)

        self.show()

    @pyqtSlot()
    def onClick(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Hello World!', "Confirm: " + textboxValue,
                             QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("...")


if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
