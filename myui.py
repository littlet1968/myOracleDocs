#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import  (pyqtSlot, QUrl, QMetaObject, QRect, Qt,
                           QCoreApplication)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QVBoxLayout,
                             QHBoxLayout, QListView, QLineEdit, QPushButton,
                             QProgressBar, QTextBrowser, QMenu, QMenuBar,
                             QStatusBar, QAction, QSizePolicy, QLayout,
                             QMessageBox)
from PyQt5.QtGui import  QIcon, QTextCursor
# from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

# import the UI
from myui1 import Ui_MainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connections()

    def _connections(self):
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_Open.triggered.connect(self.action_open)
        self.ui.action_Save.triggered.connect(self.action_save)
        self.ui.action_Sync.triggered.connect(self.action_sync)

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
    def action_sync(self):
        QMessageBox.information(self, "File Save", "work in progress")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    httpWin = AppWindow()
    httpWin.show()
    sys.exit(app.exec_())
