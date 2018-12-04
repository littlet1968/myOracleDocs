#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import  (pyqtSlot, QUrl, QMetaObject, Qt,
                           QCoreApplication)
# from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QVBoxLayout,
#                             QHBoxLayout, QListView, QLineEdit, QPushButton,
#                             QProgressBar, QTextBrowser, QMenu, QMenuBar,
#                             QStatusBar, QAction, QSizePolicy, QLayout,
#                             QMessageBox)
# from PyQt5.QtGui import  QIcon, QTextCursor
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

# import the UI
from mainGUI import Ui_MainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.docRoot = "https://oradocs-corp.documents.us2.oraclecloud.com/documents/"
        self.url = QUrl()
        self.qnam = QNetworkAccessManager()
        self.reply = None
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.setupUi.MainWindow.setTitle("OraDocs")
        self._connections()

    def _connections(self):
        self.ui.logOutput.insertPlainText("Setting up actions\n")
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_Open.triggered.connect(self.action_open)
        self.ui.action_Save.triggered.connect(self.action_save)
        self.ui.action_SyncAll.triggered.connect(self.action_syncAll)
        self.ui.action_SyncConnect.triggered.connect(self.action_syncConnect)

    @pyqtSlot()
    def action_close(self):
        # print("closing")
        self.quit()

    @pyqtSlot()
    def action_open(self):
        # print("open")
        QMessageBox.information(self, "File Open", "work in progress")

    @pyqtSlot()
    def action_save(self):
        # print("open")
        QMessageBox.information(self, "File Save", "work in progress")

    @pyqtSlot()
    def action_syncAll(self):
        QMessageBox.information(self, "Sync ALl", "work in progress")

    @pyqtSlot()
    def action_syncConnect(self):
        self.url = QUrl(self.docRoot)
        self.ui.logOutput.insertPlainText("syncConnect ...\n")
        # start the request
        self.startRequest(self.url)
        self.ui.logOutput.insertPlainText("syncConnect - after start Request\n")
        QMessageBox.information(self, "Sync Connect", "work in progress")

    def startRequest(self, url):
        self.ui.logOutput.insertPlainText("startRequest ...\n")
        return

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    httpWin = AppWindow()
    httpWin.show()
    sys.exit(app.exec_())
