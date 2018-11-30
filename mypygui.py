#!/usr/bin/env python3
# https://data-flair.training/blogs/python-pyqt5-tutorial/
# https://likegeeks.com/pyqt5-tutorial/#Install-PyQt5-designer
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLineEdit, QAction, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtNetwork import QNetworkReply

class myOraDocs():
    def doRequest(self, url):
        req = QNetworkRequest(QUrl(url))
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)

    def handleResponse(self, reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            print(str(bytes_string, 'utf-8'))
            my_return = str(bytes_string)
        else:
            print("Error occured: ", er)
            print(reply.errorString())

        return my_return

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "OraDocs by littleT"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()
        # self.doRequest()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('Starting ...')
        # for the menu first create some actions to be added like
        # File - Exit action
        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close)
        # File - open
        openAction = QAction(QIcon(''), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Opens a file')
        openAction.triggered.connect(self.openCall)
        # the help actions
        helpAction = QAction(QIcon(''), 'Help', self)
        helpAction.triggered.connect(self.openHelp)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(helpAction)

        # self.statusBar().showMessage('Loding webpage ...')
        # self.webView = QWebEngineView(self)
        # self.webView.setUrl(QUrl('https://oradocs-corp.documents.us2.oraclecloud.com/documents/'))
        # self.webView.setGeometry(5,20, 590, 300)
        self.logOutput = QTextEdit(self)
        self.logOutput.setReadOnly(True)
        # self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
        self.logOutput.setGeometry(5, 200,590,60)

        self.statusBar().showMessage('waiting for click ...')
        self.textbox = QLineEdit(self)
        # self.textbox.move(5, 300)
        # self.textbox.resize(590, 20)
        self.textbox.setGeometry(5, 325, 590, 20)

        self.button = QPushButton('Click Me', self)
        self.button.move(10, 350)
        self.button.clicked.connect(self.doRequest)

    def doRequest(self):
        #self.url = "https://oradocs-corp.documents.us2.oraclecloud.com/documents/"
        url = "https://www.google.com"
        req = QNetworkRequest(QUrl(url))
        self.net_mgr = QNetworkAccessManager()

        self.nam = self.net_mgr.get(req)
        self.nam.finished.connect(self.processReq)
        self.nam.error.connect(self.processErr)

    def openCall(self):
        print("Open Call")

    def openHelp(self):
        print("Open Help")

    @pyqtSlot()
    def onClick(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Hello World!', "Confirm: " + textboxValue,
                             QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("...")

    @pyqtSlot()
    def processReq(self):
        if self.nam.bytesAvailable():
            self.logOutput.moveCursor(QTextCursor.End)
            self.logOutput.insertPlainText('We are connected\n')
            bytes_string = self.nam.readAll()
            
        self.nam.deleteLater()

    @pyqtSlot(QNetworkReply.NetworkError)
    def processErr(self, code):
        self.msg.critical(None, "Info", "You are not connected to the Internet.")
        print(code)

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
